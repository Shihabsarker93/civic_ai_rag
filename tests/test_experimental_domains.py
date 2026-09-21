import json
from types import SimpleNamespace

import numpy as np

from scripts import manage_experimental_domains as management
from src.pipeline import CivicRAGPipeline
from src.reranking.reranker import HybridReranker
from src.retrieval.hybrid_retriever import RetrievalResult


def test_chunk_spans_preserve_all_characters_and_limits():
    body = '# Topic\n\n' + ('Bangla বাংলা text with conditions.\n' * 200) + 'x' * 3000
    spans = list(management.spans(body))
    assert ''.join(body[a:b] for a, b in spans) == body
    assert all(0 < b-a <= 1400 for a, b in spans)


def test_faq_sections_keep_their_own_heading_and_complete_pair():
    body = '# FAQ\n\n### Collection\n**Question:** What to bring?\n**Answer:** Delivery slip.\n\n### Lost slip\n**Question:** Lost it?\n**Answer:** Application summary.\n'
    pieces = list(management.section_spans(body, 'Passport', limit=30))
    assert ''.join(body[a:b] for a,b,_,_ in pieces) == body
    faq = [(body[a:b],heading) for a,b,heading,is_faq in pieces if is_faq]
    assert len(faq) == 2
    assert faq[0][1] == 'FAQ > Collection'
    assert 'Delivery slip.' in faq[0][0] and 'Lost slip' not in faq[0][0]
    assert faq[1][1] == 'FAQ > Lost slip'
    assert 'Application summary.' in faq[1][0]


def test_sibling_sections_never_inherit_the_previous_heading():
    body = '## Parent\n\n### Before\ntext\n\n### After\n' + 'More details. ' * 400
    pieces = list(management.section_spans(body, 'Doc'))
    for a,b,heading,_ in pieces:
        if a >= body.index('### After'):
            assert heading == 'Parent > After'
    assert ''.join(body[a:b] for a,b,_,_ in pieces) == body


def test_question_answer_words_in_prose_do_not_make_a_giant_faq():
    body = 'Legal question and answer discussed in prose. প্রশ্ন এবং উত্তর। ' * 1000
    pieces = list(management.section_spans(body, 'Rules'))
    assert all(not faq and b-a <= 1400 for a,b,_,faq in pieces)
    assert ''.join(body[a:b] for a,b,_,_ in pieces) == body


def test_preparation_preserves_sources_and_records_unresolved(tmp_path, monkeypatch):
    monkeypatch.setattr(management, 'ROOT', tmp_path / 'repo')
    folder = tmp_path / 'sources/cleaned_md'
    folder.mkdir(parents=True)
    source = folder / 'example.md'
    text = '---\ntitle: "Passport"\nsource_pdf: "missing.pdf"\n---\n# Procedure\nOriginal condition[cite: 1].'
    source.write_text(text)
    management.prepare(tmp_path/'sources', 'passport')
    assert source.read_text() == text
    register = json.loads((management.ROOT/'domains/passport/data/register.json').read_text())
    doc = register['documents'][0]
    assert 'original_match_unresolved' in doc['audit_flags']
    assert doc['requested_status'] == 'included'
    assert (management.ROOT/doc['snapshot_path']).read_text() == text
    chunk = management.read_chunks(management.ROOT/'domains/passport/data/interim/all_chunks.jsonl')[0]
    assert 'Original condition.' in chunk['content']
    assert '[cite:' not in chunk['content']


