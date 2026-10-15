"""Build isolated, source-preserving candidates across the three civic domains."""
from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.clean_service_corpora import has_evidence
from scripts.manage_experimental_domains import parse_markdown


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write('\n')


def normalize_row(row):
    result = copy.deepcopy(row)
    changed = []
    for field in ('content', 'retrieval_text'):
        if field not in row:
            continue
        before = row[field]
        after = unicodedata.normalize('NFC', before)
        # Canonical equivalence must preserve the complete text, not just numbers.
        if unicodedata.normalize('NFD', before) != unicodedata.normalize('NFD', after):
            raise ValueError('Noncanonical text change')
        if re.findall(r'\d+', before) != re.findall(r'\d+', after):
            raise ValueError('Numeric sequence changed')
        if before != after:
            changed.append(field)
        result[field] = after
    return result, changed


def heading_only(row, body):
    metadata = row['metadata']
    a, b = metadata.get('body_start'), metadata.get('body_end')
    if not isinstance(a, int) or not isinstance(b, int) or not 0 <= a < b <= len(body):
        return False
    evidence = body[a:b]
    # Require an exact source span, with at least one actual heading.
    return (evidence in row['content'] and bool(re.search(r'(?m)^#{1,6}\s+\S', evidence))
            and not has_evidence(evidence))


def pdf_probe(path):
    result = {'path': str(path), 'exists': path.exists()}
    if not path.exists():
        return result
    result['sha256'] = digest(path)
    if path.suffix.lower() != '.pdf':
        result['status'] = 'non_pdf_not_extracted'
        return result
    try:
        info = subprocess.run(['pdfinfo', str(path)], capture_output=True, text=True,
                              timeout=30, check=True).stdout
        pages = re.search(r'(?m)^Pages:\s+(\d+)', info)
        text = subprocess.run(['pdftotext', '-layout', str(path), '-'], capture_output=True,
                              text=True, timeout=90, check=True).stdout
        result.update(pages=int(pages[1]) if pages else None,
                      extracted_characters=len(text.strip()),
                      bengali_characters=sum('\u0980' <= c <= '\u09ff' for c in text),
                      extracted_text_sha256=hashlib.sha256(text.encode()).hexdigest(),
                      status='text_layer_probed_not_visually_verified')
        result['pages_without_extractable_text'] = [
            i + 1 for i, page in enumerate(text.split('\f')[:result['pages']]) if not page.strip()]
    except (subprocess.SubprocessError, OSError) as error:
        result.update(status='extraction_failed', error=str(error))
    return result


