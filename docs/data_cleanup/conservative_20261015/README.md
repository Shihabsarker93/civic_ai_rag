# Three-domain cleanup and validation report

Completed 2026-10-15 (Asia/Dhaka).

**Status: experiments complete for this batch; candidates are NOT activated. Full original-page certification remains incomplete.**

## What was actually processed

| Domain | Active chunks | Conservative candidate | Structural candidate | Heading-only units archived | NFC-normalized retained chunks |
| --- | ---: | ---: | ---: | ---: | ---: |
| birth_death_registration | 187 | 190 | - | 0 | 0 |
| passport | 361 | 304 | 297 | 57 | 25 |
| brta | 3161 | 2864 | 2795 | 297 | 1051 |

Birth uses the previously source-reconciled v4 candidate, including chapter corrections, rather than applying NFC alone to the 187-chunk baseline. Its 160 source checks are recorded separately. Passport and BRTA conservative variants preserve all substantive source text modulo canonical Unicode equivalence. Heading-only records are archived with their entire input rows, not destroyed.

The structural variant is regenerated from all 30 Passport and 132 BRTA registered documents. It preserves complete tables, nested list continuations and source-linked parent context. Both structural audits passed, including token checks. Eight deferred long OCR documents retain their existing content rather than receiving guessed corrections.

## Verification and rollback

- Conservative validation checked every retained record against its input, every heading exclusion against its registered Markdown source span, complete document retention, metadata preservation, source hashes and tokenizer limits. This is not full visual verification against original PDF pages.
- All three new Chroma collections completed ID/document verification. Active configurations were not changed. Model parameters and retrieval/selection architecture were held fixed.
- The two structural collections reuse historical embeddings only after exact ID/content/retrieval-text compatibility checks against the freshly regenerated corpus. They are not newly trained or re-embedded models.
- No generative LLM or judge was called. The website and Ollama were not started by this work.
- `manifest.json` records protected baseline file hashes. Original snapshots and PDFs remain unchanged; `codex/post-thesis-baseline-20261007` remains the Git fallback. Local databases still require the existing separate backup, not Git alone.
- Candidate indexes are local ignored artifacts. Configurations, corpus files, scripts, manifests and results are versionable; reproduce indexes with the build command below.

## Matched retrieval and selection diagnostics

Completed 110 runs: the existing 30 three-domain questions plus designated-source checks for Passport/BRTA, across the available variants.

| Domain | Variant | Questions | Mean selected characters | Empty selections | Designated-source checks satisfied |
| --- | --- | ---: | ---: | ---: | ---: |
| birth_death_registration | baseline | 10 | 3656.7 | 0 | not defined |
| birth_death_registration | candidate | 10 | 4583.4 | 0 | not defined |
| passport | baseline | 10 | 4220.4 | 0 | 5/5 |
| passport | candidate | 10 | 4220.8 | 0 | 5/5 |
| passport | structural | 10 | 4819.8 | 0 | 5/5 |
| brta | baseline | 10 | 3967.0 | 0 | 4/5 |
| brta | candidate | 10 | 3968.8 | 0 | 4/5 |
| brta | structural | 10 | 4599.5 | 0 | 4/5 |

These are development diagnostics, not new expert-labelled Hit@5/Precision@5 scores or custom context-relevance scores. A designated source is not an exhaustive list of relevant evidence. Smaller context is not automatically better. BGE-tokenizer counts in individual records are not generator input-token or cost measurements. Timings are single-run diagnostics with caching and variable hardware load, not a controlled latency benchmark.

## Original-source checks and OCR experiment

- passport: 30 registered documents; 26 original-file associations hash checked; 62 associated PDF pages probed; 10 pages without extractable text. Counts are per association, not necessarily unique files. 4 original associations remain unresolved.
- brta: 132 registered documents; 127 original-file associations hash checked; 1334 associated PDF pages probed; 406 pages without extractable text. Counts are per association, not necessarily unique files. 6 original associations remain unresolved.

