# P2 Citation Sweep for CivicRAG

This file maps the Phase 2 CivicRAG design to thesis-defensible citations. Use this as a citation checklist when writing Chapter 4.

## Citation Strategy

Do not cite every Python library or every implementation detail. Cite the paper behind the method, metric, or model family.

Use three levels:

- **Must cite:** Required because the method/equation/metric appears in our Chapter 4 design.
- **Recommended:** Strongly useful for background or justification.
- **Optional/future work:** Useful if we discuss future improvements such as full cross-encoder reranking, multilingual benchmarks, or OCR-heavy pipelines.

## Core RAG Framework

| Use in our thesis | Citation | Priority | Why |
|---|---|---:|---|
| Retrieval-Augmented Generation concept | Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* | Must cite | Original/standard RAG reference for combining retrieved evidence with generation. |
| Our closest reference system | Opin et al. (2025), *NextRAG: A Bilingual Retrieval-Augmented Generation Framework for Financial Question-Answering* | Must cite | Direct inspiration for bilingual Bangla-English RAG in Bangladesh, hybrid retrieval, RRF, reranking, and evaluation comparison. |
| Knowledge-intensive retrieval/generation benchmark framing | Petroni et al. (2021), *KILT* | Optional | Useful if Chapter 2/4 discusses knowledge-intensive NLP and grounded QA evaluation. |

Suggested Chapter 4 sentence:

> The proposed CivicRAG pipeline follows the RAG paradigm introduced by Lewis et al. and is adapted from the bilingual hybrid-retrieval design philosophy of NextRAG.

## Retrieval Methods

| Use in our thesis | Citation | Priority | Why |
|---|---|---:|---|
| BM25 sparse retrieval | Robertson and Zaragoza (2009), *The Probabilistic Relevance Framework: BM25 and Beyond* | Must cite | Cite when describing BM25 or the BM25 scoring equation. |
| Dense retrieval baseline | Karpukhin et al. (2020), *Dense Passage Retrieval for Open-Domain QA* | Recommended | Justifies dense retrieval as a semantic retrieval approach. |
| Sentence embeddings / semantic similarity | Reimers and Gurevych (2019), *Sentence-BERT* | Recommended | Useful background for semantic embedding similarity. |
| BGE-M3 embedding model | Chen et al. (2024), *BGE M3-Embedding* | Must cite | Our actual embedding model is `BAAI/bge-m3`; cite for multilingual, multi-functionality, multi-granularity embeddings. |
| BEIR retrieval benchmarking | Thakur et al. (2021), *BEIR* | Recommended | Useful for explaining retrieval evaluation across datasets and why retrieval metrics matter. |

Suggested Chapter 4 sentence:

> Dense retrieval is evaluated as a semantic baseline, while BM25 is retained as a lexical baseline for exact government-service terms such as fees, rules, and form names.

## Fusion and Reranking

| Use in our thesis | Citation | Priority | Why |
|---|---|---:|---|
| Reciprocal Rank Fusion | Cormack et al. (2009), *Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods* | Must cite | Cite directly beside the RRF equation. |
| BERT/cross-encoder passage reranking | Nogueira and Cho (2019), *Passage Re-ranking with BERT* | Recommended | Cite if we discuss cross-encoder reranking as the intended/future strong reranker. |
| BGE reranker family | Xiao et al./BAAI FlagEmbedding resources | Optional | There is not one universally cited BGE-reranker paper equivalent to BGE-M3; cite official model card if required, but avoid overclaiming. |

Important honesty note:

Our current code supports cross-encoder reranking if the model is locally available, but may fall back to lexical/domain-aware reranking. In Chapter 4, describe this as:

> Hybrid RRF candidates are passed to a reranking stage. The implementation supports cross-encoder reranking, with deterministic lexical/domain-aware fallback for local reproducibility.

## Evaluation Metrics

| Metric / evaluation idea | Citation | Priority | Why |
|---|---|---:|---|
| Precision, recall, IR evaluation basics | Manning et al. (2008), *Introduction to Information Retrieval* | Must cite | Safe textbook source for precision/recall and ranking evaluation terminology. |
| MRR / QA ranking evaluation | Voorhees (1999/2000), TREC-8 QA Track | Must cite if MRR is defined | Strong historical source for reciprocal-rank style QA evaluation. |
| nDCG / DCG | Järvelin and Kekäläinen (2002), *Cumulated Gain-Based Evaluation of IR Techniques* | Must cite | Cite beside nDCG equation. |
| Token F1 / exact match for QA | Rajpurkar et al. (2016), *SQuAD* | Recommended | Useful if we report token-level answer similarity or QA-style F1. |
| BERTScore semantic generation metric | Zhang et al. (2020), *BERTScore* | Recommended | Cite if using or discussing embedding/semantic similarity for generated answer quality. |
| RAGAS metrics: faithfulness, answer relevancy, context precision/recall | Es et al. (2024), *RAGAS* | Must cite if we mention RAGAS-style metrics | Relevant to RAG-specific automatic evaluation. |
| ARES RAG evaluation | Saad-Falcon et al. (2024), *ARES* | Optional | Useful for Chapter 2 or future evaluation comparison. |

Suggested Chapter 4 sentence:

> Retrieval-side verification is reported using Hit@k/Recall@k, MRR, nDCG, and Context Precision, while generation-side evaluation is planned using faithfulness, answer relevance, answer correctness, and manual qualitative scoring.

## Multilingual and Bangla-Relevant Retrieval

