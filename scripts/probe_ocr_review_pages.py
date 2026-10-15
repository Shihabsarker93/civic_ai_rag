"""Compare local Bengali/English OCR modes on deferred source pages; never activate text."""
import argparse
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.prepare_conservative_release import digest, write


def probe(release):
    output = release / 'ocr_experiment'
    if output.exists():
        raise ValueError('OCR experiment exists')
    output.mkdir()
    prior = json.loads((ROOT / 'docs/data_cleanup/2026_09_22_corpus_release/brta/manifest.json').read_text())
    deferred = {d['document_id'] for d in prior['documents']
                if 'unstructured_ocr_preserved_requires_pdf_review' in d['review_flags']}
    targets = []
    for domain in ('brta', 'passport'):
        docs = json.loads((release / domain / 'source_register_audit.json').read_text())
        for doc in docs:
            if domain == 'brta' and doc['document_id'] not in deferred:
                continue
            originals = [o for o in doc['originals'] if o.get('pages')]
            if not originals:
                continue
            original = originals[0]
            empty = original.get('pages_without_extractable_text', [])
            if domain == 'passport' and not empty:
                continue
            page = empty[0] if empty else 1
            targets.append((domain, doc['document_id'], original, page))
    results = []
    for domain, doc_id, source, page in targets:
        path = Path(source['path'])
        if digest(path) != source['registered_sha256']:
            raise ValueError('Original changed')
        with tempfile.TemporaryDirectory(prefix='civicrag-ocr-') as temp:
            image = Path(temp) / 'page'
            subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-singlefile',
                            '-scale-to', '2400', '-png', str(path), str(image)],
                           check=True, capture_output=True, timeout=120)
            for mode in (3, 6):
                command = ['tesseract', str(image) + '.png', 'stdout', '-l', 'ben+eng',
                           '--psm', str(mode), 'tsv']
                run = subprocess.run(command, check=True, capture_output=True, text=True, timeout=180)
                words = [r for r in csv.DictReader(io.StringIO(run.stdout), delimiter='\t')
                         if r.get('level') == '5' and r.get('text', '').strip()]
                text = ' '.join(r['text'] for r in words)
                name = f'{doc_id}_page_{page}_psm_{mode}.tsv'
                (output / name).write_text(run.stdout)
                confidence = [float(r['conf']) for r in words if float(r['conf']) >= 0]
                result = {'domain': domain, 'document_id': doc_id, 'source_path': str(path),
                          'source_sha256': source['sha256'], 'page': page, 'psm': mode,
                          'languages': 'ben+eng', 'render_max_dimension': 2400,
                          'words': len(words), 'text': text, 'tsv': name,
                          'mean_engine_confidence': sum(confidence) / len(confidence) if confidence else None,
                          'status': 'unreviewed_OCR_output_not_evidence'}
                results.append(result)
                print(doc_id, page, mode, 'words', len(words), flush=True)
    write(output / 'results.json', {'runs': results,
          'tesseract_version': subprocess.check_output(['tesseract', '--version'], text=True).splitlines()[0],
          'scope': 'One representative page per targeted document, not complete OCR reconstruction.',
          'warning': 'Engine confidence is not measured accuracy. No source text replaced. Needs visual/expert transcription comparison.'})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', type=Path, required=True)
    args = parser.parse_args()
    probe(args.release.resolve())
