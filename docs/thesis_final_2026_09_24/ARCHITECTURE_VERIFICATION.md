# Chapter 4 architecture verification

Documentation-only revision after c09fc42. No runtime code, prompt, model, corpus, evaluation answers or ongoing metric job was changed.

## P2 sources inspected

The authors' `submited so far/chapters/chapter_5.tex` includes `methodology_final.jpg` and `data_clean_diagram.jpg`. The methodology image was visually inspected from `images/methodology_final.jpg`. Its offline/online organization is retained as a design reference, not copied unchanged as the current architecture: it lacks the post-P2 selector and shows the legacy safe-answer route.

## Figures

1. Updated offline indexing / online three-domain architecture. Dashed edges are index access; solid edges are processing flow. Birth/death-only adjustments are separate from shared reranking.
2. Preparation and provenance flow. No universal automated OCR repair or Bijoy conversion claim.
3. Chunk ID / retrieval text / source evidence / metadata linkage. Chroma stores evidence as documents alongside the embedded retrieval text; runtime lookup uses IDs and the active chunk map.
4. Corpus donut and source-unit bar chart, generated from the frozen evidence_manifest.json by scripts/plot_thesis_corpus.py. Not a demand or accuracy chart.

## Code mapping

- `src/pipeline.py:24`: birth_death_rules is a domain equality test.
- `src/pipeline.py:45-54`: all configured domains receive HybridReranker; only domain_boosts uses the birth/death flag. Shared pipelines reuse the cross-encoder.
- `src/reranking/reranker.py:45-77`: cross-encoder or lexical fallback scoring.
- `src/reranking/reranker.py:79`: early return disables extra registration rules, not the preceding reranker.
- `src/pipeline.py:115-122`: selected-evidence path; domain-conditional augmentation followed by shared selection.
- `src/pipeline.py:448-467`: existing correction-fee supplementation, deduplicated by chunk ID.
- `src/generation/evidence_selection.py:119` onwards: reusable service/action/product/location rules, 3A+S+2T initial priority, compatible-family ordering and six-chunk/14,000-character budgeting.
- `scripts/build_index.py`: embeds retrieval_text, stores content as Chroma documents.

The added formulas describe these operations, not a newly optimized or trained algorithm. The extra registration rules are inherited domain-specific engineering. Their isolated performance benefit is not established without an ablation. Passport/BRTA retain dense+BM25, RRF, reranking and the shared selector.

All 43 original numbered headings, TOC hierarchy and original Abstract bytes must pass scripts/check_thesis_template.py after compilation. Page numbers and figure lists update automatically.
