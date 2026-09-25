# Final architecture diagrams

Open `civicrag_final_architecture.drawio` in diagrams.net/draw.io using **File > Open from > Device**. It is uncompressed editable XML, not a flattened image. Boxes, text, arrows and panels are editable. There are two pages:

1. **Final evaluated architecture:** data preparation, domain-scoped indexing/retrieval, automatic evidence selection, generation and output checks.
2. **Comparison and evaluation boundaries:** matched Simple RAG versus CivicRAG, plus the separate retrieval-only experiment.

Matching `.svg` vector versions and `.png` previews are included. For later LaTeX use, export the chosen draw.io page as PDF with cropping, or use the SVG through the appropriate LaTeX workflow. The existing thesis files have not been modified. The large architecture is best placed on a landscape page or split into its three numbered panels for readable thesis typography.

## What this figure represents

Checked against application code at `d32c107` on `feature/add-birth-death-domain`. The diagram is the selected-evidence CivicRAG route enabled by default with `CIVIC_EVIDENCE_SELECTION=1`. Qwen3:8b is the model used in the final matched comparison; the app still supports model selection and the domain configuration's default model is not necessarily Qwen3.

- `retrieval_text` is embedded and also tokenized for BM25. `content` is stored as the Chroma document together with its ID and metadata; it is not a second separately embedded branch.
- Retrieval matches chunk IDs. The retriever attaches source text from the linked local chunk corpus; it does not ask Chroma to generate an answer. Chroma document storage and local JSONL lookup are both shown.
- BM25 is built at retriever initialization from the local corpus, rather than persisted as part of Chroma. Its box appears in the index-construction panel for conceptual grouping; the label explicitly states its runtime construction.
- The domain is user-selected. There is no general automatic cross-domain search. The aggregate-query guard is heuristic, not a comprehensive semantic scope detector. The Bangla input check detects the presence of Bengali characters; it is not a strict language classifier.
- Dense and sparse searches each request 20 candidates. Weighted RRF uses k=50 with dense weight 0.55 and BM25 weight 0.45, retaining 15 candidates before reranking.
- The reranking implementation uses BGE cross-encoding when available, otherwise lexical overlap. Actual model availability must be checked in a given runtime; the figure does not assert that BGE reranking successfully loaded for every saved run.
- The implemented ranking boosts and pre-selector fee-context augmentation are birth/death-specific. Shared evidence screening, compatible section expansion and generation apply across all three domains.
- Evidence selection is a hand-written heuristic, not another LLM. It checks service, action, product/location and historical scope, handles compatible checklist/fee continuations, and groups those continuations before applying a six-passage, 14,000-character budget. This character budget is not a token count or a guarantee that all relevant information fits the model context window.
- The current selected-evidence route bypasses the old controlled-answer templates. It generates with the LLM when evidence is selected; with no selected evidence it asks for clarification. Therefore an unconditional old-style "safe answer path -> controlled answer -> LLM fallback" would misrepresent this route.
- Output checks include a language-rejection fallback and a warning on length-truncated generation. They are not a fact verifier. Canonical source IDs show supplied context, not independently checked claim-to-source attribution. The UI can display available URLs, candidate scores and selection details separately.
- Original documents and prepared MD/JSON are distinct source/preparation artifacts. The figure does not claim every original file is directly indexed, every chunk has a URL, or every domain uses identical typed chunking. Indexing is not model training.

## Implementation references

| Figure component | Code at the checked revision |
|---|---|
| Text embedding and linked Chroma content | [build_index.py](https://github.com/Shihabsarker93/civic_ai_rag/blob/d32c107/scripts/build_index.py#L45), [experimental domain indexer](https://github.com/Shihabsarker93/civic_ai_rag/blob/d32c107/scripts/manage_experimental_domains.py#L194) |
| Dense, BM25 and weighted RRF | [hybrid_retriever.py](https://github.com/Shihabsarker93/civic_ai_rag/blob/d32c107/src/retrieval/hybrid_retriever.py) |
| Reranking and conditional domain boosts | [reranker.py](https://github.com/Shihabsarker93/civic_ai_rag/blob/d32c107/src/reranking/reranker.py#L45) |
| Main selected-evidence route | [pipeline.py](https://github.com/Shihabsarker93/civic_ai_rag/blob/d32c107/src/pipeline.py#L115) |
| Applicability, expansion and family ordering | [evidence_selection.py](https://github.com/Shihabsarker93/civic_ai_rag/blob/d32c107/src/generation/evidence_selection.py#L119) |
| Prompt and local generation | [ollama_generator.py](https://github.com/Shihabsarker93/civic_ai_rag/blob/d32c107/src/generation/ollama_generator.py#L45) |
| Matched baseline used for evaluation | [run_simple_matched.py](https://github.com/Shihabsarker93/civic_ai_rag/blob/d32c107/scripts/run_simple_matched.py) |

## Evaluation page caveats

The matched baseline script uses dense retrieval only, with the same selected-evidence generation prompt and budget, not the legacy controlled branches of the live Simple RAG option. RAGAS faithfulness and answer relevancy are separate from the custom binary context-relevance measure. The current retrieval-only scores are assistant-labelled diagnostics, not human-verified gold evaluation. Their denominators differ because uncertain questions and empty relevant pools are disclosed, not filled with invented labels.

## Regeneration and checks

Run `.venv/bin/python scripts/build_final_architecture_diagram.py` from the repository root to rebuild the draw.io and SVG files. The generator checks XML parseability, unique cell IDs, and connector endpoints. SVGs were rasterized and visually inspected for text overflow and connector placement. The editable file has not been interactively tested inside draw.io itself. PNG previews are generated separately from the SVGs and should be refreshed after geometry changes.
