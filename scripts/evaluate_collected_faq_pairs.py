from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.metrics import ndcg_at_k, reciprocal_rank, token_f1
from src.pipeline import CivicRAGPipeline
from src.retrieval.hybrid_retriever import RetrievalResult

DEFAULT_CONFIG = PROJECT_ROOT / "domains/birth_death_registration/config.json"
DEFAULT_INPUT = PROJECT_ROOT / "docs/evaluation/collected_faq_pairs_2026_06_09/collected_faq_pairs_extracted.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "docs/evaluation/collected_faq_pairs_2026_06_09"


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    chunk_id: str
    category: str
    variant: str
    query: str
    expected_answer: str


def load_records(path: Path) -> list[dict[str, Any]]:
    """Load the normalized JSON extracted from the user's collected FAQ file."""
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError(f"Expected a list of records in {path}")
    required = {"chunk_id", "question", "answer"}
    for index, record in enumerate(records, start=1):
        missing = required - set(record)
        if missing:
            raise ValueError(f"Record {index} is missing required fields: {sorted(missing)}")
    return records


def build_cases(records: list[dict[str, Any]]) -> list[EvalCase]:
    cases: list[EvalCase] = []
    for record in records:
        chunk_id = str(record["chunk_id"]).strip()
        category = str(record.get("category", "")).strip()
        expected_answer = str(record.get("answer", "")).strip()
        variants = [
            ("curated_question", str(record.get("question", "")).strip()),
            ("original_question", str(record.get("original_question", "")).strip()),
        ]
        for variant, query in variants:
            if not query:
                continue
            cases.append(
                EvalCase(
                    case_id=f"{chunk_id}::{variant}",
                    chunk_id=chunk_id,
                    category=category,
                    variant=variant,
                    query=query,
                    expected_answer=expected_answer,
                )
            )
    return cases


def extract_answer_like_text(content: str) -> str:
    match = re.search(r"(?s)(?:^|\n)Answer:\s*(.*?)(?:\n(?:Legal references|Keywords BN|Keywords EN|Source URL|Service):|$)", content)
    if match:
        return match.group(1).strip()
    match = re.search(r"(?s)(?:^|\n)Content:\s*(.*)$", content)
    if match:
        return match.group(1).strip()
    return content.strip()


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 0.0
    return float(np.dot(a, b) / denominator)


class EmbeddingSimilarityCache:
    def __init__(self, pipeline: CivicRAGPipeline) -> None:
        self.pipeline = pipeline
        self.cache: dict[str, np.ndarray] = {}

    def _embed(self, text: str) -> np.ndarray:
        if text not in self.cache:
            embedding = self.pipeline.retriever.embedding_model.encode(
                [text],
                normalize_embeddings=True,
                show_progress_bar=False,
            )[0]
            self.cache[text] = np.asarray(embedding)
        return self.cache[text]

    def similarity(self, left: str, right: str) -> float:
        if not left.strip() or not right.strip():
            return 0.0
        return cosine_similarity(self._embed(left), self._embed(right))


def retrieve_with_method(pipeline: CivicRAGPipeline, query: str, method: str) -> list[RetrievalResult]:
    if method == "dense_only":
        return pipeline.retriever.dense_only_search(query, top_k=pipeline.reranking_config["top_k"])
    if method == "bm25_only":
        return pipeline.retriever.bm25_only_search(query, top_k=pipeline.reranking_config["top_k"])
    if method == "hybrid_rrf":
        return pipeline.retriever.search(
            query,
            top_k_dense=pipeline.retrieval_config["top_k_dense"],
            top_k_bm25=pipeline.retrieval_config["top_k_bm25"],
            top_k_final=pipeline.reranking_config["top_k"],
        )
    if method == "civic_rerank":
        return pipeline.retrieve(query, method="civic")
    if method == "simple":
        return pipeline.retrieve(query, method="simple")
    raise ValueError(f"Unknown evaluation method: {method}")


