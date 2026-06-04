from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DOCUMENTS = [
    {
        "filename": "birth_and_death_registration_guidelines_2021.pdf",
        "output_stem": "birth_and_death_registration_guidelines_2021_ocr",
        "title": "জন্ম ও মৃত্যু নিবন্ধন নির্দেশিকা ২০২১",
        "source_url": "https://orgbdr.gov.bd/pages/policies/6922d920dbfbab28ce048e5f",
        "document_type": "guidelines",
    },
    {
        "filename": "notice_birth_and_death_registration_certificate_correction_steps.pdf",
        "output_stem": "notice_birth_and_death_registration_certificate_correction_steps_ocr",
        "title": "জন্ম ও মৃত্যু নিবন্ধন সনদের সংশোধন ধাপসমূহ",
        "source_url": "https://orgbdr.portal.gov.bd/pages/notices/6922ea5adbfbab28ce0b3736",
        "document_type": "correction_notice",
    },
]


def run(command: list[str], *, cwd: Path | None = None) -> str:
    result = subprocess.run(command, cwd=cwd, check=True, text=True, capture_output=True)
    return result.stdout


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"Required OCR tool not found: {name}")


def normalize_ocr_text(text: str) -> str:
    text = text.replace("\ufeff", "").replace("\r", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            lines.append("")
            continue
        if re.search(r"(FASweet|Inovation|CTR|docx)$", line):
            continue
        if len(line) <= 2 and not re.search(r"[\u0980-\u09FF]", line):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def ocr_pdf(pdf_path: Path, *, dpi: int, lang: str, psm: int) -> str:
    with tempfile.TemporaryDirectory(prefix="civic_ocr_") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        image_prefix = temp_dir / "page"
        run(["pdftoppm", "-r", str(dpi), "-jpeg", str(pdf_path), str(image_prefix)])
        page_texts = []
        for image_path in sorted(temp_dir.glob("page-*.jpg")):
            page_number = image_path.stem.split("-")[-1]
            text = run(
                ["tesseract", image_path.name, "stdout", "-l", lang, "--psm", str(psm)],
                cwd=temp_dir,
            )
            page_texts.append(f"## OCR Page {int(page_number)}\n\n{normalize_ocr_text(text)}")
        return "\n\n".join(page_texts).strip()


def markdown_for_document(document: dict[str, str], ocr_text: str) -> str:
    return "\n".join(
        [
            "---",
            f"source_file: {document['filename']}",
            f"bengali_title: {document['title']}",
            f"source_url: {document['source_url']}",
            "encoding: ocr_tesseract_ben_eng",
            f"document_type_hint: {document['document_type']}",
            "note: generated from scanned PDF using Tesseract OCR; requires manual quality review",
            "---",
            "",
            f"# {document['title']}",
            "",
            "> OCR-generated text. Use with caution and cross-check against the scanned PDF for high-stakes answers.",
            "",
            ocr_text,
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="OCR scanned birth/death registration PDFs into Markdown.")
    parser.add_argument(
        "--raw-scanned-dir",
        default="/Users/shihab/01 Thesis/Rag/Pipeline/p2/raw_data/raw_docs/scanned_pdf",
    )
    parser.add_argument("--raw-ocr-output-dir", default="domains/birth_death_registration/data/raw/ocr")
    parser.add_argument("--markdown-output-dir", default="domains/birth_death_registration/data/raw/md")
    parser.add_argument("--dpi", type=int, default=250)
    parser.add_argument("--lang", default="ben+eng")
    parser.add_argument("--psm", type=int, default=6)
    args = parser.parse_args()

    require_tool("pdftoppm")
    require_tool("tesseract")

    raw_scanned_dir = Path(args.raw_scanned_dir)
    raw_ocr_output_dir = PROJECT_ROOT / args.raw_ocr_output_dir
    markdown_output_dir = PROJECT_ROOT / args.markdown_output_dir
    raw_ocr_output_dir.mkdir(parents=True, exist_ok=True)
    markdown_output_dir.mkdir(parents=True, exist_ok=True)

    for document in DOCUMENTS:
        pdf_path = raw_scanned_dir / document["filename"]
        if not pdf_path.exists():
            raise FileNotFoundError(pdf_path)
        print(f"OCR: {pdf_path}")
        ocr_text = ocr_pdf(pdf_path, dpi=args.dpi, lang=args.lang, psm=args.psm)
        raw_text_path = raw_ocr_output_dir / f"{document['output_stem']}.txt"
        markdown_path = markdown_output_dir / f"{document['output_stem']}.md"
        raw_text_path.write_text(ocr_text + "\n", encoding="utf-8")
        markdown_path.write_text(markdown_for_document(document, ocr_text), encoding="utf-8")
        print(f"  raw text: {raw_text_path}")
        print(f"  markdown: {markdown_path}")


if __name__ == "__main__":
    main()
