# Thesis completion and verification checklist

## What this manuscript is

A full six-chapter working thesis preserving the supplied template's exact chapter/section/subsection headings and index order, with references, equations, an architecture diagram and reproducible tables. It is not yet submission-ready because the following items require real evidence or author confirmation. TEMPLATE_COMPLETION_MAP.md maps each original section to its evidence and remaining tasks.

The original Abstract file, including keywords and LaTeX markup, is byte-for-byte unchanged. The original submission and template folders were not edited.

## Required author information

- Confirm submission semester/month/year and degree wording. The old title page says June 2026, while its approval text says Summer/Fall 2025 and its copyright says 2024.
- Supply supervisor, any co-supervisor, coordinator and department-head names/designations. Do not treat blank approval fields as approval.
- Confirm all author names/IDs, team contribution allocation and acknowledgement wording.
- Review the AI-assistance disclosure and declaration against university policy. Signatures cannot be generated for the authors or committee.

## Required evaluation closure

Completed: 180/180 RAGAS/custom metric calculations, with 30 valid scores per system per measure. Chapters 5-6 include the final aggregates and paired intervals. Do not restart generation or evaluation merely to compile the thesis. To regenerate final tables from saved artifacts, run from the repository root:

```sh
python3 scripts/export_thesis_final_results.py
```

Then compile in this manuscript directory:

```sh
tectonic --keep-logs --keep-intermediates main.tex
```

Re-render the PDF and inspect tables, the Abstract and Bangla questions. Review the regenerated local-judge results before final submission. Self-judging Qwen3 is exploratory and does not replace factual review.

## Human review task (not fabricated or already completed)

Review all 30 paired outputs, preferably with system labels hidden and randomized order. For each answer record:

1. Relevance: does it answer the service/procedure requested? 0/1/2.
2. Factual support: are material claims and conditions supported by applicable corpus evidence? 0/1/2 or uncertain.
3. Completeness: are the essential requested steps/conditions covered? 0/1/2.
4. Material error, omission or truncation: describe it and cite chunk IDs.
5. Pairwise preference: A/B/tie/uncertain, with a reason.

Do not turn a preference for longer answers into a correctness label. Equally, do not dismiss a domain expert's coverage judgment just because an answer has cosmetic language errors. Resolve disagreement against the source and preserve the reasoning.

Suggested task prompt: "Review the two anonymized answers using the original Bangla question and applicable corpus passages. Score relevance, factual support and completeness separately. Preserve uncertainty about current official rules. Do not infer correctness from source IDs or identify a preferred system before checking both answers. Return labels and reasons for every question."

## Metrics intentionally not invented

- MRR@5, pooled nDCG@5, Hit@1/5, Precision@5 and pooled Recall@5 are now reported from assistant-reviewed labels, explicitly provisional. There are 26 eligible questions for Hit/Precision/MRR and 25 for Recall/nDCG. Independent expert labels and held-out questions remain necessary for stronger claims.
- The separate overnight pool has 455 completed judgments but 88 uncertain labels and only one scorable question. It is exploratory, not a substitute for the 30-question comparison.
- Reference semantic similarity or factual correctness: first write or approve evidence-backed reference answers. Do not treat another model's response as gold.
- User impact, time saved or post-use trust/satisfaction: requires a chatbot-use study and any necessary ethics approval. The supplied needs-analysis questionnaire now supports stated preferences only; see SURVEY_ANALYSIS.md.

## Needs-analysis confirmation

The survey is now incorporated under existing headings with two charts. Confirm recruitment, collection dates, invitation count, repeat-participation controls, form assignment and ethics/consent documentation. The main analysis excludes one non-consenting submission and holds out four minors and two missing-age submissions. Do not restore these held-out records without clarifying eligibility and consent. Raw survey responses remain private.
- Hardware efficiency/cost/carbon: requires controlled hardware records, utilization/power data or invoices. Existing saved latency alone is insufficient.

## Corpus version warning

The evaluated active corpus contains 187 registration, 361 passport and 3161 BRTA chunks (3709 total). The registration collection includes combined legal sources, but the study focuses on birth registration. Separate cleanup candidates exist (including 297 passport and 2795 BRTA chunks), but are not the corpus behind the main saved runs. Do not substitute candidate counts or claim they were active without a new manifest-backed run.

## Template adaptations

All six chapters and every original section/subsection title are retained, including the template's spelling. Dedication, Acknowledgment, Table of Contents and both original appendix titles are retained in their original order. Extra explanatory headings are unnumbered paragraphs and do not add index entries. Earlier project-specific appendix material is retained under supplement/ outside the template index. IEEE-style numeric citations use BibTeX/IEEEtran instead of Biber to compile with local Tectonic. XeTeX/fontspec supports Unicode text. Font names are local: Times New Roman and Kohinoor Bangla; another machine needs equivalent installed fonts, with layout rechecked.

Run `.venv/bin/python scripts/check_thesis_template.py` from the repository root after compiling to check all 43 original numbered headings, front-matter/appendix TOC order and the Abstract. Page numbers change automatically as writing is completed; the index hierarchy and names do not.

## Final claims

Do not use the earlier informal 3/30 versus 6/30 assistant counts as verified results. Do not claim universal superiority or 90--95% accuracy. The contribution is dataset development plus a developed, evaluated RAG system; comparison outcomes must follow the recorded evidence.
