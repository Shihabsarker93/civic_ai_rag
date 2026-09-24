"""Local, resumable evaluation of frozen answers; never calls the RAG pipeline."""
import argparse
import asyncio
from collections import Counter
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import random
import statistics
import subprocess
import time
import unicodedata

os.environ.setdefault('RAGAS_DO_NOT_TRACK', 'true')
os.environ.setdefault('HF_HUB_OFFLINE', '1')
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/evaluation/ragas_comparison_2026_09_24'
INPUTS = {
    'simple': 'docs/evaluation/simple_matched_qwen3_30q_2026_09_24/answers.json',
    'civic': 'docs/evaluation/chunk_order_fixed_qwen3_30q_2026_09_23/answers.json',
}


def save(name, value):
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / name
    temporary = target.with_suffix(target.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False))
    temporary.replace(target)


def response_text(answer):
    return answer.split('\nSources:')[0].strip()


def load_rows():
    rows = {key: json.loads((ROOT / path).read_text())['rows'] for key, path in INPUTS.items()}
    for key, values in rows.items():
        assert len(values) == 30, (key, len(values))
        assert len({r['audit_item']['id'] for r in values}) == 30
        assert all(r['result']['model'] == 'qwen3:8b' for r in values)
        assert all('answer_contexts' in r['result'] for r in values)
    assert [r['audit_item'] for r in rows['simple']] == [r['audit_item'] for r in rows['civic']]
    plans = [json.loads((ROOT / path).with_name('plan.json').read_text()) for path in INPUTS.values()]
    assert plans[0]['file_hashes'] == plans[1]['file_hashes'], 'Frozen configurations differ'
    return rows


def descriptive(rows):
    result = {}
    for system, values in rows.items():
        times = sorted(r['elapsed_seconds'] for r in values)
        fractions = []
        for row in values:
            letters = [c for c in response_text(row['result']['answer']) if unicodedata.category(c).startswith('L')]
            fractions.append(sum('\u0980' <= c <= '\u09ff' for c in letters) / len(letters) if letters else 0)
        result[system] = {
            'completed_requests': len(values),
            'mean_latency_seconds': statistics.mean(times),
            'median_latency_seconds': statistics.median(times),
            'p95_latency_seconds_nearest_rank': times[math.ceil(.95 * len(times)) - 1],
            'routes': dict(Counter(r['result']['answer_route'] for r in values)),
            'finish_reasons': dict(Counter(str(r['result'].get('generation_metadata', {}).get('done_reason')) for r in values)),
            'mean_context_count': statistics.mean(len(r['result']['answer_contexts']) for r in values),
            'mean_context_characters': statistics.mean(sum(len(c['content']) for c in r['result']['answer_contexts']) for r in values),
            'mean_bangla_fraction_of_letters': statistics.mean(fractions),
        }
    save('descriptive_metrics.json', result)
    return result


def summarize(scores):
    result = {'note': 'Exploratory self-judge scores, NOT factual accuracy. Missing scores are excluded, never zero-filled.', 'systems': {}, 'paired_civic_minus_simple': {}}
    metrics = sorted({r['metric'] for r in scores})
    for system in INPUTS:
        result['systems'][system] = {}
        for metric in metrics:
            group = [r for r in scores if r['system'] == system and r['metric'] == metric]
            valid = [r['score'] for r in group if r['score'] is not None]
            result['systems'][system][metric] = {'valid': len(valid), 'failed': len(group) - len(valid), 'mean': statistics.mean(valid) if valid else None}
    for metric in metrics:
        by_system = {s: {r['question_id']: r['score'] for r in scores if r['system'] == s and r['metric'] == metric and r['score'] is not None} for s in INPUTS}
        ids = sorted(by_system['simple'].keys() & by_system['civic'].keys())
        differences = [by_system['civic'][i] - by_system['simple'][i] for i in ids]
        if differences:
            rng = random.Random(20260924)
            draws = sorted(statistics.mean(rng.choices(differences, k=len(differences))) for _ in range(2000))
            result['paired_civic_minus_simple'][metric] = {'paired_n': len(ids), 'mean_difference': statistics.mean(differences), 'bootstrap_95_percent_interval': [draws[49], draws[1949]]}
    save('ragas_summary.json', result)


