# Corpus investigation and repair plan

Date: 2026-10-08

Baseline: `codex/post-thesis-baseline-20261007` (`5a658f0`).
Development branch: `codex/corpus-audit-next`.

## Summary

Keep the active system unchanged. The immediate work is source traceability,
targeted OCR review, and an isolated heading-only chunk experiment, not a
replacement of the whole retrieval architecture.

This investigation inspected local prepared sources, chunk metadata, source
file availability, and saved experimental results. It did not certify original
PDF fidelity or current government rules, and did not run new retrieval or
answer-generation experiments. No site or Ollama process was started.

## 1. BRTA duplicate findings

All four identical-content groups are pairs of heading-only chunks, within
three documents. They are not four pairs of duplicate substantive procedures.
Their different source offsets explain why distinct IDs were generated.

| Document ID | Active chunk suffix pairs | Heading represented |
| --- | --- | --- |
| `brta_9a180bfd62e0eab9` | `v2_0001`, `v2_0005` | Government heading in the April 2024 fee/penalty extension notice |
| `brta_8b38af8ac3dab592` | `v2_0001`, `v2_0005` | Gazette heading in the 2017 BRTA Act and commencement notice |
| `brta_76d085ed61f044f4` | `v2_0001`, `v2_0007` | Government heading in the commercial vehicle economic-life notice |
| `brta_76d085ed61f044f4` | `v2_0002`, `v2_0008` | Ministry heading in the same economic-life document |

The complete chunk ID is the document ID followed by `_` and the suffix.
These eight chunks include a document title and section label, but their
source bodies contain only headings. The title can make them look relevant
without supplying the requested procedural details.

The final September 22 candidate already records these heading spans under
`retained_non_evidence_sections` in its BRTA manifest. They remain in the
preserved document representation, rather than standalone searchable chunks.
The candidate has zero exact duplicate-content groups.

### Proposed isolated repair

Prepare a separate candidate excluding only confirmed heading-only search
units. Preserve their headings as context/metadata for substantive sections
and retain originals and span records. Do not globally deduplicate identical
text across documents: identical wording may have different provenance or
applicability. Test this small change separately from the full September
cleaning package. No chunk has been removed in this investigation.

## 2. Birth/death registration traceability

### Fresh checks

- All 187 active chunks regenerated in memory with the current preparation
  functions and current raw Markdown/JSON inputs.
- All active IDs were found in the regenerated set. Content and retrieval text
  matched exactly for all 187 chunks.
- The locally cached BGE-M3 tokenizer was used with special tokens included:
  maximum retrieval input length was 772 tokens; none exceeded 8192.
- Recomputed retrieval token counts matched stored metadata for every chunk.
- There are 12 contributing prepared files: two JSON files produce 27 chunks;
  ten Markdown files produce 160 chunks.
- Two additional FAQ Markdown files intentionally produce no chunks because
  the configuration prefers the structured FAQ JSON. This is not, by itself,
  a missing-source defect; equivalence still needs review against original HTML.

Reproduction confirms consistency with prepared inputs, not fidelity to the
original PDF, DOCX, or HTML. Token fit likewise does not prove clean OCR.

### Original file inventory

The historical original root still exists:

`/Users/shihab/01 Thesis/Rag/Pipeline/p2/raw_data/raw_docs`

It contains 19 files, including an OCR ZIP and parallel source formats. These
are not 19 distinct service documents. Ten of the twelve prepared Markdown
files declare a source filename that exists under this root. Two Markdown
files lack an explicit `source_file`: the 2004 Act and the portal summary.
Correspondingly named HTML files exist, but filename similarity is only a
candidate association, not independently verified provenance.

The correction notice has two different PDFs with the same filename:

| Folder | SHA-256 |
| --- | --- |
| `scanned_pdf` | `47638e4023bfbe67100493a3833996d04ad7b7d7fe2878751f617f45172395b4` |
| `bijoy_pdf` | `0469faf38b954ba3c29d809d98c0038f3b938715544b5a9d8fca4f330d53ad5f` |

Therefore basename-only attribution is insufficient. Different hashes do not
necessarily mean different substantive content, but the exact source used
must be recorded. The historical audit identifies scanned-PDF OCR; the new
register should retain that history and both available alternatives pending
verification rather than silently choosing one by filename.

### Concrete repair priorities

