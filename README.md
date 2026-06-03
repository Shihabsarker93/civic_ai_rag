# Civic.ai RAG

Civic.ai is a high-accuracy, evidence-grounded, bilingual Bangla-English Retrieval-Augmented Generation system for citizen-facing government service guidance in Bangladesh.

The repository is designed as a single multi-domain project. The current working domain is `passport`, and future domains such as `BRTA`, `birth_certificate`, and `death_certificate` should be added as folders inside this repository, not as separate repositories.

## Core Principle

Accuracy comes before fluency. The system should answer from retrieved evidence, expose sources, and avoid unsupported claims.

## Repository Structure

```text
civic-ai-rag/
├── app.py                # Local web chatbot
├── domains/
│   ├── passport/         # Current active chatbot domain
│   ├── birth_death_registration/
│   │                       # Bangla birth/death registration corpus being prepared
│   │   ├── config.json
│   │   └── data/
│   │       ├── raw/
│   │       ├── processed/
│   │       ├── interim/
│   │       └── evaluation/
│   ├── _template/        # Template for future domains
│   └── _incoming/        # Source files not yet promoted to active domains
├── docs/                 # Architecture notes, thesis planning, paper summaries
├── notebooks/            # Exploration and experiments
├── scripts/              # CLI scripts for ingestion, indexing, evaluation, etc.
├── src/
│   ├── ingestion/        # PDF, OCR, web, and document loading
│   ├── preprocessing/    # Cleaning, normalization, metadata handling
│   ├── chunking/         # Bangla-aware and section-aware chunk creation
│   ├── embeddings/       # Embedding model wrappers and benchmarks
│   ├── retrieval/        # Dense, sparse, hybrid, and RRF retrieval
│   ├── reranking/        # Cross-encoder reranking and fallback rankers
│   ├── generation/       # Grounded answer generation and citation prompts
│   └── evaluation/       # Retrieval and RAG evaluation metrics
└── tests/                # Focused tests for pipeline behavior
```

## Thesis Direction

The intended architecture follows the broad direction of NextRAG: multilingual embeddings, hybrid retrieval, RRF fusion, reranking, and language-aware grounded generation. Unlike the paper's financial PDF setting, the first dataset focus is manually collected government-service FAQ data, especially passport-related questions, so OCR is optional rather than central at the beginning.

OCR should remain as a future ingestion path for scanned PDFs, notices, and raw government documents, but the first reproducible system should prioritize clean text ingestion, strong metadata, bilingual retrieval, and grounded answer generation.

## Evaluation Priorities

- Retrieval: `Recall@k`, `MRR`, `nDCG`, and qualitative relevance analysis.
- Generation: faithfulness, citation correctness, answer correctness, and abstention behavior.
- Ablation: dense-only vs sparse-only vs hybrid retrieval, reranker vs no reranker, chunking variants, and embedding model comparisons.

## Current Baseline Pipeline

The first implemented baseline follows a NextRAG-style structure adapted for the manually curated passport FAQ dataset:

```text
processed FAQ JSON
-> metadata-rich FAQ chunks
-> BGE-M3 dense embeddings in ChromaDB
-> BM25 sparse retrieval
-> weighted RRF fusion
-> Ollama local LLM generation
```

Build the local retrieval index:

```bash
python scripts/build_index.py
```

Run retrieval only:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python scripts/query_rag.py "What documents do I need for an e-Passport?" --no-generate
```

Run retrieval plus local generation:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python scripts/query_rag.py "What documents do I need for an e-Passport?" --model llama3.2
```

Select the RAG method explicitly:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python scripts/query_rag.py "how can i do passport" --method simple --model llama3.2
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python scripts/query_rag.py "how can i do passport" --method civic --model llama3.2
```

Run the local chatbot:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python app.py --host 127.0.0.1 --port 7860
```

Then open:

```text
http://127.0.0.1:7860
```

The chatbot includes two selectors:

- Method: `Simple RAG` or `CivicRAG (ours)`.
- Generator: `llama3.2`, `llama3`, or `qwen2.5:7b`.

Compare local LLMs by changing the model:

```bash
--model llama3.2
--model llama3
--model qwen2.5:7b
```

Or run the same retrieved evidence through all configured local models:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python scripts/compare_models.py "What documents do I need for an e-Passport?"
```

Note: the reranking layer is implemented. It will use `BAAI/bge-reranker-v2-m3` if that cross-encoder is cached locally; otherwise it falls back to deterministic lexical reranking so the chatbot remains usable offline.

## Adding Future Domains

Use a feature branch and copy the template:

```bash
git checkout -b feature/add-brta-domain
cp -R domains/_template domains/brta
```

Then add domain-specific data and edit:

```text
domains/brta/config.json
```

Do not create a separate repo for the new domain.

The `birth_death_registration` domain is being added on `feature/add-birth-death-domain`. Its first preprocessing step is:

```bash
python3 domains/birth_death_registration/scripts/clean_and_chunk_markdown.py
```

This converts raw Markdown into cleaned Markdown and metadata-rich retrieval chunks. The source set is mixed birth/death registration material, not birth-only, so chunks use `service_scope` metadata such as `birth` and `birth_death`.

## Numeric Evaluation

Run retrieval evaluation:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python scripts/evaluate_retrieval.py
```

This writes:

```text
data/evaluation/retrieval_evaluation.csv
data/evaluation/retrieval_summary.json
```

Run generated-answer evaluation on a small sample:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python scripts/evaluate_generation.py --limit 3 --models llama3.2 qwen2.5:7b
```

This writes:

```text
data/evaluation/generation_evaluation.csv
data/evaluation/generation_summary.json
```

Current metrics:

- Retrieval: `Recall@1`, `Recall@3`, `Recall@5`, `Precision@5`, `MRR`, `nDCG@5`.
- Generation: BGE-M3 semantic similarity, token F1, expected-source retrieval accuracy, citation accuracy.

Important limitation: the current retrieval evaluation uses the same FAQ questions that are indexed, so it is a smoke test rather than a difficult benchmark. For thesis results, add paraphrased English, Bangla, and code-mixed evaluation questions with expected source IDs.
