# Six-Question Local Model Comparison

## Setup

The same six questions, domain selections, `civic` method, retrieved corpus, and retrieval configuration were used with `llama3.2`, `llama3`, and `qwen2.5:7b`. This is a small manual diagnostic, not a statistically conclusive model benchmark.

## Evidence Retrieval

All three runs produced the same expected-evidence pattern: four of six questions contained the expected evidence hint and two did not.

| Question | Llama 3.2 | Llama 3 | Qwen 2.5:7B |
|---|---|---|---|
| Birth deadline, direct | found | found | found |
| Birth deadline, code-mixed | missed | missed | missed |
| BRTA professional-license age | found | found | found |
| BRTA vehicle-colour change, code-mixed | found | found | found |
| Passport collection, direct | missed | missed | missed |
| Passport password recovery | found | found | found |

This isolates the two misses as retrieval/query-normalization problems, rather than generator-model differences. The current pipeline retrieves before model generation, so replacing the LLM cannot recover an absent source chunk reliably.

## Answer-Level Observation

- All three models gave the supported key facts for the direct birth deadline (45 days), BRTA professional-license age (21 years), and password recovery (`Forgot password`).
- For both retrieval-miss questions, generated text was unreliable or off-topic. This is expected RAG behavior when relevant evidence is absent and confirms that source evidence must be examined alongside answer fluency.
- Qwen 2.5:7B was slowest in this sample, especially the BRTA colour-change and passport-collection prompts. Timing is hardware-dependent and should not be treated as a general model-speed ranking.

## Files

- `questions.json`: shared fixed input.
- `answers_llama3.json`, `answers_qwen2_5_7b.json`: raw answer records.
- The matching Llama 3.2 records are in the 45-question audit at `../variant_family_audit_2026_09_20/answers_llama3_2.json`.

