"""Frozen dense-only baseline; no live chatbot changes or automatic grading."""
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.pipeline import CivicRAGPipeline
from scripts import run_overnight_candidate as storage

OUT = ROOT / 'docs/evaluation/simple_matched_qwen3_30q_2026_09_24'


def answer(pipeline, query):
    query = pipeline._normalize_query_text(query)
    candidates = [pipeline._context_from_result(r) for r in pipeline.retrieve(query, 'simple')]
    evidence, chars = [], 0
    for c in candidates:
        size = len(c['content'])
        if size and len(evidence) < 6 and chars + size <= 14000:
            evidence.append(c)
            chars += size
    raw, output, metadata, route = '', '', {}, 'no_applicable_evidence'
    if evidence:
        generator = pipeline._generator('qwen3:8b', selected_evidence=True)
        output = generator.answer(query, evidence)
        raw = output
        metadata = generator.last_metadata
        route = 'llm_dense_evidence'
        if pipeline._violates_answer_language(query, output):
            output = pipeline._bangla_language_safety_answer(evidence)
            route = 'selected_evidence_language_rejection'
        elif metadata.get('done_reason') == 'length':
            output += '\n\nসতর্কতা: আউটপুট সীমার কারণে উত্তরটি অসম্পূর্ণ। এটিকে সম্পূর্ণ নির্দেশনা হিসেবে ব্যবহার করবেন না।'
            route = 'selected_evidence_truncated'
    else:
        output = 'প্রশ্নটির সেবা ও কাজের সঙ্গে মেলে এমন পর্যাপ্ত তথ্য পাওয়া যায়নি। কোন সেবা এবং কী করতে চান একটু স্পষ্ট করে বলুন।'
    return dict(query=query, model='qwen3:8b', method='simple_matched',
                domain=pipeline.domain_id, answer=output, raw_generation=raw,
                generation_metadata=metadata, answer_route=route, sources=candidates,
                answer_contexts=evidence, pipeline_variant='dense_matched_v1')


def main():
    storage.OUT = OUT
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / 'plan.json').exists():
        raise RuntimeError('Refusing to overwrite existing run')
    prior_path = ROOT / 'docs/evaluation/chunk_order_fixed_qwen3_30q_2026_09_23/plan.json'
    prior = json.loads(prior_path.read_text())
    hashes = prior['file_hashes']
    def verify():
        for path, expected in hashes.items():
            if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected:
                raise RuntimeError(f'Configuration/code/corpus differs from saved CivicRAG run: {path}')
    verify()
    revision, branch = storage.git('rev-parse', 'HEAD'), storage.git('branch', '--show-current')
    storage.save('plan.json', dict(model='qwen3:8b', revision=revision, branch=branch,
        questions=prior['questions'], file_hashes=hashes,
        comparison_plan=str(prior_path.relative_to(ROOT)),
        protocol='Dense top 6, whole-chunk 14000-character budget, identical selected-evidence prompt and generator settings; no RRF, reranking, expansion or controlled answers. Development-set evaluation.'))
    rows, pipelines, shared = [], {}, None
    for item in prior['questions']:
        try:
            verify()
            if storage.git('rev-parse', 'HEAD') != revision:
                raise RuntimeError('Git revision changed during run')
            domain = item['domain']
            if domain not in pipelines:
                print('Loading domain', domain, flush=True)
                pipelines[domain] = CivicRAGPipeline(ROOT, ROOT / f'domains/{domain}/config.json', shared_pipeline=shared)
                shared = shared or pipelines[domain]
            print('Starting', item['id'], flush=True)
            start = time.monotonic()
            result = answer(pipelines[domain], item['question'])
            rows.append(dict(audit_item=item, elapsed_seconds=round(time.monotonic()-start, 2), result=result))
            storage.save('answers.json', dict(model='qwen3:8b', rows=rows))
            lines = ['# Matched Simple RAG / Qwen3 answers', '',
                     'Raw outputs; correctness review pending. Source IDs are supplied context, not verified citations.', '']
            for row in rows:
                r = row['result']
                lines.extend([f"## {row['audit_item']['id']}", '', r['query'], '',
                    f"Route: {r['answer_route']}; time: {row['elapsed_seconds']} s", '', r['answer'], '',
                    'Supplied evidence: ' + ', '.join(c['id'] for c in r['answer_contexts']), ''])
            (OUT / 'answers.md').write_text('\n'.join(lines))
            print(f'Completed {len(rows)}/30 requests; not scored.', flush=True)
        except Exception as exc:
            storage.save('failure.json', dict(question=item['id'], completed=len(rows), error=repr(exc)))
            raise
    storage.save('completion.json', dict(completed=len(rows), manual_review='pending'))
    if storage.git('rev-parse', 'HEAD') != revision or storage.git('branch', '--show-current') != branch or storage.git('diff', '--cached', '--name-only'):
        raise RuntimeError('Git state changed; results preserved locally; publication skipped')
    storage.git('add', *[str((OUT / name).relative_to(ROOT)) for name in ('plan.json', 'answers.json', 'answers.md', 'completion.json')])
    storage.git('commit', '-m', 'Save matched Simple RAG Qwen3 30-question results; unscored')
    storage.git('push', 'origin', 'HEAD')
    print('Complete and pushed; correctness not audited.', flush=True)


if __name__ == '__main__':
    main()
