"""Plot the frozen thesis inventory, not a newly rebuilt index."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1] / "docs/thesis_final_2026_09_24"
corpus = json.loads((BASE / "evidence_manifest.json").read_text())["corpus"]
keys = ["birth_death_registration", "passport", "brta"]
labels = ["Birth/death", "Passport", "BRTA"]
counts = [corpus[k]["chunks"] for k in keys]
sources = [corpus[k]["source_units"] for k in keys]
assert sum(counts) == 3709
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "pdf.fonttype": 42})
fig, axes = plt.subplots(1, 2, figsize=(9, 4.5))
colors = ["#AD721B", "#345B89", "#167D8D"]
axes[0].pie(counts, colors=colors, startangle=90, wedgeprops={"width": .38, "edgecolor": "white"})
axes[0].text(0, 0, "3,709\nactive chunks", ha="center", va="center", weight="bold")
axes[0].set_title("Share of indexed chunks")
axes[0].legend([f"{s}: {n:,} ({100*n/sum(counts):.1f}%)" for s, n in zip(labels, counts)], loc="lower center", bbox_to_anchor=(.5, -.2), frameon=False)
axes[1].barh(labels, sources, color=colors)
for y, n in enumerate(sources):
    axes[1].text(n + 2, y, str(n), va="center")
axes[1].invert_yaxis()
axes[1].set_xlim(0, 150)
axes[1].set_xlabel("Prepared source units")
axes[1].set_title("Source-unit inventory")
axes[1].spines[["top", "right"]].set_visible(False)
fig.tight_layout(pad=2.0)
fig.savefig(BASE / "generated/corpus_distribution.pdf", bbox_inches="tight")
