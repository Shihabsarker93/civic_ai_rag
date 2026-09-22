"""Offline prompt/context ablation using frozen retrieved evidence, not live indexes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.generation.ollama_generator import build_prompt, canonicalize_answer
from src.pipeline import CivicRAGPipeline

INPUT = ROOT / "docs/evaluation/user_30q_model_comparison_2026_09_22/answers_qwen3_8b.json"
OUTPUT = ROOT / "docs/evaluation/source_preference_trial_2026_09_22"
SELECTED = ["passport_01_documents", "passport_02_fee", "brta_07_lost"]
OLD = """The retrieved sources are ranked by relevance. Source 1 is the strongest evidence.
If Source 1 directly answers the user's question, answer from Source 1.
If another retrieved source directly answers the question better than Source 1, use that source."""
NEW = """Compare all supplied sources before answering. Retrieval rank alone does not establish applicability.
Use sources that directly support the service and action requested by the user.
Distinguish application, collection, renewal, replacement and correction; do not substitute one for another.
Preserve eligibility, dates, fee categories and exceptions. Do not combine incompatible sources.
If the applicable category is unclear, ask a concise clarification. If no source supports the requested answer, say that the supplied information is insufficient."""


def trial_prompt(question, evidence, neutral=False):
    prompt = build_prompt(question, evidence)
    if neutral:
        if OLD not in prompt:
            raise RuntimeError("Baseline prompt changed; refusing an uncontrolled comparison")
        prompt = prompt.replace(OLD, NEW, 1)
    return prompt


def selector(domain):
    config = json.loads((ROOT / "domains" / domain / "config.json").read_text())
    pipeline = CivicRAGPipeline.__new__(CivicRAGPipeline)
    pipeline.chunks = [json.loads(line) for line in (ROOT / config["data"]["chunk_output_path"]).read_text().splitlines() if line.strip()]
    return pipeline, config


def render(rows):
    lines = ["# Source-preference trial", "",
             "Frozen-evidence generation experiment, not an end-to-end accuracy benchmark.",
             "Sources are supplied context IDs, not verified claim-level citations.", ""]
    for row in rows:
        lines += [f"## {row['id']} / {row['variant']}", "", row["question"], "",
                  f"Model: qwen3:8b; time: {row['seconds']} s; route: {row['route']}",
                  f"Finish reason: {row['ollama_metadata'].get('done_reason')}", "",
                  row["display_answer"], ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source = json.loads(INPUT.read_text())["rows"]
    jobs, comparisons = [], []
    for saved in source:
        if saved["result"]["answer_route"] != "llm":
            continue
        item = saved["audit_item"]
        pipeline, config = selector(item["domain"])
        question, contexts = item["question"], saved["result"]["sources"]
        k = config["generation"]["top_k_for_generation"]
        baseline = pipeline._select_generation_contexts(question, contexts, k)
        pipeline._has_dominant_single_topic_context = lambda *unused: False
        without_shortcut = pipeline._select_generation_contexts(question, contexts, k)
        comparisons.append({"id": item["id"], "same_contexts": baseline == without_shortcut,
                            "baseline_ids": [c["id"] for c in baseline],
                            "no_shortcut_ids": [c["id"] for c in without_shortcut]})
        if item["id"] not in SELECTED:
            continue
        for name, evidence, neutral in [("baseline", baseline, False), ("neutral_prompt", baseline, True),
                                        ("neutral_no_shortcut", without_shortcut, True)]:
            if name == "neutral_no_shortcut" and baseline == without_shortcut:
                continue
            g = config["generation"]
            options = {key: g[key] for key in ["temperature", "top_p", "num_predict", "repeat_last_n", "repeat_penalty"] if key in g}
            jobs.append({"id": item["id"], "question": question, "domain": item["domain"],
                         "variant": name, "contexts": evidence, "prompt": trial_prompt(question, evidence, neutral),
                         "options": options, "base_url": g["ollama_base_url"]})
    plan = {"baseline_tag": "codex/pre-source-selection-trial-20260922",
            "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "input_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "context_comparisons": comparisons, "jobs": jobs,
            "note": "Controlled paths and fresh retrieval not tested. No-op context variants are skipped, not independent results."}
    plan_path = OUTPUT / ("dry_run.json" if args.dry_run else "plan.json")
    if not args.dry_run and (OUTPUT / "results.json").exists():
        raise RuntimeError("Existing results: preserve them; do not overwrite or silently resume")
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    print(f"Plan: {len(jobs)} calls; {sum(not x['same_contexts'] for x in comparisons)} of {len(comparisons)} LLM cases affected by shortcut", flush=True)
    if args.dry_run:
        return
    rows = []
    for job in jobs:
        started = time.monotonic()
        payload = {"model": "qwen3:8b", "messages": [{"role": "user", "content": job["prompt"]}],
                   "stream": False, "think": False, "options": job["options"]}
        print("Starting", job["id"], job["variant"], flush=True)
        request = urllib.request.Request(job["base_url"].rstrip("/") + "/api/chat",
                                         data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(request, timeout=600) as response:
                result = json.load(response)
            if "message" not in result:
                raise RuntimeError(str(result))
        except Exception as exc:
            (OUTPUT / "failure.json").write_text(json.dumps({"id": job["id"], "variant": job["variant"], "error": str(exc)}, indent=2))
            raise
        raw = result["message"]["content"]
        answer = canonicalize_answer(raw, [c["id"] for c in job["contexts"][:3]])
        pipeline, _ = selector(job["domain"])
        route = "llm"
        if pipeline._violates_answer_language(job["question"], answer):
            answer = pipeline._fallback_evidence_answer(job["question"], job["contexts"]) or pipeline._bangla_language_safety_answer(job["contexts"])
            route = "llm_then_evidence_fallback"
        rows.append({"id": job["id"], "question": job["question"], "variant": job["variant"],
                     "seconds": round(time.monotonic()-started, 2), "raw_answer": raw, "display_answer": answer,
                     "route": route, "ollama_metadata": {k: v for k, v in result.items() if k != "message"}})
        (OUTPUT / "results.json").write_text(json.dumps({"rows": rows}, ensure_ascii=False, indent=2) + "\n")
        (OUTPUT / "results.md").write_text(render(rows))
        print("Completed", len(rows), "/", len(jobs), flush=True)


if __name__ == "__main__":
    main()
