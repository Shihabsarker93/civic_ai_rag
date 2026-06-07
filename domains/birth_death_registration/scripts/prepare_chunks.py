from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

from transformers import AutoTokenizer


PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

CHUNKING_VERSION = "2026-06-07-nfc-token-audit"
PRACTICAL_TOKEN_WARNING_THRESHOLD = 1024
ZERO_WIDTH_RE = re.compile(r"[\u200b\u200c\u200d\u200e\u200f\ufeff]")

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
TABLE_ROW_RE = re.compile(r"^\|(.+)\|$", re.MULTILINE)
LEGAL_HEADING_RE = re.compile(r"^###\s+(ধারা|বিধি)\s+([০-৯0-9কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়]+)[।\s—:-]*(.*)$")
CHAPTER_HEADING_RE = re.compile(r"^##\s+(.+অধ্যা[য়য়].*)$")
QUESTION_HEADING_RE = re.compile(r"^##\s+প্রশ্ন\s+([০-৯0-9]+)[।:]?\s*(.*)$")
STEP_HEADING_RE = re.compile(r"^##+\s+(ধাপ\s+[০-৯0-9]+|পরিস্থিতি\s+[০-৯0-9]+|.+প্রক্রিয়া|.+প্রক্রিয়া|.+নির্দেশনা|.+তথ্য|.+পদ্ধতি|.+সেবাসমূহ|.+যোগাযোগ).*$")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[।.!?])\s+|(?=\([০-৯0-9কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়]+\))")


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def as_metadata_value(value: Any) -> str | int | float | bool:
    if isinstance(value, (str, int, float, bool)):
        return value
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return json.dumps(value, ensure_ascii=False)