async def evaluate(rows):
    from langchain_core.callbacks import BaseCallbackHandler
    from langchain_core.embeddings import Embeddings
    from langchain_ollama import ChatOllama
    from ragas import SingleTurnSample
    from ragas.embeddings import LangchainEmbeddingsWrapper
    from ragas.llms import LangchainLLMWrapper
    from ragas.metrics import Faithfulness, ResponseRelevancy, AspectCritic
    from ragas.run_config import RunConfig

    class Trace(BaseCallbackHandler):
        def on_chat_model_start(self, serialized, messages, **kwargs):
            with (OUT / 'judge_trace.jsonl').open('a') as stream:
                stream.write(json.dumps({'time': time.time(), 'prompts': [[m.content for m in batch] for batch in messages]}, ensure_ascii=False) + '\n')
        def on_llm_end(self, response, **kwargs):
            with (OUT / 'judge_trace.jsonl').open('a') as stream:
                stream.write(json.dumps({'time': time.time(), 'output': str(response)}, ensure_ascii=False) + '\n')

    class LocalEmbeddings(Embeddings):
        model = None
        def embed_documents(self, texts):
            if self.model is None:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer('BAAI/bge-m3', device='cpu', local_files_only=True)
            return self.model.encode(texts, normalize_embeddings=True).tolist()
        def embed_query(self, text):
            return self.embed_documents([text])[0]

    judge = ChatOllama(model='qwen3:8b', base_url='http://127.0.0.1:11434', temperature=0,
                       num_ctx=16384, num_predict=4096, seed=20260924,
                       reasoning=False, client_kwargs={'timeout': 1200})
    assert judge.reasoning is False
    llm = LangchainLLMWrapper(judge, run_config=RunConfig(timeout=1200, max_retries=1, max_workers=1))
    metrics = [Faithfulness(llm=llm),
               ResponseRelevancy(llm=llm, embeddings=LangchainEmbeddingsWrapper(LocalEmbeddings()), strictness=3),
               AspectCritic(name='context_relevance_binary', llm=llm, strictness=1,
                            definition='Are the supplied retrieved contexts predominantly relevant to the service, procedure and conditions actually asked about in the user input? Ignore the response. Return 1 only if most supplied context is applicable, otherwise 0.')]
    callbacks = [Trace()]

    async def score(metric, sample):
        start = time.monotonic()
        try:
            value = float(await metric.single_turn_ascore(sample, callbacks=callbacks, timeout=1200))
            if not math.isfinite(value):
                raise ValueError('Judge returned a non-finite score')
            return {'score': value, 'error': None, 'seconds': round(time.monotonic() - start, 2)}
        except Exception as exc:
            return {'score': None, 'error': repr(exc), 'seconds': round(time.monotonic() - start, 2)}

    if not (OUT / 'sanity_checks.json').exists():
        checks = []
        for response, expected in [('পাঠাগার সকাল দশটায় খোলে।', 1), ('পাঠাগার রাত আটটায় খোলে।', 0)]:
            sample = SingleTurnSample(user_input='পাঠাগার কখন খোলে?', response=response,
                                     retrieved_contexts=['পাঠাগার প্রতিদিন সকাল দশটায় খোলে।'])
            print('Judge sanity check:', expected, flush=True)
            checks.append({'expected': expected, **await score(metrics[0], sample)})
        save('sanity_checks.json', checks)
    checks = json.loads((OUT / 'sanity_checks.json').read_text())
    if not all(c['score'] == c['expected'] for c in checks):
        raise RuntimeError('Local faithfulness judge failed basic Bangla sanity checks; batch not started')

    scores = json.loads((OUT / 'ragas_scores.json').read_text()) if (OUT / 'ragas_scores.json').exists() else []
    completed = {(r['system'], r['question_id'], r['metric']) for r in scores}
    for index in range(30):
        # Alternate system order to avoid always judging one system first.
        for system in (['simple', 'civic'] if index % 2 == 0 else ['civic', 'simple']):
            row = rows[system][index]
            item, result = row['audit_item'], row['result']
            sample = SingleTurnSample(user_input=item['question'], response=response_text(result['answer']),
                                     retrieved_contexts=[c['content'] for c in result['answer_contexts']])
            for metric in metrics:
                if (system, item['id'], metric.name) in completed:
                    continue
                print('Scoring', system, item['id'], metric.name, flush=True)
                scored = await score(metric, sample)
                scores.append({'system': system, 'question_id': item['id'], 'domain': item['domain'], 'metric': metric.name, **scored})
                save('ragas_scores.json', scores)
                summarize(scores)
                save('progress.json', {'metric_attempts': len(scores), 'expected': 180, 'valid': sum(r['score'] is not None for r in scores), 'last': scores[-1]})
                print('Saved', len(scores), '/ 180', scored, flush=True)
                if len(scores) >= 3 and all(r['score'] is None for r in scores[-3:]):
                    raise RuntimeError('Three consecutive metric failures; stopping rather than producing misleading scores')
    save('completion.json', {'metric_attempts': len(scores), 'valid': sum(r['score'] is not None for r in scores), 'manual_correctness_review': 'pending'})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--descriptive-only', action='store_true')
    args = parser.parse_args()
    rows = load_rows()
    hashes = {s: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for s, p in INPUTS.items()}
    if (OUT / 'manifest.json').exists():
        assert json.loads((OUT / 'manifest.json').read_text())['input_hashes'] == hashes
    else:
        save('manifest.json', {'inputs': INPUTS, 'input_hashes': hashes, 'judge': 'qwen3:8b',
            'judge_is_same_as_generator': True, 'embedding': 'BAAI/bge-m3',
            'metrics': ['faithfulness', 'answer_relevancy', 'context_relevance_binary'],
            'context_relevance_binary': 'Custom RAGAS AspectCritic, not standard context precision or retrieval recall',
            'dataset_role': 'reused development set; not held-out',
            'revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'packages': {p: importlib.metadata.version(p) for p in ['ragas', 'langchain-ollama', 'sentence-transformers']},
            'unsupported_without_labels': ['factual_accuracy', 'reference_answer_similarity', 'recall@k', 'MRR', 'nDCG', 'reference_context_precision']})
    descriptive(rows)
    if not args.descriptive_only:
        try:
            asyncio.run(evaluate(rows))
        except Exception as exc:
            save('failure.json', {'error': repr(exc), 'time': time.time()})
            raise


if __name__ == '__main__':
    main()
