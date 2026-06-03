from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.metrics import ndcg_at_k, precision_at_k, recall_at_k, reciprocal_rank
from src.pipeline import CivicRAGPipeline


def load_records(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize(rows: list[dict]) -> dict:
    frame = pd.DataFrame(rows)
    summary = {}
    for method, group in frame.groupby("method"):
        summary[method] = {
            "num_questions": int(len(group)),
            "recall@1": float(group["recall@1"].mean()),
            "recall@3": float(group["recall@3"].mean()),
            "recall@5": float(group["recall@5"].mean()),
            "precision@5": float(group["precision@5"].mean()),
            "mrr": float(group["mrr"].mean()),
            "ndcg@5": float(group["ndcg@5"].mean()),
        }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Simple RAG vs CivicRAG retrieval numerically.")
    parser.add_argument("--config", default="domains/birth_death_registration/config.json")
    parser.add_argument("--eval-file", required=True, help="JSON file containing question, expected_source_ids, and optional category.")
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()

    pipeline = CivicRAGPipeline(PROJECT_ROOT, PROJECT_ROOT / args.config)
    records = load_records(Path(args.eval_file))
    output_dir = PROJECT_ROOT / (args.output_dir or "domains/birth_death_registration/data/evaluation")
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for record in records:
        query = record["question"]
        expected_ids = set(record.get("expected_source_ids") or [record["expected_source_id"]])

        simple_results = pipeline.retriever.dense_only_search(query, top_k=5)
        civic_results = pipeline.retrieve(query, method="civic")

        method_results = {
            "Simple RAG": [result.chunk_id for result in simple_results],
            "CivicRAG": [result.chunk_id for result in civic_results],
        }

        for method, retrieved_ids in method_results.items():
            rows.append(
                {
                    "method": method,
                    "question_id": record.get("id", ""),
                    "category": record.get("category", ""),
                    "question": query,
                    "expected_source_ids": ",".join(sorted(expected_ids)),
                    "retrieved_ids": ",".join(retrieved_ids),
                    "recall@1": recall_at_k(retrieved_ids, expected_ids, 1),
                    "recall@3": recall_at_k(retrieved_ids, expected_ids, 3),
                    "recall@5": recall_at_k(retrieved_ids, expected_ids, 5),
                    "precision@5": precision_at_k(retrieved_ids, expected_ids, 5),
                    "mrr": reciprocal_rank(retrieved_ids, expected_ids),
                    "ndcg@5": ndcg_at_k(retrieved_ids, expected_ids, 5),
                }
            )

    csv_path = output_dir / "retrieval_evaluation.csv"
    summary_path = output_dir / "retrieval_summary.json"
    pd.DataFrame(rows).to_csv(csv_path, index=False)
    summary = summarize(rows)
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print(f"Wrote: {csv_path}")
    print(f"Wrote: {summary_path}")


if __name__ == "__main__":
    main()
