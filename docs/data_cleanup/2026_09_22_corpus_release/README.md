# Whole-corpus Passport and BRTA cleanup

## Scope

This is a question-independent structural pass over every supplied Markdown document: 30 Passport documents and 132 BRTA documents. The cleaner does not import an evaluation set, query list, model answers, or expected-answer labels. It operates on document structure and source spans. The one document-specific repair is based on the supplied original PDF, not a chatbot question.

| Domain | Original chunks | Candidate chunks | Documents retained |
|---|---:|---:|---:|
| Passport | 361 | 297 | 30/30 |
| BRTA | 3,161 | 2,795 | 132/132 |

Original Markdown snapshots, original PDFs, active registers, and baseline collections are preserved. Eight unstructured BRTA OCR documents retain their existing 1,119 chunks, with explicit review flags. No entire document has been silently discarded. A smaller chunk count is not an accuracy score.

## General corrections

- Complete Markdown tables stay together with their headers. Oversized units fail embedding validation instead of being truncated.
- Numbered and bulleted list items retain indented continuation paragraphs and conditions.
- Short introductory source prose from parent sections is carried verbatim into child or continuation chunks. Each inherited span has exact offsets in the manifest. Long introductory context is explicitly flagged, not summarized by an LLM.
- FAQ units stay together, sibling headings stay separate, and heading-only fragments remain in the Markdown/manifest rather than masquerading as answer chunks.
- Recognizable metadata preambles, including malformed `## title:` preambles, are separated from answer text. Ambiguous prose is retained. The complete removed preamble is recorded.
- Existing Unicode and citation-marker cleanup remains source preserving through retained snapshots and hashes.
- Missing link targets, embedded metadata, source gaps, duplicate document IDs, and repeated passages are audited across the entire corpus. URLs and legal facts are never guessed.
- The controlled-answer extractor no longer silently cuts evidence at 950 characters. Its existing eligibility limit remains; trailing conditions are preserved. This is not a fix for LLM hallucination.

## Original-source repair

The supplied electric-vehicle notice Markdown had an interrupted quotation followed by a second embedded Markdown document and metadata. Both pages of its registered original PDF were visually inspected. The derived replacement preserves the EV definition's exclusive electric-power condition, bicycle/rickshaw exclusion, inclusive power thresholds, dates, immediate-effect statement, and signer. It is a structured transcription/summary, not a claim of current legal validity or independent human verification.

The repair is gated by the original Markdown and PDF SHA-256 values in [reviewed_repairs.json](../reviewed_repairs.json). The previous body remains in the manifest. The corrected source is [brta_ev_notice_2020.md](../reviewed_sources/brta_ev_notice_2020.md).

## Whole-corpus validation

The independent audit checks every registered document, every source/derived SHA, every chunk owner, complete body-span coverage, verbatim inherited context, unchanged deferred OCR, unique IDs, and all BGE-M3 input lengths. These are structural checks, not answer-correctness metrics. Both corpora passed with zero structural errors. There are no exact whole-document duplicates; 30 repeated passages across BRTA documents are recorded and retained because dates and applicability can differ.

The full test suite passed 38 tests. Regression tests include missing source conditions, altered originals, unattributed chunks, nested list conditions, complete table headers, sibling-context isolation, and ambiguous metadata preservation. The website was restarted with the controlled-evidence truncation fix; `/health` and the three-domain listing passed. Live domain configs still match the baseline snapshots.

- [Passport audit: all 30 documents](passport/CORPUS_AUDIT.md)
- [BRTA audit: all 132 documents](brta/CORPUS_AUDIT.md)
- [Passport detailed machine-readable audit](passport/corpus_audit.json)
- [BRTA detailed machine-readable audit](brta/corpus_audit.json)

## What remains unresolved

Structural cleanup cannot establish that every supplied statement is faithful to its PDF or legally current. Eight long OCR documents still need original-page review. Ten documents have unresolved original-file associations. Seven Passport "Click here" references lack their actual targets in the supplied Markdown. One long BRTA parent-context dependency is flagged. Repeated passages are not automatically merged across documents. The medium/heavy licence guide has no resolved original PDF and must not be described as independently verified.

The previous raw answers also show wrong-service evidence selection and generation errors, including dropped conditions. These are separate from whitespace, table structure, or Markdown cleaning. We have not certified all-domain answer reliability or measured a new LLM accuracy score in this pass.

## Runtime and rollback

Candidate collections are separate from the live indexes. Do not activate merely because structural validation passes. The known-failure retrieval diagnostic remains a small development check, not a whole-corpus accuracy estimate. A preliminary structural candidate still moved Passport fee support below the selected generation context, so there is no basis to claim cleanup alone resolves the chatbot's known failures.

The pre-change code/data reference is Git tag `codex/pre-whole-corpus-cleanup-20260922`, pointing at `f76b41d`. Each domain folder contains its exact baseline config. Originals, derived text, repair records, manifests, code, and audits are versioned; Chroma binary indexes remain local.

Final candidate configs: `domains/passport/config.candidate_20260922_064339_716352.json` and `domains/brta/config.candidate_20260922_063637_152241.json`. Both builds completed all embedding-length and Chroma-ID checks. Neither candidate is active. The earlier `2026_09_22_corpus_v4/` directory records an intermediate structural experiment before the additional metadata and original-PDF repair; it is not the final release.

The final retrieval diagnostics completed using the actual BGE cross-encoder, with no LLM calls:

| Five-case development check | Passport baseline | Passport candidate | BRTA baseline | BRTA candidate |
|---|---:|---:|---:|---:|
| Designated evidence at rank 1 | 2 | 2 | 3 | 3 |
| Designated evidence in top 6 | 5 | 5 | 3 | 3 |
| Designated evidence in selected generation context | 5 | 4 | 3 | 3 |

The Passport fee evidence moved from rank 2 to rank 6. BRTA still missed the predefined driving-test and lost-licence evidence in the returned top six. These checks use predefined source hints and are not exhaustive relevance judgments. They show no justification for switching the live indexes, despite the structural improvements. No new generation-quality claim is made.

- [Passport raw diagnostic results](passport/retrieval_diagnostics.json)
- [BRTA raw diagnostic results](brta/retrieval_diagnostics.json)

## Reproduction

Use a new output directory to preserve revision history:

```bash
.venv/bin/python scripts/clean_service_corpora.py --domain passport --output docs/data_cleanup/NEW_REVISION
.venv/bin/python scripts/clean_service_corpora.py --domain brta --output docs/data_cleanup/NEW_REVISION
.venv/bin/python scripts/audit_service_corpora.py docs/data_cleanup/NEW_REVISION/passport --tokenizer
.venv/bin/python scripts/audit_service_corpora.py docs/data_cleanup/NEW_REVISION/brta --tokenizer
.venv/bin/python -m pytest -q
```

Original PDF availability is required to reproduce a PDF-reviewed repair. If its hash changes, preparation fails rather than applying an unverified replacement.
