"""Run the manual-audit questions through the selected CivicRAG domain and save raw answers."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import time
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
    with urllib.request.urlopen(request, timeout=600) as response:
        result = json.load(response)
    hint = item["expected_evidence_hint"].casefold()
    result["expected_evidence_present"] = any(
        hint in (
            source["id"]
            + " "
            + source["metadata"].get("source_relative_path", "")
            + " "
            + source["content"]
        ).casefold()
        for source in result.get("sources", [])
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
                f"## {item['id']} ({item['domain']} / {item['category']})",
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
    args = parser.parse_args()
    items = json.loads(args.input.read_text(encoding="utf-8"))["questions"]
    if args.limit:
        items = items[: args.limit]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    for item in items:
        row = request_answer(item, args.model)
        rows.append(row)
        args.output.write_text(
            json.dumps({"model": args.model, "rows": rows}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(item["id"], row["result"]["answer_route"], row["result"]["expected_evidence_present"], flush=True)
    write_markdown(rows, args.output)


if __name__ == "__main__":
    main()
