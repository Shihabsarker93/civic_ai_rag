"""Generate source-exact FAQ and condition-preserving DOCX review replacements."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.extract_birth_sources import ArticleParser, docx_text, html_text
from scripts.prepare_birth_review_candidate import sha


def parse_faq(text: str, expected: int):
    matches = list(re.finditer(r'^([০-৯]+)।\s*(.+)$', text, re.M))
    if [int(m[1]) for m in matches] != list(range(1, expected + 1)):
        raise ValueError('FAQ numbering is incomplete or out of order')
    pairs = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        answer = text[match.end():end].strip()
        if not answer:
            raise ValueError('Empty FAQ answer')
        pairs.append({'question': match[2].strip(), 'answer': answer})
    return text[:matches[0].start()].strip(), pairs


def prepare(original_root: Path, output: Path):
    raw = ROOT / 'domains/birth_death_registration/data/raw'
    if output.exists():
        raise ValueError('Output exists')
    output.relative_to(ROOT)
    planned = []
    comparisons = []
    for number, expected in [(1, 16), (2, 10)]:
        suffix = '' if number == 1 else '_02'
        source = original_root / f'html_unicode/faqs_on_birth_and_death_registration{suffix}.html'
        prepared = raw / f'json/faqs_birth_death_registration_0{number}.json'
        data = json.loads(prepared.read_text())
        document = data['document']
        old = copy.deepcopy(document)
        introduction, pairs = parse_faq(html_text(source), expected)
        if len(document['chunks']) != expected:
            raise ValueError('Prepared FAQ count mismatch')
        for item, pair in zip(document['chunks'], pairs):
            comparisons.append({'file': prepared.name, 'faq_number': item['faq_number'],
                                'old_question': item['question'], 'old_answer': item['answer'],
                                'source_question': pair['question'], 'source_answer': pair['answer']})
            item.update(pair)
        if number == 2:
            heading, preamble = introduction.split('\n', 1)
            document['preamble']['content'] = preamble
        document['metadata'].update(source_file=source.name,
                                    source_review_status='source_text_restored',
                                    current_applicability_verified=False,
                                    last_updated_basis='inherited_prepared_metadata_not_verified_source_date')
        document['source_review'] = {
            'introduction': introduction,
            'original_sha256': sha(source),
            'method': 'HTML article extraction; NFC and whitespace normalization only',
            'metadata_note': 'Existing categories, aliases and dates are editorial/inherited, not source quotations.',
            'old_metadata': old['metadata'],
        }
        planned.append((prepared, source, json.dumps(data, ensure_ascii=False, indent=2) + '\n'))

    source = original_root / 'converted_docx/application_for_birth_information_correction.docx'
    prepared = raw / 'md/application_for_birth_information_correction_cleaned.md'
    paragraphs = docx_text(source).splitlines()
    cases = [p.removeprefix('***').strip() for p in paragraphs if p.startswith('***')]
    if len(cases) != 4:
        raise ValueError('Expected four complete correction conditions')
    frontmatter = prepared.read_text().split('---', 2)[1]
    headings = ['পিতা/মাতার জন্ম নিবন্ধন নম্বর আছে: সংশোধন, ম্যাপিং ও পুনর্মুদ্রণ',
                'পিতা/মাতার নম্বর নেই: জন্ম 01/01/2001 এর পূর্বে',
                'পিতা/মাতার নম্বর নেই ও মৃত: জন্ম 01/01/2001 এর পরে',
                'সংশোধনের জন্য মোবাইল নম্বর বা ইমেইল']
    text = '---' + frontmatter + '---\n\n# ' + paragraphs[0] + '\n\n'
    text += '\n\n'.join('## ' + heading + '\n\n' + case for heading, case in zip(headings, cases)) + '\n'
    planned.append((prepared, source, text))

    source = original_root / 'html_unicode/birth_and_death_registration_act_2004.html'
    prepared = raw / 'md/birth_and_death_registration_act_2004.md'
    headings = ArticleParser(root_class='txt-head', root_id=None)
    bodies = ArticleParser(root_class='txt-details', root_id=None, omit_footnotes=True)
    html = source.read_text()
    headings.feed(html)
    bodies.feed(html)
    if len(headings.articles) != len(bodies.articles) or len(bodies.articles) < 20:
        raise ValueError('Act section mapping failed')
    text = ('---\nsource_file: ' + source.name + '\nbengali_title: জন্ম ও মৃত্যু নিবন্ধন আইন, ২০০৪\n'
            'source_url: http://bdlaws.minlaw.gov.bd/act-921.html\n'
            'note: Supplied HTML snapshot; amendment footnote markers omitted from evidence, original retained.\n'
            '---\n\n# জন্ম ও মৃত্যু নিবন্ধন আইন, ২০০৪\n\n')
    for heading, body in zip(headings.articles, bodies.articles):
        number = re.match(r'\[?([০-৯]+[ক-হ]?)[।৷]', body)
        if not number:
            raise ValueError(f'Act section number missing: {body[:40]}')
        text += f'### ধারা {number[1]}: {heading}\n\n{body}\n\n'
    planned.append((prepared, source, text))

    output.mkdir(parents=True)
    supplement = json.loads((ROOT / 'docs/data_cleanup/birth_review_20261008/guideline_review.json').read_text())
    for prepared, source, text in planned:
        target = output / prepared.name
        target.write_text(text, encoding='utf-8')
        supplement['files'].append({
            'prepared_file': str(prepared.relative_to(raw)), 'prepared_sha256': sha(prepared),
            'original_file': str(source.relative_to(original_root)), 'original_sha256': sha(source),
            'replacement_file': str(target.relative_to(ROOT)), 'replacement_sha256': sha(target),
            'excluded_sections': [], 'require_page': False, 'id_prefix': 'review_v3_',
            'review_status': 'source_text_reconciled_independent_review_pending',
        })
    prepared = raw / 'md/birth_and_death_registration_rules_2018.md'
    source = original_root / 'bijoy_pdf/birth_and_death_registration_rules_2018.pdf'
    supplement['files'].append({
        'prepared_file': str(prepared.relative_to(raw)), 'prepared_sha256': sha(prepared),
        'original_file': str(source.relative_to(original_root)), 'original_sha256': sha(source),
        'changes': [{
            'id': 'remove-gazette-cover-price-from-rule-2',
            'before': '(২৮৬১)মূল্যঃ টাকা ৪০.০০ ', 'after': '',
            'reason': 'PDF page 1 footer is publication price, not a registration fee or definition.'
        }, {
            'id': 'restore-rule-21-row-5-scope',
            'before': '| জন্ম তারিখ ব্যতীত অন্যান্য তথ্য সংশোধন |',
            'after': '| জন্ম তারিখ ব্যতীত নাম, পিতার নাম, মাতার নাম, ঠিকানা, ইত্যাদি অন্যান্য তথ্য সংশোধনের জন্য আবেদন ফি |',
            'reason': 'Restore full label from PDF page 20 without changing the amount.'
        }, {
            'id': 'restore-rule-21-row-6-scope',
            'before': '| বাংলা ও ইংরেজিতে মূল সনদ বা সংশোধিত সনদ |',
            'after': '| বাংলা ও ইংরেজি উভয় ভাষায় মূল সনদ বা তথ্য সংশোধনের পর সনদের কপি সরবরাহ |',
            'reason': 'Restore full label from PDF page 20.'
        }, {
            'id': 'restore-rule-21-row-7-scope',
            'before': '| সনদের নকল সরবরাহ |',
            'after': '| বাংলা ও ইংরেজি উভয় ভাষায় সনদের নকল সরবরাহ |',
            'reason': 'Restore both-language qualification from PDF page 20.'
        }]
    })
    (output / 'supplement.json').write_text(json.dumps(supplement, ensure_ascii=False, indent=2) + '\n')
    (output / 'faq_comparison.json').write_text(json.dumps(comparisons, ensure_ascii=False, indent=2) + '\n')
    return supplement


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.original_root, args.output), ensure_ascii=False, indent=2))
