from scripts.clean_service_corpora import clean_document, evidence_units, has_evidence


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
