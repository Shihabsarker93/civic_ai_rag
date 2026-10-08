# Guideline reconstruction candidate

Completed: 2026-10-09 (Asia/Dhaka).

## Scope

Reconstructed the supplied six-page 2021 Birth and Death Registration guideline scan into `reviewed_sources/guidelines_2021.md`. This is an assistant visual transcription with normalized punctuation and editorial page/section headings, not a certified verbatim transcription or independent expert review. The historical document date is 2021-08-18; current applicability has not been verified.

The replacement is used only in `candidate_v2`. Active raw files, active chunks, configuration and candidate_v1 were not changed. No Chroma index was built, and no site or Ollama service was started.

## Structure and coverage

- Seven introductory provisions are retained separately.
- Eight task forces each have distinct membership and duties sections: divisional, city corporation, district, upazila, municipality, cantonment, union and ward.
- Every searchable section carries the printed source page number and original PDF hash.
- Issuer/date, signatories and the 35-entry distribution list remain in the reviewed source and manifest, but are excluded from searchable evidence. This is a citizen-service retrieval choice, not a claim that these sections have no archival value.
- Handwritten signature graphics and an uncertain telephone number were not transcribed; the unchanged PDF remains authoritative.
- A second visual check corrected the city corporation social-worker count to two and separated its last two duties. Page-six recipients were read directly from the scan rather than inferred from similar ministry names.

## Validation results

| Check | Result |
| --- | --- |
| Full test suite | 81 passed |
| Searchable guideline sections/passages | 23 |
| Explicit provenance-only sections | 4 |
| Previous guideline passages | 12 |
| Complete Birth candidate_v2 passages | 199 |
| Active Birth passages | 187 |
| Previous candidate_v1 passages | 188 |
| Maximum guideline content length, including headers | 1,166 characters |
| Maximum guideline retrieval length | 527 BGE-M3 tokens |
| Maximum complete candidate retrieval length | 772 BGE-M3 tokens |
| Token warnings | None |
| Active baseline hash checks | Unchanged |

Coverage validation compares every substantive transcribed section against its resulting chunk payload after Unicode and whitespace normalization. It detects chunking omissions; it does not prove that the transcription itself is perfect. New guideline IDs have a `review_v2_` prefix so they cannot silently reuse the meanings of old OCR chunk IDs.

The first validation attempt stopped because source headings and chunk headings used different Unicode representations. Normalizing both consistently fixed the check. The incomplete output was moved outside the repository; it was not activated.

## Reproduce

Run from the repository root with the existing virtual environment and locally cached tokenizer. Choose a new output directory; the script refuses to overwrite any existing revision.

```sh
.venv/bin/python scripts/prepare_birth_review_candidate.py \
  --original-root '/Users/shihab/01 Thesis/Rag/Pipeline/p2/raw_data/raw_docs' \
  --output /tmp/civicrag-birth-review-new-revision \
  --supplement docs/data_cleanup/birth_review_20261008/guideline_review.json
.venv/bin/python -m pytest -q
```

`repairs.json` retains the previous targeted repairs. `guideline_review.json` adds a hash-gated replacement: both baseline sources and the reviewed replacement must match their recorded hashes before generation.

## Next gate

Have a Bangla-reading reviewer compare the transcription with the original scan, particularly committee roles, counts and legal references. Continue reconciliation of the remaining Birth source files, including FAQ HTML, Act HTML and rules DOCX. Then evaluate candidate retrieval against the frozen baseline before considering activation. No answer-quality improvement has been measured for this revision.
