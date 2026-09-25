"""Validate explicit assistant decisions and calculate provisional pooled metrics.

No inference, model loading, retrieval, or network calls. Labels are authored in
relevance_decisions.json, not inferred from citations, titles, or keyword matching.
"""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "docs/evaluation/current_30q_retrieval_only_2026_09_25"
METHODS = ("bm25_only", "dense_only", "hybrid_rrf")


def calculate(ids, relevant):
    hits = [int(cid in relevant) for cid in ids[:5]]
    dcg = sum(hit / math.log2(i + 2) for i, hit in enumerate(hits))
    ideal = sum(1 / math.log2(i + 2) for i in range(min(5, len(relevant))))
    return {
        "hit_at_1": float(bool(hits and hits[0])),
        "hit_at_5": float(any(hits)),
        "precision_at_5": sum(hits) / 5,
        "pooled_recall_at_5": len(set(ids[:5]) & relevant) / len(relevant) if relevant else None,
        "mrr_at_5": next((1 / (i + 1) for i, hit in enumerate(hits) if hit), 0.0),
        "pooled_ndcg_at_5": dcg / ideal if ideal else None,
    }


def main():
    assert calculate(["x", "a", "b"], {"a", "b", "c"})["precision_at_5"] == 0.4
    assert calculate(["x", "a", "b"], {"a", "b", "c"})["pooled_recall_at_5"] == 2 / 3
    assert calculate(["a"], {"a"})["pooled_ndcg_at_5"] == 1
    assert calculate(["x"], set())["pooled_recall_at_5"] is None
    results_path = DIRECTORY / "results.json"
    decisions_path = DIRECTORY / "relevance_decisions.json"
    rows = json.loads(results_path.read_text())
    decisions = json.loads(decisions_path.read_text())
    assert hashlib.sha256(results_path.read_bytes()).hexdigest() == decisions["results_sha256"], "Source changed; re-review decisions before resolving indices"
    assert set(decisions["questions"]) == {row["id"] for row in rows}
    catalog = {}
    for row in rows:
        domain_catalog = catalog.setdefault(row["domain"], {})
        for passages in row["top5_passages"].values():
            for passage in passages:
                old = domain_catalog.setdefault(passage["id"], passage)
                assert old["content"] == passage["content"]
    catalog = {domain: list(passages.values()) for domain, passages in catalog.items()}
    labelled = []
    question_metrics = []
    review = ["# Assistant relevance review: current 30 questions", "",
              "**AI-assisted, single-reviewer annotations. NOT human-verified gold labels.**", "",
              "Relevance means a passage contains a directly useful fact, requirement, form field, or step for the requested service and task. Partial and explicitly conditional evidence may count; irrelevant task matches and heading-only fragments do not. Relevance does not mean complete answer coverage, legal accuracy, or current policy.", "",
              "The assistant inspected saved source bodies/excerpts, including English answers where the source is bilingual. This was not a blinded independent study. Existing Qwen labels and generated answers were not used to assign these decisions. No local LLM or external judge was invoked by the exporter.", "",
              "For cost/duration questions, an unrelated fee/deadline is not relevant. First application, collection, renewal, replacement, instructor licensing and status lookup are distinguished. Forms count only when they supply requested-task fields or requirements. Conditional evidence must not be presented as universally applicable.", "",
              "A human reviewer should check uncertain cases, quoted support, legacy restrictions, and contradictory/OCR-damaged sources. Independent human approval is still pending for EVERY row."]
    for row in rows:
        decision = decisions["questions"][row["id"]]
        for method in METHODS:
            assert len(row["rankings"][method]) == len(set(row["rankings"][method]))
        passages = catalog[row["domain"]]
        index_by_id = {p["id"]: i for i, p in enumerate(passages)}
        pool = {p["id"] for items in row["top5_passages"].values() for p in items}
        expected_indices = {index_by_id[cid] for cid in pool}
        positive = {i: (quote, reason) for i, quote, reason in decision["relevant"]}
        uncertain = dict(decision.get("uncertain", []))
        negative = set(decision["irrelevant"])
        assert not (set(positive) & negative or set(positive) & set(uncertain) or negative & set(uncertain)), row["id"]
        assert set(positive) | negative | set(uncertain) == expected_indices, row["id"]
        review.extend(["", f"## {row['id']}", "", row["question"], ""])
        for index in sorted(expected_indices):
            passage = passages[index]
            if index in positive:
                label = "relevant"
                quote, reason = positive[index]
                assert quote and quote in passage["content"], (row["id"], index, quote)
            elif index in uncertain:
                label, quote, reason = "uncertain", "", uncertain[index]
            else:
                label, quote, reason = "irrelevant", "", decision["rejection_reason"]
            item = {"question_id": row["id"], "domain": row["domain"],
                    "question": row["question"], "chunk_id": passage["id"],
                    "domain_passage_index": index, "label": label,
                    "supporting_quote": quote, "reason": reason,
                    "reviewer": "Codex assistant", "human_verified": False,
                    "human_label": None,
                    "content_sha256": hashlib.sha256(passage["content"].encode()).hexdigest()}
            labelled.append(item)
            review.extend([f"### {label.upper()}: {passage['id']}", "", reason])
            if quote:
                review.extend(["", f"> {quote}"])
            review.extend(["", "<details><summary>Source passage for independent review</summary>", "", passage["content"], "", "</details>", ""])
        relevant_ids = {passages[i]["id"] for i in positive}
        question_metrics.append({"id": row["id"], "domain": row["domain"],
                                 "uncertain_count": len(uncertain),
                                 "relevant_in_pool": len(relevant_ids),
                                 "metrics": None if uncertain else {
                                     method: calculate(row["rankings"][method], relevant_ids)
                                     for method in METHODS}})
    counts = Counter(item["label"] for item in labelled)
    metadata = {
        "status": "ASSISTANT_REVIEWED_NOT_HUMAN_VERIFIED",
        "results_sha256": hashlib.sha256(results_path.read_bytes()).hexdigest(),
        "decisions_sha256": hashlib.sha256(decisions_path.read_bytes()).hexdigest(),
        "questions": len(rows), "unique_passages": sum(map(len, catalog.values())),
        "question_passage_pairs": len(labelled), "labels": dict(counts),
        "local_llm_calls": 0,
        "pool": "Union of each method's top five, separately for each question; not exhaustive corpus relevance.",
    }
    (DIRECTORY / "assistant_labels.json").write_text(json.dumps({"metadata": metadata, "labels": labelled}, ensure_ascii=False, indent=2))
    (DIRECTORY / "assistant_review.md").write_text("\n".join(review) + "\n")
    summary = {}
    for domain in [*catalog, "overall"]:
        subset = [q for q in question_metrics if domain == "overall" or q["domain"] == domain]
        eligible = [q for q in subset if q["metrics"] is not None]
        for method in METHODS:
            key = f"{domain}/{method}"
            means = {}
            ns = {}
            for metric in calculate([], set()):
                values = [q["metrics"][method][metric] for q in eligible if q["metrics"][method][metric] is not None]
                means[metric] = sum(values) / len(values) if values else None
                ns[metric] = len(values)
            summary[key] = {"total_questions": len(subset), "eligible_questions": len(eligible),
                            "mean": means, "denominator": ns}
    (DIRECTORY / "assistant_metrics.json").write_text(json.dumps({"metadata": metadata, "per_question": question_metrics, "summary": summary}, indent=2))
    report = ["# Provisional retrieval scores from assistant-reviewed labels", "",
              "**NOT human-verified results. Do not describe these as a manual expert benchmark or answer accuracy.**", "",
              f"Reviewed {len(labelled)} question/passage pairs across 30 questions and {metadata['unique_passages']} unique passages. Label counts: {dict(counts)}.",
              "Labels were authored by Codex in this conversation from saved passages. This is an unblinded single-AI review, not independent ground truth, and has not been validated against original government documents. No additional Ollama batch or external judge was called. The export/metric script itself uses only local validation and arithmetic; the annotation work was AI-assisted, not human or purely offline-script judging.", "",
              "Questions with ANY uncertain label are excluded consistently for ALL methods. For otherwise complete pools with no relevant passage, Hit/Precision/MRR are zero; pooled Recall/nDCG are undefined and omitted, with their smaller denominator shown. No unknown label is silently treated as irrelevant.", "",
              "| Domain | Method | Scored/total | Recall/nDCG N | Hit@1 | Hit@5 | Precision@5 | Pooled Recall@5 | MRR@5 | Pooled nDCG@5 |",
              "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for key, entry in summary.items():
        domain, method = key.split("/")
        values = ["N/A" if value is None else f"{value:.4f}" for value in entry["mean"].values()]
        report.append(f"| {domain} | {method} | {entry['eligible_questions']}/{entry['total_questions']} | {entry['denominator']['pooled_recall_at_5']} | " + " | ".join(values) + " |")
    report.extend(["", "## Required caveats", "",
                   "- Pooling only top-five results misses relevant passages that none of these retrievers found. Pooled recall is NOT corpus recall. Nonempty pools are not proof of full answer coverage.",
                   "- Conditional, partial, and legacy MRP evidence can be relevant to an unspecified passport question. It must retain those conditions in any answer. Broad question interpretation is a subjective annotation choice.",
                   "- Passage IDs, including near-duplicates, are the scoring unit. Redundant evidence can affect precision and pooled recall. No fact-level deduplication or reference-answer evaluation was performed.",
                   "- Precision divides relevant top-five IDs by five. MRR is truncated at five. nDCG uses binary relevance and an ideal ordering of up to five known pooled relevant IDs.",
                   "- This evaluates BM25/dense/RRF BEFORE reranking, boosts and evidence selection. It does not compare the complete Simple RAG and CivicRAG answer pipelines.",
                   "- Reused development questions, small samples, subjective labels and correlated passages limit conclusions. No superiority, legal accuracy or generalization claim is established.",
                   "", "## Questions needing adjudication", ""])
    for q in question_metrics:
        if q["uncertain_count"]:
            report.append(f"- {q['id']}: {q['uncertain_count']} uncertain label(s); excluded for all three retrievers.")
        elif not q["relevant_in_pool"]:
            report.append(f"- {q['id']}: no useful passage identified in the pool; this does NOT prove the whole database lacks an answer.")
    report.extend(["", "## Review files", "",
                   "- `assistant_review.md`: each decision, quote, and expandable source passage.",
                   "- `assistant_labels.json`: stable chunk IDs, exact quotes, content hashes, and empty human approval fields.",
                   "- `relevance_decisions.json`: explicit assistant-authored decisions; no automatic keyword label assignment.",
                   "- `assistant_metrics.json`: per-question metrics, exclusions and denominators.",
                   "- These files are separate from the earlier Qwen draft-labeling job; none of that job's labels were reused or changed."])
    (DIRECTORY / "assistant_metrics_report.md").write_text("\n".join(report) + "\n")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