def prepare(output, birth_candidate):
    from transformers import AutoTokenizer
    birth_candidate = birth_candidate.resolve()
    output = output.resolve()
    output.relative_to(ROOT)
    if output.exists():
        raise ValueError('Choose a fresh release directory')
    configs = {d: ROOT / 'domains' / d / 'config.json'
               for d in ('birth_death_registration', 'passport', 'brta')}
    protected = {}
    for path in configs.values():
        config = json.loads(path.read_text())
        for p in [path, ROOT / config['data']['chunk_output_path']]:
            protected[str(p.relative_to(ROOT))] = digest(p)
    for d in ('passport', 'brta'):
        register = ROOT / 'domains' / d / 'data/register.json'
        protected[str(register.relative_to(ROOT))] = digest(register)
        for doc in json.loads(register.read_text())['documents']:
            p = ROOT / doc['snapshot_path']
            if digest(p) != doc['sha256']:
                raise ValueError('Source snapshot changed: ' + doc['document_id'])
            protected[str(p.relative_to(ROOT))] = digest(p)
    tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-m3', local_files_only=True)
    output.mkdir(parents=True)
    summary = {'status': 'unactivated', 'protected_files': protected, 'domains': {}}
    probes = {}
    for domain, config_path in configs.items():
        directory = output / domain
        directory.mkdir()
        config = json.loads(config_path.read_text())
        active = ROOT / config['data']['chunk_output_path']
        source = birth_candidate / 'chunks.jsonl' if domain == 'birth_death_registration' else active
        rows = [json.loads(line) for line in source.read_text().splitlines() if line.strip()]
        bodies, documents = {}, []
        if domain != 'birth_death_registration':
            register = json.loads((ROOT / 'domains' / domain / 'data/register.json').read_text())
            for doc in register['documents']:
                bodies[doc['document_id']] = parse_markdown((ROOT / doc['snapshot_path']).read_text())[1]
                originals = []
                for original in doc.get('original_candidates', []):
                    path = Path(original['path'])
                    if str(path) not in probes:
                        probes[str(path)] = pdf_probe(path)
                    probe = probes[str(path)]
                    originals.append({**probe, 'registered_sha256': original['sha256'],
                                      'hash_matches': probe.get('sha256') == original['sha256']})
                documents.append({'document_id': doc['document_id'], 'snapshot': doc['snapshot_path'],
                                  'snapshot_sha256': doc['sha256'], 'originals': originals,
                                  'source_association': 'unresolved' if not originals else 'registered_not_content_certified'})
        excluded, kept, transformations = [], [], []
        counts = Counter(row['metadata'].get('doc_id') for row in rows)
        for row in rows:
            doc_id = row['metadata'].get('doc_id')
            if doc_id in bodies and heading_only(row, bodies[doc_id]) and counts[doc_id] > 1:
                counts[doc_id] -= 1
                excluded.append({'id': row['id'], 'reason': 'source_verified_heading_only',
                                 'source_row': row})
                continue
            normalized, fields = normalize_row(row)
            if fields:
                transformations.append({'id': row['id'], 'fields': fields, 'operation': 'NFC_only'})
            kept.append(normalized)
        if len({r['id'] for r in kept}) != len(kept):
            raise ValueError('Duplicate IDs')
        lengths = tokenizer([r.get('retrieval_text', r['content']) for r in kept],
                            truncation=False, padding=False)['input_ids']
        for row, tokens in zip(kept, lengths):
            if len(tokens) > 8192:
                raise ValueError('Embedding input exceeds limit: ' + row['id'])
            row['metadata'].update(cleanup_revision=output.name,
                                   retrieval_token_count=len(tokens), embedding_model_max_tokens=8192)
        chunks_path = directory / 'chunks.jsonl'
        with chunks_path.open('x', encoding='utf-8') as handle:
            for row in kept:
                handle.write(json.dumps(row, ensure_ascii=False) + '\n')
        write(directory / 'baseline_config.json', config)
        candidate = copy.deepcopy(config)
        candidate['data'].update(chunk_output_path=str(chunks_path.relative_to(ROOT)),
                                 chroma_persist_dir=f'domains/{domain}/data/processed/chroma_{output.name}',
                                 collection_name=f'{domain}_{output.name}')
        write(directory / 'candidate_config.json', candidate)
        write(directory / 'source_register_audit.json', documents)
        write(directory / 'excluded_heading_units.json', excluded)
        write(directory / 'normalization_changes.json', transformations)
        report = {'source_chunk_path': str(source.relative_to(ROOT)), 'source_sha256': digest(source),
                  'candidate_sha256': digest(chunks_path), 'input_chunks': len(rows),
                  'candidate_chunks': len(kept), 'excluded_heading_units': len(excluded),
                  'normalized_chunks': len(transformations), 'max_tokens': max(map(len, lengths)),
                  'registered_documents': len(documents),
                  'unresolved_original_associations': sum(not d['originals'] for d in documents),
                  'original_hash_failures': sum(not o['hash_matches'] for d in documents for o in d['originals']),
                  'limits': 'No semantic rewrite, source currency certification, or activation. Source offsets refer to preserved input.'}
        if report['original_hash_failures']:
            raise ValueError('Original file integrity failed')
        write(directory / 'manifest.json', report)
        summary['domains'][domain] = report
        print(domain, json.dumps(report), flush=True)
    if any(digest(ROOT / path) != sha for path, sha in protected.items()):
        raise ValueError('Protected baseline changed')
    summary['baseline_unchanged'] = True
    write(output / 'manifest.json', summary)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--birth-candidate', type=Path, required=True)
    args = parser.parse_args()
    prepare(args.output, args.birth_candidate)
