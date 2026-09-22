"""Validate every registered document and chunk, independent of evaluation questions."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.manage_experimental_domains import digest, read_chunks, write_json


def audit(directory: Path, tokenizer=None):
    manifest = json.loads((directory / 'manifest.json').read_text())
    domain = manifest['domain']
    register = json.loads((ROOT / 'domains' / domain / 'data/register.json').read_text())
    chunks = read_chunks(directory / 'chunks.jsonl')
    baseline_config = json.loads((directory / 'baseline_config.json').read_text())
    baseline = {c['id']: c for c in read_chunks(ROOT / baseline_config['data']['master_chunk_path'])}
    by_id = {c['id']: c for c in chunks}
    errors, documents, duplicated, passages = [], [], defaultdict(list), defaultdict(list)
    register_by_id = {d['document_id']: d for d in register['documents']}
    if len(by_id) != len(chunks):
        errors.append('Duplicate chunk IDs')
    registered = {d['document_id'] for d in register['documents']}
    listed = {d['document_id'] for d in manifest['documents']}
    if registered != listed or len(listed) != len(manifest['documents']):
        errors.append('Registered document coverage mismatch')
    covered_ids = []
    for doc in manifest['documents']:
        doc_errors = []
        source = (ROOT / doc['source']).read_bytes()
        body = (ROOT / doc['cleaned_path']).read_text()
        registered_doc = register_by_id.get(doc['document_id'], {})
        if registered_doc.get('sha256') != doc['source_sha256'] or registered_doc.get('snapshot_path') != doc['source']:
            doc_errors.append('Manifest provenance differs from original register')
        if digest(source) != doc['source_sha256']:
            doc_errors.append('Original SHA mismatch')
        if digest(body.encode()) != doc['cleaned_sha256']:
            doc_errors.append('Derived SHA mismatch')
        duplicated[digest(body.encode())].append(doc['document_id'])
        for match in re.finditer(r'\S[\s\S]*?(?=\n\s*\n|\Z)', body):
            normalized = re.sub(r'\s+', ' ', match[0]).strip()
            if len(normalized) >= 120:
                passages[normalized].append({'document_id': doc['document_id'],
                                             'start': match.start(), 'end': match.end()})
        preserved = 'unstructured_ocr_preserved_requires_pdf_review' in doc['review_flags']
        intervals = [(s['start'], s['end']) for s in doc['retained_non_evidence_sections']]
        inherited_count, max_tokens = 0, 0
        if not doc['chunk_ids']:
            doc_errors.append('Document has no searchable chunk')
        for cid in doc['chunk_ids']:
            covered_ids.append(cid)
            c = by_id.get(cid)
            if c is None:
                doc_errors.append(f'Missing chunk {cid}')
                continue
            if c['metadata']['doc_id'] != doc['document_id']:
                doc_errors.append(f'Incorrect source owner: {cid}')
            if preserved:
                if c != baseline.get(cid):
                    doc_errors.append(f'Unreviewed OCR was changed: {cid}')
            else:
                a, b = c['metadata']['body_start'], c['metadata']['body_end']
                intervals.append((a, b))
                if not (0 <= a < b <= len(body)) or body[a:b] not in c['content']:
                    doc_errors.append(f'Exact source span missing: {cid}')
                for span in doc['context_spans'].get(cid, []):
                    x, y = span['start'], span['end']
                    if not (0 <= x < y <= a) or body[x:y].strip() not in c['content']:
                        doc_errors.append(f'Inherited context is not verbatim: {cid}')
                    inherited_count += 1
            if tokenizer:
                count = len(tokenizer(c['retrieval_text'], truncation=False)['input_ids'])
                max_tokens = max(max_tokens, count)
                if count > 8192:
                    doc_errors.append(f'Embedding token limit exceeded: {cid}: {count}')
        if not preserved:
            cursor = 0
            for a, b in sorted(intervals):
                if a != cursor:
                    doc_errors.append(f'Source gap or overlap at {cursor}/{a}')
                cursor = b
            if cursor != len(body):
                doc_errors.append('Incomplete body coverage')
        errors.extend(f"{doc['document_id']}: {e}" for e in doc_errors)
        documents.append({'document_id': doc['document_id'], 'path': doc['cleaned_path'],
                          'chunks': len(doc['chunk_ids']), 'errors': doc_errors,
                          'inherited_context_spans': inherited_count,
                          'max_embedding_tokens': max_tokens if tokenizer else None,
                          'review_flags': doc['review_flags'], 'findings': doc.get('findings', []),
                          'status': 'original_pdf_review_required' if preserved else 'structurally_valid' if not doc_errors else 'failed'})
    if Counter(covered_ids) != Counter(by_id.keys()):
        errors.append('Chunk-to-document ownership mismatch')
    report = {'domain': domain, 'documents': documents, 'document_count': len(documents),
              'chunk_count': len(chunks), 'errors': errors,
              'duplicate_document_groups': [ids for ids in duplicated.values() if len(ids) > 1],
              'repeated_passages': [{'text': text, 'occurrences': locations} for text, locations in passages.items()
                                    if len({p['document_id'] for p in locations}) > 1],
              'tokenizer_checked': tokenizer is not None,
              'interpretation': 'Structural integrity only; not factual correctness, legal currency, or answer accuracy.'}
    write_json(directory / 'corpus_audit.json', report)
    lines = [f'# {domain.upper()} whole-corpus audit', '', report['interpretation'], '',
             f"Documents: {len(documents)}. Chunks: {len(chunks)}. Structural errors: {len(errors)}.",
             f"Embedding token-limit validation: {'performed' if tokenizer else 'not performed'}.", '',
             f"Repeated passages across documents: {len(report['repeated_passages'])}. Exact text and all locations are in corpus_audit.json; retained pending applicability review.", '',
             'All originals are retained. Possible duplicates are reported, not deleted: differing dates and provenance must not be silently merged.', '',
             '| Document | Chunks | Status | Inherited source spans | Review findings |', '|---|---:|---|---:|---|']
    for d in documents:
        relative = Path(d['path']).relative_to(directory.relative_to(ROOT))
        issues = sorted(set(f.get('kind', f.get('reason', 'unknown')) for f in d['findings']))
        flags = ', '.join(d['review_flags'] + issues) or 'No automatic flags; factual review not certified'
        lines.append(f"| [{relative.name}](<{relative}>) | {d['chunks']} | {d['status']} | {d['inherited_context_spans']} | {flags} |")
    lines += ['', '## Exact duplicate documents', '', json.dumps(report['duplicate_document_groups'], ensure_ascii=False),
              '', '## Validation errors', '', '\n'.join(errors) or 'None.', '']
    (directory / 'CORPUS_AUDIT.md').write_text('\n'.join(lines))
    print(domain, len(documents), 'documents;', len(chunks), 'chunks;', len(errors), 'errors', flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--tokenizer', action='store_true')
    args = parser.parse_args()
    tokenizer = None
    if args.tokenizer:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-m3', local_files_only=True)
    result = audit(args.directory.resolve(), tokenizer)
    raise SystemExit(bool(result['errors']))
