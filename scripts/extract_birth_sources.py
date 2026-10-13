"""Extract supplied HTML article bodies and DOCX paragraphs for source review.

No network access, OCR, source modification or index activation is performed.
"""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import unicodedata
from xml.etree import ElementTree as ET
from zipfile import ZipFile


def normalized(text: str) -> str:
    return unicodedata.normalize('NFC', text).replace('\xa0', ' ')


class ArticleParser(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
    BLOCK = {'p', 'div', 'li', 'tr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}

    def __init__(self, root_class='ck-content', root_id='hide', omit_footnotes=False, root_tag=None):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.root_depth = None
        self.parts = []
        self.articles = []
        self.root_class = root_class
        self.root_id = root_id
        self.omit_footnotes = omit_footnotes
        self.ignored_depth = None
        self.root_tag = root_tag

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.root_depth is None and (self.root_class in attrs.get('class', '').split() or
                                       (self.root_id is not None and attrs.get('id') == self.root_id) or
                                       tag == self.root_tag):
            self.root_depth = len(self.stack)
            self.parts = []
        if self.omit_footnotes and 'footnote' in attrs.get('class', '').split():
            self.ignored_depth = len(self.stack)
        if self.root_depth is not None:
            if tag in self.BLOCK or tag == 'br':
                self.parts.append('\n')
            elif tag in {'td', 'th'}:
                self.parts.append('\t')
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag not in self.stack:
            return
        index = len(self.stack) - 1 - self.stack[::-1].index(tag)
        if self.ignored_depth is not None and index <= self.ignored_depth:
            self.ignored_depth = None
        if self.root_depth is not None:
            if tag in self.BLOCK:
                self.parts.append('\n')
            if index <= self.root_depth:
                lines = [line.strip() for line in normalized(''.join(self.parts)).splitlines()]
                self.articles.append('\n'.join(line for line in lines if line))
                self.root_depth = None
        self.stack = self.stack[:index]

    def handle_data(self, data):
        if self.root_depth is not None and self.ignored_depth is None and not {'script', 'style'} & set(self.stack):
            self.parts.append(data)


def html_text(path: Path) -> str:
    parser = ArticleParser()
    parser.feed(path.read_text(encoding='utf-8'))
    articles = [a for a in parser.articles if a.strip()]
    if len(articles) != 1:
        raise ValueError(f'Expected one article, found {len(articles)}: {path.name}')
    return articles[0]


def docx_text(path: Path) -> str:
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with ZipFile(path) as archive:
        root = ET.fromstring(archive.read('word/document.xml'))
    paragraphs = []
    for paragraph in root.findall('.//w:p', ns):
        text = ''.join(node.text or '' for node in paragraph.findall('.//w:t', ns))
        if text.strip():
            paragraphs.append(normalized(text.strip()))
    return '\n'.join(paragraphs)


def extract(root: Path, output: Path):
    if output.exists():
        raise ValueError('Output exists')
    records = []
    extracted = []
    for source in sorted(root.rglob('*')):
        if source.suffix not in {'.html', '.docx'}:
            continue
        try:
            text = html_text(source) if source.suffix == '.html' else docx_text(source)
        except ValueError as error:
            records.append({'source': str(source.relative_to(root)),
                            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                            'status': 'manual_structure_review_required', 'reason': str(error)})
            continue
        name = source.name + '.txt'
        extracted.append((name, text))
        records.append({'source': str(source.relative_to(root)),
                        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                        'extraction': name, 'characters': len(text),
                        'limits': 'Text only; images, pagination, DOCX headers/footers are not extracted.'})
    output.mkdir(parents=True)
    for name, text in extracted:
        (output / name).write_text(text + '\n', encoding='utf-8')
    (output / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
    return records


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(extract(args.root, args.output), indent=2))
