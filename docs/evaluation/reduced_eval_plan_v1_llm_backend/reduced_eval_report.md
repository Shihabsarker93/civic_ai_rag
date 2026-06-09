# Reduced CivicRAG Evaluation Plan Results

Generated: 2026-06-10T04:49:03
Evaluation file: `/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/domains/birth_death_registration/data/evaluation/mixed_paraphrase_eval_flat_v1.json`

This report intentionally limits the experiment scope to parameter choices that are defensible and doable for the current thesis phase.

## Experiment A: Retrieval Variant Comparison

| Variant | Hit@1 | Hit@3 | Hit@5 | MRR | nDCG@5 | Context Precision@5 |
|---|---:|---:|---:|---:|---:|---:|
| bm25_only | 0.5345 | 0.6897 | 0.7586 | 0.6132 | 0.6112 | 0.1793 |
| dense_only | 0.7931 | 0.9828 | 0.9828 | 0.8707 | 0.8693 | 0.2483 |
| hybrid_rrf | 0.7414 | 0.8793 | 0.9483 | 0.8193 | 0.8108 | 0.2414 |

## Experiment B: RRF Weight Sensitivity

| RRF Config | Hit@1 | Hit@3 | Hit@5 | MRR | nDCG@5 | Context Precision@5 |
|---|---:|---:|---:|---:|---:|---:|
| balanced_0.50_0.50 | 0.7414 | 0.8793 | 0.9310 | 0.8149 | 0.8037 | 0.2379 |
| current_dense_0.55_bm25_0.45 | 0.7414 | 0.8793 | 0.9483 | 0.8193 | 0.8108 | 0.2414 |
| dense_0.60_bm25_0.40 | 0.7414 | 0.8793 | 0.9483 | 0.8201 | 0.8116 | 0.2414 |
| dense_0.80_bm25_0.20 | 0.7241 | 0.9310 | 0.9483 | 0.8204 | 0.8232 | 0.2448 |

## Experiment C: Generation Context k Coverage

This is retrieval-side coverage for how often the expected source would be available if the generator receives the top-k retrieved chunks.

| k | Expected Source In Context | Context Precision@k |
|---:|---:|---:|
| 1 | 0.7414 | 0.7414 |
| 2 | 0.8448 | 0.4914 |
| 3 | 0.8793 | 0.3621 |
| 4 | 0.8966 | 0.2802 |
| 5 | 0.9483 | 0.2414 |
| 6 | 0.9483 | 0.2069 |
| 7 | 0.9483 | 0.1798 |
| 8 | 0.9828 | 0.1616 |

## Experiment E: LLM Backend Comparison

Subset question IDs: `para_lost_certificate_01_v02, para_application_process_01_v01, para_birth_date_correction_fee_01_v01, para_single_parent_divorce_01_v01`

| Model | Semantic Correctness | Token F1 | Answer Relevance | Faithfulness Proxy | Source Retrieved | Mean Latency |
|---|---:|---:|---:|---:|---:|---:|
| llama3 | 0.8859 | 0.4820 | 0.7077 | 0.8742 | 1.0000 | 18.09s |
| llama3.2 | 0.8859 | 0.4820 | 0.7077 | 0.8742 | 1.0000 | 13.44s |
| qwen2.5:7b | 0.8859 | 0.4820 | 0.7077 | 0.8742 | 1.0000 | 23.38s |

## Manual Review Still Required

Automatic semantic metrics are useful for filtering, but Bangla government-service correctness still needs human inspection. Use `manual_review_template.csv` to score faithfulness, correctness, completeness, and language quality from 0-2.

## Interpretation Rule

Use retrieval-only metrics to justify evidence selection hyperparameters. Use actual-generation metrics only after retrieval is stable, because bad final answers can come from either bad evidence ranking or LLM behavior.