Local tesseract 5.5.2 was tested with `ben+eng`, page-segmentation modes 3 and 6: 32 runs on 16 sampled pages. TSV boxes, engine confidences, text and exact source hashes are retained. No OCR output was promoted into evidence.

Visual spot-check: Passport document `passport_ff2616b59b20eb7f` page 3 is blank in the local render. BRTA road-sign manual `brta_23e4ebfee3c93254` page 1 renders missing-glyph boxes. Therefore no-text pages must not all be called OCR failures or missing service information. Engine confidence does not measure accuracy; these samples do not establish a winning OCR mode.

## Remaining substantive blockers

- Ten Passport/BRTA documents lack a resolved original association. Similar filenames are not sufficient to assign provenance.
- Full page-by-page review of long OCR laws and manuals is not complete. Automated extraction and hash agreement do not certify source fidelity.
- Birth still has unresolved historical/current-rule distinctions, original embedded-image coverage, amendment-history details and independent transcription review.
- The structural audit retains cross-document repeated passages and source conflicts. It does not silently merge versions or choose which authority is current.
- No held-out expert relevance judgments were newly collected. Do not claim state-of-the-art accuracy, or activate solely because structural checks pass.

## Recommended next research step

### Interpretation of this completed batch

Passport designated-source coverage remains 5/5 and BRTA remains 4/5 in all three variants. Conservative normalization has almost no effect on mean selected context length. Structural chunking increases mean selected context from 4,220.4 to 4,819.8 characters for Passport and from 3,967.0 to 4,599.5 for BRTA. Birth v4 increases mean selected context from 3,656.7 to 4,583.4 characters. No variant produced an empty selection on the reused question set.

These results support the integrity and reproducibility of the cleanup, not a claim that it improves answer accuracy or reduces context. The designated BRTA lost-license source remains unselected in all variants. Keep this failure visible for the next source/evidence-selection investigation. Do not rewrite the thesis results using these development diagnostics.

Keep the active thesis baseline unchanged. Review the saved question-by-question evidence differences before selecting a corpus variant. Resolve the ten missing original associations and independently transcribe a representative sample of OCR-heavy pages, including amounts, exceptions and negation. Compare OCR variants against those transcriptions rather than engine confidence.

Then freeze a reviewed corpus and collect held-out expert relevance labels. Compare baseline, conservative and structural corpora with the same retrieval architecture; only after that change retrieval or selection components. This separates data-quality effects from architecture effects and preserves a defensible fallback.

## Reproduction

Use fresh output names; builders refuse to overwrite prior experiments.

```sh
.venv/bin/python scripts/prepare_conservative_release.py --output docs/data_cleanup/NEW_RELEASE --birth-candidate docs/data_cleanup/birth_review_20261014/candidate_v4
.venv/bin/python scripts/validate_conservative_release.py --release docs/data_cleanup/NEW_RELEASE
.venv/bin/python scripts/build_conservative_indexes.py --release docs/data_cleanup/NEW_RELEASE --device mps
.venv/bin/python scripts/probe_ocr_review_pages.py --release docs/data_cleanup/NEW_RELEASE
.venv/bin/python scripts/compare_conservative_release.py --release docs/data_cleanup/NEW_RELEASE --structural docs/data_cleanup/structural_20261015 --device mps
.venv/bin/python scripts/report_conservative_release.py --release docs/data_cleanup/NEW_RELEASE --structural docs/data_cleanup/structural_20261015
.venv/bin/python -m pytest -q
```

The structural comparison requires the checked historical collections. If unavailable, rebuild their exact corpora in separate stores; do not substitute active collections. The preparation script requires Poppler tools, and the OCR probe requires Tesseract Bengali/English language data.

## Method references

The [preceding research/method guide](../birth_review_20261014/README.md) records the Unicode standard, BUET Bengali-English normalizer, Indic grapheme-normalization research and Docling OCR options. This batch deliberately applies only conservative transformations that can be checked against source text, and tests OCR separately rather than installing every framework or rewriting legal evidence with an LLM.
