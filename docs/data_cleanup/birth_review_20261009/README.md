# Birth Registration: source reconciliation candidate v3

Work started 2026-10-09; validation completed 2026-10-14 (Asia/Dhaka).

Status: **unactivated source-review candidate, not production-ready**.

## Changes completed

1. Restored all 26 FAQ questions and answers from the two supplied HTML snapshots, plus the second source's separate preamble. Source spelling and qualifications are retained rather than silently rewritten. Existing categories and search aliases remain editorial metadata; they have not been independently validated.
2. Reconstructed the 2004 Act's 26 numbered sections from the supplied HTML, producing 29 passages. Amendment-marker numbers were removed from evidence while amended text, brackets and the original HTML were preserved. The opening publication material and amendment notes remain in the original rather than answer passages. Chapter grouping metadata needs reconciliation before activation; section numbers and complete section bodies are checked.
3. Rebuilt the parent-name correction document as four complete source scenarios. Previously, separate headings could detach the death-proof requirement from its date and parental-registration conditions. Each complete original scenario now fits in one passage.
4. Removed the gazette publication price from the rules' definition section after inspecting PDF page 1. It is not a registration fee. Restored three shortened labels in the fee table against PDF page 20 without changing amounts.
5. Carried forward the six-page guideline reconstruction and the earlier application/notice repairs. These earlier artifacts were not overwritten.

## Validation

| Check | Result |
| --- | --- |
| Full test suite | 88 passed |
| Source/integrity checks against supplied originals | 134 passed |
| Candidate passages | 190 |
| Active baseline passages | 187 |
| Maximum candidate retrieval input | 809 BGE-M3 tokens |
| Token warnings | None |
| Active prepared input hashes | Unchanged |
| Original source hashes | Unchanged |
| Index rebuilt or candidate activated | No |

The 134 checks include freshly extracting source HTML and comparing all FAQ answers and Act section bodies with the candidate, retaining all four correction conditions within their passages, checking IDs and checking recorded token limits. This is **not** a retrieval benchmark or proof of better generated answers. The increase or decrease in chunk count is not a quality score.

Detailed checks: `source_validation_20261014.json`. Candidate: `candidate_v3/chunks.jsonl`. Change lineage and source hashes: `candidate_v3/manifest.json`. All 26 old/new FAQ pairs: `reviewed_sources/faq_comparison.json`.

## Review register

| Prepared input | Review performed | Remaining limit |
| --- | --- | --- |
| FAQ JSON 01 | All 16 Q/A pairs restored from national registrar HTML | Source currency and editorial aliases unverified |
| FAQ JSON 02 | All 10 Q/A pairs and preamble restored from Goraduba Union Parishad HTML | Local instructions must not be assumed national |
| Correction application guide | All four substantive DOCX conditions retained intact | Converted DOCX, not full independent PDF verification; exact boundary date not resolved by source |
| 2004 Act | All 26 HTML sections mapped and coverage-checked | Chapter metadata and amendment-history provenance require a further pass |
| Fee guide | Seven DOCX rows inspected against prepared table; no values changed | Independent visual and current-fee verification not completed |
| 2021 guideline | All six pages transcribed in preceding batch | Independent Bangla transcription review pending |
| 2018 rules | All 26 rule bodies compared against DOCX; selected PDF pages inspected | Conversion artifacts and full visual verification remain; text agreement is not proof of conversion fidelity |
| Application process 01 | DOCX body inspected; earlier punctuation instruction restored | Embedded screenshot coverage not reviewed; retains 2013-year condition |
| Application process 02 | DOCX text inspected against prepared steps | Embedded images not certified; retains under/over-18 condition |
| FAQ Markdown 01 and 02 | Left untouched and excluded under the existing JSON-first policy | Full Markdown/HTML equivalence not certified |
| Portal summary | Contact emails and displayed hotline numbers checked in supplied HTML | Full link-target reconciliation and snapshot currency remain |
| Know-this guide | DOCX text inspected against prepared sections | Converted-source and current-procedure verification remain |
| Correction notice | Prior PDF-based repairs carried forward | Historical 2022 notice; current applicability not established |

The machine manifest conservatively leaves unchanged files at `pending_original_content_review`, even where this table records a limited text inspection. Do not interpret an inspection as completed independent review.

## Source differences that must remain visible

- The two FAQ sources are not interchangeable. The local union page adds hearing/certification instructions for some cases that are absent from the national FAQ. They remain separate documents with separate source URLs.
- The application guides use different parental-registration conditions: birth before/after 2013 versus age below/above 18. These are source differences, not errors to resolve by combining their sentences. The exact boundary cases are not supplied consistently.
- The correction guide distinguishes birth before/after 01/01/2001 and parental registration/death status. The source does not settle the exact boundary date. No equality case was invented.
- The standalone fee guide says birth-date correction for its 100-taka row; the rules table uses the broader source label "information correction" and separately lists non-birth-date corrections. Both source labels remain; no new rule is inferred.
- "Current" statements and dates inside saved documents are historical snapshot claims. This work did not check live law or live BDRIS behavior.

## Reproduction

Use a fresh repository-contained output directory for replacement generation and a fresh candidate directory. Every builder refuses to overwrite an existing revision.

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
.venv/bin/python -m pytest -q
```

## Next work

Complete chapter/provenance and unresolved-source checks, then compare retrieval using a separately built index with the architecture and evaluation questions held constant. Keep the active thesis baseline as the fallback. Passport and BRTA still need their own source-by-source reviews; this report does not certify all three domains as cleaned.
