# Implementation verification and known limitations

## Verification

- 60 unit/regression tests passed after the checklist and truncation fixes.
- Frozen historical 30-question screening retained at least one passage for all
  30. This does not establish relevance or correctness. No 30-question model batch
  was run and no model-to-model comparison was run on this candidate.
- The first running candidate completed three real HTTP requests with Qwen3,
  including retrieval, reranking, screening and generation. These are saved in
  `smoke.json` and `smoke.md`, including the deficient outputs.
- Final code was restarted after refinements. A fresh passport check is saved
  separately under `followup/`. It uses exactly one selected checklist and ends
  with `done_reason=stop`, not a length stop.
- `/health` reports `applicability_v1`. Browser selects Qwen3 initially and exposes
  selection decisions. Other model options remain available.

## Observed answers, not a success score

The initial passport request combined overlapping checklists, repeated items and
ended mid-word. That observation led to one-checklist-family selection, heading-only
exclusion and explicit length-stop reporting. The initial artifacts predate those
refinements and the final raw-generation/metadata fields; do not present them as
outputs of the final exact revision. The local-heading fix was also made during
this development interval without changing the already-running server mid-request.

The final passport follow-up included all seven selected checklist items and no
collection checklist. However, it renders the offline-payment condition as
`অফলাইন ভুট্টা ক্ষেত্রে`, which is wrong/garbled Bangla. This is a remaining
generation-quality failure despite the correct selected evidence. No phrase-wise
replacement or rewritten answer was applied to conceal it.

The initial BRTA answer is about duplicate/replacement guidance rather than
cancellation. It mentions Form-4(kha), GD, licensing authority and a 30-day period
from the supplied legal material. It is not a complete verified current procedure
and should preserve all fee/timing conditions more clearly.

The initial birth-registration answer gives a short application outline but adds
an unasked twins scenario. It is incomplete and includes distracting special-case
material. Selection is not a complete solution to all-domain reliability.

Only the passport known case was rerun after the final refinements. BRTA and
birth/death final-version behavior still needs new manual questions or a frozen
comparison run. No 90-95% accuracy claim is warranted.

## Ready for manual candidate testing, not final promotion

Use CivicRAG mode with Qwen3 8B first. Review the exact selected chunk IDs and
conditions, not just the answer's fluency. For a controlled comparison, use the
same question set and candidate revision with explicitly selected models.
Qwen3 versus Llama3 preserves continuity with previous comparisons; Qwen2.5 7B
is also installed but has not been validated on this candidate.

The shared candidate deliberately bypasses legacy controlled answer templates.
All three domains therefore exercise the selected LLM and can be slower than
previous controlled responses. This is an architecture/route change, not only
a prompt edit. Embeddings, index contents, BM25/RRF and reranker weights remain.

Known risks include heuristic false exclusions, retained mixed-action text,
omission of complementary checklists, source-age uncertainty, imperfect Bangla,
incomplete answers and slow local inference. Alternative excluded checklists are
retained in the candidate trace rather than deleted from the data.

Rollback: restart with `CIVIC_EVIDENCE_SELECTION=0` to use the old answer paths.
Tag `codex/pre-applicability-selection-20260923` preserves the tracked pre-change
version. No original input files or databases were overwritten. Every new
evaluation output from this change, including failures, is retained in Git.
