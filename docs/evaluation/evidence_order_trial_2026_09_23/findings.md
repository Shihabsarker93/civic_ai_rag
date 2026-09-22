# Findings: Qwen3 evidence distraction and order

Nine requests completed, three questions by three conditions, all finish reason
`stop`. No model/API failure. This report is an assistant's qualitative review
against frozen supplied passages, not independently verified government advice
or a held-out end-to-end accuracy measurement. Answers are preserved unedited.

## Results by condition

| Question | Relevant evidence only | Relevant block first + distractors | Distractor block first + relevant evidence |
| --- | --- | --- | --- |
| New passport documents | Application checklist, conditional requirements mostly preserved. Omits printed application form (item 6). Partial. | Still application checklist, same omission. No collection-content contamination observed. | Switches to collection checklist: delivery slip, child/representative collection requirements. Wrong action for the application question. |
| Passport fee | Eight supported regular/express amounts covering four page/validity categories. Omits all super-express options, domestic scope and VAT inclusion. Awkward wording and calls published fees averages. Partial. | Uses the 2012 MRP schedule without its date/product limitation, instead of the supplied domestic e-passport table. Adds a garbled unsupported statement about extra costs. Contaminated. | Presents historical MRP amounts as general fees and then only two e-passport examples. Does not preserve historical scope or complete e-passport conditions; confusing language. Contaminated. |
| Lost driving licence | Four supported duplicate-licence document requirements; ambiguous wording 'new licence'. Useful within that limited source, not a complete independently verified procedure. | Gives duplicate requirements, then appends an unrelated one-year restriction after licence cancellation. The cancellation condition is mentioned, but irrelevant to this lost-licence question and misleading in this answer. | Gives cancellation/reconsideration instructions instead of replacement. Also mangles the one-year restriction, apparently reversing its meaning. Wrong action and distorted condition. |

## Interpretation

1. Order matters for the passport-document pair: same two passage records,
   different order, application answer versus collection answer. BRTA also
   becomes substantially worse with the unrelated passage first.
2. Sorting the best passage first is not sufficient: the fee response uses an
   incompatible historical fee schedule despite four relevant chunks first;
   BRTA appends cancellation material despite its duplicate checklist first.
3. Selecting relevant evidence reduces these observed service/action mix-ups,
   but does not solve omissions, awkward Bangla or missing scope. The newly
   repeated fee control is less complete than the earlier unseeded trial.
4. This implicates context applicability and generation robustness together.
   It does not establish that embeddings, BM25, RRF or the reranker must be
   replaced. Production retrieval was not run here.

The original prompt explicitly says Source 1 is strongest. This test retains
that instruction, so it cannot separate prompt-induced preference from intrinsic
model positional sensitivity. The earlier neutral-prompt trial did not fix its
cases; that historical observation is not a paired neutral-prompt control for
these exact new context sets.

The fee question does not explicitly specify e-passport, domestic location,
pages, validity or delivery. Clarification or correctly scoped alternatives
would be acceptable. The error is not merely mentioning MRP: it is presenting
historical/different-service information without its required qualifications.

## Context and run checks

Both mixed-order conditions contain identical full chunk records, differing
only in block order. All nine calls use Qwen3 8B, thinking off, seed 42,
num_ctx 8192 and the same frozen decoding options. Fresh selected-only controls
are used because earlier trials had implicit seed/context settings.

Reported prompt lengths are below the configured context budget with the 1200
token generation allowance; none reached a length finish. Token counts are
recorded in results.json. This provides no indication of context-budget
exhaustion, not an independent tokenizer-level guarantee about server internals.
Do not treat source footers as actual claim-level citations: they list all
supplied passages, including distractors the model might or might not use.

## Important correction to prior interpretation

Not all original BRTA evidence was irrelevant. Chunk
`brta_4e08eb4e988d38e4_v2_0018` includes the duplicate-licence application,
GD requirement and a 30-day statement. The earlier receipt/30-day answer was
incomplete rather than necessarily unsupported by its context. Chunk `_0200`
also includes a relevant form fragment. Neither was used as a pure distractor.
Only the cancellation/reconsideration chunk `_0023` was added here.

The second original passport enrolment checklist is relevant as well. It was
not mislabeled as a distractor. Details and selection rationale are in README.md.

## Recommended next change, not implemented

Prototype a generic service/action/condition-aware evidence-selection step
after retrieval and before answer generation. It should retain complete
supporting requirements and fee categories while excluding incompatible actions
(application vs collection, lost vs cancelled) and flagging product/date/scope
ambiguity for clarification. Do not use exact-question answers or manually
selected IDs as a production rule. Selection itself must be evaluated because
incorrect filtering can remove useful evidence.

Compare that candidate against the preserved baseline on unseen paraphrases and
scenarios across all three domains, including ambiguous and multi-part requests.
Also measure completeness and Bangla quality; do not call an on-topic answer
automatically correct. Preserve the baseline and do not promote based on these
three known failures. A model change or source reorder alone is not demonstrated
to solve the system's problems.

## Preservation

Rollback tag: `codex/pre-evidence-order-20260923`.
The new script, exact prompts, source records, settings and model inventory are
saved in this experiment. Prior experiments and unrelated local work are intact.
No production source, configuration, dataset or index was modified. The live
chatbot was not restarted. No new recurring monitor was created.
