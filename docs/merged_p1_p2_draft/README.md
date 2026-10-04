# P1 + P2 Merged Thesis Draft

This folder contains a first merged draft built from:

- P1 LaTeX attachment: `/Users/shihab/.codex/attachments/9fe5387a-808a-4ab3-8d1d-45f6f0783a56/pasted-text.txt`
- Edited P2 PDF: `/Users/shihab/01 Thesis/Rag/miscellaneous /p2 write update/my edited p2 review - formula fixed compact.pdf`
- Corrected Phase 2 Chapter 4 source: `docs/p2_phase2_update/chapter_4_completed.tex`

## Files

- `main_p1_p2_merged.tex`: standalone XeLaTeX entry point.
- `chapters/chapter_1.tex`: revised P1 introduction/problem/objectives.
- `chapters/chapter_2.tex`: revised P1 literature review aligned with the current RAG thesis direction.
- `chapters/chapter_3.tex`: current Phase 2 methodology/evaluation chapter.
- `bibliography/references.bib`: unified references for the merged draft.
- `images/civicrag_architecture_diagram.png`: architecture figure used in Chapter 4.

## Compile

Use XeLaTeX-compatible compilation. This local draft is configured with `biblatex` + BibTeX backend so it can compile with Tectonic:

```bash
tectonic main_p1_p2_merged.tex
```

If you switch the backend back to `biber` in Overleaf, compile with:

```bash
xelatex main_p1_p2_merged.tex
biber main_p1_p2_merged
xelatex main_p1_p2_merged.tex
xelatex main_p1_p2_merged.tex
```