| Use in our thesis | Citation | Priority | Why |
|---|---|---:|---|
| Multilingual retrieval benchmark | Zhang et al. (2023), *MIRACL* | Recommended | Supports multilingual retrieval framing. |
| Multilingual MS MARCO | Bonifacio et al. (2021), *mMARCO* | Optional | Useful if discussing multilingual passage ranking datasets. |
| BGE-M3 multilingual model | Chen et al. (2024), *BGE M3-Embedding* | Must cite | Most directly relevant to our Bangla-English retrieval system. |

Suggested Chapter 4 sentence:

> Since the knowledge base is Bangla-heavy and user queries may be Bangla, English, or code-mixed, multilingual retrieval models are prioritized over English-only embedding models.

## Local LLM Backends

| Use in our thesis | Citation | Priority | Why |
|---|---|---:|---|
| Llama 3 / llama3.2 local baseline | Dubey et al. (2024), *The Llama 3 Herd of Models* | Must cite if model comparison is reported | Defensible citation for Llama 3 family. |
| Qwen2.5 local baseline | Qwen Team (2024), *Qwen2.5 Technical Report* | Must cite if model comparison is reported | Defensible citation for Qwen2.5. |
| Ollama runtime | Software/tool citation only | Optional | Cite in implementation notes, not as a research paper. |

Suggested Chapter 4 sentence:

> Local LLMs are used to avoid API dependency and support reproducibility; llama3.2 is used as the default local backend, while llama3 and qwen2.5:7b are retained for comparative experiments.

## Noisy Documents and OCR

| Use in our thesis | Citation | Priority | Why |
|---|---|---:|---|
| OCR system background | Smith (2007), *An Overview of the Tesseract OCR Engine* | Optional | Use only if OCR/scanned PDFs become a major part of our pipeline. |
| NextRAG noisy PDF/OCR preprocessing | Opin et al. (2025), NextRAG | Recommended | Directly relevant because our inspiration paper emphasizes noisy PDF preprocessing. |

Our current birth/death domain uses manually cleaned and converted data, not a full OCR-first pipeline. If we mention OCR, phrase it carefully:

> OCR-affected and scanned documents are considered in the raw-data collection stage, but the current Phase 2 implementation primarily indexes manually cleaned Markdown/JSON content.

## Current CivicRAG-Specific Claims and Best Citations

| Claim in Chapter 4 | Best citation |
|---|---|
| RAG reduces hallucination by grounding answers in external evidence. | Lewis et al. (2020); NextRAG (2025). |
| BM25 is a lexical sparse retrieval baseline. | Robertson and Zaragoza (2009). |
| Dense embeddings support semantic retrieval. | Karpukhin et al. (2020); Reimers and Gurevych (2019); Chen et al. (2024). |
| BGE-M3 is suitable for multilingual retrieval. | Chen et al. (2024). |
| RRF combines ranked outputs from multiple retrieval systems. | Cormack et al. (2009). |
| Reranking improves candidate ordering. | Nogueira and Cho (2019). |
| nDCG is a graded ranking-quality metric. | Järvelin and Kekäläinen (2002). |
| MRR evaluates where the first relevant result appears. | Voorhees (1999/2000); Manning et al. (2008). |
| RAG-specific evaluation should include faithfulness/context quality. | Es et al. (2024); Saad-Falcon et al. (2024). |
| Local LLM comparison is academically defensible. | Dubey et al. (2024); Qwen Team (2024). |

## Citation Placement Plan for Chapter 4

### Section 4.1 Design Process or Methodology Overview

Use:

- Lewis et al. (2020)
- NextRAG (2025)
- Chen et al. (2024)

### Section 4.2 Preliminary Design or Model Specification

Use:

- Robertson and Zaragoza (2009) for BM25.
- Karpukhin et al. (2020) and Chen et al. (2024) for dense/BGE-M3 retrieval.
- Cormack et al. (2009) for RRF.
- Nogueira and Cho (2019) for reranking.
- Dubey et al. (2024) and Qwen Team (2024) for LLM backends.

### Section 4.3 Data Collection and Preprocessing

Use:

- NextRAG (2025) for noisy document/RAG preprocessing motivation.
- Smith (2007) only if discussing scanned PDF/OCR handling.

### Section 4.4 Implementation of Selected Design

Use:

- Lewis et al. (2020), Chen et al. (2024), Robertson and Zaragoza (2009), Cormack et al. (2009), and Es et al. (2024).

## Metric Equations and Citations

Use these citations beside formulas:

### Recall@k / Hit@k

Use Manning et al. (2008) as the general IR reference.

### MRR

\[
MRR = \frac{1}{|Q|}\sum_{i=1}^{|Q|}\frac{1}{rank_i}
\]

Cite Voorhees/TREC QA and Manning et al.

### DCG and nDCG

\[
DCG@k = \sum_{i=1}^{k}\frac{2^{rel_i}-1}{\log_2(i+1)}
\]

\[
nDCG@k = \frac{DCG@k}{IDCG@k}
\]

Cite Järvelin and Kekäläinen (2002).

### RRF

\[
RRF(d) = \sum_{r \in R}\frac{w_r}{k + rank_r(d)}
\]

Cite Cormack et al. (2009). Note that the original RRF formula is usually unweighted; our version adds weights for dense/BM25 sensitivity testing.

### Token F1

Use Rajpurkar et al. (2016) if reporting QA-style token overlap.

### Faithfulness / Context Precision / Answer Relevance

Use RAGAS by Es et al. (2024).

## Avoid Overclaiming

Do not claim:

- That our system already outperforms NextRAG. We have replicated a NextRAG-style design in a new government-service domain.
- That hybrid RRF is always better. Our current evaluation shows dense-only is strongest on the single-domain Bangla paraphrase set.
- That cross-encoder reranking is always active. The current implementation supports it but may use fallback reranking locally.
- That automatic generation metrics alone prove factual correctness. Manual qualitative review is still required for civic/legal/procedural QA.

