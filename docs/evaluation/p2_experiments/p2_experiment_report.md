# P2 Experiment Report

Evaluation set: `/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/domains/birth_death_registration/data/evaluation/p2_20q_eval_set.json`

Fallback checkpoint before this evaluation framework: `01c663e`

Reranking mode for this run: `lexical fallback / fast mode`

## Experiment 1: Retrieval Variant Comparison

| Variant | Recall@1 | Recall@3 | Recall@5 | Context Precision@5 | MRR | nDCG@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| bm25_only | 0.450 | 0.550 | 0.800 | 0.220 | 0.546 | 0.481 |
| dense_only | 0.800 | 0.900 | 0.900 | 0.310 | 0.842 | 0.731 |
| hybrid_rrf | 0.700 | 0.800 | 0.850 | 0.300 | 0.752 | 0.661 |
| hybrid_rrf_rerank | 0.650 | 0.800 | 0.850 | 0.290 | 0.738 | 0.664 |

## Experiment 5: Parameter Sensitivity

| Config | Recall@1 | Recall@3 | Recall@5 | Context Precision@5 | MRR | nDCG@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| balanced_current | 0.650 | 0.800 | 0.850 | 0.290 | 0.738 | 0.664 |
| bm25_heavy | 0.650 | 0.800 | 0.800 | 0.300 | 0.717 | 0.642 |
| dense_heavy | 0.650 | 0.800 | 0.850 | 0.290 | 0.735 | 0.663 |
| large_topk | 0.650 | 0.800 | 0.800 | 0.290 | 0.717 | 0.658 |
| small_topk | 0.650 | 0.850 | 0.850 | 0.290 | 0.742 | 0.663 |

## Notes for Thesis Interpretation

- `Recall@k`, `MRR`, `nDCG@5`, and `Context Precision@5` evaluate retrieval before generation.
- The generation metrics are automatic proxy metrics; they should be paired with manual qualitative review for Bangla government-service correctness.
- The faithfulness metric here is a context-similarity proxy, not a full RAGAS LLM judge.
- Empty or timed-out generated answers are scored as `0.0` for generation metrics and the error is stored in `generation_rows.csv`.
- Exact repeated answers are not automatically bad for civic QA; stable grounded answers indicate reproducibility.
- Out-of-context questions are included to test refusal behavior, but retrieval metrics for empty expected-source cases should be interpreted separately.
- Use `manual_review_template.csv` to record human scores for scenario-based Bangla questions.