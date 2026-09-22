"""Question-independent structural preparation and source-span context recovery."""
from __future__ import annotations

import re

HEADING = re.compile(r"(?m)^(#{1,6})[ \t]+[^\n]+$")
ITEM = re.compile(r"^(?:[-*+] |[0-9০-৯]+[.)।][ \t]+)")
QUALIFIER = re.compile(r"^(?:\*\*)?(?:note|important|warning|condition|দ্রষ্টব্য|শর্ত|বিশেষ দ্রষ্টব্য|বি[.:])", re.I)


def atomic_spans(text):
    """Keep tables, list items with indented continuations, and fenced code intact."""
    lines = text.splitlines(keepends=True)
    offset, start, in_table, fence, blank = 0, 0, False, None, False
    for line in lines:
        stripped = line.strip()
        marker = re.match(r"^(`{3,}|~{3,})", stripped)
        top_item = bool(ITEM.match(line))
        table = line.startswith('|')
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = None
        else:
            boundary = (top_item or (table and not in_table) or
                        (in_table and bool(stripped) and not table) or
                        (blank and bool(stripped) and not line[0].isspace() and
                         not QUALIFIER.match(stripped) and not table))
            if boundary and offset > start:
                yield start, offset
                start = offset
            if marker:
                fence = marker[1]
            in_table = table if stripped else in_table
        blank = not stripped
        offset += len(line)
    if start < len(text):
        yield start, len(text)


def packed_spans(text, limit):
    start = 0
    for a, b in atomic_spans(text):
        if b - start > limit and a > start:
            yield start, a
            start = a
    if start < len(text):
        yield start, len(text)


def scope_spans(body, start, max_chars=1800):
    """Copy exact ancestor/section introductory prose, not inferred conditions.

    Long parent bodies are flagged rather than summarized or silently truncated.
    A preceding sibling heading is never treated as a parent.
    """
    headings = list(HEADING.finditer(body))
    parents = []
    for i, h in enumerate(headings):
        if h.start() > start:
            break
        level = len(h[1])
        parents = [(n, j) for n, j in parents if n < level]
        parents.append((level, i))
    spans, pending = [], []
    for _, i in parents:
        h = headings[i]
        end = headings[i + 1].start() if i + 1 < len(headings) else len(body)
        # Only introductory prose before the first list/table is inherited.
        prose_start = h.end()
        tail = body[prose_start:end]
        boundary = re.search(r"(?m)^(?:[-*+] |[0-9০-৯]+[.)।][ \t]+|\|)", tail)
        prose_end = prose_start + boundary.start() if boundary else end
        prose_end = min(prose_end, start)
        text = body[prose_start:prose_end]
        if not text.strip() or not re.sub(r"[\s*-]", "", text):
            continue
        if len(text) > max_chars:
            pending.append({'start': prose_start, 'end': prose_end, 'reason': 'long_parent_context_requires_review'})
        else:
            spans.append({'start': prose_start, 'end': prose_end})
    return spans, pending


def document_findings(body):
    """Locate possible defects, without inventing replacements or source URLs."""
    patterns = {
        'missing_link_target': r'(?i)click here|লিংক এখানে',
        'replacement_character': '\ufffd',
        'unresolved_citation_marker': r'\[cite[^\]]*\]',
        'embedded_metadata': r'(?m)^(?:document_id|source_pdf|effective_date):',
    }
    findings = []
    for kind, pattern in patterns.items():
        for match in re.finditer(pattern, body):
            findings.append({'kind': kind, 'start': match.start(), 'end': match.end(),
                             'line': body.count('\n', 0, match.start()) + 1,
                             'text': match[0]})
    return findings
