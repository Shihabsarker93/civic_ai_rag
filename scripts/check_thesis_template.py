"""Verify thesis headings against the supplied template without changing files."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = Path('/Users/shihab/01 Thesis/p3 final/Writing/01 update/FINAL YEAR THESIS Template_CSE400_Fall 2024 ONWARDS')
DEFAULT_ABSTRACT = Path('/Users/shihab/01 Thesis/p3 final/Writing/01 update/submited so far/core/abstract.tex')


def normalized(value):
    return ' '.join(value.split())


def headings(path):
    text = re.sub(r'(?m)^\s*%.*$', '', path.read_text())
    return [(kind, normalized(title)) for kind, title in
            re.findall(r'\\(chapter|section|subsection)\{([^}]*)\}', text)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument('--abstract', type=Path, default=DEFAULT_ABSTRACT)
    args = parser.parse_args()
    manuscript = ROOT / 'docs/thesis_final_2026_09_24'
    files = ['main.tex'] + [f'chapters/chapter_{n}.tex' for n in (1, 2, 3, 5, 6, 9)]
    count = 0
    for relative in files:
        expected = headings(args.template / relative)
        actual = headings(manuscript / relative)
        assert actual == expected, f'Heading mismatch: {relative}\nExpected: {expected}\nActual: {actual}'
        count += len(expected)
    assert (manuscript / 'core/abstract.tex').read_bytes() == args.abstract.read_bytes(), 'Abstract changed'
    toc = (manuscript / 'main.toc').read_text()
    ordered = ['Declaration', 'Approval', 'Ethics Statement', 'Abstract', 'Dedication',
               'Acknowledgment', 'Table of Contents', 'List of Figures', 'List of Tables',
               'Nomenclature', 'Introduction', 'Literature Review',
               'Requirements, Impacts and Constraints', 'Proposed Methodology',
               'Result Analysis', 'Conclusion', 'Bibliography',
               r'Appendix A How to install \LaTeX', r'Appendix B Overleaf: GitHub for \LaTeX']
    position = 0
    for title in ordered:
        found = toc.find(title, position)
        assert found >= 0, f'Missing or out-of-order TOC entry: {title}'
        position = found + len(title)
    assert len(re.findall(r'\\contentsline \{chapter\}', toc)) == len(ordered), 'Unexpected chapter-level TOC entry'
    print(f'PASS: {count} original chapter/section/subsection headings match; TOC order matches; Abstract bytes unchanged.')


if __name__ == '__main__':
    main()
