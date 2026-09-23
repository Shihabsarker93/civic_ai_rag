"""Replay saved candidates without retrieval or LLM calls; not an accuracy test."""
import hashlib
import json
import subprocess
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.generation.evidence_selection import select_evidence

BASELINE = 'codex/pre-chunk-order-fix-20260923'


def main():
    baseline = types.ModuleType('baseline_selection')
    sys.modules[baseline.__name__] = baseline
    code = subprocess.check_output(
        ['git', 'show', f'{BASELINE}:src/generation/evidence_selection.py'], cwd=ROOT, text=True)
    exec(compile(code, 'baseline_selection.py', 'exec'), baseline.__dict__)
    source = ROOT / 'docs/evaluation/overnight_qwen3_2026_09_23/answers.json'
    saved = json.loads(source.read_text())
    corpora, hashes, rows = {}, {}, []
    for row in saved['rows']:
        item = row['audit_item']
        domain = item['domain']
        if domain not in corpora:
            config = json.loads((ROOT / 'domains' / domain / 'config.json').read_text())
            path = ROOT / config['data']['chunk_output_path']
            corpora[domain] = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
            hashes[domain] = {'path': str(path.relative_to(ROOT)),
                              'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        candidates = row['result']['sources']
        old = baseline.select_evidence(item['question'], candidates, corpora[domain])
        new = select_evidence(item['question'], candidates, corpora[domain])
        old_ids, new_ids = old.trace['selected_ids'], new.trace['selected_ids']
        assert len(new_ids) == len(set(new_ids)) <= 6
        assert new.trace['selected_chars'] <= 14000
        rows.append({'id': item['id'], 'domain': domain, 'question': item['question'],
                     'baseline_ids': old_ids, 'new_ids': new_ids,
                     'matches_saved_baseline': old_ids == row['result']['evidence_selection']['selected_ids'],
                     'added': [i for i in new_ids if i not in old_ids],
                     'removed': [i for i in old_ids if i not in new_ids],
                     'changed': old_ids != new_ids, 'trace': new.trace})
    target = ROOT / 'docs/evaluation/chunk_order_fix_2026_09_23'
    target.mkdir(parents=True, exist_ok=True)
    report = {'note': 'Selection-only replay of saved candidates with current corpus. No new retrieval or generation. Correctness not assessed.',
              'baseline': BASELINE, 'corpora': hashes, 'rows': rows}
    (target / 'selection_replay.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'rows': len(rows), 'changed': sum(r['changed'] for r in rows),
                      'baseline_mismatches': [r['id'] for r in rows if not r['matches_saved_baseline']],
                      'changes': [{k: r[k] for k in ('id', 'added', 'removed')} for r in rows if r['changed']]}, indent=2))


if __name__ == '__main__':
    main()
