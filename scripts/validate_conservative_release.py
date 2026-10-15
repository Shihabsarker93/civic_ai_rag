"""Independently check candidate transformations and preserved source coverage."""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.prepare_conservative_release import digest, heading_only, write
from scripts.manage_experimental_domains import parse_markdown


def validate(release):
    from transformers import AutoTokenizer
    release = release.resolve()
    manifest = json.loads((release / 'manifest.json').read_text())
    tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-m3', local_files_only=True)
    errors, results = [], []
    for path, sha in manifest['protected_files'].items():
        if digest(ROOT / path) != sha:
            errors.append('Protected input changed: ' + path)
    for domain, report in manifest['domains'].items():
        directory = release / domain
        source_path = ROOT / report['source_chunk_path']
        if digest(source_path) != report['source_sha256']:
            errors.append('Candidate input changed: ' + domain)
        source = {r['id']: r for r in map(json.loads, source_path.read_text().splitlines())}
        path = directory / 'chunks.jsonl'
        if digest(path) != report['candidate_sha256']:
            errors.append('Candidate changed: ' + domain)
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        removed = json.loads((directory / 'excluded_heading_units.json').read_text())
        ids = {r['id'] for r in rows}
        removed_ids = {r['id'] for r in removed}
        if len(ids) != len(rows) or ids & removed_ids or ids | removed_ids != set(source):
            errors.append('Coverage or uniqueness failure: ' + domain)
        bodies = {}
        register = json.loads((directory / 'source_register_audit.json').read_text())
        for document in register:
            snapshot = ROOT / document['snapshot']
            if digest(snapshot) != document['snapshot_sha256']:
                errors.append('Snapshot changed: ' + document['document_id'])
            bodies[document['document_id']] = parse_markdown(snapshot.read_text())[1]
            if not any(r['metadata'].get('doc_id') == document['document_id'] for r in rows):
                errors.append('Document lost all evidence: ' + document['document_id'])
            for original in document['originals']:
                if digest(Path(original['path'])) != original['registered_sha256']:
                    errors.append('Original changed: ' + original['path'])
        for record in removed:
            row = source[record['id']]
            if row != record['source_row'] or not heading_only(row, bodies[row['metadata']['doc_id']]):
                errors.append('Unjustified exclusion: ' + row['id'])
        duplicates = defaultdict(list)
        for row in rows:
            old = source[row['id']]
            for field in ('content', 'retrieval_text'):
                if field in old and row[field] != unicodedata.normalize('NFC', old[field]):
                    errors.append('Unexpected evidence rewrite: ' + row['id'] + ':' + field)
            for key, value in old['metadata'].items():
                if key not in ('cleanup_revision', 'retrieval_token_count', 'embedding_model_max_tokens') and row['metadata'].get(key) != value:
                    errors.append('Source metadata changed: ' + row['id'] + ':' + key)
            count = len(tokenizer.encode(row.get('retrieval_text', row['content'])))
            if count != row['metadata']['retrieval_token_count'] or count > 8192:
                errors.append('Token audit mismatch: ' + row['id'])
            duplicates[row['content']].append(row['id'])
        results.append({'domain': domain, 'retained_chunks': len(rows), 'archived_heading_chunks': len(removed),
                        'source_documents_checked': len(register),
                        'exact_content_duplicate_groups': [v for v in duplicates.values() if len(v) > 1]})
    result = {'passed': not errors, 'errors': errors, 'domains': results,
              'scope': 'Canonical text equivalence, exact heading exclusions, complete source ownership, hashes and token limits; not OCR correctness.'}
    write(release / 'validation.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(not validate(args.release)['passed'])
