# Qwen3 and Llama3: 30-question Bangla comparison

## Scope

This run used the 30 direct Bangla questions supplied for Passport, Birth and Death Registration, and BRTA. Each model was run through the same current CivicRAG pipeline with the intended domain selected for every question. The raw question-by-question answers, retrieved sources, routes, and timings are stored in the adjacent JSON and Markdown files.

This is an execution and qualitative-review artifact, not an answer-correctness score. A route such as `controlled` or `llm_then_evidence_fallback` shows how the system produced an answer; it does not prove that the answer is correct. Source relevance and answer faithfulness still require manual review or a separately curated reference-answer evaluation.

## Completion

| Model | Completed questions | Total time | Mean time per question |
|---|---:|---:|---:|
| `qwen3:8b` | 30 / 30 | 3408.45 s | 113.61 s |
| `llama3` | 30 / 30 | 2013.50 s | 67.12 s |

## Observable answer routes

| Model | LLM | Controlled evidence | LLM then evidence fallback |
|---|---:|---:|---:|
| `qwen3:8b` | 22 | 8 | 0 |
| `llama3` | 10 | 8 | 12 |

The eight controlled answers occur in the birth-registration questions where the evidence-first path recognized a supported civic-service pattern. For Passport and BRTA, both models relied mainly on LLM generation or, for Llama3, the evidence fallback.

## Timing by domain

| Model | Passport mean | Birth and death mean | BRTA mean |
|---|---:|---:|---:|
| `qwen3:8b` | 122.34 s | 41.02 s | 177.49 s |
| `llama3` | 83.38 s | 36.01 s | 81.96 s |

## Interpretation and next review

- Both requested runs completed without a request failure.
- Llama3 was materially faster on this local hardware and used the evidence fallback more often.
- Qwen3 was substantially slower, especially for BRTA questions; the raw outputs should be read before deciding whether its generated Bangla is worth that latency.
- Neither route counts nor latency establish which model is more factually correct. The next evaluation step is to manually label each answer for correctness, completeness, and grounding against the cited source, then use that labelled set for quantitative generation evaluation.

## Raw artifacts

- [Qwen3 raw answers](answers_qwen3_8b.md)
- [Llama3 raw answers](answers_llama3.md)
- [Questions](questions.json)
