"""Save frozen-context screening checks and three live Qwen3 smoke answers."""
import argparse
import json
from pathlib import Path
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.generation.evidence_selection import select_evidence

OUT = ROOT / 'docs/evaluation/applicability_candidate_2026_09_23'


def save(name, value):
    path = OUT / name
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def main():
    global OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--follow-up', action='store_true')
    parser.add_argument('--domain', choices=['passport', 'brta', 'birth_death_registration'])
    args = parser.parse_args()
    if args.follow_up:
        OUT = OUT / 'followup'
    OUT.mkdir(parents=True, exist_ok=True)
    if not args.live:
        source = json.loads((ROOT / 'docs/evaluation/user_30q_model_comparison_2026_09_22/answers_qwen3_8b.json').read_text())
        corpora, rows = {}, []
        for row in source['rows']:
            item = row['audit_item']
            domain = item['domain']
            if domain not in corpora:
                cfg = json.loads((ROOT / f'domains/{domain}/config.json').read_text())
                corpora[domain] = [json.loads(l) for l in (ROOT / cfg['data']['chunk_output_path']).read_text().splitlines()]
            s = select_evidence(item['question'], row['result']['sources'], corpora[domain])
            rows.append({'id': item['id'], 'domain': domain, 'question': item['question'], 'trace': s.trace})
        save('frozen_30q_selection.json', {'note': 'Screening only on historical retrieved contexts. No new retrieval or generation; not accuracy.', 'rows': rows})
        print('30 frozen selections; empty:', [r['id'] for r in rows if not r['trace']['selected_ids']])
        return
    jobs = [
        ('passport', 'নতুন পাসপোর্ট করতে কী কী কাগজপত্র লাগবে?'),
        ('brta', 'ড্রাইভিং লাইসেন্স হারিয়ে গেলে কী করতে হবে?'),
        ('birth_death_registration', 'জন্মনিবন্ধন অনলাইনে কীভাবে করব?'),
    ]
    if args.domain:
        jobs = [job for job in jobs if job[0] == args.domain]
    if (OUT / 'smoke.json').exists():
        raise RuntimeError('Refusing to overwrite smoke results')
    rows = []
    for domain, query in jobs:
        print('Starting', domain, flush=True)
        start = time.monotonic()
        payload = {'domain': domain, 'query': query, 'model': 'qwen3:8b', 'method': 'civic'}
        request = urllib.request.Request('http://127.0.0.1:7860/chat', data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(request, timeout=1200) as response:
                result = json.load(response)
            assert result.get('pipeline_variant') == 'applicability_v1', result
        except Exception as exc:
            save('failure.json', {'domain': domain, 'error': repr(exc)})
            raise
        rows.append({'request': payload, 'seconds': round(time.monotonic()-start, 2), 'result': result})
        save('smoke.json', {'note': 'Three known functional smoke cases, not a held-out evaluation.', 'rows': rows})
        lines = ['# Applicability candidate: live smoke answers', '', 'Known questions, not accuracy evaluation. Full retrieval and selected-evidence generation.', '']
        for row in rows:
            r = row['result']
            lines += [f"## {r['domain']}", '', r['query'], '', f"Route: {r['answer_route']}; seconds: {row['seconds']}", '', r['answer'], '']
        (OUT / 'smoke.md').write_text('\n'.join(lines))
        print('Completed', len(rows), '/', len(jobs), result['answer_route'], flush=True)


if __name__ == '__main__':
    main()
