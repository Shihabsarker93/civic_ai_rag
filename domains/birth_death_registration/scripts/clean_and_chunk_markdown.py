from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))


BANGLA_RE = re.compile(r"[\u0980-\u09FF]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
MULTISPACE_RE = re.compile(r"[ \t]+")
BLANKS_RE = re.compile(r"\n{3,}")
MARKDOWN_DECORATION_RE = re.compile(r"[*_`]+")


NOISE_EXACT = {
    "বাংলাদেশ জাতীয় তথ্য বাতায়ন",
    "বাংলাদেশ জাতীয় তথ্য বাতায়ন",
    "স্থানীয় সরকার বিভাগ",
    "মেনু নির্বাচন করুন",
    "আরও",
    "এই কনটেন্টটি শেয়ার করতে ক্লিক করুন",
    "এই কনটেন্টটি শেয়ার করতে ক্লিক করুন",
    "আপনার মতামত প্রদান করুন",
    "কন্টেন্ট: পাতা",
    "কনটেন্ট: পাতা",
    "<!-- image -->",
}

NOISE_PATTERNS = [
    re.compile(r"^কনটেন্টটি শেষ হাল-নাগাদ করা হয়েছে:"),
    re.compile(r"^এই কনটেন্টটি শেষ হাল-নাগাদ করা হয়েছে:"),
    re.compile(r"^\-\s*\[?(আমাদের সম্পর্কে|কর্মকর্তাবৃন্দ|আমাদের সেবা|আইন|বিধিমালা|নিয়োগ|ডাউনলোড|যোগাযোগ|ওয়েব মেইল|নোটিশ বোর্ড)"),
    re.compile(r"^\[?রেজিস্ট্রার জেনারেলের কার্যালয়"),
    re.compile(r"^#\s*\[?রেজিস্ট্রার জেনারেলের কার্যালয়"),
    re.compile(r"^#\s*\[?গড়াডোবা ইউনিয়ন"),
]


@dataclass(frozen=True)
class Section:
    title: str
    level: int
    lines: list[str]


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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
    return metadata, text[match.end() :]


def normalize_line(line: str) -> str:
    line = line.replace("\ufeff", "")
    line = line.replace("\r", "")
    line = LINK_RE.sub(r"\1", line)
    line = MULTISPACE_RE.sub(" ", line)
    return line.strip()


def is_noise_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    plain = MARKDOWN_DECORATION_RE.sub("", stripped).strip()
    if plain in NOISE_EXACT:
        return True
    return any(pattern.search(plain) for pattern in NOISE_PATTERNS)


def clean_markdown_body(body: str) -> str:
    cleaned_lines = []
    for raw_line in body.splitlines():
        line = normalize_line(raw_line)
        if is_noise_line(line):
            continue
        cleaned_lines.append(line)
    cleaned = "\n".join(cleaned_lines)
    cleaned = BLANKS_RE.sub("\n\n", cleaned)
    return cleaned.strip()


def detect_language(text: str) -> str:
    bangla_chars = len(BANGLA_RE.findall(text))
    alpha_chars = sum(character.isalpha() for character in text)
    if alpha_chars == 0:
        return "unknown"
    if bangla_chars / alpha_chars > 0.5:
        return "bn"
    if bangla_chars:
        return "mixed"
    return "en"


def infer_service_scope(source_name: str, title: str, text: str) -> str:
    source_title = f"{source_name}\n{title}".lower()
    if "birth_and_death" not in source_title and "জন্ম ও মৃত্যু" not in source_title:
        if "birth" in source_title or "জন্ম" in source_title:
            return "birth"
        if "death" in source_title or "মৃত্যু" in source_title:
            return "death"

    haystack = f"{source_name}\n{title}\n{text[:1000]}"
    has_birth = "জন্ম" in haystack or "birth" in haystack.lower()
    has_death = "মৃত্যু" in haystack or "death" in haystack.lower()
    if has_birth and has_death:
        return "birth_death"
    if has_death:
        return "death"
    return "birth"


def infer_document_type(path: Path, metadata: dict[str, str], text: str) -> str:
    name_title = f"{path.name} {metadata.get('bengali_title', '')} {metadata.get('source_file', '')}".lower()
    if "faq" in name_title or "জিজ্ঞাসিত প্রশ্ন" in name_title:
        return "faq"
    if "fees" in name_title or "ফি" in name_title or "ফিস" in name_title:
        return "fees"
    if "act" in name_title or "আইন" in name_title:
        return "law"
    if "rules" in name_title or "বিধিমালা" in name_title:
        return "rules"
    if "correction" in name_title or "সংশোধন" in name_title:
        return "correction_process"
    if "process" in name_title or "প্রক্রিয়া" in name_title or "প্রসেস" in name_title:
        return "application_process"
    if "জেনে রাখুন" in name_title:
        return "general_guidance"
    return "webpage"


def is_meaningful_heading(title: str) -> bool:
    plain = MARKDOWN_DECORATION_RE.sub("", title).strip()
    if len(plain) < 3:
        return False
    return bool(re.search(r"[\w\u0980-\u09FF]", plain))


def split_sections(cleaned: str, fallback_title: str) -> list[Section]:
    sections: list[Section] = []
    current_title = fallback_title
    current_level = 1
    current_lines: list[str] = []

    for line in cleaned.splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            heading_title = heading.group(2).strip()
            if not is_meaningful_heading(heading_title):
                continue
            if current_lines:
                sections.append(Section(current_title, current_level, current_lines))
            current_title = heading_title
            current_level = len(heading.group(1))
            current_lines = []
            continue
        current_lines.append(line)

    if current_lines:
        sections.append(Section(current_title, current_level, current_lines))

    return sections


def paragraph_blocks(lines: list[str]) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    for line in lines:
        if not line.strip():
            if current:
                blocks.append("\n".join(current).strip())
                current = []
            continue
        if line.startswith("- ") and current:
            blocks.append("\n".join(current).strip())
            current = []
        if line.startswith("- "):
            blocks.append(line)
            continue
        current.append(line)
    if current:
        blocks.append("\n".join(current).strip())
    return [block for block in blocks if block]


def chunk_section(section: Section, *, min_chars: int, max_chars: int, overlap_paragraphs: int) -> list[str]:
    blocks = paragraph_blocks(section.lines)
    chunks: list[str] = []
    current: list[str] = []

    for block in blocks:
        candidate = "\n\n".join([*current, block]).strip()
        if current and len(candidate) > max_chars:
            chunks.append("\n\n".join(current).strip())
            current = current[-overlap_paragraphs:] if overlap_paragraphs else []
        current.append(block)

    if current:
        chunks.append("\n\n".join(current).strip())

    merged: list[str] = []
    for chunk in chunks:
        if merged and len(chunk) < min_chars:
            candidate = f"{merged[-1]}\n\n{chunk}"
            if len(candidate) <= max_chars * 1.25:
                merged[-1] = candidate
                continue
        merged.append(chunk)

    return merged


def chunk_id(path: Path, section_index: int, chunk_index: int) -> str:
    stem = re.sub(r"[^a-zA-Z0-9]+", "_", path.stem).strip("_").lower()
    return f"bdr_{stem}_s{section_index:03d}_c{chunk_index:03d}"


def build_chunks(path: Path, raw_root: Path, config: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    raw_text = path.read_text(encoding="utf-8")
    source_metadata, body = parse_frontmatter(raw_text)
    cleaned = clean_markdown_body(body)

    title = source_metadata.get("bengali_title") or path.stem.replace("_", " ")
    document_type = infer_document_type(path, source_metadata, cleaned)
    service_scope = infer_service_scope(path.name, title, cleaned)
    relative_source = path.relative_to(raw_root).as_posix()

    preprocessing_config = config["preprocessing"]
    sections = split_sections(cleaned, title)
    rows: list[dict[str, Any]] = []

    for section_index, section in enumerate(sections, start=1):
        section_chunks = chunk_section(
            section,
            min_chars=preprocessing_config["min_chunk_chars"],
            max_chars=preprocessing_config["max_chunk_chars"],
            overlap_paragraphs=preprocessing_config["overlap_paragraphs"],
        )
        for chunk_index, text in enumerate(section_chunks, start=1):
            if not text.strip():
                continue
            content = "\n".join(
                [
                    "Service: birth and death registration",
                    f"Service scope: {service_scope}",
                    f"Document type: {document_type}",
                    f"Title: {title}",
                    f"Section: {section.title}",
                    f"Content:\n{text}",
                ]
            )
            rows.append(
                {
                    "id": chunk_id(path, section_index, chunk_index),
                    "content": content,
                    "metadata": {
                        "service": "birth_death_registration",
                        "service_scope": service_scope,
                        "document_type": document_type,
                        "language": detect_language(text),
                        "title": title,
                        "section_title": section.title,
                        "section_level": section.level,
                        "source_file": source_metadata.get("source_file", path.name),
                        "source_path": relative_source,
                        "source_url": source_metadata.get("source_url", ""),
                        "encoding": source_metadata.get("encoding", ""),
                        "chunk_index": chunk_index,
                        "section_index": section_index,
                    },
                }
            )

    return cleaned, rows


def write_clean_markdown(path: Path, metadata: dict[str, str], cleaned: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = ["---"]
    for key, value in metadata.items():
        frontmatter.append(f"{key}: {value}")
    frontmatter.extend(["---", "", cleaned, ""])
    path.write_text("\n".join(frontmatter), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean and chunk birth/death registration Markdown files.")
    parser.add_argument("--config", default="domains/birth_death_registration/config.json")
    args = parser.parse_args()

    config_path = PROJECT_ROOT / args.config
    config = load_config(config_path)
    raw_root = PROJECT_ROOT / config["data"]["raw_markdown_dir"]
    clean_root = PROJECT_ROOT / config["data"]["clean_markdown_dir"]
    output_path = PROJECT_ROOT / config["data"]["chunk_output_path"]

    markdown_files = sorted(raw_root.rglob("*.md"))
    if not markdown_files:
        raise FileNotFoundError(f"No Markdown files found under {raw_root}")

    all_chunks: list[dict[str, Any]] = []
    for path in markdown_files:
        raw_text = path.read_text(encoding="utf-8")
        source_metadata, _ = parse_frontmatter(raw_text)
        cleaned, chunks = build_chunks(path, raw_root, config)

        clean_path = clean_root / path.relative_to(raw_root)
        write_clean_markdown(clean_path, source_metadata, cleaned)
        all_chunks.extend(chunks)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        for chunk in all_chunks:
            file.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"Markdown files processed: {len(markdown_files)}")
    print(f"Chunks written: {len(all_chunks)}")
    print(f"Clean Markdown dir: {clean_root}")
    print(f"Chunk output: {output_path}")


if __name__ == "__main__":
    main()