def test_experimental_domain_never_uses_birth_templates():
    pipeline = CivicRAGPipeline.__new__(CivicRAGPipeline)
    pipeline.birth_death_rules = False
    pipeline.domain_id = 'passport'
    pipeline.generation_config = {'default_model': 'test', 'top_k_for_generation': 3}
    result = RetrievalResult(chunk_id='passport_1', content='Passport evidence', retrieval_text='Passport evidence',
                             metadata={'domain': 'passport'}, score=1.0, retrievers=['dense'])
    pipeline.retrieve = lambda *args, **kwargs: [result]
    pipeline._generator = lambda model: SimpleNamespace(answer=lambda query, evidence: 'Supported answer')
    def forbidden(*args):
        raise AssertionError('Birth-specific code was invoked')
    pipeline._safe_fee_answer = forbidden
    pipeline._safe_domain_answer = forbidden
    pipeline._augment_contexts = forbidden
    answer = pipeline.ask('Passport fee?', method='civic')
    assert answer['answer_route'] == 'llm'
    assert answer['domain'] == 'passport'
    assert answer['sources'][0]['id'] == 'passport_1'


def test_direct_bangla_procedure_uses_dominant_citizen_evidence_before_llm():
    pipeline = CivicRAGPipeline.__new__(CivicRAGPipeline)
    contexts = [
        {
            'id': 'brta_fitness',
            'content': (
                '# ফিটনেস নবায়ন\n\nবর্তমানে বিআরটিএর যে কোনো সার্কেল অফিসে মোটরযান হাজির করে '
                'পরিদর্শনপূর্বক ফিটনেস নবায়ন করা যায়। ঢাকা ও চট্টগ্রাম বিভাগের ক্ষেত্রে অনলাইনে '
                'অ্যাপয়েন্টমেন্ট নিতে হয়।'
            ),
            'metadata': {'document_type': 'সাধারণ তথ্য / নির্দেশিকা', 'title': 'ফিটনেস নবায়ন'},
            'score': 0.65,
        },
        {
            'id': 'noisy_law',
            'content': 'সড়ক পরিবহণ বিধিমালার একটি দীর্ঘ অংশ।',
            'metadata': {'document_type': 'document', 'title': 'সড়ক পরিবহণ বিধিমালা, ২০২২'},
            'score': 0.12,
        },
    ]

    answer = pipeline._evidence_first_answer(
        'ফিটনেস নবায়ন কীভাবে করব?', contexts, 'civic'
    )

    assert 'সার্কেল অফিসে' in answer
    assert 'অনলাইনে' in answer
    assert answer.endswith('Sources: brta_fitness')


def test_evidence_first_does_not_override_fee_or_multi_part_questions():
    pipeline = CivicRAGPipeline.__new__(CivicRAGPipeline)
    contexts = [
        {
            'id': 'guidance',
            'content': 'ফিটনেস নবায়নের জন্য নির্ধারিত অফিসে যেতে হবে।',
            'metadata': {'document_type': 'সাধারণ তথ্য / নির্দেশিকা'},
            'score': 0.70,
        },
        {
            'id': 'other',
            'content': 'অন্য তথ্য।',
            'metadata': {},
            'score': 0.10,
        },
    ]

    assert pipeline._evidence_first_answer('ফিটনেস নবায়নে কত টাকা লাগবে?', contexts, 'civic') == ''
    assert pipeline._evidence_first_answer('ফিটনেস নবায়ন কীভাবে করব আর কোথায় যাব?', contexts, 'civic') == ''


def test_passport_fee_and_office_question_uses_complete_controlled_fee_table():
    pipeline = CivicRAGPipeline.__new__(CivicRAGPipeline)
    pipeline.domain_id = 'passport'
    pipeline.chunks = [
        {
            'id': f'fee_{pages}_{years}',
            'content': (
                f'### e-Passport with {pages} pages and {years} years validity\n'
                '* **Fee:** TK 4,025\n* **Fee:** TK 6,325\n* **Fee:** TK 8,625'
            ),
            'metadata': {
                'title': 'e-Passport Fees and Payment Options',
                'section_title': 'e-Passport Fees for Inside Bangladesh',
            },
        }
        for pages, years in [(48, 5), (48, 10), (64, 5), (64, 10)]
    ] + [
        {
            'id': 'office',
            'content': 'আবেদন বর্তমান ঠিকানা সংশ্লিষ্ট আঞ্চলিক পাসপোর্ট অফিসে দাখিল করতে হবে।',
            'metadata': {},
        }
    ]

    answer, contexts = pipeline._safe_passport_fee_and_office_answer(
        'পাসপোর্ট করতে কত টাকা লাগবে? আর কোথায় যাওয়া লাগবে?', 'civic'
    )

    assert '48 পৃষ্ঠা, 5 বছর' in answer
    assert '64 পৃষ্ঠা, 10 বছর' in answer
    assert 'বায়োমেট্রিক এনরোলমেন্টের জন্য' in answer
    assert len(contexts) == 5


