# Civic.ai thesis manuscript

Open `main.pdf` for the compiled thesis. `main.tex` is the entry point for the LaTeX source. The supplied template's six-chapter structure is retained. Original inputs were not changed.

The Abstract is preserved byte-for-byte, including its keywords and LaTeX markup. The hash and implementation/data evidence are recorded in `evidence_manifest.json`.

This is a full working manuscript, not a claim that every submission requirement is complete. Read `COMPLETION_CHECKLIST.md` for the outstanding evaluation results, administrative details and author confirmations. Partial RAGAS scores are not presented as final results.

## Build

With Tectonic and the Times New Roman and Kohinoor Bangla fonts installed:

```sh
tectonic --keep-logs --keep-intermediates main.tex
```

XeLaTeX plus BibTeX is an alternative. A different computer may require changing the font names and reviewing the layout again. All figures are drawn in LaTeX; no external image downloads are needed.

From the repository root, `scripts/build_thesis_evidence.py` regenerates tables from the frozen evaluation artifacts and active corpus, verifies matched input hashes and checks the Abstract against the original local submission. The packaged source already includes the generated tables and can compile without rerunning that audit.

`dataset_catalog.json` lists the prepared source units, chunk IDs, available URLs and unresolved flags. `REFERENCE_AUDIT.md` explains bibliographic verification. Neither file certifies the currency of government requirements.
