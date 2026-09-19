"""Small transparent diagnostic comparison, not a held-out accuracy benchmark."""
from pathlib import Path
import argparse
import json
import os
import sys
import time
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('HF_HUB_OFFLINE', '1')
os.environ.setdefault('TRANSFORMERS_OFFLINE', '1')
from src.pipeline import CivicRAGPipeline
from src.generation.ollama_generator import OllamaAnswerGenerator, build_prompt

OUT = ROOT/'docs/evaluation/chunk_fix_2026_09_18'
CASES = [
    ('brta','অপেশাদার ও পেশাদার ড্রাইভিং লাইসেন্সের জন্য ন্যূনতম বয়স কত?', 'নতুন ড্রাইভিং লাইসেন্স ইস্যু', 'বয়স'),
    ('brta','গাড়ির রং পরিবর্তনের জন্য কী কী কাগজপত্র লাগবে?', 'রং পরিবর্তন', 'মূল নিবন্ধন'),
    ('brta','মোটরযানের মালিকানা বদলীর জন্য কী কী কাগজপত্র লাগবে?', 'মালিকানা বদলী', ''),
    ('brta','গাড়ির ফিটনেস সনদ নবায়ন করব কীভাবে?', 'ফিটনেস ইস্যু', ''),
    ('brta','গাড়ির ইঞ্জিন পরিবর্তনের অনুমোদন কীভাবে পাব?', 'ইঞ্জিন পরিবর্তন', ''),
    ('brta','ট্যাক্স টোকেন নবায়ন করব কীভাবে?', 'ট্যাক্সটোকেন', ''),
    ('passport','সুপার এক্সপ্রেস পাসপোর্ট কোথা থেকে সংগ্রহ করতে হবে?', 'Urgent Applications', 'delivered only'),
    ('passport','ই-পাসপোর্ট সংগ্রহ করতে কী নিয়ে যেতে হবে?', 'Bangladesh_ePassport_FAQ', 'Original Delivery Slip'),
    ('passport','ডেলিভারি স্লিপ হারিয়ে গেলে পাসপোর্ট কীভাবে সংগ্রহ করব?', 'Bangladesh_ePassport_FAQ', 'Printed Application Summary'),
    ('passport','সরকারি চাকরি থেকে অবসর নিয়েছি। ই-পাসপোর্ট এনরোলমেন্টে কী কী কাগজপত্র লাগবে?', 'Bangladesh_ePassport_FAQ', 'PRL / Post Retirement'),
    ('passport','অপ্রাপ্তবয়স্ক সন্তানের পাসপোর্ট কে সংগ্রহ করতে পারবে?', 'Bangladesh_ePassport_FAQ', 'father or mother'),
    ('passport','অনলাইনে ভিসার আবেদন ফরম কি বাংলায় পূরণ করতে পারব?', 'Electronic Visa Applications Forms Frequently', 'only supports'),
]


def norm(text):return unicodedata.normalize('NFC',text).casefold()


def matches(context, file_hint, evidence_hint):
    return norm(file_hint) in norm(context['metadata'].get('source_relative_path','')) and norm(evidence_hint) in norm(context['content'])


def save(name, value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def retrieval(domains=('passport','brta')):
    report={'scope':'12 convenience diagnostics; predefined source/content checks are incomplete relevance labels, not gold Recall@k.', 'rows':[], 'configs':{}}
    shared=None
    for domain in domains:
        base=ROOT/'domains'/domain
        candidate=sorted(base.glob('config.candidate_*.json'))[-1]
        report['configs'][domain]={'baseline':json.loads((base/'config.json').read_text()),'candidate_path':str(candidate.relative_to(ROOT))}
        for variant,path in [('baseline',base/'config.json'),('candidate',candidate)]:
            pipeline=CivicRAGPipeline(ROOT,path,shared_pipeline=shared)
            if shared is None:shared=pipeline
            for dom,query,file_hint,evidence_hint in CASES:
                if dom!=domain:continue
                assert any(matches(c,file_hint,evidence_hint) for c in pipeline.chunks), (dom,file_hint,evidence_hint)
                start=time.monotonic()
                result=pipeline.ask(query,generate=False)
                hits=[i+1 for i,c in enumerate(result['sources']) if matches(c,file_hint,evidence_hint)]
                report['rows'].append({'domain':domain,'variant':variant,'query':query,'file_hint':file_hint,'evidence_hint':evidence_hint,
                                       'support_rank':hits[0] if hits else None,'seconds':round(time.monotonic()-start,2),'sources':result['sources']})
                save('retrieval_'+'_'.join(domains)+'.json',report)
                print(domain,variant,'support rank',hits[0] if hits else None,query,flush=True)


def generation():
    report={'scope':'Fixed correct-evidence diagnostic; two passport questions, three actual local LLMs. No retrieval or safe path in these calls.',
            'num_predict':600, 'rows':[]}
    config_path=sorted((ROOT/'domains/passport').glob('config.candidate_*.json'))[-1]
    config=json.loads(config_path.read_text())
    report['config_path']=str(config_path.relative_to(ROOT))
    chunks=[json.loads(line) for line in (ROOT/config['data']['chunk_output_path']).read_text().splitlines()]
    generation=config['generation']
    for model in generation['comparison_models']:
        generator=OllamaAnswerGenerator(model=model,base_url=generation['ollama_base_url'],temperature=generation['temperature'],
                    top_p=generation['top_p'],num_predict=600,repeat_last_n=generation.get('repeat_last_n'),repeat_penalty=generation.get('repeat_penalty'))
        for domain,query,file_hint,evidence_hint in CASES[6:8]:
            context=next(c for c in chunks if matches(c,file_hint,evidence_hint))
            start=time.monotonic()
            response=generator.llm.invoke(build_prompt(query,[context]))
            report['rows'].append({'model':model,'query':query,'context':context,'raw_answer':str(response.content),
                                   'metadata':response.response_metadata,'seconds':round(time.monotonic()-start,2)})
            save('fixed_evidence_generation.json',report)
            print(model,query,round(time.monotonic()-start,1),flush=True)


def end_to_end():
    import urllib.request
    report={'scope':'Two passport follow-up smoke questions through the running CivicRAG app; not a benchmark.', 'rows':[]}
    for _,query,_,_ in CASES[6:8]:
        request=urllib.request.Request('http://127.0.0.1:7860/chat',
            data=json.dumps({'domain':'passport','query':query,'model':'llama3.2','method':'civic'}).encode(),
            headers={'Content-Type':'application/json'})
        start=time.monotonic()
        with urllib.request.urlopen(request,timeout=600) as response:
            result=json.load(response)
        report['rows'].append({'seconds':round(time.monotonic()-start,2),**result})
        save('end_to_end.json',report)
        print(query, result.get('answer_route'),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['retrieval','generation','end-to-end'])
    parser.add_argument('--domain',choices=['passport','brta'])
    args=parser.parse_args()
    if args.mode=='retrieval':retrieval((args.domain,) if args.domain else ('passport','brta'))
    elif args.mode=='generation':generation()
    else:end_to_end()
