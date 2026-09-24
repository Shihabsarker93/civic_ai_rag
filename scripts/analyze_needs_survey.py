"""Aggregate private nested survey exports; never publish respondent-level records."""
import argparse
import collections
import csv
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/thesis_final_2026_09_24/generated"
ITEMS = {
    "willingness": (37, {"করতাম": "Would use", "করতাম না": "Would not use", "নিশ্চিত নই": "Unsure"}),
    "verified_trust": (39, {"হ্যাঁ": "Yes", "না": "No", "আমি আবার যাচাই করে নিবো": "Would recheck"}),
    "language": (40, {"হ্যাঁ": "Bangla more comfortable", "না": "No", "ইংরেজি বা বাংলা যেকোনো একটি হলেই হবে": "Either Bangla or English"}),
    "recommendation": (43, {"হ্যাঁ, দিবো": "Yes, if it works well", "হয়তো দিবো": "Maybe"}),
    "payment": (45, {"শুধুমাত্র বিনামূল্যে হলে ব্যবহার করব": "Free only", "দ্রুত ও নিরাপদ সেবা হলে টাকা দিতে আগ্রহী": "Would pay if fast and secure"}),
}
MULTI = {
    "features": (38, {
        "কোন কোন নথি/তথ্য দরকার জানানো": "Required documents / information",
        "অনলাইন ফর্ম সঠিকভাবে পূরণে সাহায্য করা": "Help completing online forms",
        "আপলোড করা নথি সঠিক কিনা যাচাই করা": "Check uploaded documents",
        "পেমেন্ট বা অ্যাপয়েন্টমেন্ট সম্পর্কিত তথ্য দিয়ে সাহায্য করা": "Payment / appointment information",
    }),
    "trust_factors": (42, {
        "সরকারি লোগো/অফিসিয়াল ওয়েবসাইট লিংক": "Official logo / website link",
        "নিরাপদ তথ্য ব্যবস্থাপনা": "Secure information handling",
        "সহজ ও স্পষ্ট ভাষা": "Simple and clear language",
        "২৪/৭ সহায়তা": "24/7 assistance",
        "প্রয়োজনে বাস্তব কর্মকর্তার সঙ্গে যোগাযোগের সুযোগ": "Access to a real official",
    }),
}


def summarize(rows):
    result = {"n": len(rows), "items": {}}
    for key, (index, mapping) in (ITEMS | MULTI).items():
        values = [r[index] for r in rows if r[index]]
        counts = collections.Counter()
        other = all_options = 0
        for value in values:
            tokens = set(t.strip() for t in value.split(";") if t.strip()) if key in MULTI else {value}
            for token in tokens:
                if token in mapping:
                    counts[mapping[token]] += 1
            other += bool(tokens - mapping.keys())
            all_options += "সবগুলো" in tokens
        result["items"][key] = {
            "valid_n": len(values), "missing_n": len(rows) - len(values),
            "counts": {label: counts[label] for label in mapping.values()},
            "other_response_n": other, "unexpanded_all_options_n": all_options,
        }
    result["age_counts"] = dict(collections.Counter(r[2] for r in rows))
    result["student_n"] = sum("শিক্ষার্থী" in r[4] or "ছাত্র" in r[4] for r in rows)
    result["gender_counts"] = dict(collections.Counter(r[3] for r in rows))
    return result


