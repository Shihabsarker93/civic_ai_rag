from scripts.clean_service_corpora import clean_document, evidence_units, has_evidence
from scripts.corpus_structure import packed_spans, scope_spans, document_findings


def test_conditions_stay_with_top_level_list_item():
    body = '# Requirements\n' + '* First item.\n' * 8 + '* Existing licence:\n  Only required for renewal, not a first application.\n' + '* Last item.\n' * 8
    units = list(evidence_units(body, 'Guide', limit=100))
    assert ''.join(body[a:b] for a, b, _, _ in units) == body
    existing = next(body[a:b] for a, b, _, _ in units if 'Existing licence:' in body[a:b])
    assert 'Only required for renewal' in existing


def test_faq_remains_complete_and_siblings_separate():
    body = '# FAQ\n## Collection\nQuestion: What?\nAnswer: Delivery slip.\n## Lost slip\nQuestion: Lost?\nAnswer: Summary.\n'
    units = list(evidence_units(body, 'FAQ', limit=12))
    assert ''.join(body[a:b] for a, b, _, _ in units) == body
    faqs = [body[a:b] for a, b, _, faq in units if faq]
    assert len(faqs) == 2
    assert 'Delivery slip.' in faqs[0] and 'Lost slip' not in faqs[0]


def test_metadata_removed_with_audit_trail_not_mistaken_for_evidence():
    raw = 'title: "MRP guide"\neffective_date: "2012-01-01"\n# Application\nBring the old passport.\n'
    metadata, body, changes = clean_document(raw)
    assert metadata['effective_date'] == '2012-01-01'
    assert body.startswith('# Application')
    assert 'Bring the old passport.' in body
    assert changes[0]['text'].startswith('title:')
    assert not has_evidence('# Parent\n---\n')
    assert has_evidence('# Rule\nDo not omit documents.\n')


def test_table_rows_are_never_cut_mid_cell():
    body = '# Fees\n| Category | Amount |\n| --- | --- |\n' + '| Renewal with a condition | 500 plus penalty |\n' * 8
    units = list(evidence_units(body, 'Fees', limit=100))
    assert ''.join(body[a:b] for a, b, _, _ in units) == body
    for a, b, _, _ in units:
        for line in body[a:b].splitlines():
            if line.startswith('|'):
                assert line.endswith('|')


def test_table_headers_and_entire_table_stay_together():
    table = '| Kind | Price |\n| --- | --- |\n' + '| Any | 10 |\n' * 30
    text = 'Introduction.\n\n' + table + '\nOther paragraph.\n'
    units = [text[a:b] for a, b in packed_spans(text, 80)]
    assert ''.join(units) == text
    assert sum('| Any |' in unit for unit in units) == 1
    assert table in next(unit for unit in units if '| Any |' in unit)


def test_numbered_lists_keep_indented_conditions_and_blank_lines():
    text = '1. Required document.\n\n  Only for renewal.\n\n2. Another requirement.\n'
    units = [text[a:b] for a, b in packed_spans(text, 25)]
    assert ''.join(units) == text
    assert 'Only for renewal.' in next(unit for unit in units if '1.' in unit)


def test_ancestor_intro_is_verbatim_and_sibling_does_not_leak():
    body = '# Service\nOnly for existing applicants.\n## First\nFirst facts.\n## Second\nSecond facts.\n'
    spans, pending = scope_spans(body, body.index('## Second'))
    inherited = ''.join(body[s['start']:s['end']] for s in spans)
    assert 'Only for existing applicants.' in inherited
    assert 'First facts.' not in inherited
    assert not pending


def test_long_ancestor_is_flagged_not_summarized():
    body = '# Parent\n' + 'Condition. ' * 100 + '\n## Child\nFacts.'
    spans, pending = scope_spans(body, body.index('## Child'), max_chars=20)
    assert not spans
    assert pending[0]['reason'] == 'long_parent_context_requires_review'


def test_fenced_text_remains_whole():
    body = '```text\n1. Example.\n\n2. More example.\n```\n'
    assert list(packed_spans(body, 10)) == [(0, len(body))]


def test_missing_links_flagged_without_guessed_urls():
    findings = document_findings('Download: Click here\n')
    assert findings[0]['kind'] == 'missing_link_target'
    assert findings[0]['line'] == 1


def test_heading_shaped_metadata_is_extracted_not_indexed():
    raw = '## title: "Guide"\nsource_pdf: "guide.pdf"\n\n# Actual content\nAll facts remain.\n'
    metadata, body, changes = clean_document(raw)
    assert metadata['title'] == 'Guide'
    assert body.startswith('# Actual content')
    assert 'All facts remain.' in body
    assert 'source_pdf:' in changes[0]['text']


def test_ambiguous_preamble_does_not_remove_facts():
    raw = 'title: Guide\nOnly for renewal applicants.\n# Steps\nBring evidence.'
    _, body, changes = clean_document(raw)
    assert 'Only for renewal applicants.' in body
    assert not changes


def test_direct_evidence_never_drops_trailing_condition():
    from src.pipeline import CivicRAGPipeline
    content = '# Requirements\n' + 'Bring the document. ' * 60 + '\nOnly for renewal, not first applications.'
    answer = CivicRAGPipeline._extract_direct_evidence_body(content)
    assert answer.endswith('Only for renewal, not first applications.')
