"""Matched retrieval/selection diagnostics; no LLM generation or new relevance labels."""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
import os
from pathlib import Path
import sys
import time
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('HF_HUB_OFFLINE', '1')
os.environ.setdefault('TRANSFORMERS_OFFLINE', '1')
os.environ['CIVIC_EVIDENCE_SELECTION'] = '1'
from scripts.prepare_conservative_release import digest, write


def attach_structural(release, structural):
    import chromadb
    historical = {'passport': 'config.candidate_20260922_064339_716352.json',
                  'brta': 'config.candidate_20260922_063637_152241.json'}
    for domain, name in historical.items():
        config = json.loads((ROOT / 'domains' / domain / name).read_text())
        source = structural / domain / 'chunks.jsonl'
        fresh = {r['id']: r for r in map(json.loads, source.read_text().splitlines())}
        old = {r['id']: r for r in map(json.loads, (ROOT / config['data']['chunk_output_path']).read_text().splitlines())}
        if set(fresh) != set(old) or any(
            any(fresh[cid][field] != old[cid][field] for field in ('content', 'retrieval_text')) for cid in fresh
        ):
            raise ValueError('Fresh structural corpus does not match cached index inputs')
        collection = chromadb.PersistentClient(path=str(ROOT / config['data']['chroma_persist_dir'])).get_collection(config['data']['collection_name'])
        stored = collection.get(include=['documents'])
        if dict(zip(stored['ids'], stored['documents'])) != {cid: row['content'] for cid, row in fresh.items()}:
            raise ValueError('Historical structural index mismatches fresh corpus')
        baseline = json.loads((release / domain / 'baseline_config.json').read_text())
        for section in ('embedding', 'retrieval', 'reranking', 'generation'):
            if config[section] != baseline[section]:
                raise ValueError('Architectural settings differ: ' + section)
        config['data']['chunk_output_path'] = str(source.relative_to(ROOT))
        write(release / domain / 'structural_config.json', config)


def compare(release, device, structural=None):
    import torch
    from src.pipeline import CivicRAGPipeline
    from scripts.evaluate_service_cleanup import CASES, matches
    torch.set_num_threads(2)
    release = release.resolve()
    if structural:
        attach_structural(release, structural.resolve())
    output = release / 'diagnostics'
    if output.exists():
        raise ValueError('Diagnostic directory exists')
    output.mkdir()
    questions_path = ROOT / 'docs/evaluation/user_30q_model_comparison_2026_09_22/questions.json'
    questions = json.loads(questions_path.read_text())['questions']
    shared = None
    rows, supports = [], []
    for domain in ('birth_death_registration', 'passport', 'brta'):
        variants = [('baseline', 'baseline_config.json'), ('candidate', 'candidate_config.json')]
        if structural and domain != 'birth_death_registration':
            variants.append(('structural', 'structural_config.json'))
        for variant, name in variants:
            path = release / domain / name
            pipeline = CivicRAGPipeline(ROOT, path, shared_pipeline=shared)
            if shared is None:
                shared = pipeline
                shared.retriever.embedding_model.to(device)
                if shared.reranker.cross_encoder is None:
                    raise RuntimeError('Cross-encoder unavailable; no fallback comparison permitted')
                shared.reranker.cross_encoder.model.to(device)
            if set(pipeline.retriever.collection.get(include=[])['ids']) != set(pipeline.chunks_by_id):
                raise ValueError('Index and corpus IDs differ')
            queries = [(q['id'], q['question'], None) for q in questions if q['domain'] == domain]
            queries += [(f'diagnostic_{i}', query, (prefixes, hint))
                        for i, (d, query, prefixes, hint) in enumerate(CASES) if d == domain]
            for qid, query, support in queries:
                started = time.monotonic()
                result = pipeline.ask(query, generate=False)
                selected = result.get('answer_contexts', [])
                row = {'domain': domain, 'variant': variant, 'id': qid, 'query': query,
                       'candidate_ids': [r['id'] for r in result['sources']],
                       'selected_ids': [r['id'] for r in selected],
                       'selected_characters': sum(len(r['content']) for r in selected),
                       'selected_tokens': sum(len(pipeline.retriever.embedding_model.tokenizer.encode(r['content'])) for r in selected),
                       'tokenizer': 'BGE-M3; not generator tokens',
                       'selected_passages': selected, 'selection_trace': result.get('evidence_selection', {}),
                       'seconds': round(time.monotonic() - started, 3)}
                if support:
                    prefixes, hint = support
                    # Match canonically equivalent strings after NFC cleanup.
                    def supported(r):
                        return matches({**r, 'content': unicodedata.normalize('NFC', r['content'])},
                                       prefixes, unicodedata.normalize('NFC', hint))
                    if not any(supported(r) for r in pipeline.chunks):
                        raise ValueError('Diagnostic support absent from corpus: ' + query)
                    ranks = [i + 1 for i, r in enumerate(result['sources']) if supported(r)]
                    row.update(support_rank=min(ranks) if ranks else None,
                               selected_support=any(supported(r) for r in selected))
                    supports.append(row)
                else:
                    retriever = pipeline.retriever
                    settings = pipeline.retrieval_config
                    q = pipeline._normalize_query_text(query)
                    dense = retriever._dense_search(q, settings['top_k_dense'])
                    bm25 = retriever._bm25_search(q, settings['top_k_bm25'])
                    hybrid = [r.chunk_id for r in retriever._rrf_fuse({'dense': dense, 'bm25': bm25})]
                    row['top5'] = {'dense': dense[:5], 'bm25': bm25[:5], 'hybrid': hybrid[:5]}
                    rows.append(row)
                write(output / f'{domain}_{variant}_{qid}.json', row)
                print(domain, variant, qid, row['selected_characters'], flush=True)
    summaries = []
    for domain in ('birth_death_registration', 'passport', 'brta'):
        for variant in dict.fromkeys(r['variant'] for r in rows if r['domain'] == domain):
            subset = [r for r in rows if r['domain'] == domain and r['variant'] == variant]
            hints = [r for r in supports if r['domain'] == domain and r['variant'] == variant]
            summaries.append({'domain': domain, 'variant': variant, 'questions': len(subset),
                              'mean_selected_chars': sum(r['selected_characters'] for r in subset) / len(subset),
                              'empty_selections': sum(not r['selected_ids'] for r in subset),
                              'known_failure_cases': len(hints),
                              'known_failure_selected_support': sum(r['selected_support'] for r in hints)})
    manifest = json.loads((release / 'manifest.json').read_text())
    if any(digest(ROOT / p) != sha for p, sha in manifest['protected_files'].items()):
        raise ValueError('Protected baseline files changed')
    code_paths = ['src/pipeline.py', 'src/generation/evidence_selection.py',
                  'src/retrieval/hybrid_retriever.py', 'src/reranking/reranker.py']
    write(output / 'summary.json', {'results': summaries, 'question_file_sha256': digest(questions_path),
          'code_hashes': {p: digest(ROOT / p) for p in code_paths},
          'completed_runs': len(rows) + len(supports), 'llm_calls': 0,
          'cross_encoder_used': True, 'device': device,
          'scope': 'Reused development questions and designated-source diagnostics, not held-out accuracy.',
          'metric_limit': 'No fresh relevance labels; no new Hit/Precision/context-relevance scores claimed.',
          'baseline_files_unchanged': True})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', type=Path, required=True)
    parser.add_argument('--device', default='mps')
    parser.add_argument('--structural', type=Path)
    args = parser.parse_args()
    compare(args.release, args.device, args.structural)
