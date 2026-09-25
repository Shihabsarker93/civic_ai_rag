# Provisional retrieval scores from assistant-reviewed labels

**NOT human-verified results. Do not describe these as a manual expert benchmark or answer accuracy.**

Reviewed 309 question/passage pairs across 30 questions and 192 unique passages. Label counts: {'relevant': 105, 'irrelevant': 199, 'uncertain': 5}.
Labels were authored by Codex in this conversation from saved passages. This is an unblinded single-AI review, not independent ground truth, and has not been validated against original government documents. No additional Ollama batch or external judge was called. The export/metric script itself uses only local validation and arithmetic; the annotation work was AI-assisted, not human or purely offline-script judging.

Questions with ANY uncertain label are excluded consistently for ALL methods. For otherwise complete pools with no relevant passage, Hit/Precision/MRR are zero; pooled Recall/nDCG are undefined and omitted, with their smaller denominator shown. No unknown label is silently treated as irrelevant.

| Domain | Method | Scored/total | Recall/nDCG N | Hit@1 | Hit@5 | Precision@5 | Pooled Recall@5 | MRR@5 | Pooled nDCG@5 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| passport | bm25_only | 8/10 | 8 | 0.5000 | 0.7500 | 0.3000 | 0.3088 | 0.5833 | 0.3798 |
| passport | dense_only | 8/10 | 8 | 0.7500 | 1.0000 | 0.6500 | 0.7173 | 0.8750 | 0.7607 |
| passport | hybrid_rrf | 8/10 | 8 | 0.3750 | 1.0000 | 0.4750 | 0.5253 | 0.6562 | 0.5328 |
| birth_death_registration | bm25_only | 9/10 | 9 | 0.3333 | 0.6667 | 0.2667 | 0.4370 | 0.4296 | 0.3938 |
| birth_death_registration | dense_only | 9/10 | 9 | 0.5556 | 0.7778 | 0.4222 | 0.6963 | 0.6481 | 0.6173 |
| birth_death_registration | hybrid_rrf | 9/10 | 9 | 0.4444 | 0.8889 | 0.4222 | 0.6685 | 0.6148 | 0.5882 |
| brta | bm25_only | 9/10 | 8 | 0.1111 | 0.5556 | 0.2667 | 0.3006 | 0.2593 | 0.2875 |
| brta | dense_only | 9/10 | 8 | 0.7778 | 0.8889 | 0.4444 | 0.7560 | 0.8333 | 0.7809 |
| brta | hybrid_rrf | 9/10 | 8 | 0.4444 | 0.7778 | 0.4444 | 0.6518 | 0.6111 | 0.6377 |
| overall | bm25_only | 26/30 | 25 | 0.3077 | 0.6538 | 0.2769 | 0.3523 | 0.4179 | 0.3553 |
| overall | dense_only | 26/30 | 25 | 0.6923 | 0.8846 | 0.5000 | 0.7221 | 0.7821 | 0.7156 |
| overall | hybrid_rrf | 26/30 | 25 | 0.4231 | 0.8846 | 0.4462 | 0.6173 | 0.6263 | 0.5863 |

## Required caveats

- Pooling only top-five results misses relevant passages that none of these retrievers found. Pooled recall is NOT corpus recall. Nonempty pools are not proof of full answer coverage.
- Conditional, partial, and legacy MRP evidence can be relevant to an unspecified passport question. It must retain those conditions in any answer. Broad question interpretation is a subjective annotation choice.
- Passage IDs, including near-duplicates, are the scoring unit. Redundant evidence can affect precision and pooled recall. No fact-level deduplication or reference-answer evaluation was performed.
- Precision divides relevant top-five IDs by five. MRR is truncated at five. nDCG uses binary relevance and an ideal ordering of up to five known pooled relevant IDs.
- This evaluates BM25/dense/RRF BEFORE reranking, boosts and evidence selection. It does not compare the complete Simple RAG and CivicRAG answer pipelines.
- Reused development questions, small samples, subjective labels and correlated passages limit conclusions. No superiority, legal accuracy or generalization claim is established.

## Questions needing adjudication

- passport_02_fee: 2 uncertain label(s); excluded for all three retrievers.
- passport_05_renewal: 1 uncertain label(s); excluded for all three retrievers.
- birth_08_birth_date_proof: 1 uncertain label(s); excluded for all three retrievers.
- brta_06_renewal: 1 uncertain label(s); excluded for all three retrievers.
- brta_10_status: no useful passage identified in the pool; this does NOT prove the whole database lacks an answer.

## Review files

- `assistant_review.md`: each decision, quote, and expandable source passage.
- `assistant_labels.json`: stable chunk IDs, exact quotes, content hashes, and empty human approval fields.
- `relevance_decisions.json`: explicit assistant-authored decisions; no automatic keyword label assignment.
- `assistant_metrics.json`: per-question metrics, exclusions and denominators.
- These files are separate from the earlier Qwen draft-labeling job; none of that job's labels were reused or changed.
