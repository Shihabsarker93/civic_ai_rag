# Current retriever: P2-style labelled evaluation

Completed 58 legacy questions in 32.2 seconds (including model loading).
No answer generation, LLM judging, reranking, boosts, or evidence selection. BGE-M3 is used only as an embedding encoder.

| Method | Hit@1 | Hit@5 | Precision@5 | Label Recall@5 | MRR@5 | nDCG@5 |
|---|---:|---:|---:|---:|---:|---:|
| bm25_only | 0.5345 | 0.7586 | 0.1793 | 0.6839 | 0.6132 | 0.6112 |
| dense_only | 0.7931 | 0.9828 | 0.2483 | 0.9411 | 0.8707 | 0.8693 |
| hybrid_rrf | 0.7414 | 0.9483 | 0.2414 | 0.9066 | 0.8193 | 0.8108 |

## Scope and limitations
- Uses the existing 58-question P2 birth-registration set (19 paraphrase groups), not the newer 30-question three-domain set. No passport or BRTA conclusions are supported.
- All expected IDs exist in the current 187-chunk corpus and Chroma IDs match the corpus. This checks ID compatibility, not a fresh expert audit or embedding reconstruction.
- Relevance is defined by the pre-existing expected_source_ids, not newly judged relevance. Other valid passages can be unlabelled; recall is relative to these labels, not all possible relevant corpus passages.
- Questions are reused development questions, not an independent held-out benchmark. Paraphrases within groups are correlated.
- Precision@5 uses denominator 5; label recall uses the number of labelled relevant IDs. Hit@5 is not recall when multiple IDs are relevant. nDCG uses binary labels; MRR is truncated at 5.
- Component rankings are top-20 searches sliced at 5, and the same rankings feed production weighted RRF (k=50, dense=0.55, BM25=0.45). Approximate dense search can differ from requesting only five directly.
- These are retrieval scores, not answer correctness or a full Simple RAG versus CivicRAG comparison.
