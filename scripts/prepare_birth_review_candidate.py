"""Build a hash-gated, unactivated Birth Registration review candidate."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def apply_changes(text: str, changes: list[dict]) -> str:
    for change in changes:
        before = change["before"]
        if text.count(before) != 1:
            raise ValueError(f"Repair anchor not unique: {change['id']}")
        text = text.replace(before, change["after"], 1)
    return text


def build(original_root: Path, output: Path, repairs_path: Path) -> dict:
    from domains.birth_death_registration.scripts import prepare_chunks as prep

    raw = ROOT / "domains/birth_death_registration/data/raw"
    config_path = ROOT / "domains/birth_death_registration/config.json"
    config = json.loads(config_path.read_text())
    active_chunks = ROOT / config["data"]["chunk_output_path"]
    files = sorted((raw / "json").glob("*.json")) + sorted((raw / "md").glob("*.md"))
    original_root = original_root.resolve()
    output = output.resolve()
    if output.exists():
        raise ValueError("Output exists; choose a new revision rather than overwrite it")
    if not original_root.is_dir():
        raise ValueError("Original source directory is required")
    repairs = json.loads(repairs_path.read_text())["files"]
    repair_by_file = {r["prepared_file"]: r for r in repairs}
    baseline_hashes = {str(p): sha(p) for p in [*files, config_path, active_chunks]}
    for repair in repairs:
        if sha(raw / repair["prepared_file"]) != repair["prepared_sha256"]:
            raise ValueError(f"Prepared source changed: {repair['prepared_file']}")
        if sha(original_root / repair["original_file"]) != repair["original_sha256"]:
            raise ValueError(f"Original source changed: {repair['original_file']}")
        apply_changes((raw / repair["prepared_file"]).read_text(), repair["changes"])

    original_files = sorted(p for p in original_root.rglob("*") if p.is_file())
    output.mkdir(parents=True)
    records, chunks = [], []
    inferred_html = {
        "birth_and_death_registration_act_2004.md": "birth_and_death_registration_act_2004.html",
        "home_registrar_generals_office_birth_and_death_registration.md": "home_registrar_generals_office_birth_and_death_registration.html",
        "faqs_birth_death_registration_01.json": "faqs_on_birth_and_death_registration.html",
        "faqs_birth_death_registration_02.json": "faqs_on_birth_and_death_registration_02.html",
    }
    for source in files:
        relative = str(source.relative_to(raw))
        target = output / "raw" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        repair = repair_by_file.get(relative)
        if repair:
            target.write_text(apply_changes(source.read_text(), repair["changes"]), encoding="utf-8")
        else:
            shutil.copy2(source, target)
        metadata = prep.parse_frontmatter(source.read_text())[0] if source.suffix == ".md" else {}
        name = metadata.get("source_file") or inferred_html.get(source.name)
        matches = [p for p in original_files if p.name == name]
        selected = repair["original_file"] if repair else None
        rows = (prep.faq_json_chunks(target) if source.suffix == ".json" else
                prep.markdown_chunks(target, skip_faq=True,
                                     max_chars=config["preprocessing"]["max_chunk_chars"]))
        review = "targeted_source_review" if repair else "pending_original_content_review"
        if "guidelines_2021_ocr" in source.name:
            review = "ocr_page_review_required"
        for row in rows:
            row["metadata"].update({
                "candidate_source": relative,
                "candidate_source_sha256": sha(target),
                "source_review_status": review,
            })
            if repair and "notice_" in source.name:
                row["metadata"]["document_date"] = "2022-12-22"
                row["metadata"]["date_basis"] = "assistant_visual_review_of_supplied_pdf"
                row["metadata"]["current_applicability_verified"] = False
        records.append({
            "prepared_file": relative,
            "baseline_sha256": sha(source), "candidate_sha256": sha(target),
            "declared_source_file": metadata.get("source_file"),
            "mapping_basis": "repair_source_hash" if repair else
                "declared_filename" if metadata.get("source_file") else "filename_hypothesis",
            "selected_original": selected,
            "original_candidates": [{"path": str(p.relative_to(original_root)), "sha256": sha(p)} for p in matches],
            "review_status": review,
            "changes": repair["changes"] if repair else [],
            "chunk_ids": [row["id"] for row in rows],
            "exclusion_reason": "FAQ Markdown excluded in favor of JSON; equivalence pending review" if not rows else None,
        })
        chunks.extend(rows)

    ids = [r["id"] for r in chunks]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate candidate chunk IDs")
    tokenizer = prep.load_tokenizer(config["embedding"]["model"], local_files_only=True)
    warnings = prep.add_token_audit_metadata(chunks, tokenizer)
    active = {r["id"]: r for r in map(json.loads, active_chunks.read_text().splitlines())}
    changed = [r["id"] for r in chunks if r["id"] in active and r["content"] != active[r["id"]]["content"]]
    manifest = {
        "status": "unactivated_partial_review_candidate",
        "original_root": str(original_root),
        "original_inventory": [{"path": str(p.relative_to(original_root)), "sha256": sha(p)} for p in original_files],
        "repairs_sha256": sha(repairs_path), "documents": records,
        "baseline_chunks": len(active), "candidate_chunks": len(chunks),
        "changed_content_ids": changed, "added_ids": sorted(set(ids) - active.keys()),
        "removed_ids": sorted(active.keys() - set(ids)),
        "max_retrieval_tokens": max(r["metadata"]["retrieval_token_count"] for r in chunks),
        "token_warnings": warnings,
        "limits": "Source fidelity review is incomplete. No current-rule or answer-quality claim. No index built.",
    }
    if any(sha(Path(p)) != digest for p, digest in baseline_hashes.items()):
        raise ValueError("A baseline input changed during candidate preparation")
    manifest["baseline_inputs_unchanged"] = True
    (output / "chunks.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in chunks), encoding="utf-8")
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repairs", type=Path, default=ROOT / "docs/data_cleanup/birth_review_20261008/repairs.json")
    args = parser.parse_args()
    result = build(args.original_root, args.output, args.repairs)
    print(json.dumps({k: result[k] for k in ("status", "baseline_chunks", "candidate_chunks", "changed_content_ids", "added_ids", "removed_ids", "max_retrieval_tokens", "baseline_inputs_unchanged")}, indent=2))
