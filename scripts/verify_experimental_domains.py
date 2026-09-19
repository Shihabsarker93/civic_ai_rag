"""Run local index-integrity checks and a small, explicitly non-benchmark QA smoke test."""
from pathlib import Path
import hashlib
import json
import time
import unicodedata
import urllib.request

import chromadb

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs/evaluation/domain_expansion_2026_09_18'
QUESTIONS = [
    ('brta', 'অপেশাদার ও পেশাদার ড্রাইভিং লাইসেন্সের জন্য ন্যূনতম বয়স কত?', 'নতুন ড্রাইভিং লাইসেন্স ইস্যু'),
    ('brta', 'গাড়ির রং পরিবর্তনের জন্য কী কী কাগজপত্র লাগবে?', 'রং পরিবর্তন'),
    ('passport', 'সুপার এক্সপ্রেস পাসপোর্ট কোথা থেকে সংগ্রহ করতে হবে?', 'Urgent Applications'),
    ('passport', 'ই-পাসপোর্ট সংগ্রহ করতে কী নিয়ে যেতে হবে?', '5 Steps to your e-Passport'),
]


def verify_indexes():
    checks = []
    for domain in ['birth_death_registration', 'brta', 'passport']:
        config = json.loads((ROOT/f'domains/{domain}/config.json').read_text())['data']
        chunks = [json.loads(line) for line in (ROOT/config['chunk_output_path']).read_text().splitlines() if line]
        collection = chromadb.PersistentClient(path=str(ROOT/config['chroma_persist_dir'])).get_collection(config['collection_name'])
        stored = collection.get(include=['documents', 'metadatas'])
        by_id = {c['id']:c for c in chunks}
        assert set(stored['ids']) == set(by_id)
        assert len(by_id) == len(chunks)
        for cid, text in zip(stored['ids'],stored['documents']):
            assert text == by_id[cid]['content']
        check = {'domain':domain, 'chunks':len(chunks), 'ids_and_text_match':True}
        if domain != 'birth_death_registration':
            register = json.loads((ROOT/config['register_path']).read_text())
            indexed = [d for d in register['documents'] if d['index_status']=='indexed']
            assert {c['metadata']['doc_id'] for c in chunks} == {d['document_id'] for d in indexed}
            for doc in register['documents']:
                assert hashlib.sha256(Path(doc['source_path']).read_bytes()).hexdigest() == doc['sha256']
                assert hashlib.sha256((ROOT/doc['snapshot_path']).read_bytes()).hexdigest() == doc['sha256']
            for source in register['originals']:
                assert hashlib.sha256(Path(source['path']).read_bytes()).hexdigest() == source['sha256']
            assert all(c['metadata']['domain']==domain for c in chunks)
            check.update(documents=len(indexed), all_sources_and_snapshots_unchanged=True)
        checks.append(check)
    return checks


def main():
    OUTPUT.mkdir(parents=True,exist_ok=True)
    report = {'scope':'Four convenience smoke questions using llama3.2; not a gold-label benchmark or full corpus validation.',
              'integrity':verify_indexes(),'answers':[]}
    for domain, query, expected in QUESTIONS:
        start = time.monotonic()
        req = urllib.request.Request('http://127.0.0.1:7860/chat',
                data=json.dumps({'domain':domain,'query':query,'model':'llama3.2','method':'civic'}).encode(),
                headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=360) as response:
            answer=json.load(response)
        assert answer['domain']==domain
        assert all(c['metadata']['domain']==domain for c in answer['sources'])
        expected=unicodedata.normalize('NFC',expected)
        hit=any(expected in unicodedata.normalize('NFC',c['metadata'].get('source_relative_path','')) for c in answer['sources'])
        report['answers'].append({'elapsed_seconds':round(time.monotonic()-start,2),'expected_source_fragment':expected,
                                 'expected_source_in_candidates':hit,**answer})
        (OUTPUT/'smoke_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
        print(domain,query,'route:',answer['answer_route'],'expected source present:',hit,flush=True)
    lines=['# Experimental domain integration check','',report['scope'],'',
           'Source hashes, indexed document coverage and Chroma/JSONL IDs and text were checked. No claims of measured answer accuracy are made.','',
           '| Domain | Documents | Chunks | Integrity |','|---|---:|---:|---|']
    for c in report['integrity']:
        lines.append(f"| {c['domain']} | {c.get('documents','Existing corpus')} | {c['chunks']} | Passed |")
    for row in report['answers']:
        lines += ['',f"## {row['domain']}: {row['query']}",'',
                  f"Model: {row['model']}; route: {row['answer_route']}; time: {row['elapsed_seconds']} s; expected source among retrieved candidates: {row['expected_source_in_candidates']}.",
                  '',row['answer'],'','Retrieved source files:']
        lines += [f"- {c['id']}: {c['metadata']['source_relative_path']}" for c in row['sources']]
    (OUTPUT/'smoke_report.md').write_text('\n'.join(lines)+'\n')
    print('Saved',OUTPUT,flush=True)


if __name__=='__main__':main()
