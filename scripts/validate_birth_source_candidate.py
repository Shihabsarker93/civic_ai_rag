"""Validate candidate source fidelity without running retrieval or generation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.extract_birth_sources import ArticleParser, docx_text, html_text, normalized
from scripts.prepare_birth_review_candidate import sha
from scripts.prepare_birth_source_reconciliation import parse_faq


def compact(text):
    return ''.join(normalized(text).split())


def validate(original_root: Path, candidate: Path):
    manifest = json.loads((candidate / 'manifest.json').read_text())
    chunks = [json.loads(line) for line in (candidate / 'chunks.jsonl').read_text().splitlines()]
    checks = []

    def check(name, passed, detail):
        checks.append({'check': name, 'passed': bool(passed), 'detail': detail})

    raw = ROOT / 'domains/birth_death_registration/data/raw'
    for document in manifest['documents']:
        relative = document['prepared_file']
        check('active_source_hash:' + relative, sha(raw / relative) == document['baseline_sha256'],
              'Original prepared input must remain unchanged.')
        check('candidate_source_hash:' + relative, sha(candidate / 'raw' / relative) == document['candidate_sha256'],
              'Candidate input must match the generated manifest.')
    for source in manifest['original_inventory']:
        check('original_hash:' + source['path'], sha(original_root / source['path']) == source['sha256'],
              'Supplied original remains unchanged.')

    for number, expected in [(1, 16), (2, 10)]:
        suffix = '' if number == 1 else '_02'
        source = original_root / f'html_unicode/faqs_on_birth_and_death_registration{suffix}.html'
        intro, pairs = parse_faq(html_text(source), expected)
        doc = json.loads((candidate / f'raw/json/faqs_birth_death_registration_0{number}.json').read_text())['document']
        for i, (item, pair) in enumerate(zip(doc['chunks'], pairs), start=1):
            check(f'faq_{number}_{i}_source_text',
                  item['question'] == pair['question'] and item['answer'] == pair['answer'],
                  'Compared with freshly extracted source HTML, not an earlier generated comparison.')
            row = next(r for r in chunks if r['id'] == item['chunk_id'])
            check(f'faq_{number}_{i}_chunk_payload', compact(pair['answer']) in compact(row['content']),
                  'Full answer retained in one chunk, including qualifications.')
        check(f'faq_{number}_count', len(doc['chunks']) == expected, 'Source question count.')
        if number == 2:
            check('faq_2_preamble', doc['preamble']['content'] == intro.split('\n', 1)[1],
                  'Preamble retained separately from the ten questions.')

    source = original_root / 'converted_docx/application_for_birth_information_correction.docx'
    cases = [p.removeprefix('***').strip() for p in docx_text(source).splitlines() if p.startswith('***')]
    rows = [r for r in chunks if r['id'].startswith('review_v3_application_for_birth')]
    for i, case in enumerate(cases, start=1):
        check(f'parent_correction_case_{i}', any(compact(case) in compact(r['content']) for r in rows),
              'Entire original condition and requirement must occur together in one candidate chunk.')

    source = original_root / 'html_unicode/birth_and_death_registration_act_2004.html'
    parser = ArticleParser(root_class='txt-details', root_id=None, omit_footnotes=True)
    parser.feed(source.read_text())
    act_rows = [r for r in chunks if r['id'].startswith('review_v3_birth_and_death_registration_act')]
    for body in parser.articles:
        number = re.match(r'\[?([০-৯]+[ক-হ]?)[।৷]', body)[1]
        parts = [r['content'].split('\nContent: ', 1)[1] for r in act_rows
                 if r['metadata']['legal_unit_no'] == number]
        check('act_section:' + number, compact(''.join(parts)) == compact(body),
              'Full source section retained in ordered chunks; HTML footnote markers excluded.')

    check('unique_ids', len(chunks) == len({r['id'] for r in chunks}), 'No duplicate IDs.')
    check('token_limits', all(r['metadata']['retrieval_token_count'] <= r['metadata']['embedding_model_max_tokens']
                             for r in chunks), 'Uses locally recorded BGE-M3 token counts.')
    return {'validation_scope': 'source extraction, condition retention and artifact integrity; not retrieval accuracy',
            'passed': all(c['passed'] for c in checks), 'checks': checks,
            'candidate_chunks': len(chunks), 'max_retrieval_tokens': manifest['max_retrieval_tokens']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original-root', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    if args.report.exists():
        raise ValueError('Report exists; choose a new output')
    result = validate(args.original_root, args.candidate)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'checks'}))
    print(f"Checks: {len(result['checks'])}")
    if not result['passed']:
        raise SystemExit(1)
