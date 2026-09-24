# Thesis completion and verification checklist

## What this manuscript is

A full six-chapter working thesis in the supplied template's chapter order, with revised front matter, references, equations, an architecture diagram and reproducible tables. It is not yet submission-ready because the following items require real evidence or author confirmation.

The original Abstract file, including keywords and LaTeX markup, is byte-for-byte unchanged. The original submission and template folders were not edited.

## Required author information

- Confirm submission semester/month/year and degree wording. The old title page says June 2026, while its approval text says Summer/Fall 2025 and its copyright says 2024.
- Supply supervisor, any co-supervisor, coordinator and department-head names/designations. Do not treat blank approval fields as approval.
- Confirm all author names/IDs, team contribution allocation and acknowledgement wording.
- Review the AI-assistance disclosure and declaration against university policy. Signatures cannot be generated for the authors or committee.

## Required evaluation closure

The RAGAS job is independent of this writing task and should not be restarted merely to update the thesis. Inspect:

`docs/evaluation/ragas_comparison_2026_09_24/completion.json`

If it is absent, inspect progress.json and failure.json plus `/tmp/civic-ragas-eval.log`. A metric attempt is not a correct answer. The complete workload is 180 attempts: 30 questions x 2 systems x 3 metrics. The thesis generation script excludes partial headline scores.

After completion, from the repository root:

```sh
.venv/bin/python scripts/build_thesis_evidence.py
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

- MRR, nDCG, Hit/Recall@k: first annotate relevant chunk IDs (including multiple relevant chunks where needed). Use a held-out set for generalization claims.
- Reference semantic similarity or factual correctness: first write or approve evidence-backed reference answers. Do not treat another model's response as gold.
- User impact, time saved, trust or satisfaction: requires an actual participant study and any necessary ethics approval.
- Hardware efficiency/cost/carbon: requires controlled hardware records, utilization/power data or invoices. Existing saved latency alone is insufficient.

## Corpus version warning

The evaluated active corpus contains 187 birth/death, 361 passport and 3161 BRTA chunks (3709 total). Separate cleanup candidates exist (including 297 passport and 2795 BRTA chunks), but are not the corpus behind the main saved runs. Do not substitute candidate counts or claim they were active without a new manifest-backed run.

## Template adaptations

Six required chapters and front-matter order retained; optional dedication omitted. Example appendices about installing LaTeX/Overleaf replaced with project reproducibility and completion requirements. IEEE-style numeric citations retained via BibTeX/IEEEtran instead of Biber, to compile with local Tectonic. XeTeX/fontspec enables the Bangla question appendix. Font names are local: Times New Roman and Kohinoor Bangla; another machine needs equivalent installed fonts, with layout rechecked.

## Final claims

Do not use the earlier informal 3/30 versus 6/30 assistant counts as verified results. Do not claim universal superiority or 90--95% accuracy. The contribution is dataset development plus a developed, evaluated RAG system; comparison outcomes must follow the recorded evidence.
