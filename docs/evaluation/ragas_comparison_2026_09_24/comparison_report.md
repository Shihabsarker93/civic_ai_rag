# Simple RAG versus CivicRAG: saved Qwen3 answers

Same 30 questions and existing saved answers. No answer regeneration. No external-paper benchmark comparison.

Judge metric attempts: 66/180. Status: incomplete.

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

Final full-set judge averages are withheld until the batch finishes. Partial scores are saved for recovery, not presented as final results.

## Interpretation limits

- Qwen3:8b is both generator and evaluator: these are exploratory self-judge scores, not independent factual accuracy.
- Faithfulness measures support by supplied text, not whether a government rule is current or applicable.
- Response relevance is not gold-answer correctness.
- context_relevance_binary is a custom RAGAS AspectCritic, not standard context precision or recall.
- The 30 questions were reused during development; these results are not held-out generalization estimates.
- No correctness percentage, MRR, nDCG or reference-answer similarity is invented without reviewed labels.
- Full question-level scores and errors are in ragas_scores.json; original answer paths and hashes are in manifest.json.
