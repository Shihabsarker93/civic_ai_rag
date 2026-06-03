# Civic.ai RAG

Civic.ai is a high-accuracy, evidence-grounded, bilingual Bangla-English Retrieval-Augmented Generation system for Bangladeshi government-service guidance.

The active thesis domain is now:

```text
domains/birth_death_registration
```

The current pipeline should be built only from the latest birth/death registration dataset.

## Core Principle

Accuracy comes before fluency. The system should answer from retrieved evidence, expose source IDs, and avoid unsupported claims.

## Active Pipeline

```text
latest birth/death JSON + Markdown files
-> document-type-aware chunking
-> BGE-M3 embeddings
-> ChromaDB vector index
-> BM25 sparse retrieval
-> weighted RRF fusion
-> reranking
-> local Ollama generation
```

## Repository Structure

```text
civic-ai-rag/
├── app.py
├── domains/
│   ├── birth_death_registration/
│   │   ├── config.json
│   │   ├── scripts/prepare_chunks.py
│   │   └── data/
│   │       ├── raw/json/
│   │       ├── raw/md/
│   │       ├── interim/
│   │       ├── processed/
│   │       └── evaluation/
│   ├── _template/
│   └── _incoming/
├── scripts/
├── src/
└── tests/
```

## Prepare Chunks

```bash
python3 domains/birth_death_registration/scripts/prepare_chunks.py
```

This creates:

```text
domains/birth_death_registration/data/interim/birth_death_chunks.jsonl
```

The current chunker uses:

- FAQ-aware chunking for structured FAQ JSON.
- Legal-aware chunking for `ধারা` and `বিধি`.
- Table-aware chunking for fees.
- Step/scenario-aware chunking for application and correction guides.
- Selective portal chunking for support/service sections.

## Build Index

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python3 scripts/build_index.py
```

This builds:

```text
domains/birth_death_registration/data/processed/chroma_birth_death_bge_m3
```

## Query

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python3 scripts/query_rag.py "জন্ম নিবন্ধনের ফি কত?"
```

Run the local chatbot:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python3 app.py --host 127.0.0.1 --port 7860
```

Then open:

```text
http://127.0.0.1:7860
```

## Models

The current local generation candidates are:

- `llama3.2`
- `llama3`
- `qwen2.5:7b`

The main embedding model is:

```text
BAAI/bge-m3
```

## Evaluation Direction

For thesis results, create a birth/death registration evaluation set with Bangla, English, and code-mixed questions. Retrieval evaluation should report `Recall@k`, `MRR`, `nDCG`, and qualitative evidence relevance.
