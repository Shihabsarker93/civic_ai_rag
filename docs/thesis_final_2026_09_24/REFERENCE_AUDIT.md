# Reference and in-text citation audit

Checked: 2026-09-25. Supersedes the earlier paper-only policy: relevant research papers are preferred; official implementation documentation is allowed.

## Scope and outcome

- 28 cited entries: 23 research papers/preprints/technical reports and five official documentation entries. Not all 23 are peer-reviewed publications.
- No Civic.ai team, internal project report, invented software paper or unrelated wrapper paper is in the bibliography.
- Added relevant work on dataset documentation, dense retrieval, generalization, chunking, RAG evaluation, judge limitations and incomplete relevance judgments. No benchmark results were added or altered.
- Each added work has an explicit in-text role. Related work is distinguished from implemented components; software documentation supports implementation details rather than research novelty.
- The unchanged Abstract and original template heading/order checks pass. Figures retain their prior intact portrait layout.

## Link verification

All bibliography URLs were checked against titles and/or primary bibliographic metadata. The accompanying reference_link_check.json records a fresh curl GET, redirect destination and HTTP status with TLS verification enabled. HTTP success alone is not a semantic check. 26 URLs returned 200; NextRAG returned 202 and BM25 returned 403, so these are NOT reported as fully accessible papers. Crossref/publisher identity checks support their citation targets despite the access restrictions.

Re-run HTTP checks from the repository root: ` .venv/bin/python scripts/check_thesis_reference_links.py `.

| Key | Direct reference link | HTTP | Identity check and in-text role |
|---|---|---|---|
| lewis2020rag | [Source](https://arxiv.org/abs/2005.11401) | 200 | arXiv title/authors checked; foundational RAG, not proof of our accuracy. |
| nextrag | [Source](https://doi.org/10.1109/ICCIT68739.2025.11491522) | 202 | IEEE DOI/title/authors/pages checked through Crossref and supplied-paper record. HTTP 202 is a publisher challenge, not full-text verification. Architectural inspiration only. |
| bm25 | [Source](https://doi.org/10.1561/1500000019) | 403 | DOI resolves to the correct publisher title but HTTP 403 prevents unrestricted retrieval. Original volume 3(4), 333-389 retained; migrated publisher/Crossref record differs. Original publisher PDF indexing confirms original pagination. |
| rrf | [Source](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf) | 200 | Author-hosted paper and Crossref DOI checked. Original RRF; our weights and k=50 are local choices. |
| bgem3 | [Source](https://aclanthology.org/2024.findings-acl.137/) | 200 | Published ACL paper checked; corrected author Jianlyu Chen, title, venue and pages. |
| qwen3 | [Source](https://arxiv.org/abs/2505.09388) | 200 | arXiv technical report checked; model family, not a guarantee of Bangla correctness. |
| qwen25 | [Source](https://arxiv.org/abs/2412.15115) | 200 | arXiv report checked; first-submission year retained. |
| lostmiddle | [Source](https://aclanthology.org/2024.tacl-1.9/) | 200 | Published TACL article checked; upgraded preprint citation to 2024 journal record. |
| ragas | [Source](https://aclanthology.org/2024.eacl-demo.16/) | 200 | ACL paper checked; evaluation framework. |
| docling | [Source](https://arxiv.org/abs/2408.09869) | 200 | arXiv report checked; related preprocessing only, not claimed as implemented. |
| trase | [Source](https://aclanthology.org/2025.lm4uc-1.2/) | 200 | ACL record checked; related Bangla RAG, not our implementation. |
| hybridragbn | [Source](https://arxiv.org/abs/2608.13004) | 200 | arXiv record checked; explicitly a 2026 preprint. |
| bert_reranking | [Source](https://arxiv.org/abs/1901.04085) | 200 | arXiv paper checked; cross-encoder approach, not documentation of our BGE checkpoint. |
| ndcg | [Source](https://researchportal.tuni.fi/en/publications/cumulated-gain-based-evaluation-of-ir-techniques/) | 200 | Institutional publication record and Crossref DOI checked; normalized cumulative gain. |
| dpr | [Source](https://aclanthology.org/2020.emnlp-main.550/) | 200 | ACL paper checked; dense retrieval background, not a claim that we use DPR weights. |
| beir | [Source](https://arxiv.org/abs/2104.08663) | 200 | arXiv and publication identity checked; heterogeneous retrieval evaluation. Published title uses Heterogeneous; arXiv title uses Heterogenous. |
| datasheets | [Source](https://arxiv.org/abs/1803.09010) | 200 | arXiv paper and published CACM DOI checked; dataset documentation rationale, not claimed full framework compliance. |
| datastatements | [Source](https://aclanthology.org/Q18-1041/) | 200 | ACL record checked; language/data scope and generalization. |
| ares | [Source](https://aclanthology.org/2024.naacl-long.20/) | 200 | ACL paper checked; related evaluation approach, not implemented or substituted for RAGAS. |
| llmjudge | [Source](https://arxiv.org/abs/2306.05685) | 200 | arXiv paper checked; judge limitations, not a quantitative bias estimate for our Qwen judge. |
| drorstats | [Source](https://aclanthology.org/P18-1128/) | 200 | ACL paper checked; significance-test design and assumptions, not a claim of significant superiority. |
| incompletejudgments | [Source](https://www.nist.gov/publications/retrieval-evaluation-incomplete-information) | 200 | NIST paper record and Crossref DOI checked; limits of incomplete judgments. We do not claim to implement bpref. |
| chroma_chunking | [Source](https://www.trychroma.com/research/evaluating-chunking) | 200 | Chroma research report with named authors and supplied BibTeX checked. Technical report, not peer reviewed; supports chunking discussion, not database internals. |
| chroma_docs | [Source](https://docs.trychroma.com/docs/collections/add-data) | 200 | Official collection API documentation; linked IDs, embeddings, documents and metadata. |
| ollama_docs | [Source](https://docs.ollama.com/api/chat) | 200 | Official chat API documentation. No verified foundational Ollama paper substituted; papers about R wrappers are not Ollama itself. |
| ragas_docs | [Source](https://docs.ragas.io/en/v0.2.12/references/metrics/) | 200 | Official v0.2.12 metric reference checked. Text discloses installed v0.2.15; archived experiment/code define actual settings. |
| langchain_ollama | [Source](https://docs.langchain.com/oss/python/integrations/chat/ollama) | 200 | Official ChatOllama integration documentation; runtime wrapper only. |
| bge_checkpoint | [Source](https://huggingface.co/BAAI/bge-reranker-v2-m3) | 200 | BAAI-owned official model card; exact checkpoint documentation, not presented as a research paper. |

## Boundaries

The Chroma chunking report is not a foundational ChromaDB paper. Ollama is supported by its official API documentation and Qwen by the model's technical report; these are separate claims. The RAGAS paper does not validate our custom binary metric. Pooled retrieval scores do not establish exhaustive recall, and local self-judge scores do not certify factual correctness.

Government-source provenance remains in dataset_catalog.json and the saved chunk/source records. This bibliography audit does not independently verify current government rules. Project experiments are supported by repository artifacts, not fabricated external authorship.

Rollback: `codex/pre-reference-audit-20260925` at `0fdb02f`. No chatbot code, model settings, source data or evaluation scores were changed.
