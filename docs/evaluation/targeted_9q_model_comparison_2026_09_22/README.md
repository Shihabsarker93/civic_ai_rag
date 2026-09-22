# Qwen3 and Llama3 targeted Bangla model comparison

## Scope

This run uses nine user-supplied Bangla questions through the local Civic.ai HTTP pipeline on 2026-09-22. Each request selects its specified domain, uses the active baseline index, hybrid retrieval and the existing reranker, then records the returned answer, answer route, sources and wall-clock time. Both models ran locally through Ollama on the same machine. No cloud model or ChatGPT answer was used.

The questions are saved in [questions.json](questions.json). The raw results are [Qwen3](answers_qwen3_8b.md) and [Llama3](answers_llama3.md), with equivalent machine-readable JSON files. These are inspection artifacts, not a labelled accuracy benchmark.

## Model and route summary

| Model | Questions | LLM answers | Controlled evidence answers | LLM language fallback | Total time | Mean time |
|---|---:|---:|---:|---:|---:|---:|
| `qwen3:8b` | 9 | 6 | 3 | 0 | 1,117.24 s | 124.14 s |
| `llama3:latest` | 9 | 5 | 3 | 1 | 607.32 s | 67.48 s |

The three Birth Registration questions used the existing controlled-evidence route for both models. Their answer text is expected to be the same because the generator is bypassed. They therefore do not demonstrate that one LLM is better than another.

| Domain | Qwen mean | Llama mean |
|---|---:|---:|
| Passport | 149.40 s | 75.96 s |
| Birth Registration | 26.23 s | 18.54 s |
| BRTA | 196.78 s | 107.94 s |

## What the raw outputs show

This run is diagnostic. It must not be presented as an accuracy score or proof that either model is correct.

- `passport_01_documents`: Qwen answered with delivery/collection material such as a delivery slip and authorization letter, not a reliable new-application document list. Llama failed the Bangla-language check and returned the pipeline's evidence fallback. This is primarily an evidence-selection problem, not a clean model win.
- `passport_02_fee`: both models produced different incomplete fee answers from a mixture of service sources. The returned source list contains Certificate of Identity, e-passport, and historical MRP material. Do not present either answer as the current universal passport fee.
- `passport_03_timeline`: both models supplied a delivery-time summary, but their wording differs. The response needs source/applicability review before being called current guidance.
- `brta_01_documents`, `brta_02_fee`, and `brta_03_learner`: both models generated Bangla answers, but the source documents contain conditions and categories. Their answers require evidence-level review; no broad correctness claim is made from this small unlabelled run.

## Interpretation

Llama3 was about 1.8x faster overall in this run, but speed does not make it safer. Qwen generated Bangla more consistently here, but it also exposed a severe wrong-intent result on the new-passport-documents question. The shared Passport fee failure appears upstream of model choice because both models received the same mixed retrieval context.

The immediate conclusion is that changing only the LLM cannot make the Passport and BRTA chatbot reliable. The next evidence-backed task is to improve retrieval/service applicability and then run a labelled, answer-by-answer evaluation. The live indexes were not changed by this comparison.
