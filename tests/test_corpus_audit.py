import json

import pytest

from scripts import audit_service_corpora as auditor
from scripts.manage_experimental_domains import digest, write_json, write_chunks


@pytest.fixture
def corpus(tmp_path, monkeypatch):
    monkeypatch.setattr(auditor, 'ROOT', tmp_path)
    directory = tmp_path / 'release'
    directory.mkdir()
    text = '# Guide\nOnly for renewal.\n'
    (tmp_path / 'original.md').write_text(text)
    (directory / 'cleaned.md').write_text(text)
    sha = digest(text.encode())
    chunk = {'id': 'c1', 'content': text, 'retrieval_text': text,
             'metadata': {'doc_id': 'd1', 'body_start': 0, 'body_end': len(text)}}
    write_chunks(tmp_path / 'baseline.jsonl', [chunk])
    write_chunks(directory / 'chunks.jsonl', [chunk])
    write_json(directory / 'baseline_config.json', {'data': {'master_chunk_path': 'baseline.jsonl'}})
    write_json(tmp_path / 'domains/passport/data/register.json', {
        'documents': [{'document_id': 'd1', 'sha256': sha, 'snapshot_path': 'original.md'}]})
    write_json(directory / 'manifest.json', {'domain': 'passport', 'documents': [{
        'document_id': 'd1', 'source': 'original.md', 'source_sha256': sha,
        'cleaned_path': 'release/cleaned.md', 'cleaned_sha256': sha,
        'review_flags': [], 'retained_non_evidence_sections': [], 'chunk_ids': ['c1'],
        'context_spans': {}, 'findings': []}]})
    return directory, chunk


def test_audit_accepts_complete_verbatim_document(corpus):
    directory, _ = corpus
    assert not auditor.audit(directory)['errors']


def test_audit_rejects_lost_condition(corpus):
    directory, chunk = corpus
    chunk['content'] = '# Guide\n'
    write_chunks(directory / 'chunks.jsonl', [chunk])
    assert any('Exact source span missing' in e for e in auditor.audit(directory)['errors'])


def test_audit_rejects_unattributed_chunks(corpus):
    directory, chunk = corpus
    write_chunks(directory / 'chunks.jsonl', [chunk, {**chunk, 'id': 'c2'}])
    assert 'Chunk-to-document ownership mismatch' in auditor.audit(directory)['errors']


def test_audit_rejects_modified_original(corpus):
    directory, _ = corpus
    (directory.parent / 'original.md').write_text('Replaced source')
    assert any('Original SHA mismatch' in e for e in auditor.audit(directory)['errors'])
