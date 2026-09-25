# Simple RAG versus CivicRAG: saved Qwen3 answers

Same 30 questions and existing saved answers. No answer regeneration. No external-paper benchmark comparison.

Judge metric attempts: 180/180. Status: complete.

## Descriptive results for all 30 answers per system

| Measure | Simple RAG | CivicRAG |
|---|---:|---:|
| Completed requests (not correct answers) | 30.000 | 30.000 |
| Mean saved generation latency (seconds) | 193.699 | 181.823 |
| Median saved generation latency (seconds) | 181.060 | 161.845 |
| 95th percentile saved latency (seconds) | 319.910 | 285.100 |
| Mean supplied passages | 6.000 | 4.900 |
| Mean supplied context characters | 5218.900 | 3948.033 |
| Mean Bangla-letter fraction (not fluency) | 0.935 | 0.933 |

Saved latency comes from separate runs, not a controlled hardware speed experiment.

## RAGAS comparison

| Metric | Simple mean (valid/30) | Civic mean (valid/30) | Paired Civic minus Simple |
|---|---:|---:|---:|
| faithfulness | 0.7983 (30/30; failed 0) | 0.7323 (30/30; failed 0) | -0.0660 (n=30) |
| answer_relevancy | 0.8460 (30/30; failed 0) | 0.8375 (30/30; failed 0) | -0.0085 (n=30) |
| context_relevance_binary | 0.9333 (30/30; failed 0) | 0.9667 (30/30; failed 0) | 0.0333 (n=30) |

Paired descriptive bootstrap intervals are retained in ragas_summary.json. Missing judgments are excluded, not treated as zero.

## Interpretation limits

- Qwen3:8b is both generator and evaluator: these are exploratory self-judge scores, not independent factual accuracy.
- Faithfulness measures support by supplied text, not whether a government rule is current or applicable.
- Response relevance is not gold-answer correctness.
- context_relevance_binary is a custom RAGAS AspectCritic, not standard context precision or recall.
- The 30 questions were reused during development; these results are not held-out generalization estimates.
- No correctness percentage, MRR, nDCG or reference-answer similarity is invented without reviewed labels.
- Full question-level scores and errors are in ragas_scores.json; original answer paths and hashes are in manifest.json.
