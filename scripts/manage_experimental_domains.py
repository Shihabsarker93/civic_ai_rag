"""Traceable, versioned ingestion for BRTA and passport; never modifies supplied files."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {'brta': ['brta', 'fahim_brta'], 'passport': ['cleaned_md']}
ORIGINALS = {'brta': ['brta_original_pdfs_araf', 'fahim_brta_original'], 'passport': ['passport_original_pdfs_araf']}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_name(value: str) -> str:
    return re.sub(r'[^\w\u0980-\u09ff]', '', unicodedata.normalize('NFC', value).lower()).replace('_', '')


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def read_chunks(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def write_chunks(path: Path, chunks: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in chunks), encoding='utf-8')


def parse_markdown(text: str) -> tuple[dict, str]:
    """Keep malformed/embedded metadata as text rather than silently discarding it."""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    metadata = {}
    match = re.match(r'\A---\s*\n(.*?)\n---\s*(?:\n|$)', text, re.S)
    if match:
        for line in match[1].splitlines():
            field = re.match(r'^([A-Za-z_][\w-]*):\s*(.*?)\s*$', line)
            if field:
                metadata[field[1]] = field[2].strip('"\'')
        text = text[match.end():]
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'\[cite:\s*[^\]]*\]', '', text)
    text = re.sub('[\u200b\ufeff]', '', text)
    return metadata, text.strip()


def spans(body: str, limit: int = 1400):
    """Contiguous, exhaustive spans; prefer headings/paragraphs, then lines/spaces."""
    start = 0
    while start < len(body):
        end = min(start + limit, len(body))
        if end < len(body):
            lower = start + limit // 2
            candidates = [m.start() + start for m in re.finditer(r'\n(?=#{1,6} )|\n\n', body[start:end])]
            candidates = [p for p in candidates if p >= lower]
            if candidates:
                end = candidates[-1]
            else:
                boundary = max(body.rfind('\n', lower, end), body.rfind(' ', lower, end))
                if boundary > start:
                    end = boundary + 1
        yield start, end
        start = end


def section_spans(body: str, title: str, limit: int = 1400):
    """Never mix sibling sections; keep a complete FAQ pair as one evidence unit."""
    headings = list(re.finditer(r'^(#{1,6})[ \t]+([^\n]+)$', body, re.M))
    boundaries = sorted({0, *(m.start() for m in headings), len(body)})
    at = {m.start(): m for m in headings}
    parents = []
    for start, end in zip(boundaries, boundaries[1:]):
        heading = at.get(start)
        if heading:
            level = len(heading[1])
            parents = [(n, name) for n, name in parents if n < level]
            parents.append((level, heading[2].strip()))
        section = ' > '.join(name for _, name in parents) or title
        text = body[start:end]
        label_prefix = r'(?im)^[ \t]*(?:[-*][ \t]+)?(?:\*\*)?(?:(?:English|Bengali|Bangla)[ \t]+)?'
        is_faq = bool(re.search(label_prefix + r'(?:Question|প্রশ্ন)(?:[ \t]*\([^\n)]*\))?[ \t]*:', text)
                      and re.search(label_prefix + r'(?:Answer|উত্তর)(?:[ \t]*\([^\n)]*\))?[ \t]*:', text))
        # Oversized FAQ units are rejected by the embedding token-limit check, not silently truncated.
        pieces = [(0, len(text))] if is_faq else list(spans(text, limit))
        for a, b in pieces:
            yield start+a, start+b, section, is_faq


def rechunk(domain: str) -> Path:
    base = ROOT / 'domains' / domain
    register = json.loads((base / 'data/register.json').read_text())
    old = read_chunks(base / 'data/interim/all_chunks.jsonl')
    templates = {c['metadata']['doc_id']: c['metadata'] for c in old}
    chunks = []
    for doc in register['documents']:
        if doc.get('error'): continue
        raw = (ROOT / doc['snapshot_path']).read_bytes()
        if digest(raw) != doc['sha256']: raise ValueError('Source snapshot changed')
        _, body = parse_markdown(raw.decode('utf-8'))
        meta = templates[doc['document_id']]
        pieces = list(section_spans(body, meta['title']))
        if ''.join(body[a:b] for a,b,_,_ in pieces) != body: raise ValueError('Chunk coverage lost')
        for number, (start, end, section, faq) in enumerate(pieces, 1):
            if not body[start:end].strip(): continue
            payload = {**meta, 'body_start':start, 'body_end':end, 'section_title':section,
                       'chunking_version':'heading_faq_v2', 'faq_unit':faq}
            content = f"{meta['title']}\n{section}\n\n{body[start:end]}"
            chunks.append({'id':f"{doc['document_id']}_v2_{number:04d}", 'content':content,
                           'retrieval_text':f'{domain}\n{content}', 'metadata':payload})
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    path = base / f'data/interim/all_chunks_heading_v2_{stamp}.jsonl'
    write_chunks(path, chunks)
    print(f'{domain}: prepared {len(chunks)} candidate chunks at {path.relative_to(ROOT)}', flush=True)
    return path


def prepare(source_root: Path, domain: str) -> None:
    base = ROOT / 'domains' / domain
    register_path = base / 'data/register.json'
    if register_path.exists():
        raise RuntimeError(f'{domain} already prepared; refusing to overwrite its register/snapshots')
    originals = []
    for folder in ORIGINALS[domain]:
        for p in sorted((source_root / folder).rglob('*.pdf')):
            originals.append({'path': str(p.resolve()), 'relative_path': str(p.relative_to(source_root)),
                              'sha256': digest(p.read_bytes()), 'status': 'reference_only_not_separately_embedded'})
    documents, chunks = [], []
    for folder in SOURCES[domain]:
        for p in sorted((source_root / folder).rglob('*.md')):
            raw = p.read_bytes()
            relative = str(p.relative_to(source_root))
            doc_id = domain + '_' + digest(unicodedata.normalize('NFC', relative).encode())[:16]
            snapshot = base / 'data/source_snapshots' / relative
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, snapshot)
            document = {'document_id': doc_id, 'source_path': str(p.resolve()), 'relative_path': relative,
                        'snapshot_path': str(snapshot.relative_to(ROOT)), 'sha256': digest(raw),
                        'requested_status': 'included', 'index_status': 'not_built', 'history': [], 'chunk_ids': []}
            try:
                text = raw.decode('utf-8')
                metadata, body = parse_markdown(text)
                if not body:
                    raise ValueError('No body text')
                names = {normalized_name(p.stem), normalized_name(Path(metadata.get('source_pdf', '')).stem)} - {''}
                matches = [o for o in originals if normalized_name(Path(o['path']).stem) in names]
                flags = []
                if not matches: flags.append('original_match_unresolved')
                if '[cite:' in text: flags.append('citation_markers_removed_from_derived_text')
                if not re.search(r'https?://|www\.', text): flags.append('no_web_address')
                if not text.startswith('---'): flags.append('nonstandard_metadata_layout')
                if re.search(r'২০০[০-৯]|২০১[০-৯]|202[0-5]|201[0-9]|200[0-9]', p.stem): flags.append('dated_document_review_applicability')
                if len(body) > 50000: flags.append('long_document_check_ocr')
                if 'ডাউনটাইম' in p.stem: flags.append('temporary_service_notice')
                document.update(original_candidates=matches, audit_flags=flags, declared_metadata=metadata,
                                normalized_body_sha256=digest(body.encode()), normalized_body_chars=len(body))
                title = metadata.get('title', p.stem)
                for number, (start, end, section, faq) in enumerate(section_spans(body, title), 1):
                    content = body[start:end]
                    if not content.strip(): continue
                    chunk_id = f'{doc_id}_v2_{number:04d}'
                    payload = {'domain': domain, 'doc_id': doc_id, 'document_id': doc_id,
                               'title': title, 'section_title': section, 'document_type': metadata.get('document_type', 'document'),
                               'source_path': str(p.resolve()), 'source_relative_path': relative,
                               'snapshot_path': str(snapshot.relative_to(ROOT)), 'source_sha256': digest(raw),
                               'original_paths': json.dumps([o['path'] for o in matches], ensure_ascii=False),
                               'document_date': metadata.get('date', metadata.get('effective_date', 'unknown')),
                               'date_verified': False, 'audit_flags': ', '.join(flags), 'experimental': True,
                               'body_start': start, 'body_end': end,
                               'chunking_version': 'heading_faq_v2', 'faq_unit': faq,
                               'source_url': metadata.get('source_url', '')}
                    chunks.append({'id': chunk_id, 'content': f'{title}\n{section}\n\n{content}',
                                   'retrieval_text': f'{domain}\n{title}\n{section}\n\n{content}', 'metadata': payload})
                    document['chunk_ids'].append(chunk_id)
            except (UnicodeError, ValueError) as exc:
                document.update(requested_status='failed', index_status='failed', error=str(exc))
            documents.append(document)
    write_chunks(base / 'data/interim/all_chunks.jsonl', chunks)
    write_json(register_path, {'domain': domain, 'source_root': str(source_root), 'originals': originals, 'documents': documents})
    print(f'{domain}: {len(documents)} Markdown documents, {len(chunks)} chunks, {sum(d["requested_status"]=="failed" for d in documents)} failures', flush=True)


def build(domain: str, device: str, chunks_path: Path | None = None, stage_only: bool = False) -> None:
    import chromadb
    from sentence_transformers import SentenceTransformer
    base = ROOT / 'domains' / domain
    register_path = base / 'data/register.json'
    register = json.loads(register_path.read_text())
    included = {d['document_id'] for d in register['documents'] if d['requested_status'] == 'included'}
    config_path = base / 'config.json'
    existing_config = json.loads(config_path.read_text()) if config_path.exists() else None
    if chunks_path is None:
        chunks_path = ROOT / existing_config['data']['master_chunk_path'] if existing_config and existing_config['data'].get('master_chunk_path') else base / 'data/interim/all_chunks.jsonl'
    chunks = [c for c in read_chunks(chunks_path) if c['metadata']['doc_id'] in included]
    if not chunks: raise ValueError('No active chunks; refusing to publish empty domain')
    revision = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    config = json.loads(json.dumps(existing_config)) if existing_config else json.loads((ROOT / 'domains/birth_death_registration/config.json').read_text())
    config['domain'].update(id=domain, display_name={'brta': 'BRTA', 'passport': 'Passport and Immigration'}[domain], experimental=True,
                            description=f'Experimental {domain} corpus; source dates and claims are not independently verified.')
    active = base / f'data/interim/active_{revision}.jsonl'
    db_path = base / 'data/processed/chroma_experimental'
    collection_name = f'{domain}_{revision}'
    config['data'] = {'chunk_output_path': str(active.relative_to(ROOT)), 'chroma_persist_dir': str(db_path.relative_to(ROOT)),
                      'collection_name': collection_name, 'register_path': str(register_path.relative_to(ROOT)),
                      'master_chunk_path': str(chunks_path.relative_to(ROOT))}
    model = SentenceTransformer(config['embedding']['model'], device=device, local_files_only=True)
    client = chromadb.PersistentClient(path=str(db_path))
    collection = client.create_collection(collection_name)
    cached = {}
    if existing_config:
        previous = client.get_collection(existing_config['data']['collection_name']).get(include=['embeddings'])
        previous_chunks = {c['id']:c for c in read_chunks(ROOT / existing_config['data']['chunk_output_path'])}
        cached = {previous_chunks[cid]['retrieval_text']: vector for cid, vector in zip(previous['ids'], previous['embeddings'])}
    for start in range(0, len(chunks), 32):
        batch = chunks[start:start+32]
        lengths = [len(model.tokenizer.encode(c['retrieval_text'])) for c in batch]
        if max(lengths) > model.max_seq_length: raise ValueError('Chunk exceeds embedding input limit')
        missing = [c['retrieval_text'] for c in batch if c['retrieval_text'] not in cached]
        if missing:
            vectors = model.encode(missing, batch_size=8, normalize_embeddings=True, show_progress_bar=False)
            cached.update(zip(missing, vectors))
        vectors = [cached[c['retrieval_text']].tolist() for c in batch]
        collection.add(ids=[c['id'] for c in batch], documents=[c['content'] for c in batch],
                       metadatas=[c['metadata'] for c in batch], embeddings=vectors)
        print(f'{domain}: embedded {min(start+32,len(chunks))}/{len(chunks)}', flush=True)
    if set(collection.get(include=[])['ids']) != {c['id'] for c in chunks}: raise RuntimeError('Index IDs do not match active chunks')
    write_chunks(active, chunks)
    if stage_only:
        staged = base / f'config.candidate_{revision}.json'
        write_json(staged, config)
        print(f'Candidate ready: {staged.relative_to(ROOT)}; active config/register unchanged', flush=True)
        return
    if config_path.exists():
        shutil.copyfile(config_path, base / f'config.before_{revision}.json')
    for doc in register['documents']:
        doc['chunk_ids'] = [c['id'] for c in chunks if c['metadata']['doc_id'] == doc['document_id']]
        doc['index_status'] = 'indexed' if doc['document_id'] in included else doc['requested_status']
        doc['history'].append({'revision': revision, 'status': doc['index_status'], 'reason': doc.get('reason','Initial experimental inclusion')})
    register['active_revision'] = revision
    register['active_chunk_count'] = len(chunks)
    write_json(register_path, register)
    # Publish only after a complete, validated index exists. Prior collections remain available.
    write_json(config_path, config)
    print(f'Published {domain}: {len(included)} documents / {len(chunks)} chunks', flush=True)


def activate(domain: str, backup_name: str) -> None:
    """Reactivate a complete previous data version and reconcile the inclusion register."""
    import chromadb
    base = ROOT / 'domains' / domain
    backup = base / backup_name
    if backup.parent.resolve() != base.resolve() or not backup.name.startswith(('config.before_', 'config.candidate_')):
        raise ValueError('Choose a config.before_*.json or config.candidate_*.json filename from this domain')
    config = json.loads(backup.read_text())
    if config['domain']['id'] != domain:
        raise ValueError('Backup belongs to a different domain')
    chunks = read_chunks(ROOT / config['data']['chunk_output_path'])
    collection = chromadb.PersistentClient(path=str(ROOT / config['data']['chroma_persist_dir'])).get_collection(config['data']['collection_name'])
    if set(collection.get(include=[])['ids']) != {c['id'] for c in chunks}:
        raise ValueError('Backup index does not match its chunk file')
    register_path = base / 'data/register.json'
    register = json.loads(register_path.read_text())
    included = {c['metadata']['doc_id'] for c in chunks}
    event = datetime.now(timezone.utc).isoformat()
    for doc in register['documents']:
        if doc.get('error'): continue
        doc['requested_status'] = 'included' if doc['document_id'] in included else 'excluded'
        doc['index_status'] = 'indexed' if doc['document_id'] in included else 'excluded'
        doc['chunk_ids'] = [c['id'] for c in chunks if c['metadata']['doc_id'] == doc['document_id']]
        doc['reason'] = f'Reactivated {backup_name}'
        doc['history'].append({'at': event, 'status': doc['index_status'], 'reason': doc['reason']})
    register['active_revision'] = config['data']['collection_name'].removeprefix(domain + '_')
    register['active_chunk_count'] = len(chunks)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    shutil.copyfile(base / 'config.json', base / f'config.before_activate_{stamp}.json')
    write_json(register_path, register)
    write_json(base / 'config.json', config)
    print('Selected data version activated and register updated. Restart the app to use it.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare','rechunk','build','set-status','export','activate'])
    parser.add_argument('--domain', choices=SOURCES, required=True)
    parser.add_argument('--source-root',type=Path)
    parser.add_argument('--device',default='cpu')
    parser.add_argument('--document-id')
    parser.add_argument('--status',choices=['included','excluded'])
    parser.add_argument('--reason')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--config-backup')
    parser.add_argument('--chunks-path', type=Path)
    parser.add_argument('--stage-only', action='store_true')
    args=parser.parse_args()
    base=ROOT/'domains'/args.domain
    if args.action=='prepare':
        if not args.source_root: parser.error('--source-root required')
        prepare(args.source_root,args.domain)
    elif args.action=='rechunk':rechunk(args.domain)
    elif args.action=='build':build(args.domain,args.device, (ROOT / args.chunks_path) if args.chunks_path else None, args.stage_only)
    elif args.action=='activate':
        if not args.config_backup: parser.error('--config-backup required')
        activate(args.domain,args.config_backup)
    elif args.action=='set-status':
        if not all([args.document_id,args.status,args.reason]):parser.error('--document-id, --status and --reason required')
        p=base/'data/register.json'; register=json.loads(p.read_text())
        doc=next((d for d in register['documents'] if d['document_id']==args.document_id),None)
        if doc is None:raise ValueError('Unknown document ID')
        if doc.get('error'):raise ValueError('Failed source needs preparation repair before inclusion')
        doc.update(requested_status=args.status,reason=args.reason)
        write_json(p,register)
        print('Requested status recorded. Run build and restart app to activate it; current index is unchanged.')
    else:
        import chromadb
        if not args.output:parser.error('--output required')
        if args.output.exists():raise FileExistsError('Refusing to overwrite export destination')
        c=json.loads((base/'config.json').read_text())['data']
        result=chromadb.PersistentClient(path=str(ROOT/c['chroma_persist_dir'])).get_collection(c['collection_name']).get(include=['documents','metadatas'])
        write_json(args.output,result)
        print(f'Exported {len(result["ids"])} records; vectors and original PDF layout are not included')


if __name__=='__main__':main()
