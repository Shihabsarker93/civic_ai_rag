# Civic.ai thesis manuscript

All six chapters were revised on 2026-09-25 following the supplied briefs. See `FINAL_REVISION_2026_09_25.md` for the latest integration and diagram audit; `CHAPTERS_1_4_REVISION_2026_09_25.md` records the earlier revision. The Abstract remains unchanged. Completed RAGAS results, provisional retrieval metrics and exploratory passage judgments are now incorporated into Chapters 5-6. Docling is related work, not claimed as implemented without a conversion record.

Open `main.pdf` for the compiled thesis. `main.tex` is the entry point for the LaTeX source. The supplied template's original chapter/section/subsection names and index order are retained. Original inputs were not changed. `TEMPLATE_COMPLETION_MAP.md` identifies the remaining evidence needed in each original section and gives follow-up task prompts.

The Abstract is preserved byte-for-byte, including its keywords and LaTeX markup. The hash and implementation/data evidence are recorded in `evidence_manifest.json`.

This is a full working manuscript, not a claim that every submission requirement is complete. Read `COMPLETION_CHECKLIST.md` for administrative confirmations and the limits of automatic/assistant evaluation. All 180 automatic metric calculations are complete; independent factual correctness is not established by those scores.

The pre-correction draft is preserved at Git revision `64d3650`. The original appendix titles are restored; the former project-specific appendices and question list remain available in `supplement/` and `generated/questions.tex`, outside the official index. New technical paragraph labels do not change the template's section numbering.

## Build

With Tectonic and the Times New Roman and Kohinoor Bangla fonts installed:

```sh
tectonic --keep-logs --keep-intermediates main.tex
```

XeLaTeX plus BibTeX is an alternative. A different computer may require changing the font names and reviewing the layout again. Architecture exports are included as PNG/SVG; preparation and evidence-linkage figures use LaTeX. Survey, corpus and evaluation charts are included as vector PDFs. No external image downloads are needed.

Chapter 4 contains six figures. Section 4.2 presents the offline/online architecture, generation flow and evaluation boundaries. Section 4.4 maps these to implementation modules. These documentation changes do not alter the frozen chatbot or evaluation.

`SURVEY_ANALYSIS.md` documents the needs-analysis questionnaire and reproducible inclusion/counting rules. There are 79 consenting adult submissions in the primary analysis, with item-specific denominators. Only aggregate artifacts are distributed, not the private raw archive. The survey measures stated needs, not chatbot accuracy or demonstrated social impact.

From the repository root, `scripts/build_thesis_evidence.py` regenerates tables from the frozen evaluation artifacts and active corpus, verifies matched input hashes and checks the Abstract against the original local submission. The packaged source already includes the generated tables and can compile without rerunning that audit.

`python3 scripts/export_thesis_final_results.py` exports the final score tables and architecture panels from saved artifacts without model calls. The editable master diagram is under `docs/architecture/final_2026_09_25/` in the repository.

`dataset_catalog.json` lists the prepared source units, chunk IDs, available URLs and unresolved flags. `REFERENCE_AUDIT.md` explains bibliographic verification. Neither file certifies the currency of government requirements.
