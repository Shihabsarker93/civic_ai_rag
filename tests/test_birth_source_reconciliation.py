import json
from pathlib import Path

import pytest

from scripts.extract_birth_sources import ArticleParser, html_text, normalized
from scripts.prepare_birth_review_candidate import ROOT, apply_changes
from scripts.prepare_birth_source_reconciliation import act_sections, parse_faq

REVIEW = ROOT / 'docs/data_cleanup/birth_review_20261009'


def test_act_structure_keeps_order_and_footnote_text():
    html = ('<div class="act-chapter-group"><p>অধ্যায়-১</p><p>প্রারম্ভিক</p></div>'
            '<div class="txt-head">Name</div><div class="txt-details">১। First</div>'
            '<div class="act-chapter-group"><p>অধ্যায়-২</p></div>'
            '<div class="txt-head">Next</div><div class="txt-details">'
            '<span class="footnote">99</span>[২। Amended]</div>')
    sections = act_sections(html)
    assert sections[0]['chapter'] == normalized('অধ্যায়-১ / প্রারম্ভিক')
    assert sections[1]['chapter'] == normalized('অধ্যায়-২')
    assert sections[1]['body'] == '[২। Amended]'
    with pytest.raises(ValueError):
        act_sections('<div class="txt-head">Orphan</div>')


def test_legal_chunker_flushes_before_chapter_change():
    from domains.birth_death_registration.scripts import prepare_chunks as prep
    body = '# Act\n\n## অধ্যায়-১\n\n### ধারা ১: First\nFirst condition\n\n'
    body += '## অধ্যায়-২\n\n### ধারা ২: Second\nSecond condition\n'
    rows = prep.legal_chunks(Path('act.md'), {}, prep.normalize_text(body),
                             doc_type='act', max_chars=1400)
    assert len(rows) == 2
    assert rows[0]['metadata']['chapter'] == prep.normalize_text('অধ্যায়-১')
    assert rows[1]['metadata']['chapter'] == prep.normalize_text('অধ্যায়-২')
    assert 'Second condition' not in rows[0]['content']


def test_html_extraction_keeps_paragraphs_and_excludes_navigation(tmp_path):
    path = tmp_path / 'faq.html'
    path.write_text('<nav>not evidence</nav><div class="wrapper ck-content"><p>১। Question?</p>'
                    '<p>Answer <b>condition</b><br>exception</p></div><footer>not evidence</footer>')
    assert html_text(path) == '১। Question?\nAnswer condition\nexception'
    path.write_text('<p>No recognized article</p>')
    with pytest.raises(ValueError):
        html_text(path)


def test_footnotes_do_not_remove_amended_text():
    parser = ArticleParser(root_class='txt-details', root_id=None, omit_footnotes=True)
    parser.feed('<div class="txt-details"><span class="footnote"><sup><a>10</a></sup></span>'
                '[৪। amended text]<div>condition</div></div>')
    assert parser.articles == ['[৪। amended text]\ncondition']


def test_faq_numbering_fails_closed():
    intro, pairs = parse_faq('Intro\n১। Q?\nA\n২। Q2?\nA2', 2)
    assert intro == 'Intro'
    assert pairs[1] == {'question': 'Q2?', 'answer': 'A2'}
    with pytest.raises(ValueError):
        parse_faq('১। Q?\nA\n৩। Q3?\nA3', 2)


def test_all_26_saved_faq_answers_match_extracted_sources():
    comparisons = json.loads((REVIEW / 'reviewed_sources/faq_comparison.json').read_text())
    assert len(comparisons) == 26
    for comparison in comparisons:
        doc = json.loads((REVIEW / 'reviewed_sources' / comparison['file']).read_text())['document']
        item = next(x for x in doc['chunks'] if x['faq_number'] == comparison['faq_number'])
        assert item['question'] == comparison['source_question']
        assert item['answer'] == comparison['source_answer']


def candidate_rows():
    return [json.loads(line) for line in (REVIEW / 'candidate_v3/chunks.jsonl').read_text().splitlines()]


def test_parent_proof_rules_retain_their_conditions_in_same_chunk():
    rows = [r for r in candidate_rows() if r['id'].startswith('review_v3_application_for_birth')]
    assert len(rows) == 4
    before = next(r['content'] for r in rows if '01/01/2001 এর পূর্বে' in r['content'])
    after = next(r['content'] for r in rows if '01/01/2001 এর পরে' in r['content'])
    assert 'মৃত্যুর কোন প্রমাণপত্র দাখিল করতে হবে না' in before
    assert 'মৃত্যুর প্রমাণপত্র দাখিল করতে হবে' in after
    assert 'পিতা/মাতা মৃত' in after
    assert not any(r['metadata']['section_title'] in ['গুরুত্বপূর্ণ তথ্য', 'প্রয়োজনীয় প্রমাণপত্র'] for r in rows)


def test_rule_repairs_remove_print_price_not_service_amounts():
    repairs = json.loads((REVIEW / 'reviewed_sources/supplement.json').read_text())['files']
    record = next(r for r in repairs if 'rules_2018' in r['prepared_file'])
    original = (ROOT / 'domains/birth_death_registration/data/raw' / record['prepared_file']).read_text()
    updated = apply_changes(original, record['changes'])
    assert '(২৮৬১)মূল্যঃ টাকা ৪০.০০' not in updated
    assert '১০০ টাকা | ২ মার্কিন ডলার' in updated
    assert '৫০ টাকা | ১ মার্কিন ডলার' in updated


def test_candidate_has_unique_ids_and_safe_token_lengths():
    rows = candidate_rows()
    assert len(rows) == len({r['id'] for r in rows})
    assert all(r['metadata']['retrieval_token_count'] <= r['metadata']['embedding_model_max_tokens'] for r in rows)
