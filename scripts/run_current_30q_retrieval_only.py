"""Save three retrieval rankings for the current 30 questions; no LLM or judging."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["ANONYMIZED_TELEMETRY"] = "False"


def main():
    import torch
    from src.retrieval.hybrid_retriever import HybridRetriever

    torch.set_num_threads(2)
    started = time.monotonic()
    source = ROOT / "docs/evaluation/user_30q_model_comparison_2026_09_22/questions.json"
    questions = json.loads(source.read_text())["questions"]
    assert len(questions) == 30
    out = ROOT / "docs/evaluation/current_30q_retrieval_only_2026_09_25"
    out.mkdir(parents=True, exist_ok=True)
    manifest = {
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question_file": str(source.relative_to(ROOT)),
        "question_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "llm_calls": 0, "judging": False, "generation": False,
        "reranking": False, "evidence_selection": False,
        "protocol": "Raw questions; domain-filtered current indices; top-20 component rankings; production weighted RRF; top-5 passages exported for review.",
        "domains": {},
    }
    encoder = None
    rows = []
    for domain in dict.fromkeys(q["domain"] for q in questions):
        config_path = ROOT / f"domains/{domain}/config.json"
        config = json.loads(config_path.read_text())
        chunk_path = ROOT / config["data"]["chunk_output_path"]
        chunks = [json.loads(line) for line in chunk_path.read_text().splitlines() if line.strip()]
        retrieval = config["retrieval"]
        retriever = HybridRetriever(
            chunks=chunks, chroma_dir=str(ROOT / config["data"]["chroma_persist_dir"]),
            collection_name=config["data"]["collection_name"],
            embedding_model_name=config["embedding"]["model"], embedding_device="cpu",
            local_files_only=True, rrf_k=retrieval["rrf_k"], rrf_weights=retrieval["rrf_weights"],
            embedding_model=encoder,
        )
        encoder = retriever.embedding_model
        assert set(retriever.collection.get(include=[])["ids"]) == set(retriever.chunk_by_id)
        manifest["domains"][domain] = {
            "config": config, "chunks": len(chunks),
            "config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
            "corpus_sha256": hashlib.sha256(chunk_path.read_bytes()).hexdigest(),
        }
        for question in (q for q in questions if q["domain"] == domain):
            t0 = time.monotonic()
            dense = retriever._dense_search(question["question"], retrieval["top_k_dense"])
            bm25 = retriever._bm25_search(question["question"], retrieval["top_k_bm25"])
            hybrid = retriever._rrf_fuse({"dense": dense, "bm25": bm25})
            rankings = {"bm25_only": bm25, "dense_only": dense,
                        "hybrid_rrf": [r.chunk_id for r in hybrid]}
            rows.append({**question, "retrieval_seconds": time.monotonic() - t0,
                         "rankings": rankings,
                         "top5_passages": {method: [retriever.chunk_by_id[cid] for cid in ids[:5]]
                                           for method, ids in rankings.items()}})
            (out / "results.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2))
            print(f"{len(rows)}/30 retrieved: {question['id']}", flush=True)
    manifest["elapsed_seconds"] = time.monotonic() - started
    manifest["completed_questions"] = len(rows)
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    report = ["# Current 30-question retrieval-only run", "",
              f"Completed 30 questions across three domains in {manifest['elapsed_seconds']:.1f} seconds including encoder loading.",
              "BM25-only, BGE-M3 dense-only and Hybrid RRF used the current domain indices. No generative LLM, judge, reranker, selector, or answer generation was called.", "",
              "## Metric status",
              "Hit@k, Precision@k, Recall@k, MRR and nDCG are NOT calculated: these questions lack complete verified relevance labels. Saved retrieved IDs are not ground truth. No machine-drafted labels were used.",
              "This is a retrieval export for review, not an answer-accuracy benchmark or the full CivicRAG pipeline. Legacy P2 scores cannot be transferred to these questions.", "",
              "| Domain | Questions | Methods | Status |", "|---|---:|---:|---|"]
    for domain in manifest["domains"]:
        report.append(f"| {domain} | {sum(r['domain'] == domain for r in rows)} | 3 | Rankings saved; relevance review pending |")
    (out / "report.md").write_text("\n".join(report) + "\n")
    review = ["# Top-five retrieved passages", "", "Unjudged retrieval output, not generated answers or verified evidence."]
    for row in rows:
        review.extend(["", f"## {row['id']}", "", row["question"]])
        for method, passages in row["top5_passages"].items():
            review.extend(["", f"### {method}"])
            for rank, passage in enumerate(passages, 1):
                review.extend(["", f"#### {rank}. {passage['id']}", "",
                               passage.get("answer_evidence") or passage["content"]])
    (out / "passages.md").write_text("\n".join(review) + "\n")
    print(f"Finished in {manifest['elapsed_seconds']:.1f}s; no LLM calls.", flush=True)


if __name__ == "__main__":
    main()
