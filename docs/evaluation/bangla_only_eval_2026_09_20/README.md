# Bangla-Only Q/A Evaluation

## Scope and Protocol

This evaluation reflects the proposed production scope: Bangla direct, paraphrased, and scenario-based questions within a user-selected civic-service domain. It excludes Banglish/code-mixed and cross-domain questions.

- Questions: 27 total, with 9 each for birth/death registration, BRTA, and passport.
- Forms: 9 direct, 9 paraphrased, and 9 scenario-based Bangla questions.
- Retrieval: unchanged CivicRAG pipeline and selected-domain corpus.
- Output policy: Bangla-only guard. Unsafe generated output is replaced with Bangla evidence fallback when possible, otherwise a Bangla-safe message.
- Backends: `llama3`, `llama3.2`, and `qwen2.5:7b` using the identical input and application settings.
- Diagnostic: `expected_evidence_present` checks for a predefined source hint after retrieval; it is not an automatic answer-correctness score.

## Results

| Metric | Llama 3 | Llama 3.2 | Qwen 2.5:7B |
|---|---:|---:|---:|
| Expected evidence present | 25/27 (92.6%) | 25/27 (92.6%) | 25/27 (92.6%) |
| Controlled birth-domain answers | 7 | 7 | 7 |
| Direct LLM answers | 12 | 19 | 14 |
| LLM then Bangla evidence fallback | 8 | 1 | 6 |
| Mean answer time | 86.76 s | 54.17 s | 83.10 s |
| Total batch time | 2342.5 s | 1462.7 s | 2243.8 s |
| Chinese/Japanese/Korean output exposed | 0 | 0 | 0 |

Both runs missed the same expected evidence for `brta_age_scenario` and `passport_collect_direct`. Because retrieval happens before LLM generation, these are retrieval/chunk/query-alignment issues, not evidence that one generator is worse than the other.

## Decision

Use **Llama 3.2** as the current deployment and demonstration backend. All three models retrieved the same evidence, but Llama 3.2 required substantially fewer language-safety fallbacks and was about 35--38% faster than the other two models on this local hardware. The Bangla-only guard prevented unsafe multilingual output from reaching the user in every run.

## Files

- `questions.json`: shared fixed Bangla-only evaluation questions.
- `answers_llama3.json` and `answers_llama3.md`: Llama 3 raw and readable answers.
- `answers_llama3_2.json` and `answers_llama3_2.md`: Llama 3.2 raw and readable answers.
- `answers_qwen2_5_7b.json` and `answers_qwen2_5_7b.md`: Qwen 2.5:7B raw and readable answers.
