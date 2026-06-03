from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.metrics import cosine_similarity, token_f1
from src.pipeline import CivicRAGPipeline


def load_records(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize(rows: list[dict]) -> dict:
    frame = pd.DataFrame(rows)
    summary = {}
    for (method, model), group in frame.groupby(["method", "model"]):
        summary[f"{method} + {model}"] = {
            "num_questions": int(len(group)),
            "mean_semantic_similarity": float(group["semantic_similarity"].mean()),
            "mean_token_f1": float(group["token_f1"].mean()),
            "source_retrieval_accuracy": float(group["expected_source_retrieved"].mean()),
            "citation_accuracy": float(group["expected_source_cited"].mean()),
        }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate generated answers with numeric metrics.")
    parser.add_argument("--config", default="domains/passport/config.json")
    parser.add_argument("--models", nargs="+", default=None)
    parser.add_argument("--methods", nargs="+", choices=["simple", "civic"], default=["simple", "civic"])
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()

    pipeline = CivicRAGPipeline(PROJECT_ROOT, PROJECT_ROOT / args.config)
    records = load_records(PROJECT_ROOT / pipeline.data_config["processed_faq_path"])
    records = records[: args.limit] if args.limit else records
    models = args.models or pipeline.generation_config["comparison_models"]

    output_dir = PROJECT_ROOT / (args.output_dir or "domains/passport/data/evaluation")
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for record in records:
        expected_answer = record["answer"]
        expected_source_id = record["id"]
        expected_embedding = pipeline.retriever.embedding_model.encode(
            [expected_answer],
            normalize_embeddings=True,
            show_progress_bar=False,
        )[0]

        for method in args.methods:
            method_label = "Simple RAG" if method == "simple" else "CivicRAG"
            for model in models:
                response = pipeline.ask(record["question"], model=model, method=method)
                answer = response["answer"]
                answer_embedding = pipeline.retriever.embedding_model.encode(
                    [answer],
                    normalize_embeddings=True,
                    show_progress_bar=False,
                )[0]
                retrieved_ids = [source["id"] for source in response["sources"]]

                rows.append(
                    {
                        "model": model,
                        "method": method_label,
                        "question_id": expected_source_id,
                        "category": record["category"],
                        "question": record["question"],
                        "expected_answer": expected_answer,
                        "generated_answer": answer,
                        "retrieved_ids": ",".join(retrieved_ids),
                        "semantic_similarity": cosine_similarity(np.asarray(answer_embedding), np.asarray(expected_embedding)),
                        "token_f1": token_f1(answer, expected_answer),
                        "expected_source_retrieved": float(expected_source_id in retrieved_ids),
                        "expected_source_cited": float(expected_source_id in answer),
                    }
                )

    csv_path = output_dir / "generation_evaluation.csv"
    summary_path = output_dir / "generation_summary.json"
    pd.DataFrame(rows).to_csv(csv_path, index=False)
    summary = summarize(rows)
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print(f"Wrote: {csv_path}")
    print(f"Wrote: {summary_path}")


if __name__ == "__main__":
    main()
