# Current 30-question retrieval-only run

Completed 30 questions across three domains in 16.1 seconds including encoder loading.
BM25-only, BGE-M3 dense-only and Hybrid RRF used the current domain indices. No generative LLM, judge, reranker, selector, or answer generation was called.

## Metric status
Hit@k, Precision@k, Recall@k, MRR and nDCG are NOT calculated: these questions lack complete verified relevance labels. Saved retrieved IDs are not ground truth. No machine-drafted labels were used.
This is a retrieval export for review, not an answer-accuracy benchmark or the full CivicRAG pipeline. Legacy P2 scores cannot be transferred to these questions.

| Domain | Questions | Methods | Status |
|---|---:|---:|---|
| passport | 10 | 3 | Rankings saved; relevance review pending |
| birth_death_registration | 10 | 3 | Rankings saved; relevance review pending |
| brta | 10 | 3 | Rankings saved; relevance review pending |
