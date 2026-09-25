"""Export saved metrics and diagram source views; never call a model."""
import json
from pathlib import Path
from xml.etree import ElementTree as ET
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/thesis_final_2026_09_24"
OUT = BASE / "generated"
EV = ROOT / "docs/evaluation"


def table(name, caption, label, headers, rows, columns):
    text = [r"\begin{table}[htbp]\centering\small",
            "\\caption{" + caption + "}\\label{" + label + "}",
            "\\begin{tabularx}{\\linewidth}{" + columns + "}\\toprule",
            " & ".join(headers) + r"\\\midrule"]
    text.extend(" & ".join(map(str, row)) + r"\\" for row in rows)
    text.append(r"\bottomrule\end{tabularx}\end{table}")
    (OUT / name).write_text("\n".join(text) + "\n")


def main():
    OUT.mkdir(exist_ok=True)
    summary = json.loads((EV / "ragas_comparison_2026_09_24/ragas_summary.json").read_text())
    names = {"faithfulness": "Faithfulness", "answer_relevancy": "Answer relevancy",
             "context_relevance_binary": "Custom context relevance"}
    rows, intervals = [], []
    for metric, label in names.items():
        s, c = (summary["systems"][x][metric] for x in ("simple", "civic"))
        assert s["valid"] == c["valid"] == 30 and s["failed"] == c["failed"] == 0
        pair = summary["paired_civic_minus_simple"][metric]
        rows.append([label, f'{s["mean"]:.4f}', f'{c["mean"]:.4f}',
                     f'{pair["mean_difference"]:+.4f}', "30"])
        lo, hi = pair["bootstrap_95_percent_interval"]
        intervals.append([label, f'{pair["mean_difference"]:+.4f}', f'[{lo:.4f}, {hi:.4f}]'])
    table("ragas_final.tex", "Completed saved-answer evaluation: Qwen3 self-judge scores, not independent accuracy.",
          "tab:ragas-final", ["Metric", "Simple", "CivicRAG", r"$\Delta$", "Pairs"], rows, "Xrrrr")
    table("ragas_intervals.tex", "Paired CivicRAG minus Simple RAG differences with descriptive bootstrap intervals.",
          "tab:ragas-intervals", ["Metric", r"Mean $\Delta$", r"95\% interval"], intervals, "Xrr")
    retrieval = json.loads((EV / "current_30q_retrieval_only_2026_09_25/assistant_metrics.json").read_text())["summary"]
    methods = {"bm25_only": "BM25", "dense_only": "Dense", "hybrid_rrf": "Hybrid RRF"}
    keys = ["hit_at_1", "hit_at_5", "precision_at_5", "pooled_recall_at_5", "mrr_at_5", "pooled_ndcg_at_5"]
    for domain, label in [("overall", "Overall"), ("passport", "Passport"),
                          ("birth_death_registration", "Birth registration"), ("brta", "BRTA")]:
        rows = []
        for method, display in methods.items():
            r = retrieval[f"{domain}/{method}"]
            rows.append([display] + [f'{r["mean"][k]:.4f}' for k in keys])
        n = r["eligible_questions"]
        nr = r["denominator"]["pooled_recall_at_5"]
        caption = (f"{label}: provisional retrieval-only scores with assistant-reviewed labels. "
                   f"Hit, precision and MRR use {n} questions; pooled recall and nDCG use {nr}.")
        table(f"retrieval_{domain}.tex", caption, f"tab:retrieval-{domain}",
              ["Method", "H@1", "H@5", "P@5", "R@5*", "MRR@5", "nDCG@5*"],
              rows, "Xrrrrrr")
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "pdf.fonttype": 42})
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    xs = list(range(3))
    for offset, system, color in [(-.18, "simple", "#345B89"), (.18, "civic", "#167D8D")]:
        vals = [summary["systems"][system][m]["mean"] for m in names]
        bars = ax.bar([x + offset for x in xs], vals, .34, label="Simple RAG" if system == "simple" else "CivicRAG", color=color)
        ax.bar_label(bars, fmt="%.3f", padding=3, fontsize=9)
    ax.set_xticks(xs, ["Faithfulness", "Answer relevancy", "Custom context\nrelevance (binary)"])
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("Mean self-judge score")
    ax.legend(loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "ragas_final_chart.pdf", bbox_inches="tight")
    plt.close(fig)
    # Reframe editable vector source, not the user's raster originals.
    source = ROOT / "docs/architecture/final_2026_09_25"
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    for file, name, view in [
        ("civicrag_final_architecture", "architecture_retrieval", (30, 130, 1740, 775)),
        ("civicrag_final_architecture", "architecture_generation", (30, 925, 1740, 390)),
        ("evaluation_boundaries", "evaluation_design", (30, 140, 1740, 950)),
    ]:
        svg = ET.parse(source / (file + ".svg"))
        x, y, w, h = view
        svg.getroot().set("viewBox", f"{x} {y} {w} {h}")
        svg.getroot().set("width", str(w))
        svg.getroot().set("height", str(h))
        svg.write(OUT / (name + ".svg"), encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