1. Create a candidate source register linking prepared files to exact original
   relative paths and hashes. Record uncertain mappings explicitly, including
   the two FAQ JSON-to-HTML associations.
2. Review the 2021 guideline OCR against its scanned pages. Current prepared
   text visibly includes fragments such as `ee,`, broken dates, mixed symbols,
   and disrupted table layout. Twelve active chunks derive from this file.
3. Review the correction notice's six chunks against the identified original
   version, not just against the already cleaned Markdown.
4. Check FAQ question/answer completeness against the original HTML and legal
   section coverage against original sources. Exact regeneration is not a
   substitute for these checks.
5. Keep the complete fee table and its seven row chunks during this review.
   Their overlap is intentional; blind deduplication would remove useful
   alternative retrieval units. Check row conditions and headers explicitly.

No original pages were visually reviewed in this investigation. These are
the next review tasks, not claims that those sources have been repaired.

## 3. Saved candidate versus active data

The final saved candidate is `docs/data_cleanup/2026_09_22_corpus_release`,
not the earlier plain or v4 experiment.

| Domain | Active chunks | Final candidate chunks | Documents retained | Fresh structural errors |
| --- | ---: | ---: | ---: | ---: |
| Passport | 361 | 297 | 30 | 0 |
| BRTA | 3161 | 2795 | 132 | 0 |

The existing whole-corpus auditor was rerun on disposable copies of each
candidate. Only the disposable manifests' derived-file locations were rebased;
original source references and hashes remained unchanged. Temporary audit
outputs were removed with their temporary directories. Historical reports
were not overwritten. This pass did not rerun candidate tokenization; the
saved September audits report that earlier check separately.

The fresh audit validates source and derived hashes, document/chunk ownership,
body-span coverage, inherited context, and unchanged deferred OCR. It found
30 repeated BRTA passages across documents, retained for applicability review.
This is distinct from the four exact active-chunk duplicate groups above.

### Important unresolved candidate issues

- Eight BRTA OCR documents remain deferred, retaining 1119 existing chunks.
- Four Passport and six BRTA original-file associations remain unresolved.
- Missing URLs and dated-document flags require review, not automatic deletion.
- Structural validation cannot establish semantic equivalence or rule currency.

### Why the candidates are still inactive

The saved five-case diagnostics show the following designated evidence in
selected generation context:

| Domain | Baseline | Final candidate |
| --- | ---: | ---: |
| Passport | 5/5 | 4/5 |
| BRTA | 3/5 | 3/5 |

These are historical development diagnostics, not newly executed results or
held-out accuracy estimates. They used predefined support hints and may not
cover all relevant evidence. The final release notes identify Passport fee
support moving from rank 2 to rank 6; BRTA still missed the designated
driving-test and lost-licence sources. The current applicability selector and
later changes require fresh matched testing before extrapolating these results.

Consequently, do not activate the full candidate merely because it contains
fewer chunks or passes structural checks.

## 4. Implementation order and acceptance gates

1. Add the candidate Birth Registration provenance register without changing
   active files. Resolve ambiguous original mappings before transcription.
2. Review one OCR document page by page and retain a source-linked change log.
3. Build a minimal heading-only exclusion candidate in a separate collection.
4. Compare baseline and candidate using identical models, retrieval settings,
   prompts, and questions. Include source-preservation and condition checks;
   use fresh held-out expert questions for improvement claims.
5. Record Hit@5, Precision@5, context judgments, answer support, actual token
   counts, and latency separately. Do not equate smaller input with better
   answers or faster end-to-end runtime.
6. Activate only after review and evaluation; retain the old config, chunks,
   and collection for rollback. Do not overwrite the thesis baseline.

The first implementation should be the provenance register and the small
heading-only experiment, not additional frameworks or broad corpus rewriting.

## References within the repository

- `scripts/audit_service_corpora.py`
- `domains/birth_death_registration/scripts/prepare_chunks.py`
- `docs/data_cleanup/2026_09_22_corpus_release/README.md`
- `docs/data_cleanup/2026_09_22_corpus_release/brta/manifest.json`
- `docs/data_cleanup/2026_09_22_corpus_release/passport/retrieval_diagnostics.json`
- `docs/data_cleanup/2026_09_22_corpus_release/brta/retrieval_diagnostics.json`
- `docs/birth_death_raw_data_audit.md` (historical; its runtime description is not assumed current)