def test_birth_boosts_can_be_disabled():
    reranker = HybridReranker(enabled=False, model_name='', device='cpu', local_files_only=True,
                             fallback='none', domain_boosts=False)
    results = [RetrievalResult(chunk_id='x', content='x', retrieval_text='x', metadata={'document_type':'fee_row'}, score=0.1, retrievers=['dense'])]
    assert reranker.rerank('ফি কত?', results, 1)[0].score == 0.1


def test_versioned_exclusion_and_restore_keep_old_index(tmp_path, monkeypatch):
    import chromadb
    import sentence_transformers
    project = tmp_path/'repo'
    monkeypatch.setattr(management, 'ROOT', project)
    class FakeModel:
        def __init__(self, *args, **kwargs):
            self.max_seq_length = 8192
            self.tokenizer = SimpleNamespace(encode=lambda text: list(text))
        def encode(self, texts, **kwargs):
            return np.array([[1.0, 0.0, 0.0] for text in texts])
    monkeypatch.setattr(sentence_transformers, 'SentenceTransformer', FakeModel)
    management.write_json(project/'domains/birth_death_registration/config.json', {
        'domain': {}, 'embedding': {'model': 'fake'}, 'data': {}})
    source = tmp_path/'sources/cleaned_md'
    source.mkdir(parents=True)
    (source/'a.md').write_text('Evidence A')
    (source/'b.md').write_text('Evidence B')
    management.prepare(tmp_path/'sources','passport')
    management.build('passport','cpu')
    config_path = project/'domains/passport/config.json'
    old = json.loads(config_path.read_text())['data']
    register_path = project/'domains/passport/data/register.json'
    config_before = config_path.read_bytes()
    register_before = register_path.read_bytes()
    management.build('passport','cpu', stage_only=True)
    assert config_path.read_bytes() == config_before
    assert register_path.read_bytes() == register_before
    assert list((project/'domains/passport').glob('config.candidate_*.json'))
    register = json.loads(register_path.read_text())
    excluded_id = register['documents'][0]['document_id']
    register['documents'][0].update(requested_status='excluded', reason='Evaluation found incorrect evidence')
    management.write_json(register_path,register)
    management.build('passport','cpu')
    current = json.loads(config_path.read_text())['data']
    active = management.read_chunks(project/current['chunk_output_path'])
    assert all(c['metadata']['doc_id'] != excluded_id for c in active)
    client = chromadb.PersistentClient(path=str(project/current['chroma_persist_dir']))
    assert client.get_collection(old['collection_name']).count() == 2
    assert client.get_collection(current['collection_name']).count() == 1
    assert set(client.get_collection(current['collection_name']).get(include=[])['ids']) == {c['id'] for c in active}
    backup = next(p for p in (project/'domains/passport').glob('config.before_*.json')
                  if json.loads(p.read_text())['data']['collection_name'] == old['collection_name'])
    management.activate('passport', backup.name)
    assert json.loads(config_path.read_text())['data']['collection_name'] == old['collection_name']
    assert all(d['index_status']=='indexed' for d in json.loads(register_path.read_text())['documents'])
    register = json.loads(register_path.read_text())
    register['documents'][0].update(requested_status='included', reason='Restored after review')
    management.write_json(register_path, register)
    management.build('passport','cpu')
    restored = json.loads(config_path.read_text())['data']
    assert client.get_collection(restored['collection_name']).count() == 2
