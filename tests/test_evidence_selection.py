from copy import deepcopy
from types import SimpleNamespace

import pytest

from src.generation.evidence_selection import select_evidence
from src.generation.ollama_generator import build_prompt
from src.pipeline import CivicRAGPipeline
from src.retrieval.hybrid_retriever import RetrievalResult


def context(key, section, body='Supported facts.', **metadata):
    return {'id': key, 'content': body, 'metadata': {'section_title': section, **metadata}}


@pytest.mark.parametrize('service,query', [
    ('Passport', 'নতুন পাসপোর্ট করতে কী কী কাগজপত্র লাগে?'),
    ('Driving licence', 'নতুন ড্রাইভিং লাইসেন্স করতে কী কী কাগজ লাগে?'),
    ('Birth registration', 'নতুন জন্ম নিবন্ধন করতে কী কী কাগজ লাগে?'),
])
def test_application_is_not_collection_across_domains(service, query):
    bad = context('bad', service + ' > Collection documents')
    good = context('good', service + ' > Application documents')
    for order in ([bad, good], [good, bad]):
        assert [c['id'] for c in select_evidence(query, order).contexts] == ['good']


def test_scenario_lost_is_not_cancelled():
    rows = [context('appeal', 'Driving licence cancellation appeal'),
            context('duplicate', 'Driving licence duplicate requirements')]
    assert select_evidence('আমার ড্রাইভিং লাইসেন্স হারিয়ে গেছে, এখন কী করতে হবে?', rows).contexts == rows[1:]


def test_document_wide_renewal_heading_and_conditional_warning_do_not_relabel_application():
    row = context('learner', 'ড্রাইভিং লাইসেন্স > লার্নার লাইসেন্স প্রাপ্তির প্রক্রিয়া > প্রয়োজনীয় কাগজপত্র',
                  'লাইসেন্স ইস্যু ও নবায়ন\nশিরোনাম\n\nআবেদনপত্র। নবায়নের ক্ষেত্রে পুরোনো লাইসেন্স। মিথ্যা তথ্য দিলে বাতিল হবে।')
    assert select_evidence('নতুন ড্রাইভিং লাইসেন্স করতে কী কী কাগজপত্র লাগে?', [row]).contexts == [row]


def test_explicit_cancellation_and_multipart_not_overfiltered():
    rows = [context('cancel', 'Driving licence cancellation'), context('renew', 'Driving licence renewal')]
    assert select_evidence('লাইসেন্স বাতিলের আপিল এবং নবায়ন সম্পর্কে বলুন', rows).contexts == rows


def test_fee_families_expand_but_never_other_parent_or_domain():
    base = context('fee1', 'e-Passport Fees > Inside Bangladesh fees > 48 pages', doc_id='doc')
    sibling = context('fee2', 'e-Passport Fees > Inside Bangladesh fees > 64 pages', doc_id='doc')
    abroad = context('foreign', 'e-Passport Fees > Mission fees > 48 pages', doc_id='doc')
    other = context('other', 'e-Passport Fees > Inside Bangladesh fees > 64 pages', doc_id='different')
    result = select_evidence('পাসপোর্টের ফি কত?', [base], [base, sibling, abroad, other])
    assert result.contexts == [base, sibling]


def test_historical_and_wrong_service_are_not_mixed_with_current_scope():
    rows = [context('coi', 'Passport department > Certificate of Identity fees'),
            context('mrp', 'Machine Readable Passport fees 2012', audit_flags='dated_document_review_applicability'),
            context('ep', 'e-Passport fees')]
    assert [c['id'] for c in select_evidence('পাসপোর্ট বানাতে কত টাকা লাগে?', rows).contexts] == ['ep']
    assert [c['id'] for c in select_evidence('২০১২ সালের MRP পাসপোর্টের ফি কত?', rows).contexts] == ['mrp']


