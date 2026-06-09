from __future__ import annotations

import argparse
import csv
import json
import signal
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.metrics import cosine_similarity, ndcg_at_k, precision_at_k, recall_at_k, reciprocal_rank, token_f1
from src.pipeline import CivicRAGPipeline
from src.retrieval.hybrid_retriever import RetrievalResult


DEFAULT_EVAL_FILE = PROJECT_ROOT / "domains/birth_death_registration/data/evaluation/mixed_paraphrase_eval_flat_v1.json"
DEFAULT_CONFIG = PROJECT_ROOT / "domains/birth_death_registration/config.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "docs/evaluation/reduced_eval_plan_v1"

GENERATION_SUBSET_IDS = [
    "para_lost_certificate_01_v02",
    "para_manual_to_online_01_v02",
    "para_application_process_01_v01",
    "para_registration_deadline_fee_01_v02",
    "para_birth_date_correction_fee_01_v01",
    "para_online_visibility_01_v01",
]

LLM_SUBSET_IDS = [
    "para_lost_certificate_01_v02",
    "para_application_process_01_v01",
    "para_birth_date_correction_fee_01_v01",
    "para_single_parent_divorce_01_v01",
]


class AnswerTimeoutError(RuntimeError):
    pass


def load_records(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def filter_records(records: list[dict[str, Any]], ids: list[str]) -> list[dict[str, Any]]:
    by_id = {record["id"]: record for record in records}
    return [by_id[record_id] for record_id in ids if record_id in by_id]


def expected_ids(record: dict[str, Any]) -> set[str]:
    return set(record.get("expected_source_ids") or [])


def result_ids(results: list[RetrievalResult] | list[dict[str, Any]]) -> list[str]:
    ids: list[str] = []
    for result in results:
        if isinstance(result, RetrievalResult):
            ids.append(result.chunk_id)
        else:
            ids.append(str(result["id"]))
    return ids


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict[str, Any]], group_key: str, metric_keys: list[str]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row[group_key])].append(row)

    summary: dict[str, Any] = {}
    for label, group in grouped.items():
        summary[label] = {"num_questions": len(group)}
        for metric in metric_keys:
            summary[label][metric] = float(mean(float(row[metric]) for row in group))
    return dict(sorted(summary.items()))


