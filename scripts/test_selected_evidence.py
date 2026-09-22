"""Six generation-only calls with manually inspected corpus evidence; no live edits."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys
import time
import unicodedata
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.generation.ollama_generator import build_prompt, canonicalize_answer

OUT = ROOT / "docs/evaluation/selected_evidence_trial_2026_09_23"
CASES = [
    ("passport_01_documents", "passport", ["passport_73ac41f2327257f9_v2_0004"],
     "Application/enrolment checklist, not passport collection. Preserve conditional items. Six-bullet prompt may compress seven source items."),
    ("passport_02_fee", "passport", [f"passport_12e10027cfdfeeee_v2_{n:04d}" for n in range(7, 11)],
     "Four domestic e-passport categories. State location, pages, validity and delivery conditions; VAT is included. Do not substitute COI/MRP fees. General question also permits clarification."),
    ("brta_07_lost", "brta", ["brta_cbe22ab64acf3d03_v2_0013"],
     "Duplicate licence requirements only. Supports form, GD/traffic clearance, fee receipt and photo; does not supply a complete online procedure, exact fee or processing time."),
]


def save(path, value):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    tmp.replace(path)


def render(rows):
    lines = ["# Manually selected evidence diagnostic", "",
             "Generation-only experiment, not end-to-end retrieval or accuracy evaluation.",
             "Evidence relevance was inspected against saved corpus text, not independently verified against current government rules.",
             "Controlled answer paths, retrieval, reranking and language fallback are bypassed intentionally. Raw model output is retained.",
             "Source IDs list supplied evidence; they are not verified claim-level citations. Manual correctness review is pending.", ""]
    for row in rows:
        lines += [f"## {row['id']} / {row['model']}", "", row['question'], "",
                  f"Time: {row['seconds']} s; finish: {row['metadata'].get('done_reason')}; route: diagnostic_llm", "",
                  row['display_answer'], ""]
    return "\n".join(lines)


def prepare():
    source = ROOT / "docs/evaluation/user_30q_model_comparison_2026_09_22/answers_qwen3_8b.json"
    questions = {r['audit_item']['id']: r['audit_item']['question'] for r in json.loads(source.read_text())['rows']}
    jobs = []
    for model in ['qwen3:8b', 'llama3']:
        for key, domain, ids, note in CASES:
            cfg = json.loads((ROOT / f'domains/{domain}/config.json').read_text())
            chunk_path = ROOT / cfg['data']['chunk_output_path']
            chunks = {c['id']: c for c in map(json.loads, chunk_path.read_text().splitlines())}
            contexts = [chunks[i] for i in ids]
            provenance = []
            for c in contexts:
                snapshot = ROOT / c['metadata']['snapshot_path']
                # Compare canonical Unicode forms without changing the prompt text.
                body = c['content'].split('\n\n', 1)[1].strip()
                snapshot_text = re.sub(r'\[cite:\s*[^\]]+\]', '', snapshot.read_text())
                if unicodedata.normalize('NFC', body) not in unicodedata.normalize('NFC', snapshot_text):
                    raise ValueError(f"Source body mismatch: {c['id']}")
                provenance.append({'id': c['id'], 'snapshot_path': str(snapshot.relative_to(ROOT)),
                                   'snapshot_sha256': hashlib.sha256(snapshot.read_bytes()).hexdigest()})
            g = cfg['generation']
            jobs.append({'id': key, 'domain': domain, 'model': model, 'question': questions[key],
                         'contexts': contexts, 'review_note': note, 'provenance': provenance,
                         'prompt': build_prompt(questions[key], contexts),
                         'options': {k: g[k] for k in ['temperature', 'top_p', 'num_predict', 'repeat_last_n', 'repeat_penalty']},
                         'base_url': g['ollama_base_url'],
                         'chunk_file': str(chunk_path.relative_to(ROOT)),
                         'chunk_sha256': hashlib.sha256(chunk_path.read_bytes()).hexdigest()})
    with urllib.request.urlopen('http://localhost:11434/api/tags', timeout=10) as response:
        models = json.load(response)
    save(OUT / 'plan.json', {'baseline_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                           'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                           'model_inventory': models, 'jobs': jobs,
                           'limitations': 'Purposive known-failure sample; not held-out accuracy. No prompt changes, source rewrites or fine-tuning. Four fee chunks intentionally bypass production top-three selection. Compare previous Qwen trial cautiously: not a contemporaneous baseline; no matching previous Llama trial.'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.prepare:
        if (OUT / 'plan.json').exists():
            raise RuntimeError('Frozen plan already exists; refusing overwrite')
        prepare()
        print('Saved six frozen jobs; no generation performed.', flush=True)
        return
    plan = json.loads((OUT / 'plan.json').read_text())
    rows = json.loads((OUT / 'results.json').read_text())['rows'] if (OUT / 'results.json').exists() else []
    completed = {(r['id'], r['model']) for r in rows}
    for job in plan['jobs']:
        if (job['id'], job['model']) in completed:
            continue
        print('Starting', job['model'], job['id'], flush=True)
        started = time.monotonic()
        payload = {'model': job['model'], 'messages': [{'role': 'user', 'content': job['prompt']}],
                   'stream': False, 'options': job['options']}
        if job['model'].startswith('qwen3'):
            payload['think'] = False
        try:
            request = urllib.request.Request(job['base_url'].rstrip('/') + '/api/chat',
                                             data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=900) as response:
                result = json.load(response)
            if not result.get('done') or 'message' not in result:
                raise RuntimeError(str(result))
        except Exception as exc:
            save(OUT / 'failure.json', {'id': job['id'], 'model': job['model'], 'error': repr(exc), 'time': time.time()})
            raise
        raw = result['message']['content']
        rows.append({'id': job['id'], 'model': job['model'], 'question': job['question'],
                     'seconds': round(time.monotonic() - started, 2), 'raw_answer': raw,
                     'display_answer': canonicalize_answer(raw, [c['id'] for c in job['contexts']]),
                     'message': result['message'], 'metadata': {k: v for k, v in result.items() if k != 'message'},
                     'route': 'diagnostic_llm', 'correctness': 'pending_manual_review'})
        save(OUT / 'results.json', {'rows': rows})
        (OUT / 'results.md').write_text(render(rows))
        print(f'Completed {len(rows)}/6 requests; correctness not yet reviewed.', flush=True)
    print('COMPLETE: 6/6. Manual review pending.', flush=True)


if __name__ == '__main__':
    main()
