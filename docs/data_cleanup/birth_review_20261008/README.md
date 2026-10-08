# Birth Registration source review: first candidate

Date: 2026-10-08. Status: **partial review; not activated**.

This is the first source-review batch, not a declaration that all three
domains have been cleaned. Architecture, active sources, configuration and
Chroma collections are unchanged. No new embedding index or model answers
were generated.

## Delivered

- A source inventory with hashes for all 19 files in the supplied original
  directory, including alternative formats and the OCR archive.
- A per-file register for all 14 prepared Markdown/JSON inputs, with source
  filename associations, candidate hashes, repair records, and chunk ownership.
- Four hash-gated, source-based corrections across two prepared documents.
- A separate candidate with 188 chunks versus 187 active chunks. No old IDs
  were removed; one omitted source section is now represented.
- Local BGE-M3 token checks: maximum retrieval input 772 tokens, below 8192.
- Regression tests for exact repair anchors, preserved restrictions and
  refusal to overwrite an existing candidate revision.

See `candidate_v1/manifest.json` and `repairs.json` for exact changes and hashes.
Candidate text is under `candidate_v1/raw`; chunks are in
`candidate_v1/chunks.jsonl`. The candidate is deliberately not an active
domain configuration.

## Corrections actually made

| Repair | Evidence | Candidate change |
| --- | --- | --- |
| Weakened punctuation instruction | Original application-process DOCX instruction | Restored the source's prohibition rather than "better not to use" wording |
| Required attachments described as examples | Correction-notice PDF page 2, step 6 | Removed the illustrative "such as" qualification and retained all four attachments |
| Missing operator for nationality correction | Correction-notice PDF page 2 | Restored entry using the registrar assistant's ID |
| Missing birth-date correction service | Correction-notice PDF page 2, final row | Restored the historical restriction, day/month-only permission, and specified administrative offices |

Both notice PDF pages were rendered and visually inspected. The notice is
dated 22 December 2022. Its historical wording has been preserved; this does
not establish today's law or current BDRIS capabilities. Candidate notice
chunks carry that date and `current_applicability_verified: false` metadata.
No claim is made that the unchanged generation pipeline enforces that flag.

The PDF under `scanned_pdf` was used and hash-locked. The similarly named
PDF under `bijoy_pdf` has different bytes and remains an alternative in the
register, rather than being silently treated as the same source.

## Six-page 2021 guideline review

All six scanned pages were visually inspected for structure and compared
with the prepared OCR's layout. Full transcription is **not complete**.

| Page | Source structure | Required work |
| --- | --- | --- |
| 1 | Dated circular and introductory provisions 1-5 | Correct OCR words and restore missing sentence portions against scan |
| 2 | Provisions 6-7; divisional and city-corporation task-force tables | Separate membership from responsibilities instead of interleaving columns |
| 3 | District and upazila task-force tables | Preserve each body's members, offices and duties as distinct units |
| 4 | Municipality and cantonment task-force tables | Reconstruct the two-column relationships with their headings |
| 5 | Union and ward task-force tables; signature | Preserve committee-specific duties and keep signature/provenance separate |
| 6 | Distribution/copy list | Retain for provenance; assess separately from citizen-answer evidence |

The existing OCR interleaves membership and duty columns. Simple whitespace
cleanup cannot repair those relationships. The guideline is therefore copied
unchanged into this first candidate, with `ocr_page_review_required` status.
Its 12 chunks have not been dropped or certified as clean.

## Other source findings

- The six converted DOCX files are available. Text from five non-rules files
  was extracted for initial inspection; this is not an exhaustive review of
  each DOCX or its embedded images.
- The seven fee rows in the prepared table agree in amounts and conditions
  with the extracted DOCX table text on this initial inspection. No fee value
  was changed, and the full-table/row overlap was preserved.
- The two application guides use different parental-registration conditions:
  a 2013 birth-year distinction versus an under/over-18 distinction. These
  distinctions exist in the supplied DOCX text. They must not be blended into
  a new rule or resolved merely by preferring one chunk.
- The same two guides leave boundary cases unclear (the exact year/date or
  exactly age 18). No missing boundary rule was invented.
- The 2004 Act and portal summary lack an explicit original filename in their
  prepared metadata. Corresponding HTML filenames are recorded as hypotheses.
- FAQ JSON-to-HTML associations are also filename hypotheses until the full
  question/answer text is reconciled. The FAQ Markdown versions stay excluded
  from chunking by the existing configuration, not newly deleted.
- Rules/DOCX fidelity, complete Act/HTML comparison, FAQ completeness and
  parent-condition preservation across chunks are still pending.

## Safeguards and reproduction

The builder checks both the prepared-input and reviewed-original SHA-256
before applying each correction. Every replacement requires one exact
anchor. It refuses an existing output directory, validates unique chunk IDs
and embedding input length, and checks active input hashes after preparation.
Unrepaired prepared files are copied byte-for-byte.

```bash
.venv/bin/python scripts/prepare_birth_review_candidate.py \
  --original-root '/Users/shihab/01 Thesis/Rag/Pipeline/p2/raw_data/raw_docs' \
  --output docs/data_cleanup/birth_review_20261008/candidate_NEW
.venv/bin/python -m pytest -q
```

The current builder deliberately retains the existing chunker and aliases.
It is a source-correction baseline, not yet the proposed context-preserving
chunking experiment. Hashes provide change detection, not factual verification.

## Remaining work, in order

1. Reconstruct the six-page guideline faithfully, retaining page-level
   provenance and keeping each committee's membership and duties distinct.
2. Complete DOCX/HTML reconciliation for the remaining Birth Registration
   sources, including alternate-source conflicts and uncertain associations.
3. Test parent-condition preservation with source-derived regression cases,
   without rewriting factual statements or merging distinct procedures.
4. Continue the same source-by-source process for Passport and BRTA.
5. Only after review, build separate indexes and compare them against the
   frozen baseline with the architecture held constant.
