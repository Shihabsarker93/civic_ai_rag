from __future__ import annotations

import argparse
import itertools
import json
import signal
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.metrics import cosine_similarity, ndcg_at_k, precision_at_k, recall_at_k, reciprocal_rank, token_f1
from src.pipeline import CivicRAGPipeline
from src.retrieval.hybrid_retriever import RetrievalResult


DEFAULT_EVAL_FILE = "domains/birth_death_registration/data/evaluation/p2_20q_eval_set.json"
DEFAULT_OUTPUT_DIR = "docs/evaluation/p2_experiments"


class AnswerTimeoutError(RuntimeError):
    pass


def load_records(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    records = json.loads(path.read_text(encoding="utf-8"))
    return records[:limit] if limit else records


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


def ask_with_timeout(
    pipeline: CivicRAGPipeline,
    question: str,
    *,
    model: str,
    method: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    if timeout_seconds <= 0:
        return pipeline.ask(question, model=model, method=method)

    def handle_timeout(signum: int, frame: Any) -> None:
        raise AnswerTimeoutError(f"answer generation exceeded {timeout_seconds} seconds")

    previous_handler = signal.signal(signal.SIGALRM, handle_timeout)
    signal.alarm(timeout_seconds)
    try:
        return pipeline.ask(question, model=model, method=method)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous_handler)


def summarize_numeric(rows: list[dict[str, Any]], group_cols: list[str], metric_cols: list[str]) -> dict[str, Any]:
    if not rows:
        return {}
    frame = pd.DataFrame(rows)
    summary: dict[str, Any] = {}
    for group_key, group in frame.groupby(group_cols):
        if not isinstance(group_key, tuple):
            group_key = (group_key,)
        label = " + ".join(str(value) for value in group_key)
        summary[label] = {"num_questions": int(len(group))}
        for metric in metric_cols:
            summary[label][metric] = float(group[metric].mean())
    return summary


def retrieval_variants(pipeline: CivicRAGPipeline, query: str, top_k: int) -> dict[str, list[RetrievalResult]]:
    hybrid_candidates = pipeline.retriever.search(
        query,
        top_k_dense=pipeline.retrieval_config["top_k_dense"],
        top_k_bm25=pipeline.retrieval_config["top_k_bm25"],
        top_k_final=pipeline.retrieval_config["top_k_final"],
    )
    return {
        "dense_only": pipeline.retriever.dense_only_search(query, top_k=top_k),
        "bm25_only": pipeline.retriever.bm25_only_search(query, top_k=top_k),
        "hybrid_rrf": hybrid_candidates[:top_k],
        "hybrid_rrf_rerank": pipeline.reranker.rerank(query, hybrid_candidates, top_k=top_k),
    }


def evaluate_retrieval_variants(
    pipeline: CivicRAGPipeline,
    records: list[dict[str, Any]],
    *,
    top_k: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        query = record["question"]
        expected = expected_ids(record)
        variants = retrieval_variants(pipeline, query, top_k=top_k)
        for variant, results in variants.items():
            retrieved_ids = result_ids(results)
            rows.append(
                {
                    "experiment": "retrieval_variant",
                    "variant": variant,
                    "question_id": record["id"],
                    "category": record["category"],
                    "question_type": record["question_type"],
                    "question": query,
                    "expected_source_ids": ",".join(sorted(expected)),
                    "retrieved_ids": ",".join(retrieved_ids),
                    "recall@1": recall_at_k(retrieved_ids, expected, 1),
                    "recall@3": recall_at_k(retrieved_ids, expected, 3),
                    "recall@5": recall_at_k(retrieved_ids, expected, 5),
                    "context_precision@5": precision_at_k(retrieved_ids, expected, 5),
                    "mrr": reciprocal_rank(retrieved_ids, expected),
                    "ndcg@5": ndcg_at_k(retrieved_ids, expected, 5),
                    "out_of_context_no_hit": float(not expected and not retrieved_ids),
                }
            )
    summary = summarize_numeric(
        rows,
        ["variant"],
        ["recall@1", "recall@3", "recall@5", "context_precision@5", "mrr", "ndcg@5"],
    )
    return rows, summary


def evaluate_parameter_sensitivity(
    pipeline: CivicRAGPipeline,
    records: list[dict[str, Any]],
    *,
    top_k: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    configs = [
        {"name": "dense_heavy", "weights": {"dense": 0.70, "bm25": 0.30}, "top_k_dense": 20, "top_k_bm25": 20},
        {"name": "balanced_current", "weights": {"dense": 0.55, "bm25": 0.45}, "top_k_dense": 20, "top_k_bm25": 20},
        {"name": "bm25_heavy", "weights": {"dense": 0.40, "bm25": 0.60}, "top_k_dense": 20, "top_k_bm25": 20},
        {"name": "small_topk", "weights": {"dense": 0.55, "bm25": 0.45}, "top_k_dense": 10, "top_k_bm25": 10},
        {"name": "large_topk", "weights": {"dense": 0.55, "bm25": 0.45}, "top_k_dense": 30, "top_k_bm25": 30},
    ]

    rows: list[dict[str, Any]] = []
    for config in configs:
        for record in records:
            expected = expected_ids(record)
            candidates = pipeline.retriever.search(
                record["question"],
                top_k_dense=config["top_k_dense"],
                top_k_bm25=config["top_k_bm25"],
                top_k_final=pipeline.retrieval_config["top_k_final"],
                rrf_weights=config["weights"],
            )
            reranked = pipeline.reranker.rerank(record["question"], candidates, top_k=top_k)
            retrieved_ids = result_ids(reranked)
            rows.append(
                {
                    "experiment": "parameter_sensitivity",
                    "config": config["name"],
                    "weights": json.dumps(config["weights"], ensure_ascii=False),
                    "top_k_dense": config["top_k_dense"],
                    "top_k_bm25": config["top_k_bm25"],
                    "question_id": record["id"],
                    "category": record["category"],
                    "question_type": record["question_type"],
                    "expected_source_ids": ",".join(sorted(expected)),
                    "retrieved_ids": ",".join(retrieved_ids),
                    "recall@1": recall_at_k(retrieved_ids, expected, 1),
                    "recall@3": recall_at_k(retrieved_ids, expected, 3),
                    "recall@5": recall_at_k(retrieved_ids, expected, 5),
                    "context_precision@5": precision_at_k(retrieved_ids, expected, 5),
                    "mrr": reciprocal_rank(retrieved_ids, expected),
                    "ndcg@5": ndcg_at_k(retrieved_ids, expected, 5),
                }
            )
    summary = summarize_numeric(
        rows,
        ["config"],
        ["recall@1", "recall@3", "recall@5", "context_precision@5", "mrr", "ndcg@5"],
    )
    return rows, summary


def encode_texts(pipeline: CivicRAGPipeline, texts: list[str]) -> np.ndarray:
    return np.asarray(
        pipeline.retriever.embedding_model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
    )


def context_support_similarity(pipeline: CivicRAGPipeline, answer: str, contexts: list[dict[str, Any]]) -> float:
    if not answer.strip() or not contexts:
        return 0.0
    texts = [answer, *[str(context["content"]) for context in contexts[:5]]]
    embeddings = encode_texts(pipeline, texts)
    answer_embedding = embeddings[0]
    context_embeddings = embeddings[1:]
    if len(context_embeddings) == 0:
        return 0.0
    return max(cosine_similarity(answer_embedding, context_embedding) for context_embedding in context_embeddings)


def evaluate_generation(
    pipeline: CivicRAGPipeline,
    records: list[dict[str, Any]],
    *,
    models: list[str],
    methods: list[str],
    answer_timeout_seconds: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        expected = expected_ids(record)
        expected_answer = record["expected_answer"]
        expected_embedding = encode_texts(pipeline, [expected_answer])[0]
        question_embedding = encode_texts(pipeline, [record["question"]])[0]

        for method in methods:
            for model in models:
                started = time.perf_counter()
                error = ""
                try:
                    response = ask_with_timeout(
                        pipeline,
                        record["question"],
                        model=model,
                        method=method,
                        timeout_seconds=answer_timeout_seconds,
                    )
                except Exception as exc:
                    response = {"answer": "", "sources": []}
                    error = str(exc)
                elapsed = round(time.perf_counter() - started, 2)
                answer = response["answer"]
                retrieved_ids = [source["id"] for source in response["sources"]]
                if answer.strip():
                    answer_embedding = encode_texts(pipeline, [answer])[0]
                    semantic_similarity = cosine_similarity(answer_embedding, expected_embedding)
                    answer_relevance = cosine_similarity(answer_embedding, question_embedding)
                    faithfulness_proxy = context_support_similarity(pipeline, answer, response["sources"])
                    answer_token_f1 = token_f1(answer, expected_answer)
                else:
                    semantic_similarity = 0.0
                    answer_relevance = 0.0
                    faithfulness_proxy = 0.0
                    answer_token_f1 = 0.0
                rows.append(
                    {
                        "experiment": "generation",
                        "method": method,
                        "model": model,
                        "question_id": record["id"],
                        "category": record["category"],
                        "question_type": record["question_type"],
                        "question": record["question"],
                        "expected_answer": expected_answer,
                        "generated_answer": answer,
                        "retrieved_ids": ",".join(retrieved_ids),
                        "elapsed_seconds": elapsed,
                        "answer_correctness_semantic": semantic_similarity,
                        "answer_correctness_token_f1": answer_token_f1,
                        "answer_relevance": answer_relevance,
                        "faithfulness_proxy_context_similarity": faithfulness_proxy,
                        "expected_source_retrieved": float(bool(expected.intersection(retrieved_ids))) if expected else float(not retrieved_ids),
                        "expected_source_cited": float(any(source_id in answer for source_id in expected)) if expected else 0.0,
                        "error": error,
                    }
                )
    summary = summarize_numeric(
        rows,
        ["method", "model"],
        [
            "answer_correctness_semantic",
            "answer_correctness_token_f1",
            "answer_relevance",
            "faithfulness_proxy_context_similarity",
            "expected_source_retrieved",
            "expected_source_cited",
        ],
    )
    return rows, summary


def evaluate_stability(
    pipeline: CivicRAGPipeline,
    records: list[dict[str, Any]],
    *,
    model: str,
    method: str,
    repeats: int,
    answer_timeout_seconds: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        answers: list[str] = []
        source_sets: list[set[str]] = []
        for run_index in range(1, repeats + 1):
            error = ""
            try:
                response = ask_with_timeout(
                    pipeline,
                    record["question"],
                    model=model,
                    method=method,
                    timeout_seconds=answer_timeout_seconds,
                )
            except Exception as exc:
                response = {"answer": "", "sources": []}
                error = str(exc)
            answers.append(response["answer"])
            source_sets.append(set(source["id"] for source in response["sources"]))
            rows.append(
                {
                    "experiment": "stability_raw",
                    "method": method,
                    "model": model,
                    "question_id": record["id"],
                    "run_index": run_index,
                    "answer": response["answer"],
                    "source_ids": ",".join(sorted(source_sets[-1])),
                    "error": error,
                }
            )

        answer_embeddings = encode_texts(pipeline, answers)
        similarities = []
        source_jaccards = []
        for i, j in itertools.combinations(range(repeats), 2):
            similarities.append(cosine_similarity(answer_embeddings[i], answer_embeddings[j]))
            union = source_sets[i] | source_sets[j]
            intersection = source_sets[i] & source_sets[j]
            source_jaccards.append(len(intersection) / len(union) if union else 1.0)
        rows.append(
            {
                "experiment": "stability_summary",
                "method": method,
                "model": model,
                "question_id": record["id"],
                "exact_answer_match": float(len(set(answers)) == 1),
                "mean_pairwise_answer_similarity": statistics.mean(similarities) if similarities else 1.0,
                "mean_source_jaccard": statistics.mean(source_jaccards) if source_jaccards else 1.0,
            }
        )

    summary_rows = [row for row in rows if row["experiment"] == "stability_summary"]
    summary = summarize_numeric(
        summary_rows,
        ["method", "model"],
        ["exact_answer_match", "mean_pairwise_answer_similarity", "mean_source_jaccard"],
    )
    return rows, summary


def write_manual_review_template(path: Path, records: list[dict[str, Any]]) -> None:
    rows = []
    for record in records:
        rows.append(
            {
                "question_id": record["id"],
                "category": record["category"],
                "question_type": record["question_type"],
                "question": record["question"],
                "expected_answer": record["expected_answer"],
                "expected_source_ids": ",".join(record.get("expected_source_ids") or []),
                "manual_retrieval_relevance_0_2": "",
                "manual_faithfulness_0_2": "",
                "manual_answer_correctness_0_2": "",
                "manual_answer_relevance_0_2": "",
                "manual_language_quality_0_2": "",
                "notes": "",
            }
        )
    path.write_text(pd.DataFrame(rows).to_csv(index=False), encoding="utf-8")


def write_markdown_report(
    path: Path,
    *,
    retrieval_summary: dict[str, Any],
    parameter_summary: dict[str, Any],
    generation_summary: dict[str, Any] | None,
    stability_summary: dict[str, Any] | None,
    eval_file: Path,
    fallback_commit: str,
    fast_rerank: bool,
) -> None:
    lines = [
        "# P2 Experiment Report",
        "",
        f"Evaluation set: `{eval_file}`",
        "",
        f"Fallback checkpoint before this evaluation framework: `{fallback_commit}`",
        "",
        f"Reranking mode for this run: `{'lexical fallback / fast mode' if fast_rerank else 'configured cross-encoder when available'}`",
        "",
        "## Experiment 1: Retrieval Variant Comparison",
        "",
        "| Variant | Recall@1 | Recall@3 | Recall@5 | Context Precision@5 | MRR | nDCG@5 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for variant, metrics in retrieval_summary.items():
        lines.append(
            f"| {variant} | {metrics['recall@1']:.3f} | {metrics['recall@3']:.3f} | "
            f"{metrics['recall@5']:.3f} | {metrics['context_precision@5']:.3f} | "
            f"{metrics['mrr']:.3f} | {metrics['ndcg@5']:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Experiment 5: Parameter Sensitivity",
            "",
            "| Config | Recall@1 | Recall@3 | Recall@5 | Context Precision@5 | MRR | nDCG@5 |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for config, metrics in parameter_summary.items():
        lines.append(
            f"| {config} | {metrics['recall@1']:.3f} | {metrics['recall@3']:.3f} | "
            f"{metrics['recall@5']:.3f} | {metrics['context_precision@5']:.3f} | "
            f"{metrics['mrr']:.3f} | {metrics['ndcg@5']:.3f} |"
        )

    if generation_summary:
        lines.extend(
            [
                "",
                "## Experiments 2 and 3: Generation/System Comparison",
                "",
                "| Method + Model | Semantic Correctness | Token F1 | Answer Relevance | Faithfulness Proxy | Source Retrieved | Source Cited |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for label, metrics in generation_summary.items():
            lines.append(
                f"| {label} | {metrics['answer_correctness_semantic']:.3f} | "
                f"{metrics['answer_correctness_token_f1']:.3f} | {metrics['answer_relevance']:.3f} | "
                f"{metrics['faithfulness_proxy_context_similarity']:.3f} | "
                f"{metrics['expected_source_retrieved']:.3f} | {metrics['expected_source_cited']:.3f} |"
            )

    if stability_summary:
        lines.extend(
            [
                "",
                "## Experiment 4: Stability Test",
                "",
                "| Method + Model | Exact Answer Match | Mean Pairwise Answer Similarity | Mean Source Jaccard |",
                "| --- | ---: | ---: | ---: |",
            ]
        )
        for label, metrics in stability_summary.items():
            lines.append(
                f"| {label} | {metrics['exact_answer_match']:.3f} | "
                f"{metrics['mean_pairwise_answer_similarity']:.3f} | {metrics['mean_source_jaccard']:.3f} |"
            )

    lines.extend(
        [
            "",
            "## Notes for Thesis Interpretation",
            "",
            "- `Recall@k`, `MRR`, `nDCG@5`, and `Context Precision@5` evaluate retrieval before generation.",
            "- The generation metrics are automatic proxy metrics; they should be paired with manual qualitative review for Bangla government-service correctness.",
            "- The faithfulness metric here is a context-similarity proxy, not a full RAGAS LLM judge.",
            "- Empty or timed-out generated answers are scored as `0.0` for generation metrics and the error is stored in `generation_rows.csv`.",
            "- Exact repeated answers are not automatically bad for civic QA; stable grounded answers indicate reproducibility.",
            "- Out-of-context questions are included to test refusal behavior, but retrieval metrics for empty expected-source cases should be interpreted separately.",
            "- Use `manual_review_template.csv` to record human scores for scenario-based Bangla questions.",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run P2 CivicRAG evaluation experiments.")
    parser.add_argument("--config", default="domains/birth_death_registration/config.json")
    parser.add_argument("--eval-file", default=DEFAULT_EVAL_FILE)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--run-generation", action="store_true")
    parser.add_argument("--run-stability", action="store_true")
    parser.add_argument("--models", nargs="+", default=None)
    parser.add_argument("--methods", nargs="+", choices=["simple", "civic"], default=["simple", "civic"])
    parser.add_argument("--stability-repeats", type=int, default=3)
    parser.add_argument(
        "--answer-timeout-seconds",
        type=int,
        default=120,
        help="Maximum seconds allowed per generated answer; set 0 to disable.",
    )
    parser.add_argument("--fallback-commit", default="01c663e")
    parser.add_argument(
        "--fast-rerank",
        action="store_true",
        help="Use lexical reranking instead of the slower BGE cross-encoder for quick experiment iteration.",
    )
    args = parser.parse_args()

    eval_file = PROJECT_ROOT / args.eval_file
    output_dir = PROJECT_ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    records = load_records(eval_file, args.limit)
    config_path = PROJECT_ROOT / args.config
    if args.fast_rerank:
        fast_config = json.loads(config_path.read_text(encoding="utf-8"))
        fast_config["reranking"]["enabled"] = False
        config_path = output_dir / "fast_rerank_config.json"
        config_path.write_text(json.dumps(fast_config, ensure_ascii=False, indent=2), encoding="utf-8")
    pipeline = CivicRAGPipeline(PROJECT_ROOT, config_path)
    models = args.models or pipeline.generation_config["comparison_models"]

    retrieval_rows, retrieval_summary = evaluate_retrieval_variants(pipeline, records, top_k=args.top_k)
    parameter_rows, parameter_summary = evaluate_parameter_sensitivity(pipeline, records, top_k=args.top_k)

    generation_rows: list[dict[str, Any]] = []
    generation_summary = None
    if args.run_generation:
        generation_rows, generation_summary = evaluate_generation(
            pipeline,
            records,
            models=models,
            methods=args.methods,
            answer_timeout_seconds=args.answer_timeout_seconds,
        )

    stability_rows: list[dict[str, Any]] = []
    stability_summary = None
    if args.run_stability:
        stability_rows, stability_summary = evaluate_stability(
            pipeline,
            records,
            model=models[0],
            method="civic",
            repeats=args.stability_repeats,
            answer_timeout_seconds=args.answer_timeout_seconds,
        )

    (output_dir / "retrieval_variant_rows.csv").write_text(pd.DataFrame(retrieval_rows).to_csv(index=False), encoding="utf-8")
    (output_dir / "retrieval_variant_summary.json").write_text(json.dumps(retrieval_summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "parameter_sensitivity_rows.csv").write_text(pd.DataFrame(parameter_rows).to_csv(index=False), encoding="utf-8")
    (output_dir / "parameter_sensitivity_summary.json").write_text(json.dumps(parameter_summary, ensure_ascii=False, indent=2), encoding="utf-8")

    if generation_rows:
        (output_dir / "generation_rows.csv").write_text(pd.DataFrame(generation_rows).to_csv(index=False), encoding="utf-8")
        (output_dir / "generation_summary.json").write_text(json.dumps(generation_summary, ensure_ascii=False, indent=2), encoding="utf-8")
    if stability_rows:
        (output_dir / "stability_rows.csv").write_text(pd.DataFrame(stability_rows).to_csv(index=False), encoding="utf-8")
        (output_dir / "stability_summary.json").write_text(json.dumps(stability_summary, ensure_ascii=False, indent=2), encoding="utf-8")

    write_manual_review_template(output_dir / "manual_review_template.csv", records)
    (output_dir / "run_config.json").write_text(
        json.dumps(
            {
                "eval_file": str(eval_file),
                "config_file": str(config_path),
                "num_records": len(records),
                "top_k": args.top_k,
                "models": models,
                "methods": args.methods,
                "run_generation": args.run_generation,
                "run_stability": args.run_stability,
                "stability_repeats": args.stability_repeats,
                "answer_timeout_seconds": args.answer_timeout_seconds,
                "fast_rerank": args.fast_rerank,
                "fallback_commit": args.fallback_commit,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    report_path = output_dir / "p2_experiment_report.md"
    write_markdown_report(
        report_path,
        retrieval_summary=retrieval_summary,
        parameter_summary=parameter_summary,
        generation_summary=generation_summary,
        stability_summary=stability_summary,
        eval_file=eval_file,
        fallback_commit=args.fallback_commit,
        fast_rerank=args.fast_rerank,
    )

    print(json.dumps({"retrieval": retrieval_summary, "parameter_sensitivity": parameter_summary}, ensure_ascii=False, indent=2))
    print(f"Wrote report: {report_path}")


if __name__ == "__main__":
    main()
