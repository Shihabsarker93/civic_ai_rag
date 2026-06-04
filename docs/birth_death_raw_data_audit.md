# Birth/Death Registration Raw Data Audit

Date: 2026-06-04

## Current Active Index

The active Civic.ai birth/death vector database is built from:

- `domains/birth_death_registration/data/raw/json/*.json`
- `domains/birth_death_registration/data/raw/md/*.md`
- prepared chunk file: `domains/birth_death_registration/data/interim/birth_death_chunks.jsonl`
- Chroma directory: `domains/birth_death_registration/data/processed/chroma_birth_death_bge_m3`

Current chunk count: `187`

Chunk distribution:

| Document type | Chunks |
|---|---:|
| `legal_rules` | 45 |
| `legal_act` | 30 |
| `application_process` | 30 |
| `faq` | 26 |
| `correction_process` | 12 |
| `portal_summary` | 9 |
| `general_guidance` | 8 |
| `fee_row` | 7 |
| `correction_notice_ocr` | 6 |
| `faq_preamble` | 1 |
| `fees_table` | 1 |
| `guidelines_ocr` | 12 |

Each indexed chunk has:

- `content`: clean evidence sent to the LLM.
- `retrieval_text`: evidence plus search aliases used for dense/BM25 retrieval.
- `metadata`: source path, document type, service scope, title, section/category, and source URL when available.

Retrieval aliases are not included in `content`, so they are not directly passed as answer evidence.

## Raw Source Folders Received

Raw root:

`/Users/shihab/01 Thesis/Rag/Pipeline/p2/raw_data/raw_docs`

| Folder | Purpose | Approx. size | Notes |
|---|---|---:|---|
| `bijoy_pdf` | original Bijoy-font PDFs | 2.3 MB | not directly reliable for Unicode NLP |
| `converted_docx` | manually converted Unicode DOCX | 1.8 MB | best text source for process/rules/fees/guidance |
| `html_unicode` | government portal HTML | 1.7 MB | Unicode but noisy with navigation/footer content |
| `scanned_pdf` | image/scanned PDFs and OCR ZIP | 5.8 MB | requires OCR before text indexing |

## Coverage Compared With Current Index

Currently represented in the active index:

- `application_for_birth_information_correction`
- `birth_and_death_registration_act_2004`
- `birth_and_death_registration_fees`
- `birth_and_death_registration_rules_2018`
- `birth_registration_application_process`
- `birth_registration_application_process_02`
- `faqs_on_birth_and_death_registration`
- `faqs_on_birth_and_death_registration_02`
- `home_registrar_generals_office_birth_and_death_registration`
- `know_this_01`

OCR sources now represented in the active index:

- `birth_and_death_registration_guidelines_2021.pdf`
- `notice_birth_and_death_registration_certificate_correction_steps.pdf`

These were converted using Tesseract OCR with `ben+eng` language data. The generated raw OCR text is stored in:

`domains/birth_death_registration/data/raw/ocr`

The generated Markdown sources are:

- `domains/birth_death_registration/data/raw/md/birth_and_death_registration_guidelines_2021_ocr.md`
- `domains/birth_death_registration/data/raw/md/notice_birth_and_death_registration_certificate_correction_steps_ocr.md`

These OCR-derived sources are indexed, but they are explicitly marked as OCR-generated. The correction notice Markdown has been manually cleaned after OCR because the raw Tesseract output contained malformed Bangla words. The guideline OCR remains lower-confidence until fully reviewed.

## Quality Findings

The converted DOCX files are generally usable Unicode text. For example, `birth_registration_application_process_02.docx` was converted into a cleaner Markdown file with explicit step headings. This is a good transformation for retrieval because it preserves meaning while improving section-level chunking.

The HTML files are Unicode, but the raw HTML contains heavy portal noise such as office selectors, menus, accessibility controls, footer links, and unrelated service lists. The current cleaned Markdown/JSON versions are therefore preferable to indexing raw HTML directly.

The FAQ JSON files are curated and retrieval-friendly. The raw FAQ HTML contains enough noise that automatic extraction should be validated manually before replacing the curated JSON.

The scanned PDFs are image-heavy. `birth_and_death_registration_guidelines_2021.pdf` is image-only, and `notice_birth_and_death_registration_certificate_correction_steps.pdf` behaves like an image-based PDF. OCR was performed with Tesseract. The correction notice was manually cleaned into structured Markdown and is now useful for duplicate-certificate cancellation and special correction queries. The guideline OCR still contains recognizable OCR noise such as malformed words, mixed English fragments, and table-layout errors.

## Risks

The current hallucination/repetition problems are not primarily caused by bad chunking. The latest tests show retrieval now ranks application-process chunks first for Bangla how-to queries and correction-notice chunks first for duplicate-certificate cancellation queries. However, small local LLMs can still paraphrase Bangla evidence badly, so CivicRAG now uses a safe extractive answer mode for Bangla procedural questions.

The biggest current data risks are:

- OCR guideline content is present but noisy.
- Small local LLMs can produce awkward or unsupported Bangla paraphrases unless procedural answers are constrained extractively.
- HTML pages may have lost useful details during manual cleaning.
- FAQ data is curated but should be cross-checked against raw HTML.
- Some legal/rules chunks are long and may need question-type-aware retrieval constraints.

## Recommended Next Steps

1. Keep the current manually cleaned Markdown/JSON pipeline as the main thesis baseline.
2. Add a raw-data provenance folder or manifest so every cleaned file can be traced to an original source.
3. Manually review the OCR-derived guideline Markdown file and promote the corrected version once verified.
4. Create a data coverage table for the thesis: raw file, cleaned file, indexed chunks, document type, language/encoding, and notes.
5. Build a small gold QA set before further tuning. This will tell us whether problems come from source coverage, chunking, retrieval, or generation.
6. Run an ablation comparing retrieval with OCR chunks enabled vs disabled.