def evaluate_retrieval_variants(pipeline: CivicRAGPipeline, records: list[dict[str, Any]], *, top_k: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        variants = {
            "dense_only": pipeline.retriever.dense_only_search(record["question"], top_k=top_k),
            "bm25_only": pipeline.retriever.bm25_only_search(record["question"], top_k=top_k),
            "hybrid_rrf": pipeline.retriever.search(
                record["question"],
                top_k_dense=pipeline.retrieval_config["top_k_dense"],
                top_k_bm25=pipeline.retrieval_config["top_k_bm25"],
                top_k_final=top_k,
            ),
        }
        expected = expected_ids(record)
        for variant, results in variants.items():
            retrieved_ids = result_ids(results)
            rows.append(
                {
                    "experiment": "retrieval_variant",
                    "variant": variant,
                    "question_id": record["id"],
                    "group_id": record.get("group_id", ""),
                    "category": record["category"],
                    "source_type": record.get("source_type", ""),
                    "question": record["question"],
                    "expected_source_ids": ";".join(sorted(expected)),
                    "retrieved_ids": ";".join(retrieved_ids),
                    "hit@1": recall_at_k(retrieved_ids, expected, 1),
                    "hit@3": recall_at_k(retrieved_ids, expected, 3),
                    "hit@5": recall_at_k(retrieved_ids, expected, 5),
                    "mrr": reciprocal_rank(retrieved_ids, expected),
                    "ndcg@5": ndcg_at_k(retrieved_ids, expected, 5),
                    "context_precision@5": precision_at_k(retrieved_ids, expected, 5),
                }
            )
    summary = summarize(rows, "variant", ["hit@1", "hit@3", "hit@5", "mrr", "ndcg@5", "context_precision@5"])
    return rows, summary


def evaluate_rrf_weights(pipeline: CivicRAGPipeline, records: list[dict[str, Any]], *, top_k: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    configs = [
        ("dense_0.80_bm25_0.20", {"dense": 0.80, "bm25": 0.20}),
        ("dense_0.60_bm25_0.40", {"dense": 0.60, "bm25": 0.40}),
        ("current_dense_0.55_bm25_0.45", {"dense": 0.55, "bm25": 0.45}),
        ("balanced_0.50_0.50", {"dense": 0.50, "bm25": 0.50}),
    ]
    rows: list[dict[str, Any]] = []
    for label, weights in configs:
        for record in records:
            expected = expected_ids(record)
            results = pipeline.retriever.search(
                record["question"],
                top_k_dense=pipeline.retrieval_config["top_k_dense"],
                top_k_bm25=pipeline.retrieval_config["top_k_bm25"],
                top_k_final=top_k,
                rrf_weights=weights,
            )
            retrieved_ids = result_ids(results)
            rows.append(
                {
                    "experiment": "rrf_weight_sensitivity",
                    "config": label,
                    "weights": json.dumps(weights),
                    "question_id": record["id"],
                    "group_id": record.get("group_id", ""),
                    "category": record["category"],
                    "source_type": record.get("source_type", ""),
                    "question": record["question"],
                    "expected_source_ids": ";".join(sorted(expected)),
                    "retrieved_ids": ";".join(retrieved_ids),
                    "hit@1": recall_at_k(retrieved_ids, expected, 1),
                    "hit@3": recall_at_k(retrieved_ids, expected, 3),
                    "hit@5": recall_at_k(retrieved_ids, expected, 5),
                    "mrr": reciprocal_rank(retrieved_ids, expected),
                    "ndcg@5": ndcg_at_k(retrieved_ids, expected, 5),
                    "context_precision@5": precision_at_k(retrieved_ids, expected, 5),
                }
            )
    summary = summarize(rows, "config", ["hit@1", "hit@3", "hit@5", "mrr", "ndcg@5", "context_precision@5"])
    return rows, summary


def evaluate_generation_context_k(pipeline: CivicRAGPipeline, records: list[dict[str, Any]], *, max_k: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        expected = expected_ids(record)
        results = pipeline.retriever.search(
            record["question"],
            top_k_dense=pipeline.retrieval_config["top_k_dense"],
            top_k_bm25=pipeline.retrieval_config["top_k_bm25"],
            top_k_final=max_k,
        )
        retrieved_ids = result_ids(results)
        for k in range(1, max_k + 1):
            rows.append(
                {
                    "experiment": "generation_context_k_coverage",
                    "k": k,
                    "question_id": record["id"],
                    "group_id": record.get("group_id", ""),
                    "category": record["category"],
                    "source_type": record.get("source_type", ""),
                    "question": record["question"],
                    "expected_source_ids": ";".join(sorted(expected)),
                    "generation_context_ids": ";".join(retrieved_ids[:k]),
                    "expected_source_in_context": recall_at_k(retrieved_ids, expected, k),
                    "context_precision@k": precision_at_k(retrieved_ids, expected, k),
                }
            )
    summary = summarize(rows, "k", ["expected_source_in_context", "context_precision@k"])
    return rows, summary


def encode_one(pipeline: CivicRAGPipeline, text: str) -> np.ndarray:
    return np.asarray(
        pipeline.retriever.embedding_model.encode(
            [text],
            normalize_embeddings=True,
            show_progress_bar=False,
        )[0]
    )


def support_similarity(pipeline: CivicRAGPipeline, answer: str, sources: list[dict[str, Any]]) -> float:
    if not answer.strip() or not sources:
        return 0.0
    answer_embedding = encode_one(pipeline, answer)
    scores = []
    for source in sources[:5]:
        scores.append(cosine_similarity(answer_embedding, encode_one(pipeline, str(source["content"]))))
    return max(scores) if scores else 0.0


def ask_with_timeout(
    pipeline: CivicRAGPipeline,
    question: str,
    *,
    model: str,
    method: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    def handle_timeout(signum: int, frame: Any) -> None:
        raise AnswerTimeoutError(f"answer generation exceeded {timeout_seconds} seconds")

    previous_handler = signal.signal(signal.SIGALRM, handle_timeout)
    signal.alarm(timeout_seconds)
    try:
        return pipeline.ask(question, model=model, method=method)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous_handler)


def evaluate_generation_topk(
    pipeline: CivicRAGPipeline,
    records: list[dict[str, Any]],
    *,
    top_ks: list[int],
    model: str,
    timeout_seconds: int,
    output_dir: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    original_k = pipeline.generation_config.get("top_k_for_generation", 3)
    csv_path = output_dir / "generation_topk_rows.csv"
    for k in top_ks:
        pipeline.generation_config["top_k_for_generation"] = k
        for record in records:
            print(f"[top-k={k}] {record['id']}", flush=True)
            expected_answer = record["expected_answer"]
            expected = expected_ids(record)
            started = time.perf_counter()
            error = ""
            response = {"answer": "", "sources": []}
            try:
                response = ask_with_timeout(
                    pipeline,
                    record["question"],
                    model=model,
                    method="civic",
                    timeout_seconds=timeout_seconds,
                )
            except Exception as exc:
                error = str(exc)
            elapsed = round(time.perf_counter() - started, 2)
            answer = str(response.get("answer", "")).strip()
            sources = list(response.get("sources", []))
            source_ids = [str(source["id"]) for source in sources]
            if answer:
                answer_embedding = encode_one(pipeline, answer)
                expected_embedding = encode_one(pipeline, expected_answer)
                question_embedding = encode_one(pipeline, record["question"])
                correctness_semantic = cosine_similarity(answer_embedding, expected_embedding)
                answer_relevance = cosine_similarity(answer_embedding, question_embedding)
                faithfulness_proxy = support_similarity(pipeline, answer, sources)
                answer_f1 = token_f1(answer, expected_answer)
            else:
                correctness_semantic = 0.0
                answer_relevance = 0.0
                faithfulness_proxy = 0.0
                answer_f1 = 0.0
            rows.append(
                {
                    "experiment": "generation_topk",
                    "top_k_for_generation": k,
                    "model": model,
                    "question_id": record["id"],
                    "group_id": record.get("group_id", ""),
                    "category": record["category"],
                    "source_type": record.get("source_type", ""),
                    "question": record["question"],
                    "expected_answer": expected_answer,
                    "generated_answer": answer,
                    "source_ids": ";".join(source_ids),
                    "elapsed_seconds": elapsed,
                    "answer_correctness_semantic": correctness_semantic,
                    "answer_correctness_token_f1": answer_f1,
                    "answer_relevance": answer_relevance,
                    "faithfulness_proxy_context_similarity": faithfulness_proxy,
                    "expected_source_retrieved": float(bool(expected.intersection(source_ids))),
                    "error": error,
                }
            )
            write_csv(csv_path, rows)
    pipeline.generation_config["top_k_for_generation"] = original_k
    summary = summarize(
        rows,
        "top_k_for_generation",
        [
            "answer_correctness_semantic",
            "answer_correctness_token_f1",
            "answer_relevance",
            "faithfulness_proxy_context_similarity",
            "expected_source_retrieved",
            "elapsed_seconds",
        ],
    )
    return rows, summary


def evaluate_llm_subset(
    pipeline: CivicRAGPipeline,
    records: list[dict[str, Any]],
    *,
    models: list[str],
    timeout_seconds: int,
    output_dir: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    csv_path = output_dir / "llm_backend_rows.csv"
    for model in models:
        for record in records:
            print(f"[model={model}] {record['id']}", flush=True)
            expected = expected_ids(record)
            expected_answer = record["expected_answer"]
            started = time.perf_counter()
            error = ""
            response = {"answer": "", "sources": []}
            try:
                response = ask_with_timeout(
                    pipeline,
                    record["question"],
                    model=model,
                    method="civic",
                    timeout_seconds=timeout_seconds,
                )
            except Exception as exc:
                error = str(exc)
            elapsed = round(time.perf_counter() - started, 2)
            answer = str(response.get("answer", "")).strip()
            sources = list(response.get("sources", []))
            source_ids = [str(source["id"]) for source in sources]
            if answer:
                answer_embedding = encode_one(pipeline, answer)
                expected_embedding = encode_one(pipeline, expected_answer)
                question_embedding = encode_one(pipeline, record["question"])
                correctness_semantic = cosine_similarity(answer_embedding, expected_embedding)
                answer_relevance = cosine_similarity(answer_embedding, question_embedding)
                faithfulness_proxy = support_similarity(pipeline, answer, sources)
                answer_f1 = token_f1(answer, expected_answer)
            else:
                correctness_semantic = 0.0
                answer_relevance = 0.0
                faithfulness_proxy = 0.0
                answer_f1 = 0.0
            rows.append(
                {
                    "experiment": "llm_backend",
                    "model": model,
                    "question_id": record["id"],
                    "group_id": record.get("group_id", ""),
                    "category": record["category"],
                    "source_type": record.get("source_type", ""),
                    "question": record["question"],
                    "expected_answer": expected_answer,
                    "generated_answer": answer,
                    "source_ids": ";".join(source_ids),
                    "elapsed_seconds": elapsed,
                    "answer_correctness_semantic": correctness_semantic,
                    "answer_correctness_token_f1": answer_f1,
                    "answer_relevance": answer_relevance,
                    "faithfulness_proxy_context_similarity": faithfulness_proxy,
                    "expected_source_retrieved": float(bool(expected.intersection(source_ids))),
                    "error": error,
                }
            )
            write_csv(csv_path, rows)
    summary = summarize(
        rows,
        "model",
        [
            "answer_correctness_semantic",
            "answer_correctness_token_f1",
            "answer_relevance",
            "faithfulness_proxy_context_similarity",
            "expected_source_retrieved",
            "elapsed_seconds",
        ],
    )
    return rows, summary


def write_manual_review_template(path: Path, rows: list[dict[str, Any]]) -> None:
    template = []
    for row in rows:
        template.append(
            {
                "experiment": row.get("experiment", ""),
                "question_id": row.get("question_id", ""),
                "category": row.get("category", ""),
                "question": row.get("question", ""),
                "expected_answer": row.get("expected_answer", ""),
                "generated_answer": row.get("generated_answer", ""),
                "manual_faithfulness_0_2": "",
                "manual_answer_correctness_0_2": "",
                "manual_completeness_0_2": "",
                "manual_language_quality_0_2": "",
                "failure_reason": "",
                "notes": "",
            }
        )
    write_csv(path, template)


def write_report(
    path: Path,
    *,
    eval_file: Path,
    retrieval_summary: dict[str, Any],
    rrf_summary: dict[str, Any],
    context_k_summary: dict[str, Any],
    generation_topk_summary: dict[str, Any] | None,
    llm_summary: dict[str, Any] | None,
    generation_subset_ids: list[str],
    llm_subset_ids: list[str],
) -> None:
    lines = [
        "# Reduced CivicRAG Evaluation Plan Results",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Evaluation file: `{eval_file}`",
        "",
        "This report intentionally limits the experiment scope to parameter choices that are defensible and doable for the current thesis phase.",
        "",
        "## Experiment A: Retrieval Variant Comparison",
        "",
        "| Variant | Hit@1 | Hit@3 | Hit@5 | MRR | nDCG@5 | Context Precision@5 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for label, metrics in retrieval_summary.items():
        lines.append(
            f"| {label} | {metrics['hit@1']:.4f} | {metrics['hit@3']:.4f} | {metrics['hit@5']:.4f} | "
            f"{metrics['mrr']:.4f} | {metrics['ndcg@5']:.4f} | {metrics['context_precision@5']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Experiment B: RRF Weight Sensitivity",
            "",
            "| RRF Config | Hit@1 | Hit@3 | Hit@5 | MRR | nDCG@5 | Context Precision@5 |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for label, metrics in rrf_summary.items():
        lines.append(
            f"| {label} | {metrics['hit@1']:.4f} | {metrics['hit@3']:.4f} | {metrics['hit@5']:.4f} | "
            f"{metrics['mrr']:.4f} | {metrics['ndcg@5']:.4f} | {metrics['context_precision@5']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Experiment C: Generation Context k Coverage",
            "",
            "This is retrieval-side coverage for how often the expected source would be available if the generator receives the top-k retrieved chunks.",
            "",
            "| k | Expected Source In Context | Context Precision@k |",
            "|---:|---:|---:|",
        ]
    )
    for label, metrics in sorted(context_k_summary.items(), key=lambda item: int(item[0])):
        lines.append(
            f"| {label} | {metrics['expected_source_in_context']:.4f} | {metrics['context_precision@k']:.4f} |"
        )

    if generation_topk_summary:
        lines.extend(
            [
                "",
                "## Experiment D: Actual Generation Top-k Sensitivity",
                "",
                f"Subset question IDs: `{', '.join(generation_subset_ids)}`",
                "",
                "| top_k_for_generation | Semantic Correctness | Token F1 | Answer Relevance | Faithfulness Proxy | Source Retrieved | Mean Latency |",
                "|---:|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for label, metrics in sorted(generation_topk_summary.items(), key=lambda item: int(item[0])):
            lines.append(
                f"| {label} | {metrics['answer_correctness_semantic']:.4f} | {metrics['answer_correctness_token_f1']:.4f} | "
                f"{metrics['answer_relevance']:.4f} | {metrics['faithfulness_proxy_context_similarity']:.4f} | "
                f"{metrics['expected_source_retrieved']:.4f} | {metrics['elapsed_seconds']:.2f}s |"
            )

    if llm_summary:
        lines.extend(
            [
                "",
                "## Experiment E: LLM Backend Comparison",
                "",
                f"Subset question IDs: `{', '.join(llm_subset_ids)}`",
                "",
                "| Model | Semantic Correctness | Token F1 | Answer Relevance | Faithfulness Proxy | Source Retrieved | Mean Latency |",
                "|---|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for label, metrics in llm_summary.items():
            lines.append(
                f"| {label} | {metrics['answer_correctness_semantic']:.4f} | {metrics['answer_correctness_token_f1']:.4f} | "
                f"{metrics['answer_relevance']:.4f} | {metrics['faithfulness_proxy_context_similarity']:.4f} | "
                f"{metrics['expected_source_retrieved']:.4f} | {metrics['elapsed_seconds']:.2f}s |"
            )

    lines.extend(
        [
            "",
            "## Manual Review Still Required",
            "",
            "Automatic semantic metrics are useful for filtering, but Bangla government-service correctness still needs human inspection. Use `manual_review_template.csv` to score faithfulness, correctness, completeness, and language quality from 0-2.",
            "",
            "## Interpretation Rule",
            "",
            "Use retrieval-only metrics to justify evidence selection hyperparameters. Use actual-generation metrics only after retrieval is stable, because bad final answers can come from either bad evidence ranking or LLM behavior.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the reduced, thesis-defensible CivicRAG evaluation plan.")
    parser.add_argument("--eval-file", type=Path, default=DEFAULT_EVAL_FILE)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--max-generation-context-k", type=int, default=8)
    parser.add_argument("--run-generation-topk", action="store_true")
    parser.add_argument("--run-llm-comparison", action="store_true")
    parser.add_argument("--generation-model", default="llama3.2")
    parser.add_argument("--llm-models", nargs="+", default=["llama3.2", "llama3", "qwen2.5:7b"])
    parser.add_argument("--timeout-seconds", type=int, default=90)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    records = load_records(args.eval_file)
    generation_subset = filter_records(records, GENERATION_SUBSET_IDS)
    llm_subset = filter_records(records, LLM_SUBSET_IDS)

    pipeline = CivicRAGPipeline(PROJECT_ROOT, args.config)

    retrieval_rows, retrieval_summary = evaluate_retrieval_variants(pipeline, records, top_k=args.top_k)
    rrf_rows, rrf_summary = evaluate_rrf_weights(pipeline, records, top_k=args.top_k)
    context_k_rows, context_k_summary = evaluate_generation_context_k(
        pipeline,
        records,
        max_k=args.max_generation_context_k,
    )

    write_csv(args.output_dir / "retrieval_variant_rows.csv", retrieval_rows)
    (args.output_dir / "retrieval_variant_summary.json").write_text(json.dumps(retrieval_summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(args.output_dir / "rrf_weight_rows.csv", rrf_rows)
    (args.output_dir / "rrf_weight_summary.json").write_text(json.dumps(rrf_summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(args.output_dir / "generation_context_k_rows.csv", context_k_rows)
    (args.output_dir / "generation_context_k_summary.json").write_text(json.dumps(context_k_summary, ensure_ascii=False, indent=2), encoding="utf-8")

    generation_topk_rows: list[dict[str, Any]] = []
    generation_topk_summary = None
    if args.run_generation_topk:
        generation_topk_rows, generation_topk_summary = evaluate_generation_topk(
            pipeline,
            generation_subset,
            top_ks=[1, 2, 3, 4, 5],
            model=args.generation_model,
            timeout_seconds=args.timeout_seconds,
            output_dir=args.output_dir,
        )
        (args.output_dir / "generation_topk_summary.json").write_text(json.dumps(generation_topk_summary, ensure_ascii=False, indent=2), encoding="utf-8")

    llm_rows: list[dict[str, Any]] = []
    llm_summary = None
    if args.run_llm_comparison:
        llm_rows, llm_summary = evaluate_llm_subset(
            pipeline,
            llm_subset,
            models=args.llm_models,
            timeout_seconds=args.timeout_seconds,
            output_dir=args.output_dir,
        )
        (args.output_dir / "llm_backend_summary.json").write_text(json.dumps(llm_summary, ensure_ascii=False, indent=2), encoding="utf-8")

    generated_rows_for_review = [*generation_topk_rows, *llm_rows]
    if generated_rows_for_review:
        write_manual_review_template(args.output_dir / "manual_review_template.csv", generated_rows_for_review)

    (args.output_dir / "run_config.json").write_text(
        json.dumps(
            {
                "eval_file": str(args.eval_file),
                "config": str(args.config),
                "num_records": len(records),
                "top_k": args.top_k,
                "max_generation_context_k": args.max_generation_context_k,
                "generation_subset_ids": GENERATION_SUBSET_IDS,
                "llm_subset_ids": LLM_SUBSET_IDS,
                "run_generation_topk": args.run_generation_topk,
                "run_llm_comparison": args.run_llm_comparison,
                "generation_model": args.generation_model,
                "llm_models": args.llm_models,
                "timeout_seconds": args.timeout_seconds,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    write_report(
        args.output_dir / "reduced_eval_report.md",
        eval_file=args.eval_file,
        retrieval_summary=retrieval_summary,
        rrf_summary=rrf_summary,
        context_k_summary=context_k_summary,
        generation_topk_summary=generation_topk_summary,
        llm_summary=llm_summary,
        generation_subset_ids=GENERATION_SUBSET_IDS,
        llm_subset_ids=LLM_SUBSET_IDS,
    )

    print(
        json.dumps(
            {
                "retrieval": retrieval_summary,
                "rrf_weights": rrf_summary,
                "generation_context_k": context_k_summary,
                "generation_topk": generation_topk_summary,
                "llm_backend": llm_summary,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    print(f"Wrote report: {args.output_dir / 'reduced_eval_report.md'}")


if __name__ == "__main__":
    main()
