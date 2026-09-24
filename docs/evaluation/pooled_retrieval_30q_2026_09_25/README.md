# Saved-evidence retrieval evaluation: 30 questions

## Scope and current status

Compares the final supplied evidence of Simple RAG and CivicRAG, not isolated BM25/dense/RRF stages. Uses the two existing Qwen3 answer files, without changing or regenerating answers, rebuilding indexes or calling RAGAS. All runtime inference goes to local Ollama at 127.0.0.1.

To permit low-conversation-token background processing, Qwen3:8b drafts relevance labels. **These are automatic labels, not human-reviewed ground truth.** Local labeling still takes model compute time. Only the subsequent metric calculations are instantaneous. This protocol must not be presented as manual evaluation or independent adjudication.

The local worker is `scripts/evaluate_saved_retrieval.py`, in detached screen session `civic-retrieval-30q`. No periodic assistant monitor is created. Check progress.json and run.log on request. Network/server failures are recorded in failure.json and terminate the worker; completed labels are checkpointed. Validation failures/uncertainty remain visible and are not silently scored as irrelevant. Seven deterministic metric tests are in scripts/test_saved_retrieval_metrics.py.

## Labeling pool and fairness

- Thirty identical questions, ten per domain; birth questions do not test death registration, and BRTA questions concern driving licences.
- 455 question/passage pairs in the union of both systems' saved candidate and supplied passages, including passages outside the scored top five.
- Candidate content equality checked for shared IDs. No generated answer is provided to the relevance judge.
- Both systems use the same labels. Opaque passage IDs and seeded shuffled order hide method names and ranking from the judge.
- Each judgment includes relevant/irrelevant/uncertain, a reason and an exact supporting quote for relevance. A missing/nonverbatim quote becomes uncertain.
- Partial directly useful evidence is relevant. Broad service-name overlap, collection instead of application and other procedure mismatches are not enough.
- Pooling cannot guarantee exhaustive relevance coverage. Unretrieved valid alternatives may be missing. Local Qwen3 self-judge bias and reused development-question bias remain.

## Metrics and tables

The first five actual answer_contexts are scored in their saved order. No final-answer accuracy is inferred. Table rows are Simple/Civic for each domain and overall, averaged over questions with fully judged pools and at least one relevant passage.

- Hit@5: any relevant passage within five.
- Precision@5: relevant retrieved passages divided by five, even if fewer than five were supplied.
- **Pooled Recall@5**: relevant top-five passages divided by relevant passages found in the inspected union. Not exhaustive corpus Recall@5 or RAGAS Context Recall.
- MRR@5: reciprocal first relevant rank within five, otherwise zero.
- **Pooled nDCG@5**: binary discounted gain normalized by the ideal ordering derived from that pool.

Uncertain/unjudged pools exclude the same question from both systems. Pools with no known relevant passage are also excluded, not assigned fabricated perfect/zero recall. Tables disclose valid-question denominators and remain provisional even when all local-model requests finish. The full candidate pool, ranks, labels and exact scoring protocol remain available for human correction.

## Artifacts

- manifest.json: input hashes, model digest, exact prompt, schema and settings.
- review_pool.json: saved question/passages and system rankings for later review.
- draft_judgments.json: resumable automatic labels (created as batches finish).
- judge_trace.jsonl: raw local judge responses and validation issues.
- metrics.json: per-question scores, exclusions and per-domain/overall means.
- report.md: provisional comparison tables, refreshed as processing advances.
- completion.json: draft completion, explicitly not human-review completion.

Do not insert these as final thesis results before reviewing relevance labels and checking for missed evidence. No thesis files are edited by this worker.
