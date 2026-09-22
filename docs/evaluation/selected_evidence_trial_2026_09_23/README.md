# Selected-evidence diagnostic

Baseline: `5a444fa0bccc25ce6bed0f376a7445cd809e951d`.
Production code, prompts, data, index and configs are unchanged.

## Purpose

Three known failures, two models (Qwen3 8B and Llama3), six calls.
Supply inspected relevant corpus passages directly to the existing generation
prompt. This deliberately bypasses retrieval, controlled routes and language
fallback to expose raw generator behavior. It is not the full CivicRAG pipeline
and cannot establish deployment accuracy or a model ranking.

The original Bangla questions are unchanged. Passage bodies are checked against
saved Markdown snapshots after canonical Unicode normalization and removal of
existing `[cite: ...]` artifacts for comparison only. Prompt text is unchanged.
This verifies provenance and relevance, not
current legal correctness or fidelity to the original PDF. Source audit flags
are retained. The broad passport questions remain ambiguous; domestic e-passport
answers must state their scope or ask clarification. The BRTA passage supports
requirements, not a full procedural timeline.

Fee input includes all four relevant category chunks, unlike production's
top-three selection. This is an intentional evidence-sufficiency intervention.
Do not attribute any improvement solely to rank. The earlier Qwen baseline is
historical, not a paired simultaneous control; there is no equivalent prior
Llama3 source-preference trial. Outputs vary and six calls are diagnostic only.

## Preserved records

- `plan.json`: exact prompts, complete chunks, source hashes, model digests and settings.
- `results.json`: raw responses and Ollama metadata, saved after every call.
- `results.md`: readable answers, not automatically scored as correct.
- `run.log`: progress or exact failure. No silent restarts.
- The previous source-preference trial is preserved in its original directory.

Run using `.venv/bin/python scripts/test_selected_evidence.py --prepare`, then
`.venv/bin/python scripts/test_selected_evidence.py`. Existing completed jobs
are skipped; the frozen plan is not regenerated during execution.

## Remembered literature and next decision

- NextRAG inspired the existing BGE-M3/Chroma, BM25, fusion and reranking stack.
  It additionally uses Dirichlet query-likelihood retrieval; do not add it blindly.
- TraSe compared automatic contexts with human-selected contexts. This inspires
  this diagnostic only; we are not implementing its translation/answer-selection stack.
- HybridRAG-BN suggests preserving surrounding context and separate verification.
  Its fine-tuned verifier, score fusion and external search are not implemented here.

If selected relevant evidence still fails, investigate generation. If it works,
test distraction using the same evidence plus unrelated passages before changing
retrieval. If relevant evidence is absent from the production prompt, investigate
retrieval/context selection. Never call these selected cases a held-out benchmark.

No architecture change is approved by a single successful output. Preserve this
baseline and compare any later candidate before promotion. Unrelated untracked
cleanup drafts and literature PDFs are left intact, not indiscriminately committed.
