# Findings: manually selected evidence, two models

All six requests completed with Ollama `done_reason=stop`. No API failures.
This is an assistant's qualitative review against the supplied corpus passages,
not an independent correctness assessment, current-government-rule verification,
held-out benchmark or deployment accuracy estimate. The raw artifacts retain
their original pending-review label; this separate report provides the review.

## Question-by-question assessment

| Question | Qwen3 8B | Llama3 |
| --- | --- | --- |
| New passport documents | Relevant application checklist rather than collection checklist. Omits the separate printed application form (source item 6). Conditional old-passport, offline-payment and GO/NOC details mostly preserved. Partial, not fully complete. | Relevant but omits application form and conditional correction documents; drops appointment and NID/BRC detail and adds English prose. Partial and violates the requested Bangla-only presentation. |
| Passport fees | All twelve amounts and page/validity/delivery combinations agree with the four supplied domestic fee chunks. However, omits domestic scope and VAT-included status, calls published amounts averages and repeatedly uses unnatural `আমলাতন্ত্র ফি ঘটে টক`. Numerically much improved, not a polished complete answer. | Gives only one category's regular-to-super-express range, labels it approximate, omits VAT/location scope and adds a long English translation. The two amounts are supported, but the answer is incomplete and mixed-language. |
| Lost driving licence | Gives the four supported duplicate-licence document requirements without inventing an exact fee or processing time. Substantially usable within this limited evidence; should explicitly say duplicate/replacement rather than ambiguous new licence. The passage itself does not cover the whole procedure. | Says `আপনাকে অবশ্যই উকিল করতে হবে` and adds an English note. The supplied passage does not require a lawyer. Unsupported generation failure despite relevant evidence. |

## What changed compared with the previous Qwen trial

Only supplied evidence changed; the production prompt and decoding settings were
kept. Earlier passport-document responses copied collection requirements. The
application checklist was already present as source 2 in that earlier context:
retrieval did not entirely miss the useful passage. Removing the distractor let
Qwen use it, although this historical, single-run comparison is not a controlled
repeat proving causation.

The earlier fee response used another service's fee. The selected context now
contains all four domestic e-passport categories, not the unrelated service and
old MRP material. Therefore both relevance and coverage changed. This cannot
isolate ranking from evidence completeness or be called an RRF improvement.

The earlier lost-licence response supplied a generic receipt/timeline. The new
Qwen response uses the duplicate-licence requirements. The production retrieval
and context-selection stages were bypassed; they have not been fixed by this test.

There was no corresponding Llama3 run in the previous source-preference trial,
so do not describe its current outputs as a measured before/after improvement.

## Decision

1. Keep the current production baseline unchanged. No experimental prompt,
   retriever, index, controlled route or model-default change is promoted.
2. Qwen3 is the more promising of these two generators on these three selected
   failures, but neither demonstrates 90-95% accuracy. Llama3 is not reliable
   merely because it is larger than Llama3.2. No Llama3.2 comparison was run here.
3. Next diagnostic, if approved: use the same selected evidence with and without
   the original distractors and swap order while holding prompt/model/settings
   fixed. This separates source distraction from missing coverage more cleanly.
4. Then consider service/action-aware evidence selection across domains, not
   question-specific answers. Keep complete fee conditions and required-document
   lists; examine the six-bullet instruction (seven document items here).
5. Preserve Bangla quality and unsupported-claim failures as generation problems,
   not merely retrieval problems. No model or prompt is guaranteed to solve them.

## Reproducibility and rollback

The frozen plan includes exact prompts, full context records, active chunk hashes,
snapshot hashes, model inventory/digests and generation settings. Body checks
allow only canonical Unicode equivalence and removal of pre-existing citation
artifacts in the comparison. Original source files are untouched.

Qwen3 reasoning is off as in the earlier trial; Llama3 receives no thinking flag.
Models ran sequentially on the local Ollama server. Sources displayed below
answers are supplied-context IDs, not independently validated citations.

Baseline tag: `codex/pre-selected-evidence-20260923`, pointing to
`5a444fa0bccc25ce6bed0f376a7445cd809e951d`. The live server was not restarted.
The diagnostic scripts never load or mutate ChromaDB. All results are generated
outputs, not rewritten expected answers. Unrelated local files remain untouched.
