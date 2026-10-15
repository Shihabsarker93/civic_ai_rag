import copy

from scripts.prepare_conservative_release import heading_only, normalize_row


def test_nfc_keeps_numbers_conditions_aliases_and_original():
    row = {'id': '1', 'content': 'নবায়ন ১০০ টাকা; না হলে 01/01/2001',
           'retrieval_text': 'নবায়ন Search labels: renewal', 'metadata': {'body_start': 0}}
    saved = copy.deepcopy(row)
    normalized, changed = normalize_row(row)
    assert row == saved
    assert set(changed) == {'content', 'retrieval_text'}
    assert '১০০ টাকা; না হলে 01/01/2001' in normalized['content']
    assert 'Search labels' not in normalized['content']
    assert normalized['metadata'] == row['metadata']
    assert normalize_row(normalized)[1] == []


def test_only_exact_heading_spans_can_be_excluded():
    body = '# Heading\n\n'
    row = {'content': 'Title\n' + body, 'metadata': {'body_start': 0, 'body_end': len(body)}}
    assert heading_only(row, body)
    assert not heading_only(row, '# Altered\n\n')
    body = '# Heading\n\nFee: 100\n'
    row = {'content': body, 'metadata': {'body_start': 0, 'body_end': len(body)}}
    assert not heading_only(row, body)
    assert not heading_only({'content': '# Heading', 'metadata': {}}, '# Heading')
