# Evidence-contract reliability update

## Status and comparison

This is a bounded answer-routing experiment, not a measured accuracy improvement.
Rollback reference: `codex/pre-reliability-gate-20260922`.
The unchanged questions and previous answers are in
`docs/evaluation/user_30q_model_comparison_2026_09_22/`.
New raw results are written incrementally to `answers_qwen3_8b.json` and `.md` here.
A partial file must not be reported as a completed 30-question evaluation.

## Changes

- `generation.evidence_contract=true` activates one shared CivicRAG answer route
  for Birth/Death, Passport and BRTA. Other retrieval methods retain their prior route.
- Existing unchecked controlled handlers are bypassed in this mode, including the
  narrow passport fee/location handler. They remain available for rollback.
- Retrieval, embedding, fusion, reranking, source files and active collections are
  unchanged. Up to six returned chunks reach generation rather than the former
  top-three/dominant-top-one shortcut. Birth-specific post-retrieval augmentation
  and procedure expansion are not used in this route.
- Qwen3:8b is the provisional UI/API/config default; other models remain selectable.
  Temperature remains 0.05 and Qwen3 reasoning remains disabled.
- One structured LLM call uses separate system/user messages. It chooses answer,
  partial answer, clarification or abstention after assessing service, action,
  audience, dates and conditions. It supplies source quotes per answer item.
- Local validation rejects malformed JSON, unknown source IDs, quotes absent from
  source content, unsupported numeric values and major language violations.
- Displayed citations come from validated model-selected supports, not the first
  three candidate IDs. All candidates remain in the debugging output. Full model
  output and checked supports are retained under `evidence_check` in the JSON.
- No second model/verifier, index rebuild or question-specific answer patch was added.
- The structured route explicitly requests a 16,384-token window rather than the
  observed 4,096-token runtime default. A conservative UTF-8 byte budget reserves
  room for instructions, schema and output, keeping complete chunks and recording
  any omitted IDs. This is intentionally conservative, not exact token accounting.

## Limits and tradeoffs

Exact quote presence does NOT establish that an answer follows from the quote.
The same model assesses applicability and composes the answer; it is not an
independent semantic judge. Numeric matching cannot detect wrong units, wrong
conditions or misapplied fees already present in the source. Language checks do
not prove grammatical quality. Sources are not independently verified as current.
Structured output can exhaust the existing token limit; malformed/truncated output
fails closed and is recorded, rather than returning a possibly unsupported answer.
Disabling controlled paths increases LLM usage and may increase latency. Keeping
six candidates can improve coverage but can also add noise. Both need measurement.

## Acceptance review

Review each answer against its quoted source and the full source conditions.
Record correct/partial/incorrect, wrong service or action, missing conditions,
unsupported claims, language quality, justified/unjustified abstention and latency.
Report answer coverage separately from correctness; refusals are not correct answers
to answerable questions. Treat these 30 previously seen questions as development
regressions. Obtain unseen questions from a teammate before reporting final accuracy.
No 90-95% accuracy claim is supported by the implementation or unit tests.

## Run / rollback

```sh
.venv/bin/python scripts/run_manual_audit.py --input docs/evaluation/user_30q_model_comparison_2026_09_22/questions.json --output docs/evaluation/reliability_gate_2026_09_22/answers_qwen3_8b.json --model qwen3:8b --resume
```

Set `generation.evidence_contract=false` in each active domain config and restart
the server to restore legacy routing without changing any source data. Set the
default model back separately if needed. The Git tag records the entire previous
tracked state; do not use destructive reset on a working tree with unrelated files.

Automated verification: 53 tests passed on 2026-09-22, including 15 new contract,
message-role and all-domain routing tests. These are software tests, not model
accuracy measurements.