def flatten_metadata(metadata: dict[str, Any]) -> dict[str, str | int | float | bool]:
    return {key: as_metadata_value(value) for key, value in metadata.items()}


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    metadata: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")
    return metadata, text[match.end() :].strip()


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = ZERO_WIDTH_RE.sub("", text)
    text = text.replace("\r", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_tokenizer(model_name: str, *, local_files_only: bool) -> Any:
    return AutoTokenizer.from_pretrained(model_name, local_files_only=local_files_only)


def token_count(tokenizer: Any, text: str) -> int:
    return len(tokenizer.encode(text, add_special_tokens=True))


def add_token_audit_metadata(chunks: list[dict[str, Any]], tokenizer: Any) -> list[str]:
    warnings: list[str] = []
    model_limit = int(getattr(tokenizer, "model_max_length", 8192))
    for chunk in chunks:
        content_tokens = token_count(tokenizer, chunk["content"])
        retrieval_tokens = token_count(tokenizer, chunk.get("retrieval_text", chunk["content"]))
        chunk["metadata"]["chunking_version"] = CHUNKING_VERSION
        chunk["metadata"]["content_token_count"] = content_tokens
        chunk["metadata"]["retrieval_token_count"] = retrieval_tokens
        chunk["metadata"]["embedding_model_max_tokens"] = model_limit
        if retrieval_tokens > PRACTICAL_TOKEN_WARNING_THRESHOLD:
            warnings.append(
                f"{chunk['id']} has {retrieval_tokens} retrieval tokens "
                f"(practical warning threshold: {PRACTICAL_TOKEN_WARNING_THRESHOLD})"
            )
        if retrieval_tokens > model_limit:
            raise ValueError(
                f"Chunk {chunk['id']} has {retrieval_tokens} retrieval tokens, "
                f"exceeding tokenizer limit {model_limit}"
            )
    return warnings


def slug(text: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9\u0980-\u09FF]+", "_", text).strip("_").lower()
    return value[:80] or "chunk"


def split_heading_sections(body: str) -> list[dict[str, Any]]:
    lines = body.splitlines()
    sections: list[dict[str, Any]] = []
    current = {"level": 1, "title": "document", "lines": []}
    for line in lines:
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            if current["lines"]:
                sections.append(current)
            current = {"level": len(match.group(1)), "title": match.group(2).strip(), "lines": []}
            continue
        current["lines"].append(line)
    if current["lines"]:
        sections.append(current)
    return sections


def split_long_text(text: str, max_chars: int) -> list[str]:
    text = normalize_text(text)
    if len(text) <= max_chars:
        return [text] if text else []

    units = [unit.strip() for unit in SENTENCE_SPLIT_RE.split(text) if unit.strip()]
    chunks: list[str] = []
    current: list[str] = []
    for unit in units:
        candidate = " ".join([*current, unit]).strip()
        if current and len(candidate) > max_chars:
            chunks.append(" ".join(current).strip())
            current = []
        current.append(unit)
    if current:
        chunks.append(" ".join(current).strip())
    return chunks


def make_chunk(
    *,
    chunk_id: str,
    content: str,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    metadata = dict(metadata)
    content = normalize_text(content)
    retrieval_text = content
    aliases = english_retrieval_aliases(
        str(metadata.get("document_type", "")),
        content,
        scope=str(metadata.get("service_scope", "")) or None,
    )
    if aliases:
        metadata["search_aliases"] = aliases
        retrieval_text = f"{content}\nRetrieval aliases (for search only, not answer evidence): {aliases}"
    return {
        "id": chunk_id,
        "content": content,
        "retrieval_text": normalize_text(retrieval_text),
        "metadata": flatten_metadata(metadata),
    }


def faq_json_chunks(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))["document"]
    doc_meta = data["metadata"]
    chunks: list[dict[str, Any]] = []

    if "preamble" in data:
        preamble = data["preamble"]
        content = "\n".join(
            [
                "Service: birth and death registration",
                "Document type: faq_preamble",
                f"Title: {doc_meta.get('title', '')}",
                f"Title EN: {doc_meta.get('title_en', '')}",
                f"Content: {preamble.get('content', '')}",
                f"Legal references: {', '.join(preamble.get('legal_references', []))}",
                f"Keywords BN: {', '.join(preamble.get('keywords', []))}",
                f"Keywords EN: {', '.join(preamble.get('keywords_en', []))}",
            ]
        )
        chunks.append(
            make_chunk(
                chunk_id=preamble["chunk_id"],
                content=content,
                metadata={
                    **doc_meta,
                    "source_path": str(path.name),
                    "document_type": "faq_preamble",
                    "category": preamble.get("category", "legal_overview"),
                    "service": "birth_death_registration",
                    "service_scope": "birth_death",
                },
            )
        )

    for item in data.get("chunks", []):
        content = "\n".join(
            [
                "Service: birth and death registration",
                "Document type: faq",
                f"Category: {item.get('category', '')}",
                f"Title: {doc_meta.get('title', '')}",
                f"Title EN: {doc_meta.get('title_en', '')}",
                f"Question: {item.get('question', '')}",
                f"Answer: {item.get('answer', '')}",
                f"Legal references: {', '.join(item.get('legal_references', []))}",
                f"Keywords BN: {', '.join(item.get('keywords', []))}",
                f"Keywords EN: {', '.join(item.get('keywords_en', []))}",
            ]
        )
        chunks.append(
            make_chunk(
                chunk_id=item["chunk_id"],
                content=content,
                metadata={
                    **doc_meta,
                    "source_path": str(path.name),
                    "document_type": "faq",
                    "category": item.get("category", ""),
                    "faq_number": item.get("faq_number", ""),
                    "service": "birth_death_registration",
                    "service_scope": infer_scope(item.get("question", "") + " " + item.get("answer", "")),
                },
            )
        )
    return chunks


def infer_scope(text: str) -> str:
    has_birth = "জন্ম" in text or "birth" in text.lower()
    has_death = "মৃত্যু" in text or "death" in text.lower()
    if has_birth and has_death:
        return "birth_death"
    if has_death:
        return "death"
    return "birth"


def english_retrieval_aliases(doc_type: str, text: str, *, scope: str | None = None) -> str:
    text_lc = text.lower()
    aliases = {
        "Bangladesh government service",
        "birth and death registration",
        "BDRIS",
        "civil registration",
        "certificate",
    }

    scope = scope or infer_scope(text)
    if scope in {"birth", "birth_death"}:
        aliases.update(
            {
                "জন্ম নিবন্ধন",
                "জন্ম নিবন্ধন আবেদন",
                "জন্ম সনদ",
                "জন্ম সনদ আবেদন",
                "আমি কীভাবে জন্ম নিবন্ধন করতে পারি",
                "কিভাবে জন্ম নিবন্ধন করব",
                "কীভাবে জন্ম নিবন্ধন করব",
                "birth certificate",
                "birth registration",
                "birth certificate registration",
                "birth registration certificate",
                "online birth registration",
                "apply for birth certificate",
            }
        )
    if scope in {"death", "birth_death"}:
        aliases.update(
            {
                "মৃত্যু নিবন্ধন",
                "মৃত্যু নিবন্ধন আবেদন",
                "মৃত্যু সনদ",
                "মৃত্যু সনদ আবেদন",
                "আমি কীভাবে মৃত্যু নিবন্ধন করতে পারি",
                "death certificate",
                "death registration",
                "death certificate registration",
                "death registration certificate",
                "online death registration",
                "apply for death certificate",
            }
        )

    if doc_type in {"application_process", "portal_summary", "general_guidance", "guidelines_ocr"}:
        aliases.update(
            {
                "আবেদন প্রক্রিয়া",
                "আবেদন পদ্ধতি",
                "ধাপে ধাপে আবেদন",
                "নিবন্ধন প্রক্রিয়া",
                "নিবন্ধন পদ্ধতি",
                "প্রয়োজনীয় কাগজপত্র",
                "application process",
                "registration process",
                "how to apply",
                "online application",
                "required documents",
                "citizen service",
            }
        )
    if doc_type in {"correction_process", "correction_notice_ocr"} or "সংশোধন" in text or "correction" in text_lc:
        aliases.update(
            {
                "সংশোধন আবেদন",
                "জন্ম নিবন্ধন সংশোধন",
                "মৃত্যু নিবন্ধন সংশোধন",
                "certificate correction",
                "birth certificate correction",
                "death certificate correction",
                "fix certificate information",
                "amend registration information",
                "name correction",
            }
        )
    if "জন্ম তারিখ" in text or "date of birth" in text_lc:
        aliases.update({"জন্ম তারিখ সংশোধন", "date of birth correction"})
    if "জাতীয়তা" in text or "nationality" in text_lc:
        aliases.update({"জাতীয়তা সংশোধন", "nationality correction"})
    if "রেজিস্ট্রেশন তারিখ" in text or "registration date" in text_lc:
        aliases.update({"রেজিস্ট্রেশন তারিখ সংশোধন", "registration date correction"})
    if "ইস্যু তারিখ" in text or "issue date" in text_lc:
        aliases.update({"ইস্যু তারিখ সংশোধন", "issue date correction"})
    if "একাধিক" in text or "বাতিল" in text or "duplicate" in text_lc or "cancel" in text_lc:
        aliases.update(
            {
                "একাধিক জন্ম সনদ বাতিল",
                "একাধিক মৃত্যু সনদ বাতিল",
                "ডুপ্লিকেট জন্ম সনদ বাতিল",
                "duplicate certificate cancellation",
                "cancel duplicate birth certificate",
                "cancel duplicate death certificate",
            }
        )
    if doc_type == "guidelines_ocr":
        aliases.update(
            {
                "নির্দেশিকা",
                "জন্ম ও মৃত্যু নিবন্ধন নির্দেশিকা",
                "নিবন্ধকের দায়িত্ব",
                "৪৫ দিনের মধ্যে নিবন্ধন",
                "টাস্ক ফোর্স",
                "registration guideline",
                "birth and death registration guideline",
                "registrar responsibility",
                "register within 45 days",
                "task force",
            }
        )
    if doc_type in {"fees_table", "fee_row"}:
        aliases.update(
            {
                "নিবন্ধন ফি",
                "সনদ ফি",
                "আবেদন ফি",
                "registration fee",
                "certificate fee",
                "government fee",
                "cost",
                "payment",
            }
        )
    if doc_type in {"legal_act", "legal_rules", "faq_preamble"}:
        aliases.update(
            {
                "law",
                "legal rule",
                "registration rule",
                "legal requirement",
                "act",
            }
        )
    if doc_type == "faq":
        aliases.update({"প্রশ্ন উত্তর", "সাধারণ জিজ্ঞাসা", "FAQ", "question answer", "common question", "citizen question"})
    if "ওয়েবসাইট" in text or "ওয়েবসাইট" in text or "website" in text_lc:
        aliases.update({"ওয়েবসাইটে আবেদন", "অনলাইন আবেদন", "অনলাইন পোর্টাল", "website", "online portal", "service portal"})
    if "যাচাই" in text:
        aliases.update({"verify certificate", "certificate verification", "registration verification"})
    if "পিতা" in text or "মাতা" in text or "parent" in text_lc:
        aliases.update({"parent information", "father mother information", "parents registration"})
    if "নিবন্ধক" in text or "কার্যালয়" in text or "office" in text_lc:
        aliases.update({"registration office", "registrar office", "local government office"})

    return ", ".join(sorted(aliases, key=str.lower))


def classify_markdown(path: Path, metadata: dict[str, str], body: str) -> str:
    document_type_hint = metadata.get("document_type_hint", "").strip()
    if document_type_hint == "guidelines":
        return "guidelines_ocr"
    if document_type_hint == "correction_notice":
        return "correction_notice_ocr"

    name_title = f"{path.name} {metadata.get('bengali_title', '')} {metadata.get('title', '')}".lower()
    heading = first_heading(body)
    if "faq" in name_title or "প্রশ্ন" in body[:500]:
        return "faq_markdown"
    if "_act_" in path.stem.lower() or "আইন, ২০০৪" in heading:
        return "legal_act"
    if "rules" in name_title or "বিধিমালা" in name_title:
        return "legal_rules"
    if "fees" in name_title or "ফি" in name_title or re.search(r"^\|", body, re.MULTILINE):
        return "fees"
    if "correction" in name_title or "সংশোধন" in name_title:
        return "correction_process"
    if "process" in name_title or "প্রক্রিয়া" in name_title or "প্রক্রিয়া" in name_title or "প্রসেস" in name_title:
        return "application_process"
    if "home" in name_title or "কার্যালয়" in body[:300] or "কার্যালয়" in body[:300]:
        return "portal_summary"
    return "general_guidance"


def markdown_chunks(path: Path, *, skip_faq: bool, max_chars: int) -> list[dict[str, Any]]:
    metadata, raw_body = parse_frontmatter(path.read_text(encoding="utf-8"))
    body = normalize_text(raw_body)
    doc_type = classify_markdown(path, metadata, body)
    if doc_type == "faq_markdown" and skip_faq:
        return []

    if doc_type == "fees":
        return fees_chunks(path, metadata, body)
    if doc_type in {"legal_act", "legal_rules"}:
        return legal_chunks(path, metadata, body, doc_type=doc_type, max_chars=max_chars)

    return section_chunks(path, metadata, body, doc_type=doc_type, max_chars=max_chars)


def fees_chunks(path: Path, metadata: dict[str, str], body: str) -> list[dict[str, Any]]:
    title = metadata.get("bengali_title") or metadata.get("title") or first_heading(body) or path.stem
    table_rows = [row.strip() for row in TABLE_ROW_RE.findall(body)]
    chunks: list[dict[str, Any]] = []
    chunks.append(
        make_chunk(
            chunk_id=f"{slug(path.stem)}_table_full",
            content="\n".join(["Service: birth and death registration", "Document type: fees_table", f"Title: {title}", body]),
            metadata=base_md_metadata(path, metadata, "fees_table", title),
        )
    )

    data_rows = [row for row in table_rows if "---" not in row and "ক্রম" not in row and "বাবদ" not in row]
    for index, row in enumerate(data_rows, start=1):
        cells = [cell.strip() for cell in row.split("|")]
        label = cells[1] if len(cells) > 1 else row
        amount = cells[-1] if cells else ""
        chunks.append(
            make_chunk(
                chunk_id=f"{slug(path.stem)}_fee_row_{index:02d}",
                content="\n".join(
                    [
                        "Service: birth and death registration",
                        "Document type: fee_row",
                        f"Title: {title}",
                        f"Fee item: {label}",
                        f"Fee amount: {amount}",
                        f"Original row: | {row} |",
                    ]
                ),
                metadata={
                    **base_md_metadata(path, metadata, "fee_row", title),
                    "row_index": index,
                    "fee_item": label,
                    "fee_amount": amount,
                },
            )
        )
    return chunks


def legal_chunks(path: Path, metadata: dict[str, str], body: str, *, doc_type: str, max_chars: int) -> list[dict[str, Any]]:
    title = metadata.get("bengali_title") or first_heading(body) or path.stem
    chunks: list[dict[str, Any]] = []
    current_chapter = ""
    current_heading = title
    current_legal_type = "document"
    current_legal_no = ""
    current_lines: list[str] = []

    def flush() -> None:
        if not current_lines:
            return
        text = normalize_text("\n".join(current_lines))
        for index, part in enumerate(split_long_text(text, max_chars), start=1):
            chunks.append(
                make_chunk(
                    chunk_id=f"{slug(path.stem)}_{slug(current_legal_type)}_{slug(current_legal_no or current_heading)}_{index:02d}",
                    content="\n".join(
                        [
                            "Service: birth and death registration",
                            f"Document type: {doc_type}",
                            f"Title: {title}",
                            f"Chapter: {current_chapter}",
                            f"Legal unit: {current_legal_type} {current_legal_no} {current_heading}",
                            f"Content: {part}",
                        ]
                    ),
                    metadata={
                        **base_md_metadata(path, metadata, doc_type, title),
                        "chapter": current_chapter,
                        "legal_unit_type": current_legal_type,
                        "legal_unit_no": current_legal_no,
                        "section_title": current_heading,
                        "part_index": index,
                    },
                )
            )

    for line in body.splitlines():
        chapter = CHAPTER_HEADING_RE.match(line)
        if chapter:
            current_chapter = chapter.group(1).strip()
            continue
        legal = LEGAL_HEADING_RE.match(line)
        if legal:
            flush()
            current_lines = []
            current_legal_type = legal.group(1)
            current_legal_no = legal.group(2)
            current_heading = legal.group(3).strip() or line.strip("# ")
            continue
        if line.startswith("# "):
            continue
        current_lines.append(line)
    flush()
    return chunks


def section_chunks(path: Path, metadata: dict[str, str], body: str, *, doc_type: str, max_chars: int) -> list[dict[str, Any]]:
    title = metadata.get("bengali_title") or metadata.get("title") or first_heading(body) or path.stem
    chunks: list[dict[str, Any]] = []
    for section_index, section in enumerate(split_heading_sections(body), start=1):
        section_title = section["title"]
        if section_title == "document" or section_title == title:
            continue
        if doc_type == "portal_summary" and not is_useful_portal_section(section_title):
            continue
        text = normalize_text("\n".join(section["lines"]))
        if not text:
            continue
        for part_index, part in enumerate(split_long_text(text, max_chars), start=1):
            chunks.append(
                make_chunk(
                    chunk_id=f"{slug(path.stem)}_{section_index:03d}_{part_index:02d}",
                    content="\n".join(
                        [
                            "Service: birth and death registration",
                            f"Document type: {doc_type}",
                            f"Title: {title}",
                            f"Section: {section_title}",
                            f"Content: {part}",
                        ]
                    ),
                    metadata={
                        **base_md_metadata(path, metadata, doc_type, title),
                        "section_title": section_title,
                        "section_index": section_index,
                        "part_index": part_index,
                    },
                )
            )
    return chunks


def is_useful_portal_section(section_title: str) -> bool:
    useful_terms = [
        "যোগাযোগ",
        "সহায়তা",
        "সহায়তা",
        "নাগরিক সেবা",
        "অভ্যন্তরীণ ই-সেবা",
        "আপনার জিজ্ঞাসা",
        "জন্ম নিবন্ধন",
        "মৃত্যু নিবন্ধন",
        "BDRIS",
        "বিডিআরআইএস",
        "জরুরি যোগাযোগ",
    ]
    return any(term in section_title for term in useful_terms)


def first_heading(body: str) -> str:
    match = HEADING_RE.search(body)
    return match.group(2).strip() if match else ""


def base_md_metadata(path: Path, metadata: dict[str, str], doc_type: str, title: str) -> dict[str, Any]:
    return {
        "service": "birth_death_registration",
        "service_scope": infer_scope(f"{path.name} {title}"),
        "document_type": doc_type,
        "title": title,
        "source_file": metadata.get("source_file", path.name),
        "source_path": f"md/{path.name}",
        "source_url": metadata.get("source_url", metadata.get("source_url", "")),
        "encoding": metadata.get("encoding", ""),
        "language": "bn",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare document-type-aware chunks for birth/death registration.")
    parser.add_argument("--config", default="domains/birth_death_registration/config.json")
    args = parser.parse_args()

    config = load_config(PROJECT_ROOT / args.config)
    data_config = config["data"]
    preprocessing_config = config["preprocessing"]
    embedding_config = config["embedding"]
    raw_json_dir = PROJECT_ROOT / data_config["raw_json_dir"]
    raw_markdown_dir = PROJECT_ROOT / data_config["raw_markdown_dir"]
    output_path = PROJECT_ROOT / data_config["chunk_output_path"]

    chunks: list[dict[str, Any]] = []
    for path in sorted(raw_json_dir.glob("*.json")):
        chunks.extend(faq_json_chunks(path))
    for path in sorted(raw_markdown_dir.glob("*.md")):
        chunks.extend(
            markdown_chunks(
                path,
                skip_faq=preprocessing_config.get("skip_markdown_faq_duplicates", True),
                max_chars=preprocessing_config.get("max_chunk_chars", 1400),
            )
        )

    seen: set[str] = set()
    duplicates = [chunk["id"] for chunk in chunks if chunk["id"] in seen or seen.add(chunk["id"])]
    if duplicates:
        raise ValueError(f"Duplicate chunk ids found: {duplicates[:10]}")

    tokenizer = load_tokenizer(
        embedding_config["model"],
        local_files_only=embedding_config.get("local_files_only", True),
    )
    token_warnings = add_token_audit_metadata(chunks, tokenizer)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    by_type: dict[str, int] = {}
    for chunk in chunks:
        doc_type = str(chunk["metadata"].get("document_type", "unknown"))
        by_type[doc_type] = by_type.get(doc_type, 0) + 1

    print(f"Chunks written: {len(chunks)}")
    print(json.dumps(by_type, ensure_ascii=False, indent=2))
    print(f"Chunking version: {CHUNKING_VERSION}")
    print(f"Tokenizer max tokens: {tokenizer.model_max_length}")
    print(f"Chunks above practical {PRACTICAL_TOKEN_WARNING_THRESHOLD}-token warning threshold: {len(token_warnings)}")
    for warning in token_warnings[:10]:
        print(f"WARNING: {warning}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
