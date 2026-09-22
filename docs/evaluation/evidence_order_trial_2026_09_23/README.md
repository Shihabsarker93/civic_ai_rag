# Frozen Qwen3 distraction/order experiment

The user approved testing the previously selected relevant evidence alongside
original distracting passages, reversing their order. No production code,
data, prompt, index, controlled route or model default is changed.

## Design fixed before outputs

For each of the same three Bangla questions, run Qwen3 8B with:

1. Selected relevant evidence only (fresh control).
2. The same relevant block, then distractors.
3. The exact same chunks as condition 2, distractor block first.

Nine calls total, one sample per condition. Keep relative order within each block.
Passage text and question text are unchanged. Source numbers necessarily change
with order; the production prompt still privileges Source 1. Thus order effects
include that instruction and are not isolated intrinsic positional bias.

Temperature, top_p, output budget and repetition settings match the prior trial.
For this new test, seed=42 and num_ctx=8192 are explicit for every condition.
Qwen3 thinking is off. Compare within this run, not as identical settings to
the earlier run whose seed/context were implicit. A fixed seed does not establish
robustness over repeated samples. More evidence also increases prompt length.

## Distractor selection rationale

- Passport documents: collection requirements, not application requirements.
  The other original enrolment checklist is relevant, so it is NOT a distractor.
- Passport fee: Certificate of Identity fees (different service) and historical
  2012 MRP fees (different product/date). The broad query is ambiguous: a model
  may clarify or explicitly distinguish dated MRP fees, but must not present
  them as current e-passport fees or mix COI charges into passport fees.
- Lost licence: cancellation, disqualification and reconsideration passage.
  Original BRTA chunk `_0018` actually includes replacement procedure, GD and
  a 30-day statement; `_0200` contains a partly relevant duplicate form fragment.
  Neither is treated as a wholly irrelevant distractor. Earlier descriptions of
  the original BRTA context as merely irrelevant/generic were too broad: its
  evidence had useful content but the answer omitted the actionable procedure.

## Review criteria

Assess correct service/action, supported facts, conditions, completeness, Bangla
quality and distractor contamination separately. For fees check all supplied
categories, scope and VAT; clarification is acceptable. For documents note the
seven-item source versus the unchanged six-bullet prompt. For BRTA distinguish
duplicate requirements from cancellation appeals. No automatic accuracy score.

This is a purposive, generation-only diagnosis, not a held-out end-to-end test.
Source text has not been verified as current government advice. No birth/death
question is included. Retrieval, safe paths and post-generation language fallback
are intentionally bypassed. Source footers are context inventories, not verified
claim-level citations. Do not promote changes from a single successful response.

## Artifacts and execution

`plan.json` freezes prompts, full context, source IDs, input hashes, settings and
model inventory. `results.json` preserves raw model responses and metadata after
each call; `results.md` is the readable view. `run.log` records progress. Errors
stop execution and are saved to `failure.json`; no silent restart or modification.
Run with `.venv/bin/python scripts/test_evidence_order.py --prepare` once, then
`.venv/bin/python scripts/test_evidence_order.py`. Completed pairs are skipped on
explicit rerun. Prior experiment folders are untouched.
