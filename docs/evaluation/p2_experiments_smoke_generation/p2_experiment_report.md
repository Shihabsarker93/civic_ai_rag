# P2 Experiment Report

Evaluation set: `/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/domains/birth_death_registration/data/evaluation/p2_20q_eval_set.json`

Fallback checkpoint before this evaluation framework: `01c663e`

Reranking mode for this run: `lexical fallback / fast mode`

## Experiment 1: Retrieval Variant Comparison

| Variant | Recall@1 | Recall@3 | Recall@5 | Context Precision@5 | MRR | nDCG@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| bm25_only | 0.000 | 1.000 | 1.000 | 0.200 | 0.333 | 0.195 |
| dense_only | 0.000 | 1.000 | 1.000 | 0.400 | 0.333 | 0.346 |
| hybrid_rrf | 1.000 | 1.000 | 1.000 | 0.400 | 1.000 | 0.586 |
| hybrid_rrf_rerank | 1.000 | 1.000 | 1.000 | 0.400 | 1.000 | 0.541 |

## Experiment 5: Parameter Sensitivity

| Config | Recall@1 | Recall@3 | Recall@5 | Context Precision@5 | MRR | nDCG@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| balanced_current | 1.000 | 1.000 | 1.000 | 0.400 | 1.000 | 0.541 |
| bm25_heavy | 1.000 | 1.000 | 1.000 | 0.400 | 1.000 | 0.586 |
| dense_heavy | 1.000 | 1.000 | 1.000 | 0.400 | 1.000 | 0.541 |
| large_topk | 1.000 | 1.000 | 1.000 | 0.400 | 1.000 | 0.559 |
| small_topk | 1.000 | 1.000 | 1.000 | 0.200 | 1.000 | 0.390 |

## Experiments 2 and 3: Generation/System Comparison

| Method + Model | Semantic Correctness | Token F1 | Answer Relevance | Faithfulness Proxy | Source Retrieved | Source Cited |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| civic + llama3.2 | 0.852 | 0.158 | 0.726 | 0.809 | 1.000 | 1.000 |
| simple + llama3.2 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Experiment 4: Stability Test

| Method + Model | Exact Answer Match | Mean Pairwise Answer Similarity | Mean Source Jaccard |
| --- | ---: | ---: | ---: |
| civic + llama3.2 | 1.000 | 1.000 | 1.000 |

## Notes for Thesis Interpretation

- `Recall@k`, `MRR`, `nDCG@5`, and `Context Precision@5` evaluate retrieval before generation.
- The generation metrics are automatic proxy metrics; they should be paired with manual qualitative review for Bangla government-service correctness.
- The faithfulness metric here is a context-similarity proxy, not a full RAGAS LLM judge.
- Empty or timed-out generated answers are scored as `0.0` for generation metrics and the error is stored in `generation_rows.csv`.
- Exact repeated answers are not automatically bad for civic QA; stable grounded answers indicate reproducibility.
- Out-of-context questions are included to test refusal behavior, but retrieval metrics for empty expected-source cases should be interpreted separately.
- Use `manual_review_template.csv` to record human scores for scenario-based Bangla questions.