"""Summarize completed cleanup experiments without claiming unmeasured accuracy."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.prepare_conservative_release import digest


def report(release, structural):
    manifest = json.loads((release / 'manifest.json').read_text())
    validation = json.loads((release / 'validation.json').read_text())
    builds = json.loads((release / 'index_build.json').read_text())
    diagnostics = json.loads((release / 'diagnostics/summary.json').read_text())
    ocr = json.loads((release / 'ocr_experiment/results.json').read_text())
    if not validation['passed'] or any(digest(ROOT / p) != sha for p, sha in manifest['protected_files'].items()):
        raise ValueError('Cannot report a successful release with changed baseline or failed checks')
    lines = ['# Three-domain cleanup and validation report', '', 'Completed 2026-10-15 (Asia/Dhaka).', '',
             '**Status: experiments complete for this batch; candidates are NOT activated. Full original-page certification remains incomplete.**', '',
             '## What was actually processed', '',
             '| Domain | Active chunks | Conservative candidate | Structural candidate | Heading-only units archived | NFC-normalized retained chunks |',
             '| --- | ---: | ---: | ---: | ---: | ---: |']
    for domain, data in manifest['domains'].items():
        structural_count = '-'
        active_count = data['input_chunks']
        if domain != 'birth_death_registration':
            audit = json.loads((structural / domain / 'corpus_audit.json').read_text())
            if audit['errors']:
                raise ValueError('Structural audit failed')
            structural_count = audit['chunk_count']
        else:
            active_count = 187
        lines.append(f"| {domain} | {active_count} | {data['candidate_chunks']} | {structural_count} | {data['excluded_heading_units']} | {data['normalized_chunks']} |")
    lines += ['', 'Birth uses the previously source-reconciled v4 candidate, including chapter corrections, rather than applying NFC alone to the 187-chunk baseline. Its 160 source checks are recorded separately. Passport and BRTA conservative variants preserve all substantive source text modulo canonical Unicode equivalence. Heading-only records are archived with their entire input rows, not destroyed.', '',
              'The structural variant is regenerated from all 30 Passport and 132 BRTA registered documents. It preserves complete tables, nested list continuations and source-linked parent context. Both structural audits passed, including token checks. Eight deferred long OCR documents retain their existing content rather than receiving guessed corrections.', '',
              '## Verification and rollback', '',
              '- Conservative validation checked every retained record against its input, every heading exclusion against its registered Markdown source span, complete document retention, metadata preservation, source hashes and tokenizer limits. This is not full visual verification against original PDF pages.',
              '- All three new Chroma collections completed ID/document verification. Active configurations were not changed. Model parameters and retrieval/selection architecture were held fixed.',
              '- The two structural collections reuse historical embeddings only after exact ID/content/retrieval-text compatibility checks against the freshly regenerated corpus. They are not newly trained or re-embedded models.',
              '- No generative LLM or judge was called. The website and Ollama were not started by this work.',
              '- `manifest.json` records protected baseline file hashes. Original snapshots and PDFs remain unchanged; `codex/post-thesis-baseline-20261007` remains the Git fallback. Local databases still require the existing separate backup, not Git alone.',
              '- Candidate indexes are local ignored artifacts. Configurations, corpus files, scripts, manifests and results are versionable; reproduce indexes with the build command below.', '',
              '## Matched retrieval and selection diagnostics', '',
              f"Completed {diagnostics['completed_runs']} runs: the existing 30 three-domain questions plus designated-source checks for Passport/BRTA, across the available variants.", '',
              '| Domain | Variant | Questions | Mean selected characters | Empty selections | Designated-source checks satisfied |',
              '| --- | --- | ---: | ---: | ---: | ---: |']
    for row in diagnostics['results']:
        support = f"{row['known_failure_selected_support']}/{row['known_failure_cases']}" if row['known_failure_cases'] else 'not defined'
        lines.append(f"| {row['domain']} | {row['variant']} | {row['questions']} | {row['mean_selected_chars']:.1f} | {row['empty_selections']} | {support} |")
    lines += ['', 'These are development diagnostics, not new expert-labelled Hit@5/Precision@5 scores or custom context-relevance scores. A designated source is not an exhaustive list of relevant evidence. Smaller context is not automatically better. BGE-tokenizer counts in individual records are not generator input-token or cost measurements. Timings are single-run diagnostics with caching and variable hardware load, not a controlled latency benchmark.', '',
              '## Original-source checks and OCR experiment', '']
    for domain in ('passport', 'brta'):
        docs = json.loads((release / domain / 'source_register_audit.json').read_text())
        originals = [o for d in docs for o in d['originals']]
        lines.append(f"- {domain}: {len(docs)} registered documents; {len(originals)} original-file associations hash checked; {sum(o.get('pages', 0) or 0 for o in originals)} associated PDF pages probed; {sum(len(o.get('pages_without_extractable_text', [])) for o in originals)} pages without extractable text. Counts are per association, not necessarily unique files. {sum(not d['originals'] for d in docs)} original associations remain unresolved.")
    lines += ['', f"Local {ocr['tesseract_version']} was tested with `ben+eng`, page-segmentation modes 3 and 6: {len(ocr['runs'])} runs on {len({(r['source_path'], r['page']) for r in ocr['runs']})} sampled pages. TSV boxes, engine confidences, text and exact source hashes are retained. No OCR output was promoted into evidence.", '',
              'Visual spot-check: Passport document `passport_ff2616b59b20eb7f` page 3 is blank in the local render. BRTA road-sign manual `brta_23e4ebfee3c93254` page 1 renders missing-glyph boxes. Therefore no-text pages must not all be called OCR failures or missing service information. Engine confidence does not measure accuracy; these samples do not establish a winning OCR mode.', '',
              '## Remaining substantive blockers', '',
              '- Ten Passport/BRTA documents lack a resolved original association. Similar filenames are not sufficient to assign provenance.',
              '- Full page-by-page review of long OCR laws and manuals is not complete. Automated extraction and hash agreement do not certify source fidelity.',
              '- Birth still has unresolved historical/current-rule distinctions, original embedded-image coverage, amendment-history details and independent transcription review.',
              '- The structural audit retains cross-document repeated passages and source conflicts. It does not silently merge versions or choose which authority is current.',
              '- No held-out expert relevance judgments were newly collected. Do not claim state-of-the-art accuracy, or activate solely because structural checks pass.', '',
              '## Recommended next research step', '',
              'Keep the active thesis baseline unchanged. Review the saved question-by-question evidence differences before selecting a corpus variant. Resolve the ten missing original associations and independently transcribe a representative sample of OCR-heavy pages, including amounts, exceptions and negation. Compare OCR variants against those transcriptions rather than engine confidence.', '',
              'Then freeze a reviewed corpus and collect held-out expert relevance labels. Compare baseline, conservative and structural corpora with the same retrieval architecture; only after that change retrieval or selection components. This separates data-quality effects from architecture effects and preserves a defensible fallback.', '',
              '## Reproduction', '', 'Use fresh output names; builders refuse to overwrite prior experiments.', '', '```sh',
              '.venv/bin/python scripts/prepare_conservative_release.py --output docs/data_cleanup/NEW_RELEASE --birth-candidate docs/data_cleanup/birth_review_20261014/candidate_v4',
              '.venv/bin/python scripts/validate_conservative_release.py --release docs/data_cleanup/NEW_RELEASE',
              '.venv/bin/python scripts/build_conservative_indexes.py --release docs/data_cleanup/NEW_RELEASE --device mps',
              '.venv/bin/python scripts/probe_ocr_review_pages.py --release docs/data_cleanup/NEW_RELEASE',
              '.venv/bin/python scripts/compare_conservative_release.py --release docs/data_cleanup/NEW_RELEASE --structural docs/data_cleanup/structural_20261015 --device mps',
              '.venv/bin/python scripts/report_conservative_release.py --release docs/data_cleanup/NEW_RELEASE --structural docs/data_cleanup/structural_20261015',
              '.venv/bin/python -m pytest -q', '```', '',
              'The structural comparison requires the checked historical collections. If unavailable, rebuild their exact corpora in separate stores; do not substitute active collections. The preparation script requires Poppler tools, and the OCR probe requires Tesseract Bengali/English language data.', '',
              '## Method references', '',
              'The [preceding research/method guide](../birth_review_20261014/README.md) records the Unicode standard, BUET Bengali-English normalizer, Indic grapheme-normalization research and Docling OCR options. This batch deliberately applies only conservative transformations that can be checked against source text, and tests OCR separately rather than installing every framework or rewriting legal evidence with an LLM.', '']
    target = release / 'README.md'
    with target.open('x', encoding='utf-8') as handle:
        handle.write('\n'.join(lines))
    print(target)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', type=Path, required=True)
    parser.add_argument('--structural', type=Path, required=True)
    args = parser.parse_args()
    report(args.release.resolve(), args.structural.resolve())