def summarize(rows: list[dict[str, Any]], method: str) -> dict[str, Any]:
    method_rows = [row for row in rows if row["method"] == method]
    if not method_rows:
        return {}
    return {
        "method": method,
        "num_cases": len(method_rows),
        "hit_at_1": round(mean(row["hit_at_1"] for row in method_rows), 4),
        "hit_at_3": round(mean(row["hit_at_3"] for row in method_rows), 4),
        "hit_at_5": round(mean(row["hit_at_5"] for row in method_rows), 4),
        "mrr": round(mean(row["mrr"] for row in method_rows), 4),
        "ndcg_at_5": round(mean(row["ndcg_at_5"] for row in method_rows), 4),
        "top_answer_semantic_similarity": round(mean(row["top_answer_semantic_similarity"] for row in method_rows), 4),
        "top_answer_token_f1": round(mean(row["top_answer_token_f1"] for row in method_rows), 4),
    }


def paraphrase_consistency(rows: list[dict[str, Any]], method: str) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, dict[str, Any]]] = {}
    for row in rows:
        if row["method"] != method:
            continue
        grouped.setdefault(row["chunk_id"], {})[row["variant"]] = row

    consistency_rows: list[dict[str, Any]] = []
    for chunk_id, variants in grouped.items():
        curated = variants.get("curated_question")
        original = variants.get("original_question")
        if not curated or not original:
            continue
        consistency_rows.append(
            {
                "method": method,
                "chunk_id": chunk_id,
                "category": curated["category"],
                "curated_top_id": curated["top_id"],
                "original_top_id": original["top_id"],
                "same_top_id": int(curated["top_id"] == original["top_id"]),
                "curated_hit_at_5": curated["hit_at_5"],
                "original_hit_at_5": original["hit_at_5"],
                "both_hit_at_5": int(bool(curated["hit_at_5"]) and bool(original["hit_at_5"])),
            }
        )
    return consistency_rows