def test_explicit_foreign_scope_not_domestic():
    rows = [context('home', 'e-Passport fees inside Bangladesh'), context('away', 'e-Passport mission fees')]
    assert select_evidence('বিদেশে ই-পাসপোর্টের ফি কত?', rows).contexts == rows[1:]


def test_unknown_query_preserves_candidates_and_input_not_mutated():
    rows = [context('a', 'Unclassified source'), context('b', 'Another source')]
    before = deepcopy(rows)
    assert select_evidence('এটা সম্পর্কে বলুন', rows).contexts == rows
    assert rows == before


def test_document_continuation_not_parallel_language_or_other_heading():
    a = context('a', 'Passport > Application documents', doc_id='doc')
    b = context('b', 'Passport > Application documents', doc_id='doc')
    c = context('c', 'Passport > Application documents English', doc_id='doc')
    assert select_evidence('পাসপোর্টের কাগজপত্র কী লাগে?', [a], [a, b, c]).contexts == [a, b]


def test_whole_chunk_budget_and_duplicate_ids():
    rows = [context('a', 'Unknown', 'a' * 20), context('b', 'Unknown', 'b' * 50)]
    result = select_evidence('প্রশ্ন', [rows[0], *rows], max_chars=25)
    assert result.contexts == rows[:1]
    assert result.trace['decisions'][-1]['reason'] == 'whole_chunk_budget'


def test_prompt_retains_legacy_and_selected_prompt_avoids_rank_and_bullet_cap():
    rows = [context('a', 'Passport', 'Exact evidence and conditions')]
    old = build_prompt('প্রশ্ন', rows)
    new = build_prompt('প্রশ্ন', rows, selected_evidence=True)
    assert 'Source 1 is the strongest evidence' in old
    assert 'Source 1 is the strongest evidence' not in new
    assert 'at most 6 short bullets' not in new
    assert 'Exact evidence and conditions' in new


@pytest.mark.parametrize('domain', ['passport', 'brta', 'birth_death_registration'])
def test_new_shared_path_filters_before_llm_and_never_calls_old_templates(domain):
    pipeline = CivicRAGPipeline.__new__(CivicRAGPipeline)
    pipeline.domain_id = domain
    pipeline.birth_death_rules = domain == 'birth_death_registration'
    pipeline.evidence_selection_enabled = True
    pipeline.generation_config = {'default_model': 'test'}
    pipeline.chunks = []
    rows = [context('wrong', 'Cancellation'), context('right', 'Duplicate replacement')]
    pipeline.retrieve = lambda *a, **k: [RetrievalResult(chunk_id=c['id'], content=c['content'], retrieval_text='', metadata=c['metadata'], score=1, retrievers=['dense']) for c in rows]
    pipeline._augment_contexts = lambda q, cs: cs
    seen = []
    def answer(q, cs):
        seen.extend(c['id'] for c in cs)
        return 'হারানো সনদের প্রতিলিপির জন্য আবেদন করুন।'
    pipeline._generator = lambda model, **kw: SimpleNamespace(answer=answer)
    pipeline._safe_domain_answer = lambda *a: pytest.fail('Legacy route bypassed selector')
    result = pipeline.ask('সনদ হারিয়ে গেলে কী করব?')
    assert seen == ['right']
    assert result['answer_route'] == 'llm_selected_evidence'
    assert result['sources'][0]['id'] == 'wrong'
    assert result['answer_contexts'][0]['id'] == 'right'


def test_no_applicable_evidence_does_not_invoke_model():
    pipeline = CivicRAGPipeline.__new__(CivicRAGPipeline)
    pipeline.domain_id = 'brta'
    pipeline.birth_death_rules = False
    pipeline.evidence_selection_enabled = True
    pipeline.generation_config = {'default_model': 'test'}
    pipeline.chunks = []
    pipeline.retrieve = lambda *a, **k: []
    pipeline._generator = lambda *a, **k: pytest.fail('Must not generate without evidence')
    assert pipeline.ask('লাইসেন্স হারিয়ে গেলে কী করব?')['answer_route'] == 'no_applicable_evidence'
