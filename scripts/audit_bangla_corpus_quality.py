"""Read-only Unicode and duplication diagnostics for configured active corpora.

Flags are review candidates, not proof of errors; no text is rewritten.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import unicodedata

ROOT = Path(__file__).resolve().parents[1]


def text_flags(text: str) -> list[str]:
    flags = []
    if unicodedata.normalize('NFC', text) != text:
        flags.append('non_nfc')
    if '\ufffd' in text:
        flags.append('replacement_character')
    if any(unicodedata.category(c) == 'Co' for c in text):
        flags.append('private_use_character')
    if any(c in text for c in ('\u200c', '\u200d')):
        flags.append('joiner_review_do_not_blindly_remove')
    if any(c in text for c in ('\u200b', '\ufeff', '\u202a', '\u202b', '\u202c', '\u202d', '\u202e')):
        flags.append('invisible_or_directional_control')
    if any('০' <= c <= '৯' for c in text) and any('0' <= c <= '9' for c in text):
        flags.append('mixed_digit_scripts_not_necessarily_error')
    return flags


def audit(root: Path = ROOT) -> dict:
    domains = []
    for config_path in sorted((root / 'domains').glob('*/config.json')):
        config = json.loads(config_path.read_text())
        path = root / config['data']['chunk_output_path']
        data = path.read_bytes()
        rows = [json.loads(line) for line in data.decode('utf-8').splitlines() if line.strip()]
        issues = []
        groups = defaultdict(list)
        ids = [row['id'] for row in rows]
        for row in rows:
            content = row['content']
            digest = hashlib.sha256(unicodedata.normalize('NFC', content).encode()).hexdigest()
            groups[digest].append(row['id'])
            for field in ('content', 'retrieval_text'):
                if field not in row:
                    continue
                flags = text_flags(row[field])
                if flags:
                    issues.append({'id': row['id'], 'field': field, 'flags': flags})
        if path.read_bytes() != data:
            raise ValueError('Corpus changed during audit')
        domains.append({'domain': config_path.parent.name,
                        'path': str(path.relative_to(root)),
                        'sha256': hashlib.sha256(data).hexdigest(),
                        'chunks': len(rows), 'unique_ids': len(ids) == len(set(ids)),
                        'flagged_fields': issues,
                        'exact_nfc_content_duplicate_groups': [v for v in groups.values() if len(v) > 1]})
    return {'scope': 'Active chunk diagnostics only; not OCR/source fidelity verification.',
            'policy': 'Report only. Preserve originals, numbers, joiners and provenance.',
            'domains': domains}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    with args.output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    for domain in result['domains']:
        print(domain['domain'], 'chunks:', domain['chunks'],
              'flagged fields:', len(domain['flagged_fields']),
              'duplicate groups:', len(domain['exact_nfc_content_duplicate_groups']))
