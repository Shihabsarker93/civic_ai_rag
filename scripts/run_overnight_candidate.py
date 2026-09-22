"""One local batch, no AI monitoring or automatic answer scoring."""
import hashlib
import json
from pathlib import Path
import subprocess
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/evaluation/overnight_qwen3_2026_09_23'


def save(name, data):
    path = OUT / name
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    tmp.replace(path)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / 'plan.json').exists():
        raise RuntimeError('Existing run preserved. Refusing overwrite.')
    source = ROOT / 'docs/evaluation/user_30q_model_comparison_2026_09_22/questions.json'
    items = json.loads(source.read_text())['questions']
    assert len(items) == 30
    revision = git('rev-parse', 'HEAD')
    branch = git('branch', '--show-current')
    files = list((ROOT / 'src').rglob('*.py')) + [ROOT / 'app.py']
    for domain in ['passport', 'brta', 'birth_death_registration']:
        config = ROOT / f'domains/{domain}/config.json'
        files.extend([config, ROOT / json.loads(config.read_text())['data']['chunk_output_path']])
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    save('plan.json', {'model': 'qwen3:8b', 'revision': revision, 'branch': branch,
                       'questions': items, 'file_hashes': hashes,
                       'note': 'Existing development questions. Full local CivicRAG candidate, not manually selected context. No correctness scoring.'})
    rows = []
    for item in items:
        try:
            if git('rev-parse', 'HEAD') != revision or any(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != h for p, h in hashes.items()):
                raise RuntimeError('Code/config/corpus changed during frozen run; stopped.')
            with urllib.request.urlopen('http://127.0.0.1:7860/health', timeout=10) as response:
                assert json.load(response).get('pipeline_variant') == 'applicability_v1'
            payload = {'query': item['question'], 'domain': item['domain'], 'model': 'qwen3:8b', 'method': 'civic'}
            print('Starting', item['id'], flush=True)
            started = time.monotonic()
            request = urllib.request.Request('http://127.0.0.1:7860/chat', data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=1800) as response:
                result = json.load(response)
            assert result.get('pipeline_variant') == 'applicability_v1', result
            rows.append({'audit_item': item, 'elapsed_seconds': round(time.monotonic()-started, 2), 'result': result})
            save('answers.json', {'model': 'qwen3:8b', 'rows': rows})
            lines = ['# Overnight Qwen3 candidate outputs', '', 'Raw outputs; correctness review pending. Sources are context IDs, not verified claim-level citations.', '']
            for row in rows:
                r = row['result']
                lines += [f"## {row['audit_item']['id']}", '', r['query'], '', f"Route: {r['answer_route']}; time: {row['elapsed_seconds']} s", '', r['answer'], '', 'Selected evidence: ' + ', '.join(c['id'] for c in r.get('answer_contexts', [])), '']
            (OUT / 'answers.md').write_text('\n'.join(lines))
            print(f'Completed {len(rows)}/30 requests; not scored.', flush=True)
        except Exception as exc:
            save('failure.json', {'question': item['id'], 'completed': len(rows), 'error': repr(exc)})
            raise
    save('completion.json', {'completed': len(rows), 'manual_review': 'pending'})
    if git('branch', '--show-current') != branch or git('rev-parse', 'HEAD') != revision:
        raise RuntimeError('Git state changed; outputs kept locally, automatic publication skipped.')
    if git('diff', '--cached', '--name-only'):
        raise RuntimeError('Other staged work exists; outputs kept locally, automatic commit skipped.')
    names = ['plan.json', 'answers.json', 'answers.md', 'completion.json']
    git('add', *[str((OUT / n).relative_to(ROOT)) for n in names])
    git('commit', '-m', 'Save overnight 30-question Qwen3 candidate outputs; review pending')
    git('push', 'origin', 'HEAD')
    print('Complete and pushed. No correctness audit performed.', flush=True)


if __name__ == '__main__':
    main()
