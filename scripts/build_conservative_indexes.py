"""Build candidate-only Chroma stores, reusing only exact-text baseline vectors."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('HF_HUB_OFFLINE', '1')
os.environ.setdefault('TRANSFORMERS_OFFLINE', '1')
from scripts.prepare_conservative_release import digest, write


def build(release, device):
    import chromadb
    from sentence_transformers import SentenceTransformer
    release = release.resolve()
    report_path = release / 'index_build.json'
    if report_path.exists():
        raise ValueError('Build report exists; do not overwrite a completed build')
    manifest = json.loads((release / 'manifest.json').read_text())
    model = SentenceTransformer('BAAI/bge-m3', device=device, local_files_only=True)
    results = []
    for domain in manifest['domains']:
        directory = release / domain
        config = json.loads((directory / 'candidate_config.json').read_text())
        baseline = json.loads((directory / 'baseline_config.json').read_text())
        path = ROOT / config['data']['chroma_persist_dir']
        if path.resolve() == (ROOT / baseline['data']['chroma_persist_dir']).resolve():
            raise ValueError('Candidate cannot share the active store')
        if path.exists():
            raise ValueError(f'Refusing to replace an existing candidate store: {path}')
        chunk_path = ROOT / config['data']['chunk_output_path']
        if digest(chunk_path) != manifest['domains'][domain]['candidate_sha256']:
            raise ValueError('Candidate chunks changed after preparation')
        rows = [json.loads(line) for line in chunk_path.read_text().splitlines()]
        old_rows = {r['id']: r for r in map(json.loads, (ROOT / baseline['data']['chunk_output_path']).read_text().splitlines())}
        old_client = chromadb.PersistentClient(path=str(ROOT / baseline['data']['chroma_persist_dir']))
        old_collection = old_client.get_collection(baseline['data']['collection_name'])
        old = old_collection.get(include=['embeddings', 'documents'])
        if set(old['ids']) != set(old_rows):
            raise ValueError('Baseline index IDs differ from baseline corpus')
        cached = {}
        for cid, vector, document in zip(old['ids'], old['embeddings'], old['documents']):
            row = old_rows[cid]
            if document != row['content']:
                raise ValueError('Baseline stored content differs: ' + cid)
            cached[row.get('retrieval_text', row['content'])] = vector
        client = chromadb.PersistentClient(path=str(path))
        collection = client.create_collection(config['data']['collection_name'], metadata=old_collection.metadata)
        reused = encoded = 0
        for start in range(0, len(rows), 24):
            batch = rows[start:start + 24]
            texts = [r.get('retrieval_text', r['content']) for r in batch]
            lengths = [len(model.tokenizer.encode(text)) for text in texts]
            if max(lengths) > model.max_seq_length:
                raise ValueError('Would truncate evidence; abort candidate build')
            missing = list(dict.fromkeys(text for text in texts if text not in cached))
            reused += sum(text in cached for text in texts)
            if missing:
                vectors = model.encode(missing, batch_size=4, normalize_embeddings=True, show_progress_bar=False)
                cached.update(zip(missing, vectors))
                encoded += len(missing)
            collection.add(ids=[r['id'] for r in batch], documents=[r['content'] for r in batch],
                           metadatas=[r['metadata'] for r in batch],
                           embeddings=[cached[text].tolist() for text in texts])
            print(domain, min(start + 24, len(rows)), '/', len(rows), flush=True)
        stored = collection.get(include=['documents'])
        expected = {r['id']: r['content'] for r in rows}
        if dict(zip(stored['ids'], stored['documents'])) != expected:
            raise ValueError('Candidate index content or IDs mismatch')
        result = {'domain': domain, 'chunks': len(rows), 'reused_vectors': reused,
                  'newly_encoded_distinct_texts': encoded, 'collection': collection.name,
                  'device': device, 'verified_ids_and_documents': True}
        results.append(result)
        write(directory / 'index_build.json', result)
    unchanged = all(digest(ROOT / p) == sha for p, sha in manifest['protected_files'].items())
    if not unchanged:
        raise ValueError('Protected files changed')
    write(report_path, {'results': results, 'baseline_files_unchanged': unchanged, 'activated': False})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', type=Path, required=True)
    parser.add_argument('--device', default='mps')
    args = parser.parse_args()
    build(args.release, args.device)
