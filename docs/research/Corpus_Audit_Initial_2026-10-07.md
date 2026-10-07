# Initial post-thesis corpus audit

Date: 2026-10-07. Baseline: `5a658f0`.

## Git baseline and rollback

The completed thesis branch was fast-forwarded into `main`, preserving all
107 commits beyond the previous main revision. The remote default branch is
`main`. The annotated rollback tag `codex/post-thesis-baseline-20261007` was
pushed to GitHub. New work is on `codex/corpus-audit-next`.

The user confirmed a separate folder backup exists; its contents were not
independently verified. Git does not back up ignored Chroma databases or the
virtual environment. Preserve that folder backup for a full runtime rollback.

## Read-only inspection results

The active `chunk_output_path` and named Chroma collection in each domain's
configuration were inspected. SQLite was opened with `mode=ro`, not through
the Chroma client, to avoid application-level migrations or index writes.

| Domain | Active chunks | Indexed IDs | Minimum / median / maximum content characters | Identical-content groups |
| --- | ---: | ---: | --- | ---: |
| Passport | 361 | 361 | 46 / 567 / 1668 | 0 |
| BRTA | 3161 | 3161 | 35 / 665 / 1781 | 4 |
| Birth and death registration | 187 | 187 | 180 / 547 / 1655 | 0 |

For all three domains:

- No duplicate chunk IDs or empty content were found.
- Every chunk had nonempty retrieval text.
- No Unicode replacement characters were found in content. This is not proof of correct OCR.
- Active chunk IDs matched indexed IDs exactly, with no missing or extra IDs.
- SQLite `quick_check` returned `ok`.

All 30 registered Passport source snapshots and all 132 registered BRTA
source snapshots existed and matched their registered SHA-256 hashes.
Equivalent source-provenance validation for birth/death registration remains
to be designed around its separate preparation pipeline.

## Interpretation and next work

These are structural checks, not a full source-to-chunk semantic audit or
verification of factual currency. Matching IDs does not validate vector
contents, stored document text, embedding model identity, or ANN integrity.
Token lengths have not been measured in this inspection.

1. Inspect the four BRTA identical-content groups with their source metadata;
   preserve them where source, date, or applicability differs.
2. Map birth/death chunks to original source files and establish comparable
   provenance checks.
3. Compare active Passport/BRTA September 19 configurations with the saved
   September 22 cleaning candidates before choosing any replacement.
4. Review OCR and chunk boundaries against originals, retaining headings,
   tables, conditions, and necessary parent context.
5. Build any approved candidates into new collections. Evaluate against the
   frozen baseline before switching active configurations.

No corpus files, active configurations, historical evaluation reports, or
database contents were intentionally modified. The site and Ollama were not
started. The previously run post-relocation test suite passed all 76 tests;
it was not rerun for this documentation-only audit record.
