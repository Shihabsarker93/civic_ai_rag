# Query Decomposition Improvement Evaluation

Date: 2026-06-07

Branch: `feature/add-birth-death-domain`

Baseline checkpoint before this improvement: `be9f69a`

## What Changed

This update keeps the existing retrieval stack unchanged:

- BAAI/bge-m3 embeddings
- ChromaDB vector index
- BM25 sparse retrieval
- RRF fusion
- BGE reranking
- Existing CivicRAG safe-answer paths

The improvement adds a lightweight question-handling layer before LLM fallback:

- Unicode/typo normalization for noisy Bangla queries, for example `অনলাইনাে` -> `অনলাইনে`.
- Multi-intent query detection for long citizen-style questions.
- Query decomposition into controlled service intents such as application process, documents, status/progress, upload error, manual-to-online migration, overseas case, lost certificate, one-parent registration, and parent-name correction.
- Curated evidence selection from already indexed chunks for high-risk intents, instead of running multiple expensive retrieval/reranking passes.
- More explicit answer-completeness behavior when the dataset does not contain a specific operational detail.

## Why This Was Needed

The previous pipeline worked well for focused questions, but complex citizen questions often contained several different problems in one message. For example, one question could ask about application status, file upload error, required documents, and old offline registration at the same time.

Without decomposition, the system tended to answer only the dominant intent, usually generic application steps. This was grounded, but incomplete.

## Seven-Question Regression Summary

| Question Area | Before | After |
| --- | --- | --- |
| Application + documents + progress | Answered application/documents but missed progress clearly | Separates progress/status, application steps, and documents; states that exact online progress tracking is not present in the dataset |
| Lost certificate | Strong | Still strong; no regression |
| Divorce / one-parent information | Model-dependent; Qwen could produce corrupted text | Controlled FAQ answer; no LLM fallback needed |
| Online record not found | One model hallucinated awkward UI wording | Normalizes noisy Bangla and uses verification/manual-migration evidence |
| Long multi-problem query | Collapsed into generic application steps | Separates status, upload/file issue, manual-to-online migration, and application guidance |
| Outside Bangladesh | Long generic process answer | Adds overseas/diplomatic-mission guidance and caveat for people born in Bangladesh but now abroad |
| Parent-name correction | Mostly strong but missed document uncertainty | Keeps correction guidance and explicitly says full uploadable document list is not fully available in the dataset |

## Remaining Limitations

- The answer can become long when many intents are detected.
- Some operational details, such as exact live application progress tracking or specific BDRIS upload-error troubleshooting, are not fully available in the current dataset.
- The reranker still adds noticeable CPU latency during retrieval. The decomposition layer avoids multiple reranking passes, but each user query still performs the normal CivicRAG retrieval pipeline.
- Curated safe paths should be reviewed when new domain documents are added, because source IDs may change if chunks are regenerated with a different chunking strategy.

## Thesis Interpretation

This is a defensible improvement over simple RAG because it targets a real government-service chatbot failure mode: users rarely ask clean benchmark-style questions. They ask noisy, multi-part, emotionally phrased service questions.

The upgraded CivicRAG behavior is now closer to a practical civic-service assistant:

1. Detect the user’s language and service intent.
2. Split complex questions into smaller grounded sub-questions.
3. Retrieve or select evidence for each sub-question.
4. Give a controlled answer when evidence is clear.
5. Explicitly say when the dataset does not contain enough detail.

This supports the thesis priority: accuracy and groundedness over fluent but unsupported generation.
