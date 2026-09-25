# Reference audit

## Paper-only bibliography revision

At the authors' request, the numbered bibliography now contains research papers and identifiable technical reports/preprints only. Software documentation, model cards, Unicode documentation, the IR textbook and internal Civic.ai experiment archives were removed from the BibTeX file and numbered citations. The historical source-verification table below remains a reproducibility record, not the current bibliography.

Old references 17, 21, 22 and 24 were RAGAS documentation and three internal project reports, respectively. Internal reports remain available at revision d32c107 in the evaluation directories identified in FINAL_REVISION_2026_09_25.md; they are evidence for our own experiments, not external research papers.

Ollama, Chroma, LangChain, model checkpoint IDs and package versions remain implementation details. No fictitious Ollama paper was introduced. Qwen technical reports support model-family statements; no newer Llama-family paper is substituted as if it documented the exact original Llama 3 checkpoint.

Added Nogueira and Cho, Passage Re-ranking with BERT (arXiv:1901.04085), for the cross-encoder approach, not as a BGE checkpoint citation. Added Jarvelin and Kekalainen, Cumulated Gain-Based Evaluation of IR Techniques, ACM TOIS 20(4), 422-446 (2002), DOI 10.1145/582415.582418, for normalized cumulative gain. Verified against the paper's arXiv record and the authors' institutional publication record. Preprints remain distinguishable from peer-reviewed publications.

References were selected for actual use, not copied wholesale from the previous bibliography.

| Key | Verification source | Role |
|---|---|---|
| nextrag | Local supplied IEEE paper, title/author block and DOI 10.1109/ICCIT68739.2025.11491522 | Principal inspiration; not replication |
| lewis2020rag | arXiv 2005.11401 | Foundational RAG |
| bm25 | Publisher DOI 10.1561/1500000019 | BM25 theory |
| rrf | Author-hosted paper / DOI 10.1145/1571941.1572114 | Rank fusion |
| bgem3 | arXiv 2402.03216 | Dense multilingual embeddings |
| bgereranker | BAAI official Hugging Face model card | Actual reranker implementation |
| qwen3 | arXiv 2505.09388 | Main model family and modes |
| qwen25 | arXiv 2412.15115 | Secondary model; first-submission year distinguished from revisions |
| llama3card | Meta official model card | Original Llama3, not the paper's Llama3.1 |
| lostmiddle | arXiv 2307.03172 | Context-use motivation, not proof of our measured cause |
| ragas | ACL Anthology 2024.eacl-demo.16 | Evaluation framework |
| ragasdocs | Versioned RAGAS API documentation plus installed source | Metric definitions |
| chroma | Official Chroma documentation | Vector/document storage |
| rankbm25 | Upstream source repository | BM25Okapi implementation |
| ollama | Official API documentation | Local inference |
| docling | arXiv 2408.09869, checked 2026-09-25 | Structured document conversion; project use remains unconfirmed |
| langchain_ollama | Official LangChain ChatOllama integration documentation, checked 2026-09-25 | Implemented wrapper, not an architectural research contribution |
| irbook | Stanford-hosted Introduction to Information Retrieval, evaluation chapter | Ranked retrieval metrics and pooled relevance limitations |
| unicode_nfc | Unicode Standard Annex #15 | NFC normalization terminology |
| project_ragas, project_retrieval, project_pool | Saved project reports pinned to d32c107 | Primary experimental artifacts, not external validation |

Dataset-specific source titles, available URLs and IDs are supplied in dataset_catalog.json, derived from the active corpus. Missing URLs are not filled with guesses. That catalog documents provenance; it does not certify current government rules or original-to-Markdown fidelity.

TraSe was checked against its original PDF and ACL Anthology entry (2025.lm4uc-1.2), including the authors and DOI. HybridRAG-BN was checked against its supplied PDF and arXiv:2608.13004 and is labelled as a preprint. Both are related work, not implemented components. NextRAG's reference list itself is not assumed reliable for every secondary citation.

Previous planned references/benchmarks for fine-tuning, surveys, GLUE, SuperGLUE and broad QA benchmarking were removed because no matching completed experiment is reported. No bibliography entry is added merely to enlarge the reference count.
