"""Isolated Qwen3 distraction/order experiment; never changes production state."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.generation.ollama_generator import build_prompt, canonicalize_answer

OUT = ROOT / 'docs/evaluation/evidence_order_trial_2026_09_23'
DISTRACTORS = {
    'passport_01_documents': ['passport_23d845d3ab38ea43_v2_0040'],
    'passport_02_fee': ['passport_6f7d900581956bef_v2_0016', 'passport_5eb6c21efe103a4f_v2_0026'],
    'brta_07_lost': ['brta_4e08eb4e988d38e4_v2_0023'],
}


def save(path, obj):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    temp.replace(path)


def prepare():
    selected = ROOT / 'docs/evaluation/selected_evidence_trial_2026_09_23/plan.json'
    original = ROOT / 'docs/evaluation/source_preference_trial_2026_09_22/plan.json'
    old = {j['id']: j for j in json.loads(original.read_text())['jobs'] if j['variant'] == 'baseline'}
    jobs = []
    for j in json.loads(selected.read_text())['jobs']:
        if j['model'] != 'qwen3:8b':
            continue
        relevant = j['contexts']
        by_id = {c['id']: c for c in old[j['id']]['contexts']}
        extra = [by_id[i] for i in DISTRACTORS[j['id']]]
        assert not set(c['id'] for c in relevant) & set(c['id'] for c in extra)
        for variant, contexts in [('selected_only', relevant), ('relevant_first', relevant + extra), ('distractors_first', extra + relevant)]:
            jobs.append({'id': j['id'], 'question': j['question'], 'model': j['model'],
                         'variant': variant, 'contexts': contexts,
                         'relevant_ids': [c['id'] for c in relevant], 'distractor_ids': [c['id'] for c in extra],
                         'prompt': build_prompt(j['question'], contexts),
                         'options': dict(j['options'], seed=42, num_ctx=8192),
                         'think': False, 'base_url': j['base_url']})
    with urllib.request.urlopen('http://localhost:11434/api/tags', timeout=10) as r:
        inventory = json.load(r)
    save(OUT / 'plan.json', {'baseline_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                           'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                           'input_hashes': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in [selected, original]},
                           'model_inventory': inventory, 'jobs': jobs,
                           'limitations': 'Nine calls, one seed, known failures only. Generation-only; no production retrieval or controlled paths. Seed and 8192 context explicitly fixed across new calls, unlike earlier diagnostics; use new selected_only controls. Original rank-preferring prompt retained, so order effect includes explicit Source 1 priority, not a pure intrinsic positional-bias measurement.'})


def render(rows):
    lines = ['# Qwen3 evidence distraction/order trial', '',
             'Generation-only diagnostic, not end-to-end accuracy. Raw answers unchanged.',
             'Source footer lists all supplied contexts, not verified citations. See findings.md for assessment.', '']
    for r in rows:
        lines += [f"## {r['id']} / {r['variant']}", '', r['question'], '',
                  f"Model: qwen3:8b; seconds: {r['seconds']}; finish: {r['metadata'].get('done_reason')}", '',
                  r['display_answer'], '']
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prepare', action='store_true')
    args = p.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.prepare:
        if (OUT / 'plan.json').exists():
            raise RuntimeError('Refusing to replace frozen plan')
        prepare()
        print('Prepared nine calls; no model generation yet.', flush=True)
        return
    plan = json.loads((OUT / 'plan.json').read_text())
    rows = json.loads((OUT / 'results.json').read_text())['rows'] if (OUT / 'results.json').exists() else []
    completed = {(r['id'], r['variant']) for r in rows}
    for j in plan['jobs']:
        if (j['id'], j['variant']) in completed:
            continue
        print('Starting', j['id'], j['variant'], flush=True)
        start = time.monotonic()
        payload = {'model': j['model'], 'messages': [{'role': 'user', 'content': j['prompt']}],
                   'stream': False, 'think': j['think'], 'options': j['options']}
        try:
            request = urllib.request.Request(j['base_url'].rstrip('/') + '/api/chat', data=json.dumps(payload).encode(),
                                             headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=1200) as response:
                result = json.load(response)
            if not result.get('done') or 'message' not in result:
                raise RuntimeError(str(result))
        except Exception as exc:
            save(OUT / 'failure.json', {'id': j['id'], 'variant': j['variant'], 'error': repr(exc), 'time': time.time()})
            raise
        raw = result['message']['content']
        rows.append({'id': j['id'], 'variant': j['variant'], 'model': j['model'], 'question': j['question'],
                     'seconds': round(time.monotonic() - start, 2), 'raw_answer': raw,
                     'display_answer': canonicalize_answer(raw, [c['id'] for c in j['contexts']]),
                     'context_ids': [c['id'] for c in j['contexts']], 'message': result['message'],
                     'metadata': {k: v for k, v in result.items() if k != 'message'},
                     'route': 'diagnostic_llm', 'correctness': 'not_automatically_scored'})
        save(OUT / 'results.json', {'rows': rows})
        (OUT / 'results.md').write_text(render(rows))
        print(f'Completed {len(rows)}/9 requests; correctness not scored.', flush=True)
    print('COMPLETE: 9/9', flush=True)


if __name__ == '__main__':
    main()