def pct(item, label):
    return f'{item["counts"][label]}/{item["valid_n"]} ({100 * item["counts"][label] / item["valid_n"]:.1f}\\%)'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    records, forms = [], []
    with zipfile.ZipFile(args.archive) as outer:
        for name in sorted(outer.namelist()):
            if not name.endswith(".csv.zip") or name.startswith("__MACOSX/"):
                continue
            version = int(re.search(r"form (\d)", name).group(1))
            with zipfile.ZipFile(io.BytesIO(outer.read(name))) as inner:
                csv_name = next(n for n in inner.namelist() if n.endswith(".csv"))
                data = list(csv.reader(io.StringIO(inner.read(csv_name).decode("utf-8-sig"))))
            assert len(data[0]) == 46
            rows = [[v.strip() for v in row] for row in data[1:]]
            assert all(len(row) == 46 for row in rows)
            forms.append({"form": version, "submitted": len(rows)})
            # Canonical order: common fields, birth, passport, BRTA, common AI block.
            slices = {1: [(7, 15), (15, 26), (26, 37)], 2: [(18, 26), (26, 37), (7, 18)], 3: [(29, 37), (7, 18), (18, 29)]}[version]
            for row in rows:
                canonical = row[:7] + sum((row[a:b] for a, b in slices), []) + row[37:]
                records.append(canonical)
    consented = [r for r in records if r[1] == "হ্যাঁ, সম্মতি দিচ্ছি"]
    # Deduplicate identical submissions only, never infer participant identity.
    unique = list({tuple(r): r for r in consented}.values())
    adults = [r for r in unique if r[2] and r[2] != "১৮ বছরের নিচে"]
    age_options = {r[2] for r in adults}
    assert age_options <= {"১৮ - ২৫ বছর", "২৬ - ৩৫ বছর", "৩৬ - ৫০ বছর", "৫০ বছরের বেশি"}, age_options
    report = {
        "archive_sha256": hashlib.sha256(args.archive.read_bytes()).hexdigest(),
        "forms": forms, "submitted_n": len(records), "consented_n": len(consented),
        "nonconsenting_excluded_n": len(records) - len(consented),
        "identical_consented_duplicates_removed_n": len(consented) - len(unique),
        "consented_under18_held_out_n": sum(r[2] == "১৮ বছরের নিচে" for r in unique),
        "consented_age_missing_held_out_n": sum(not r[2] for r in unique),
        "primary": summarize(adults),
        "policy": "Confirmed adults with affirmative consent only. Percentages use nonblank item denominators. Multi-select explicit choices only; all-options text is not expanded. No unique-person or population claim. Raw/free-text data remain private.",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "survey_aggregate.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    items = report["primary"]["items"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "pdf.fonttype": 42})
    fig, axes = plt.subplots(2, 1, figsize=(8.2, 6.1))
    for ax, key, title in zip(axes, ["willingness", "verified_trust"], ["Would use an AI information assistant instead of an intermediary", "Trust if the assistant provides verified information"]):
        item = items[key]
        labels, counts = list(item["counts"]), list(item["counts"].values())
        values = [100 * n / item["valid_n"] for n in counts]
        ax.barh(labels, values, color=["#187b80", "#9c5353", "#6d7c8c"])
        for y, (n, value) in enumerate(zip(counts, values)):
            ax.text(value + 1, y, f"{n}/{item['valid_n']} ({value:.1f}%)", va="center", fontsize=10)
        ax.set_xlim(0, 105)
        ax.invert_yaxis()
        ax.set_title(title, loc="left", fontsize=11, weight="bold", pad=12)
        ax.set_xlabel("Percentage of valid item responses")
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(pad=1.5)
    fig.savefig(OUT / "survey_willingness_trust.pdf", bbox_inches="tight")
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8.2, 3.5))
    item = items["features"]
    counts = list(item["counts"].values())
    values = [100 * n / item["valid_n"] for n in counts]
    ax.barh(list(item["counts"]), values, color="#187b80")
    for y, (n, value) in enumerate(zip(counts, values)):
        ax.text(value + 1, y, f"{n}/{item['valid_n']} ({value:.1f}%)", va="center", fontsize=10)
    ax.set_xlim(0, 113)
    ax.invert_yaxis()
    ax.set_xlabel("Explicit selections (% of valid item responses; multiple choices)")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "survey_features.pdf", bbox_inches="tight")
    plt.close(fig)
    table = [r"\begin{table}[htbp]\centering\small", r"\caption{Needs-analysis responses among consenting adults. Denominators exclude blank answers to each item.}\label{tab:needs-survey}", r"\begin{tabularx}{\linewidth}{Xr}\toprule", r"Response & Count / valid responses (percentage)\\\midrule"]
    for key, label, text in [
        ("willingness", "Would use", "Would use the proposed AI assistant"),
        ("willingness", "Would not use", "Would not use it"),
        ("willingness", "Unsure", "Unsure about using it"),
        ("verified_trust", "Would recheck", "Would recheck even verified information"),
        ("language", "Bangla more comfortable", "Bangla would be more comfortable"),
        ("language", "Either Bangla or English", "Either Bangla or English acceptable"),
        ("recommendation", "Yes, if it works well", "Would recommend if it works well"),
    ]:
        table.append(text + " & " + pct(items[key], label) + r"\\")
    table += [r"\bottomrule\end{tabularx}\end{table}"]
    (OUT / "survey_table.tex").write_text("\n".join(table) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
