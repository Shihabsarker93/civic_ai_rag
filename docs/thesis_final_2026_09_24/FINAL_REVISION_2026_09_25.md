# Final integration and diagram audit

Rollback: `codex/pre-final-thesis-integration-20260925` at `ab354ee`.
This revision changes documentation and reproducible figure/table exports only. No chatbot code, corpus, prompts, models or saved evaluation answers were changed. No model calls were made.

## Supplied diagrams

The original PNGs under the user's `Final/draw io` folder remain untouched. Corrected exports were generated from the existing editable diagram builder and integrated in Section 4.2. The architecture is split into two landscape panels for readability; the evaluation diagram is a third figure. The complete editable draw.io file remains in `docs/architecture/final_2026_09_25/`.

Corrections and interpretation:

- Use birth registration for study scope. Combined legal sources and literal internal storage identifiers are not renamed.
- Retrieval returns up to 20 candidates per channel; positive-score filtering can return fewer BM25 candidates. Weighted RRF retains up to 15.
- Same generation prompt does not mean the baseline has an evidence selector. Simple RAG uses dense top-six retrieval and matched budgeting/generation only.
- Scope checks are targeted guards, not guaranteed detection of every unsupported or cross-domain question.
- Original content is stored with the vector record, not embedded as another answer. Retrieval IDs also resolve against the local chunk map. The later resolve-content box represents answer-context preparation, not the first possible access to content.
- BM25 is constructed at retriever load, not persisted in ChromaDB. Its placement in the preparation panel is logical, not a claim of a separately persisted offline index.
- BGE cross-encoder and lexical fallback are alternative reranking routes. Registration-specific boosting/fee augmentation is conditional; all domains still use the shared reranking stage.
- The selector is heuristic, not an LLM judge. Expansion and ordering precede the whole-chunk budget.
- Output checks group generator-wrapper and pipeline operations; canonicalizing source IDs is not claim-level citation validation. Empty selection gives clarification; selected evidence still does not guarantee correctness.
- Dashed lines indicate index access, not an additional answer-generation route. The evaluation diagram is outside the live answer pipeline.

Code anchors: `src/pipeline.py`, retrieval/reranking/selection modules described in Section 4.4, and `scripts/run_simple_matched.py`. Constants and behavior are documented in the revised methodology rather than inferred from the diagrams alone.

## Evaluation integration

- Completed automatic scores: 180/180, 30 per system per measure. CivicRAG has higher custom binary context relevance; Simple RAG has higher mean faithfulness and answer relevancy. None is labelled factual accuracy.
- Paired bootstrap intervals are descriptive, with 2,000 resamples and the recorded seed; all three intervals include zero.
- Assistant-reviewed retrieval: overall and three per-domain tables. 26/30 eligible for Hit/Precision/MRR; 25 nonempty eligible pools for Recall/nDCG. These remain provisional and pooled, not independent human gold or corpus-wide recall.
- Separate overnight pool: 455 judgments, 88 uncertain, one scorable question. Completion is not full evaluation coverage.
- User-supplied qualitative examples are labelled separately because their response times differ from the frozen comparison. They are not silently inserted as benchmark rows or averaged with saved timings.

## Preserved constraints and remaining work

The original Abstract is byte-identical. All 43 official numbered headings and index order are checked with `scripts/check_thesis_template.py`. Author order remains Shihab, Araf, Tapu, Fahim, Zunaid. The original template and prior submissions are untouched. Chapter text avoids internal phase labels.

Remaining author confirmations are administrative details, survey recruitment/ethics information, and any independent factual review. Further experiments are not invented or required merely to fill tables; stronger accuracy/generalization claims would require new evidence. See `COMPLETION_CHECKLIST.md`.
