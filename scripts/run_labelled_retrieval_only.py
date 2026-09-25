"""Evaluate existing P2 labels against current retrieval, without LLM calls."""
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def score(ids, expected, k=5):
    expected = set(expected)
    if not expected:
        raise ValueError("Relevance labels are required")
    hits = [int(cid in expected) for cid in ids[:k]]
    dcg = sum(hit / math.log2(rank + 2) for rank, hit in enumerate(hits))
    ideal = sum(1 / math.log2(rank + 2) for rank in range(min(k, len(expected))))
    return {
        "hit_at_1": float(bool(hits and hits[0])),
        "hit_at_5": float(any(hits)),
        "precision_at_5": sum(hits) / k,
        "label_recall_at_5": len(set(ids[:k]) & expected) / len(expected),
        "mrr_at_5": next((1 / (i + 1) for i, hit in enumerate(hits) if hit), 0.0),
        "ndcg_at_5": dcg / ideal,
    }


def main():
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["ANONYMIZED_TELEMETRY"] = "False"
    import torch
    from src.retrieval.hybrid_retriever import HybridRetriever

    torch.set_num_threads(2)
    started = time.monotonic()
    config_path = ROOT / "domains/birth_death_registration/config.json"
    eval_path = ROOT / "domains/birth_death_registration/data/evaluation/mixed_paraphrase_eval_flat_v1.json"
    out = ROOT / "docs/evaluation/p2_style_retrieval_2026_09_25"
    out.mkdir(parents=True, exist_ok=True)
    config = json.loads(config_path.read_text())
    chunk_path = ROOT / config["data"]["chunk_output_path"]
    chunks = [json.loads(line) for line in chunk_path.read_text().splitlines() if line.strip()]
    records = json.loads(eval_path.read_text())
    corpus_ids = {chunk["id"] for chunk in chunks}
    for record in records:
        assert record["expected_source_ids"], record["id"]
        assert set(record["expected_source_ids"]) <= corpus_ids, record["id"]
    retrieval = config["retrieval"]
    retriever = HybridRetriever(
        chunks=chunks,
        chroma_dir=str(ROOT / config["data"]["chroma_persist_dir"]),
        collection_name=config["data"]["collection_name"],
        embedding_model_name=config["embedding"]["model"],
        embedding_device="cpu", local_files_only=True,
        rrf_k=retrieval["rrf_k"], rrf_weights=retrieval["rrf_weights"],
    )
    assert set(retriever.collection.get(include=[])["ids"]) == corpus_ids
    manifest = {
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "config": config, "questions": len(records), "chunks": len(chunks),
        "groups": len({r["group_id"] for r in records}),
        "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in (config_path, chunk_path, eval_path, ROOT / "src/retrieval/hybrid_retriever.py")},
        "llm_calls": 0, "reranking": False, "evidence_selection": False,
        "ranking_protocol": "Retrieve top 20 per component once, fuse using production RRF, score top 5. Raw labelled questions; no query rewriting.",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    rows = []
    for record in records:
        query = record["question"]
        dense = retriever._dense_search(query, retrieval["top_k_dense"])
        bm25 = retriever._bm25_search(query, retrieval["top_k_bm25"])
        hybrid = [r.chunk_id for r in retriever._rrf_fuse({"dense": dense, "bm25": bm25})]
        rankings = {"bm25_only": bm25, "dense_only": dense, "hybrid_rrf": hybrid}
        rows.append({"id": record["id"], "question": query,
                     "group_id": record["group_id"], "expected_source_ids": record["expected_source_ids"],
                     "rankings": rankings,
                     "metrics": {name: score(ids, record["expected_source_ids"]) for name, ids in rankings.items()}})
        (out / "results.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2))
        print(f"{len(rows)}/{len(records)} completed", flush=True)
    summary = {name: {metric: sum(row["metrics"][name][metric] for row in rows) / len(rows)
                      for metric in rows[0]["metrics"][name]} for name in rankings}
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    report = ["# Current retriever: P2-style labelled evaluation", "",
              f"Completed {len(rows)} legacy questions in {time.monotonic() - started:.1f} seconds (including model loading).",
              "No answer generation, LLM judging, reranking, boosts, or evidence selection. BGE-M3 is used only as an embedding encoder.", "",
              "| Method | Hit@1 | Hit@5 | Precision@5 | Label Recall@5 | MRR@5 | nDCG@5 |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for name, metrics in summary.items():
        report.append("| " + name + " | " + " | ".join(f"{value:.4f}" for value in metrics.values()) + " |")
    report.extend(["", "## Scope and limitations",
                   "- Uses the existing 58-question P2 birth-registration set (19 paraphrase groups), not the newer 30-question three-domain set. No passport or BRTA conclusions are supported.",
                   "- All expected IDs exist in the current 187-chunk corpus and Chroma IDs match the corpus. This checks ID compatibility, not a fresh expert audit or embedding reconstruction.",
                   "- Relevance is defined by the pre-existing expected_source_ids, not newly judged relevance. Other valid passages can be unlabelled; recall is relative to these labels, not all possible relevant corpus passages.",
                   "- Questions are reused development questions, not an independent held-out benchmark. Paraphrases within groups are correlated.",
                   "- Precision@5 uses denominator 5; label recall uses the number of labelled relevant IDs. Hit@5 is not recall when multiple IDs are relevant. nDCG uses binary labels; MRR is truncated at 5.",
                   "- Component rankings are top-20 searches sliced at 5, and the same rankings feed production weighted RRF (k=50, dense=0.55, BM25=0.45). Approximate dense search can differ from requesting only five directly.",
                   "- These are retrieval scores, not answer correctness or a full Simple RAG versus CivicRAG comparison."])
    (out / "report.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