def write_report(
    output_path: Path,
    *,
    input_path: Path,
    cases: list[EvalCase],
    rows: list[dict[str, Any]],
    summaries: list[dict[str, Any]],
    consistency_rows: list[dict[str, Any]],
) -> None:
    primary_method = "hybrid_rrf" if any(row["method"] == "hybrid_rrf" for row in rows) else rows[0]["method"]
    weak_cases = [
        row
        for row in rows
        if row["method"] == primary_method and (not row["hit_at_5"] or row["top_answer_semantic_similarity"] < 0.72)
    ]
    consistency_score = mean([row["both_hit_at_5"] for row in consistency_rows]) if consistency_rows else 0.0
    same_top_score = mean([row["same_top_id"] for row in consistency_rows]) if consistency_rows else 0.0

    lines = [
        "# Collected FAQ Pair Evaluation",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Input dataset: `{input_path}`",
        f"Evaluation cases: {len(cases)} query variants from {len({case.chunk_id for case in cases})} expected FAQ chunks.",
        "",
        "## What This Measures",
        "",
        "- Source retrieval: whether the expected FAQ chunk appears in top-k retrieved evidence.",
        "- Answer-evidence similarity: whether the top retrieved chunk contains answer-like text similar to the collected reference answer.",
        "- Paraphrase consistency: whether the curated question and original citizen-style question retrieve the same/similar expected evidence.",
        "- This pass avoids local LLM generation so one slow model call cannot hide retrieval errors.",
        "",
        "## Summary",
        "",
        "| Method | Cases | Hit@1 | Hit@3 | Hit@5 | MRR | nDCG@5 | Top answer semantic sim | Top answer token F1 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for summary in summaries:
        lines.append(
            "| {method} | {num_cases} | {hit_at_1:.4f} | {hit_at_3:.4f} | {hit_at_5:.4f} | {mrr:.4f} | {ndcg_at_5:.4f} | {top_answer_semantic_similarity:.4f} | {top_answer_token_f1:.4f} |".format(
                **summary
            )
        )

    lines.extend(
        [
            "",
            "## Paraphrase Consistency",
            "",
            f"- Both curated and original question hit expected source in top-5: {consistency_score:.4f}",
            f"- Curated and original question returned same top source: {same_top_score:.4f}",
            "",
            f"## {primary_method} Cases To Inspect",
            "",
        ]
    )
    if not weak_cases:
        lines.append(f"No weak {primary_method} cases under the current thresholds.")
    else:
        lines.append("| Case | Category | Expected chunk | Rank | Top chunk | Similarity | Query |")
        lines.append("|---|---|---|---:|---|---:|---|")
        for row in weak_cases:
            query = str(row["query"]).replace("|", "\\|").replace("\n", " ")[:140]
            lines.append(
                f"| {row['variant']} | {row['category']} | `{row['chunk_id']}` | {row['expected_rank'] or '-'} | `{row['top_id']}` | {row['top_answer_semantic_similarity']:.4f} | {query} |"
            )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "For this dataset, the strongest requirement is not that the generated wording is identical. The first requirement is that the expected official evidence is retrieved. If Hit@5 is high but answer similarity is lower, the issue is likely generation/answer formatting. If Hit@5 is low, the issue is retrieval, chunking, metadata, or query-intent handling.",
            "",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate collected FAQ Q/A pairs against the birth/death CivicRAG pipeline.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--methods",
        default="dense_only,bm25_only,hybrid_rrf",
        help="Comma-separated methods: dense_only,bm25_only,hybrid_rrf,civic_rerank,simple",
    )
    args = parser.parse_args()

    records = load_records(args.input)
    cases = build_cases(records)
    methods = [method.strip() for method in args.methods.split(",") if method.strip()]
    pipeline = CivicRAGPipeline(PROJECT_ROOT, DEFAULT_CONFIG)
    similarity_cache = EmbeddingSimilarityCache(pipeline)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    normalized_path = args.output_dir / "collected_faq_pairs_normalized.json"
    normalized_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    rows: list[dict[str, Any]] = []
    for method in methods:
        print(f"Evaluating method={method} with {len(cases)} cases", flush=True)
        for index, case in enumerate(cases, start=1):
            results = retrieve_with_method(pipeline, case.query, method)
            retrieved_ids = [result.chunk_id for result in results]
            top = results[0] if results else None
            expected_rank = retrieved_ids.index(case.chunk_id) + 1 if case.chunk_id in retrieved_ids else None
            top_answer_text = extract_answer_like_text(top.content) if top else ""
            sim = similarity_cache.similarity(case.expected_answer, top_answer_text)
            row = {
                "method": method,
                "case_id": case.case_id,
                "chunk_id": case.chunk_id,
                "category": case.category,
                "variant": case.variant,
                "query": case.query,
                "expected_answer": case.expected_answer,
                "top_id": top.chunk_id if top else "",
                "top_document_type": top.metadata.get("document_type", "") if top else "",
                "top_category": top.metadata.get("category", "") if top else "",
                "top_section_title": top.metadata.get("section_title", "") if top else "",
                "expected_rank": expected_rank,
                "hit_at_1": int(case.chunk_id in retrieved_ids[:1]),
                "hit_at_3": int(case.chunk_id in retrieved_ids[:3]),
                "hit_at_5": int(case.chunk_id in retrieved_ids[:5]),
                "mrr": reciprocal_rank(retrieved_ids, {case.chunk_id}),
                "ndcg_at_5": ndcg_at_k(retrieved_ids, {case.chunk_id}, 5),
                "top_answer_semantic_similarity": sim,
                "top_answer_token_f1": token_f1(top_answer_text, case.expected_answer),
                "retrieved_ids": ";".join(retrieved_ids[:10]),
                "top_answer_text": top_answer_text,
            }
            rows.append(row)
            print(
                f"  {index:02d}/{len(cases)} {case.chunk_id} {case.variant}: "
                f"rank={expected_rank or '-'} top={row['top_id']} sim={sim:.3f}",
                flush=True,
            )

    csv_path = args.output_dir / "collected_faq_pairs_eval_rows.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summaries = [summarize(rows, method) for method in methods]
    summary_path = args.output_dir / "collected_faq_pairs_eval_summary.json"
    summary_path.write_text(json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8")

    consistency_rows = [item for method in methods for item in paraphrase_consistency(rows, method)]
    consistency_path = args.output_dir / "collected_faq_pairs_paraphrase_consistency.csv"
    with consistency_path.open("w", encoding="utf-8", newline="") as handle:
        if consistency_rows:
            writer = csv.DictWriter(handle, fieldnames=list(consistency_rows[0]))
            writer.writeheader()
            writer.writerows(consistency_rows)

    report_path = args.output_dir / "collected_faq_pairs_eval_report.md"
    write_report(
        report_path,
        input_path=args.input,
        cases=cases,
        rows=rows,
        summaries=summaries,
        consistency_rows=consistency_rows,
    )
    print(f"\nWrote report: {report_path}")
    print(f"Wrote rows: {csv_path}")
    print(f"Wrote summary: {summary_path}")


if __name__ == "__main__":
    main()
