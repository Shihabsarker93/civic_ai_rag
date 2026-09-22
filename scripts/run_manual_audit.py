"""Run the manual-audit questions through the selected CivicRAG domain and save raw answers."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "docs/evaluation/manual_audit_2026_09_19/questions.json"
DEFAULT_OUTPUT = ROOT / "docs/evaluation/manual_audit_2026_09_19/answers_llama3_2.json"


def request_answer(item: dict, model: str) -> dict:
    payload = json.dumps(
        {"domain": item["domain"], "query": item["question"], "model": model, "method": "civic"}
    ).encode()
    request = urllib.request.Request(
        "http://127.0.0.1:7860/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=600) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Chat request failed for {item['id']}: HTTP {error.code}: {body}") from error
    hint = item.get("expected_evidence_hint", "").casefold()
    result["expected_evidence_present"] = (
        any(
            hint in (
                source["id"]
                + " "
                + source["metadata"].get("source_relative_path", "")
                + " "
                + source["content"]
            ).casefold()
            for source in result.get("sources", [])
        )
        if hint
        else None
    )
    return {
        "audit_item": item,
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "result": result,
    }


def write_markdown(rows: list[dict], output: Path) -> None:
    lines = [
        "# Manual audit answers",
        "",
        "These are raw chatbot outputs. Expected-evidence-present checks only a predefined hint and is not an answer-correctness score.",
        "",
    ]
    for row in rows:
        item, result = row["audit_item"], row["result"]
        lines.extend(
            [
                f"## {item['id']} ({item['domain']} / {item.get('family', item.get('category', 'uncategorized'))} / {item.get('variant', 'single')})",
                "",
                f"Question: {item['question']}",
                "",
                f"Model: {result['model']}; route: {result['answer_route']}; time: {row['elapsed_seconds']} s; expected evidence present: {result['expected_evidence_present']}.",
                "",
                "Answer:",
                "",
                result["answer"],
                "",
                "Retrieved sources:",
                *[
                    f"- {source['id']}: {source['metadata'].get('source_relative_path', 'unknown source')}"
                    for source in result.get("sources", [])
                ],
                "",
            ]
        )
    output.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--model", default="llama3.2")
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Continue from existing output rows whose audit-item IDs are already complete.",
    )
    args = parser.parse_args()
    items = json.loads(args.input.read_text(encoding="utf-8"))["questions"]
    if args.limit:
        items = items[: args.limit]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output.with_suffix(".manifest.json")
    files = [*sorted((ROOT / "src").rglob("*.py")),
             *[ROOT / "domains" / d / "config.json" for d in ("birth_death_registration", "passport", "brta")]]
    signature = {"model": args.model, "question_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
                 "files": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    if args.resume and args.output.exists():
        if not manifest_path.exists() or json.loads(manifest_path.read_text())["signature"] != signature:
            raise RuntimeError("Refusing to mix runs: missing or changed code/config/question manifest. Use a new output path.")
    else:
        manifest_path.write_text(json.dumps({"signature": signature,
            "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "domain_configs": {d: json.loads((ROOT / "domains" / d / "config.json").read_text())
                               for d in ("birth_death_registration", "passport", "brta")},
            "input": str(args.input), "started_at_unix": time.time()}, ensure_ascii=False, indent=2) + "\n")
    rows: list[dict] = []
    completed_ids: set[str] = set()
    if args.resume and args.output.exists():
        previous = json.loads(args.output.read_text(encoding="utf-8"))
        rows = previous.get("rows", [])
        completed_ids = {row["audit_item"]["id"] for row in rows}

    for item in items:
        if item["id"] in completed_ids:
            print(item["id"], "skipped", flush=True)
            continue
        try:
            row = request_answer(item, args.model)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as error:
            args.output.write_text(
                json.dumps({"model": args.model, "rows": rows}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            raise RuntimeError(f"Audit stopped on {item['id']}: {error}") from error
        rows.append(row)
        args.output.write_text(
            json.dumps({"model": args.model, "rows": rows}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        write_markdown(rows, args.output)
        print(item["id"], row["result"]["answer_route"], row["result"]["expected_evidence_present"], flush=True)
    write_markdown(rows, args.output)


if __name__ == "__main__":
    main()
