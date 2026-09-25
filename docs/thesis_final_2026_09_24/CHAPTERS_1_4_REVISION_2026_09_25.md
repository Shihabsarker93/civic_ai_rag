# Chapters 1-4 revision

## Scope

- Rewritten Chapters 1-3 and revised Chapter 4 against the supplied brief.
- Rollback: `codex/pre-chapters1-4-rewrite-20260925` at `6ffb99a`.
- Chapter 4 is stored in `chapters/chapter_5.tex`, following the original template mapping. This is not Result Analysis.
- Result Analysis (`chapters/chapter_6.tex`), Conclusion (`chapters/chapter_9.tex`), Abstract, main chapter order and author order were not edited.
- No chatbot, configuration, corpus, saved answer or metric changed. No LLM run launched.

## Improvements

- Connected introduction, separate research/system objectives, survey-to-design rationale and explicit current/future scope.
- Comparative literature discussion, with NextRAG as inspiration rather than a cross-dataset performance baseline.
- ChromaDB cited at first meaningful appearance; Docling citation added with verified-use boundary.
- Functional/non-functional/software/resource requirements separated inside the original section.
- Chapter 3 placeholders replaced by documented Git milestones and realistic resource/cost discussion. No historical hours, responsibilities, measured costs or citizen savings invented.
- Chapter 4 retains four figures and equations, adds design-decision justification, and follows one saved Bangla query through the pipeline.
- Hybrid design rationale is distinguished from measured superiority. Registration-only adjustments remain separate from shared reranking.

## Evidence

Implementation and corpus hashes still match `evidence_manifest.json`. Main files checked: `src/pipeline.py`, `src/generation/ollama_generator.py`, retrieval/reranking/selection modules, index builders and the matched baseline runner.

Running example: `docs/evaluation/chunk_order_fixed_qwen3_30q_2026_09_23/answers.json`, row `brta_05_test`. Verified six contexts, 5,770 selected characters, service `licence`, no action label, no family expansion, route `llm_selected_evidence`, normal stop. The excerpt is a recorded response, not a gold answer. Illustrative RRF arithmetic is not presented as this row's observed scores.

Survey counts retain the existing aggregate analysis and item-specific denominators. Active corpus counts remain 187 birth/death, 361 passport and 3,161 BRTA chunks. Management dates come from recorded Git revisions.

## Docling

No usage was established by searches of scripts, source, requirements, manuscript/P2 files or supplied Markdown. Docling is discussed as a relevant document-conversion framework, not inserted into the implemented architecture. Author confirmation or conversion records are needed before attributing specific derivatives to it.

References checked: https://arxiv.org/abs/2408.09869 and https://docs.trychroma.com/docs/collections/add-data. TraSe and HybridRAG-BN entries were rechecked against ACL/arXiv.

## Validation

- Chapter/section/subsection headings and sequence match the original supplied template, allowing whitespace normalization.
- Abstract unchanged against original submission and pre-edit Git revision: SHA-256 `802f7c1f4f4f78752e9f1e5ce7b1baf6bb6dac64fde3234d984b25947e8901ac`.
- Result Analysis, Conclusion and `main.tex` remain byte-identical to rollback revision.
- Tectonic/BibTeX compilation succeeded without unresolved citations/references, missing glyph warnings or overfull boxes. Underfull spacing and system-font portability warnings remain.
- Rendered and inspected all 31 body pages covering Chapters 1-4, including figures, equations and Bangla example.
- Full compiled PDF: 58 pages. Chapters 5-6 retain their previous wording and still need the separate results/conclusion update; this is not a submission-final certification.

## Next pass

Incorporate completed evaluation into Chapters 5-6, preserving distinctions between RAGAS, custom metrics and assistant-reviewed retrieval labels. Confirm remaining administrative details separately. No new experiments were required for this writing pass.
