# Civic.ai thesis manuscript

Chapters 1-4 were revised on 2026-09-25 following the supplied rewrite brief. See `CHAPTERS_1_4_REVISION_2026_09_25.md` for verification and rollback. The Abstract and Chapters 5-6 are unchanged; completed evaluation artifacts still need to be incorporated into those later chapters. Docling is cited as related document-conversion work, not claimed as implemented without a conversion record.

Open `main.pdf` for the compiled thesis. `main.tex` is the entry point for the LaTeX source. The supplied template's original chapter/section/subsection names and index order are retained. Original inputs were not changed. `TEMPLATE_COMPLETION_MAP.md` identifies the remaining evidence needed in each original section and gives follow-up task prompts.

The Abstract is preserved byte-for-byte, including its keywords and LaTeX markup. The hash and implementation/data evidence are recorded in `evidence_manifest.json`.

This is a full working manuscript, not a claim that every submission requirement is complete. Read `COMPLETION_CHECKLIST.md` for the outstanding evaluation results, administrative details and author confirmations. Partial RAGAS scores are not presented as final results.

The pre-correction draft is preserved at Git revision `64d3650`. The original appendix titles are restored; the former project-specific appendices and question list remain available in `supplement/` and `generated/questions.tex`, outside the official index. New technical paragraph labels do not change the template's section numbering.

## Build

With Tectonic and the Times New Roman and Kohinoor Bangla fonts installed:

```sh
tectonic --keep-logs --keep-intermediates main.tex
```

XeLaTeX plus BibTeX is an alternative. A different computer may require changing the font names and reviewing the layout again. Architecture, preparation and evidence-linkage diagrams are drawn in LaTeX. Two survey charts and the corpus-distribution chart are included as vector PDFs generated from aggregate counts. No external image downloads are needed.

Chapter 4 now contains four figures, including an updated P2-style offline/online architecture and explicit differentiation of shared reranking from registration-only rules. See ARCHITECTURE_VERIFICATION.md for source/code mappings. These documentation changes do not alter the frozen chatbot or evaluation.

`SURVEY_ANALYSIS.md` documents the needs-analysis questionnaire and reproducible inclusion/counting rules. There are 79 consenting adult submissions in the primary analysis, with item-specific denominators. Only aggregate artifacts are distributed, not the private raw archive. The survey measures stated needs, not chatbot accuracy or demonstrated social impact.

From the repository root, `scripts/build_thesis_evidence.py` regenerates tables from the frozen evaluation artifacts and active corpus, verifies matched input hashes and checks the Abstract against the original local submission. The packaged source already includes the generated tables and can compile without rerunning that audit.

`dataset_catalog.json` lists the prepared source units, chunk IDs, available URLs and unresolved flags. `REFERENCE_AUDIT.md` explains bibliographic verification. Neither file certifies the currency of government requirements.
