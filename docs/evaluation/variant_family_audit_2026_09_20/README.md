# Grouped Question-Family Audit

## Purpose

This manual robustness audit checks whether CivicRAG retrieves the intended supplied-source evidence when the same service intent is expressed in different ways. It is not a legal-accuracy benchmark: the results show grounding against the project corpus, whose policy content still requires source maintenance and human review.

## Protocol

- Domains: birth/death registration, BRTA, and passport.
- Per domain: three core intent families, each expressed as a direct question, Bangla paraphrase, scenario, and Banglish/code-mixed question; two multi-condition questions; and one out-of-domain boundary question.
- Total: 45 questions.
- Backend held fixed: `llama3.2`.
- Method: `civic` (the normal deployed CivicRAG path).
- Evidence diagnostic: `expected_evidence_present` is true only when a predeclared source hint appears in the returned sources. It is not an automatic answer-correctness metric.
- Boundary questions have no expected source hint and are intentionally unscored.

## Results

| Domain | Scorable questions | Expected evidence present | Result |
|---|---:|---:|---:|
| Birth/death registration | 14 | 13 | 92.9% |
| BRTA | 14 | 12 | 85.7% |
| Passport | 14 | 13 | 92.9% |
| Total | 42 | 38 | 90.5% |

Birth/death used nine controlled answers and six LLM-grounded answers. BRTA and Passport used the LLM-grounded route for all 15 questions each because their birth-specific controlled templates do not apply.

## Retrieval Cases Requiring Review

- `birth_deadline_code_mixed`: the Banglish/code-mixed wording did not contain the expected birth-deadline evidence.
- `brta_age_scenario` and `brta_age_code_mixed`: the scenario and code-mixed forms did not contain the expected professional-license-age evidence.
- `passport_collect_direct`: the direct collection question did not contain the expected passport-collection evidence, although its three alternative forms did.

These are candidate follow-up improvements for query normalization, aliases, or source/chunk wording. They must be manually checked in `answers_llama3_2.md` before changing the production pipeline.

## Files

- `questions.json`: question set and expected evidence hints.
- `answers_llama3_2.json`: structured raw chatbot responses, source lists, routes, and elapsed time.
- `answers_llama3_2.md`: readable version of every answer.

