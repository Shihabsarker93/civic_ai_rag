# Bangla data-quality milestone: 2026-10-14

Status: unactivated review candidate. Active corpora and indexes are unchanged.

## Implemented

- Recovered Act chapter labels directly from ordered blocks in the supplied HTML.
- Fixed the legal chunker's chapter-boundary bug: flush the previous section before changing chapter metadata. Empty lines no longer produce a legal chunk.
- Built `candidate_v4` separately, retaining v1-v3 and the thesis baseline.
- Added chapter/source validation and regression tests.
- Audited the three configured active corpora without changing their text.

## Results

Birth candidate: 190 passages; maximum recorded retrieval length 809 BGE-M3 tokens. All 160 source checks passed. These checks establish extraction/coverage consistency, not answer accuracy or current legal validity.

| Active domain | Chunks | Non-NFC fields | Mixed-digit fields | Exact NFC content duplicate groups |
| --- | ---: | ---: | ---: | ---: |
| Birth Registration | 187 | 0 | 54 | 0 |
| BRTA | 3161 | 2306 | 2500 | 4 |
| Passport | 361 | 58 | 80 | 0 |

Counts refer to fields (`content` and `retrieval_text`), not distinct erroneous passages. One field can have multiple flags. Mixed-script digits are not necessarily errors. No replacement-character, private-use or listed control/joiner flags were found in the audited chunk fields; this does not prove original documents or OCR are correct. Duplicate groups compare complete NFC-normalized content, including any embedded headers. They do not detect all semantic or overlapping duplicates.

The chapter-boundary fix also corrects some rules' chapter assignments when generating this candidate. It does not modify rules' source wording beyond the already recorded v3 repairs. Existing chunk IDs are retained where possible; candidate directory and content hashes distinguish revisions.

## Method selection

There is no demonstrated single best or officially recommended Bangladesh civic-RAG cleaning pipeline established by this work. The following is a source-informed shortlist, not a claim of state-of-the-art results.

1. **Conservative canonical normalization.** Keep source files immutable; compare NFC-normalized text and retain change records. Compatibility normalization and spelling correction require separate experiments, not silent replacement. Unicode distinguishes canonical from compatibility equivalence. [Unicode normalization FAQ](https://www.unicode.org/faq/normalization.html)
2. **Bangla-specific normalization experiment.** BUET's Bengali-English normalizer is relevant local research tooling, but its published use is translation preprocessing, its default is NFKC, and its repository has a noncommercial share-alike license. Evaluate changes and licensing before integration; it is not installed or applied here. [Official BUET normalizer](https://github.com/csebuetnlp/normalizer)
3. **Grapheme-aware review.** Indic normalization research addresses script-specific malformed sequences and grapheme structure. This motivates a controlled comparison, not automatic acceptance of every rewrite on legal evidence. [Unicode Normalization and Grapheme Parsing of Indic Languages](https://arxiv.org/abs/2306.01743)
4. **Layout-aware OCR comparison.** Docling offers OCR and table extraction options. Compare selected difficult scanned pages using a Bangla-capable backend against human-reviewed transcriptions before converting the corpus. Its framework capabilities alone do not establish Bangla recognition quality. [Official full-page OCR example](https://docling-project.github.io/docling/_generated/examples/full_page_ocr/)

These sources were consulted on 2026-10-14. No new OCR/normalizer dependencies or external model calls were introduced by this milestone.

## Corpus-specific policy

- Preserve amounts, dates, negation, jurisdiction, eligibility conditions and exceptions. Do not remove stopwords or stem source evidence.
- Keep retrieval aliases distinct from source evidence. Do not translate Bangla into English as a mandatory cleaning step.
- Keep fee labels, currencies and applicable conditions attached to amounts. Preserve FAQ answers with their questions and legal units with chapters.
- Review duplicates with source identity and version information before exclusion. Similar wording from different authorities is not necessarily redundant.
- Preserve source conflicts instead of guessing which instruction is current.
- Review zero-width handling separately. The existing Birth normalizer removes joiners; this milestone does not change that policy. Absence of joiners in already-cleaned chunks cannot prove their removal was harmless in source text.

## Reproduce

Run from the repository with fresh output paths; tools refuse existing outputs.

```sh
.venv/bin/python scripts/prepare_birth_source_reconciliation.py \
  --original-root '/Users/shihab/01 Thesis/Rag/Pipeline/p2/raw_data/raw_docs' \
  --output "$PWD/docs/data_cleanup/NEW_REVIEW/reviewed_sources"
.venv/bin/python scripts/prepare_birth_review_candidate.py \
  --original-root '/Users/shihab/01 Thesis/Rag/Pipeline/p2/raw_data/raw_docs' \
  --output docs/data_cleanup/NEW_REVIEW/candidate \
  --supplement docs/data_cleanup/NEW_REVIEW/reviewed_sources/supplement.json
.venv/bin/python scripts/validate_birth_source_candidate.py \
  --original-root '/Users/shihab/01 Thesis/Rag/Pipeline/p2/raw_data/raw_docs' \
  --candidate docs/data_cleanup/NEW_REVIEW/candidate \
  --report docs/data_cleanup/NEW_REVIEW/source_validation.json
.venv/bin/python scripts/audit_bangla_corpus_quality.py \
  --output docs/data_cleanup/NEW_REVIEW/quality_audit.json
.venv/bin/python -m pytest -q
```

## Remaining work and activation boundary

Next inspect the four BRTA duplicate groups and original-source mappings, then create a hash-gated NFC experiment with digit/condition preservation checks and fresh token counts. Passport's non-NFC fields need the same treatment. Do not merely rewrite active JSONL: existing vectors would no longer correspond to updated text.

Birth still needs full rules-PDF visual review, embedded DOCX image coverage, independent scanned-guideline transcription review, amendment-history provenance and conflicting-source resolution. Passport and BRTA source-by-source audits are not complete. The previous review register remains applicable except that Act chapter metadata is now checked.

Before activation, build a separate candidate index and evaluate held-out retrieval using a fixed architecture. Record fidelity checks, retrieval/answer results and runtime/token costs separately. A lower chunk count or cleaner appearance is not evidence of better retrieval.

Fallback: `codex/post-thesis-baseline-20261007` retains the Git baseline, and earlier candidates remain untouched. Revert this milestone to undo code changes if needed; no active database rollback is necessary because none was written. Local untracked resources remain covered by the user's separate backup, not by Git alone.
