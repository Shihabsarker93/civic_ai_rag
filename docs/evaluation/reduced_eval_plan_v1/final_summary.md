# Reduced Evaluation Plan: Final Summary

Date: 2026-06-10

Evaluation dataset: `domains/birth_death_registration/data/evaluation/mixed_paraphrase_eval_flat_v1.json`

Dataset size: 58 Bangla paraphrase questions across FAQ, fee rows, legal rules, correction process, application process, OCR notice, and general guidance.

## What We Evaluated

This evaluation intentionally avoids a huge grid search. It focuses on hyperparameters and design choices that are explainable for the thesis panel:

1. Retrieval variant: BM25-only vs Dense-only vs Hybrid RRF.
2. RRF weights: selected dense/BM25 weighting choices.
3. Generation context size: top-k coverage from k=1 to k=8.
4. Actual generation top-k: k=1 to k=5 on a small representative subset using `llama3.2`.
5. LLM backend comparison: `llama3.2`, `llama3`, and `qwen2.5:7b` on a small representative subset.

## Key Result 1: Dense Retrieval Is Currently Strongest

| Variant | Hit@1 | Hit@3 | Hit@5 | MRR | nDCG@5 |
|---|---:|---:|---:|---:|---:|
| BM25-only | 0.5345 | 0.6897 | 0.7586 | 0.6132 | 0.6112 |
| Dense-only | 0.7931 | 0.9828 | 0.9828 | 0.8707 | 0.8693 |
| Hybrid RRF | 0.7414 | 0.8793 | 0.9483 | 0.8193 | 0.8139 |

Interpretation: for Bangla paraphrased citizen queries, BGE-M3 dense retrieval currently handles semantic variation better than BM25 and the current hybrid setting. This does not mean hybrid is useless; it means our current hybrid weighting/fusion does not yet outperform dense retrieval on this dataset.

## Key Result 2: Current RRF Weight Is Defensible, But Dense-Heavy Is Worth Testing Later

| RRF Config | Hit@1 | Hit@3 | Hit@5 | MRR | nDCG@5 |
|---|---:|---:|---:|---:|---:|
| balanced 0.50/0.50 | 0.7414 | 0.8793 | 0.9310 | 0.8149 | 0.8068 |
| current 0.55/0.45 | 0.7414 | 0.8793 | 0.9483 | 0.8193 | 0.8139 |
| dense 0.60 / BM25 0.40 | 0.7414 | 0.8793 | 0.9483 | 0.8201 | 0.8147 |
| dense 0.80 / BM25 0.20 | 0.7241 | 0.9310 | 0.9483 | 0.8204 | 0.8232 |

Interpretation: current `0.55 dense / 0.45 BM25` is reasonable because it preserves Hit@5 = 0.9483. A more dense-heavy setting improves nDCG@5 slightly, but lowers Hit@1. For now, changing RRF weights is not urgent.

## Key Result 3: Generation Context k Has a Clear Coverage-Noise Tradeoff

| k | Expected Source In Context | Context Precision@k |
|---:|---:|---:|
| 1 | 0.7414 | 0.7414 |
| 2 | 0.8448 | 0.4914 |
| 3 | 0.8793 | 0.3621 |
| 4 | 0.8966 | 0.2802 |
| 5 | 0.9483 | 0.2448 |
| 6 | 0.9483 | 0.2069 |
| 7 | 0.9483 | 0.1798 |
| 8 | 0.9828 | 0.1616 |

Interpretation: `k=3` is more precise but misses more expected sources. `k=5` substantially improves expected-source coverage. `k=8` gives the best coverage but adds much more irrelevant context. A good next candidate default is therefore `top_k_for_generation=5`, but only after manual answer review confirms it does not make answers more verbose or confused.

## Key Result 4: Actual Generation Top-k Did Not Change Automatic Scores On The Small Subset

On 6 representative questions with `llama3.2`, automatic generation metrics were identical for k=1 to k=5:

| top_k_for_generation | Semantic Correctness | Token F1 | Faithfulness Proxy | Source Retrieved |
|---:|---:|---:|---:|---:|
| 1 | 0.8424 | 0.3329 | 0.8798 | 0.8333 |
| 2 | 0.8424 | 0.3329 | 0.8798 | 0.8333 |
| 3 | 0.8424 | 0.3329 | 0.8798 | 0.8333 |
| 4 | 0.8424 | 0.3329 | 0.8798 | 0.8333 |
| 5 | 0.8424 | 0.3329 | 0.8798 | 0.8333 |

Interpretation: in these selected cases, controlled CivicRAG safe-answer paths dominated, so changing generation top-k did not affect final answer text. This is not a failed experiment. It shows that for high-confidence civic intents, the system can bypass model improvisation and remain stable.

## Key Result 5: LLM Backend Scores Were Identical, But Latency Differed

On 4 representative questions:

| Model | Semantic Correctness | Faithfulness Proxy | Source Retrieved | Mean Latency |
|---|---:|---:|---:|---:|
| llama3.2 | 0.8859 | 0.8742 | 1.0000 | 13.44s |
| llama3 | 0.8859 | 0.8742 | 1.0000 | 18.09s |
| qwen2.5:7b | 0.8859 | 0.8742 | 1.0000 | 23.38s |

Interpretation: for this subset, answers were effectively model-independent because safe paths produced controlled answers. `llama3.2` is currently the best local backend for speed when safe paths are active.

## Current Defensible Defaults

Based on this reduced evaluation, the current defaults are defensible with caveats:

| Setting | Current Value | Evaluation-Based Position |
|---|---:|---|
| Embedding model | `BAAI/bge-m3` | Strong for Bangla paraphrase retrieval. |
| Retrieval design | Hybrid RRF + safe paths | Defensible, but dense-only is stronger in retrieval-only metrics. |
| RRF weights | dense 0.55 / BM25 0.45 | Reasonable; dense-heavy variants are worth future testing. |
| generation top-k | 3 | Safe and precise, but k=5 has better expected-source coverage. |
| local LLM | `llama3.2` default | Fastest among tested local models on the small subset. |
| temperature | 0.05 | Keep low for factual civic QA; not evaluated in this reduced run. |

## Manual Review Needed Before Changing Defaults

Do not change production defaults only from automatic metrics. The next necessary step is manual review of generated answers using:

`docs/evaluation/reduced_eval_plan_v1/manual_review_template.csv`

Suggested scoring:

- Faithfulness: 0/1/2
- Answer correctness: 0/1/2
- Completeness: 0/1/2
- Bangla language quality: 0/1/2
- Failure reason: wrong retrieval, bad ranking, LLM ignored evidence, too verbose, missing condition, language mismatch, expected-answer issue.

## Recommended Next Decision

For now, keep the current pipeline defaults unchanged. For thesis discussion, report that:

1. Dense retrieval is currently strongest for Bangla paraphrase matching.
2. Hybrid RRF remains useful as a comparative/proposed architecture but needs tuning.
3. k=5 improves evidence coverage, while k=3 is more conservative.
4. Safe-answer paths reduce LLM sensitivity and improve consistency for high-confidence government-service intents.
5. Manual answer review is required before changing `top_k_for_generation` from 3 to 5.
