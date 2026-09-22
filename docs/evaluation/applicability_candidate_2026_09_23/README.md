# Applicability-selection candidate: all three domains

Status: candidate for manual testing, not a validated accuracy improvement.
Rollback baseline tag: `codex/pre-applicability-selection-20260923`.

## What changed

The CivicRAG path for birth/death registration, passport and BRTA now shares:

Query -> existing domain retrieval (BGE-M3/Chroma + BM25/RRF) -> existing
reranker, keeping up to 15 candidates -> applicability screening -> related
section completion -> chosen LLM -> existing Bangla language check -> response.

`src/generation/evidence_selection.py` screens reusable action/service vocabulary
and explicit product/location mismatches. It does not contain question matches,
answer templates, selected source IDs or fee values. Specific actions supersede
generic 'application' words. Unknown queries retain retrieval ordering. With a
direct action match, unclassified action fragments may be excluded (fee sections
are retained for fee queries). This is heuristic filtering, not semantic proof.

Flagged historical alternatives are suppressed only when a plausible unflagged
alternative exists and history/MRP/year is not explicitly requested. Unflagged
does not mean independently verified or current. Original audit flags remain.

Up to six whole chunks and 14,000 source characters are supplied. Sibling fee
categories come only from the same retrieved document and parent section;
document-checklist continuation must have the same section heading. Original
source text is never rewritten. These bounds can omit evidence; the trace records
that and the prompt must not invent missing facts. A character budget is not an
exact token budget. The model context window is explicitly 8192 tokens.

The candidate does NOT run legacy domain-specific controlled-answer templates
or the raw extractive shortcut. This is deliberate: those routes could bypass
screening and would prevent a genuine generator comparison. Existing cross-domain
aggregate clarification remains. Simple RAG and rollback mode retain their old
paths. Controlled paths remain in source code, not deleted.

Only the candidate generation prompt removes Source-1 authority and the six-bullet
cap. It asks for service/action/date/location compatibility, full conditions and
clarification for missing constraints. No strict JSON answer schema or quote
validation gate is added. Old diagnostic scripts keep their legacy prompt default.
The Bangla language guard can still reject a model response; that route is labeled
`selected_evidence_language_rejection`, not counted as a correct answer.

Qwen3 is preselected in the browser; all four model choices remain. API callers
must explicitly select their comparison model (existing config defaults remain).

## Visibility and records

API returns `pipeline_variant=applicability_v1`, original retrieved `sources`,
exact `answer_contexts` and `evidence_selection` decisions. Candidate responses
also retain `raw_generation` for diagnosing language rejection. Source footers
list all selected inputs, not claim-level verified citations. Browser evidence
details expose included/excluded IDs and reasons; source links use selected inputs.

Implementation files: `src/generation/evidence_selection.py`, `src/pipeline.py`,
`src/generation/ollama_generator.py` and `app.py`.
Tests: `tests/test_evidence_selection.py`, plus the pre-existing regression suite.

`frozen_30q_selection.json` applies screening to the historical 30-question
retrieved contexts. It is NOT a new 30-question model run or an accuracy score.
`smoke.json`/`smoke.md` contain three live Qwen3 known-case functional checks,
not a held-out benchmark. No 30-question generation batch has been started.

## Limitations and next evaluation

These action/service dictionaries cannot perfectly interpret every paraphrase,
negation or long scenario. They may remove useful passages or retain mixed-topic
ones, especially when broad legal sections contain multiple actions. Missing
evidence cannot be recovered unless retrieval or bounded sibling expansion finds
it. Do not infer 90-95% correctness from unit tests or known-case smoke answers.
No dataset, index, embedding model, RRF weights or model weights were changed.

Test unseen direct, paraphrased, scenario, ambiguous and multi-condition questions
in each domain. Review actual applicability, completeness and Bangla quality,
not only whether an answer appeared. Keep domain selection explicit. For model
comparison, choose Qwen3 8B and either Llama3 (continuity with prior comparisons)
or Qwen2.5 7B; no claim is made that the second Qwen is superior without testing.

## Reversible operation

Set `CIVIC_EVIDENCE_SELECTION=0` when restarting `app.py` to restore the old CivicRAG
answer routes and legacy prompt; set it to `1` for this candidate. Do not reset the
worktree or delete results. The Git tag preserves the complete prior tracked
version. Runtime source changes require a server restart; `/health` reports the
loaded variant. No recurring monitoring automation was created.
