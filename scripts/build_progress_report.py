from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "docs" / "civic_ai_progress_report.pdf"


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=27,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#172033"),
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#667085"),
        spaceAfter=18,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#116A5C"),
        spaceBefore=10,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        name="Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#172033"),
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#667085"),
    )
)


def p(text: str, style: str = "Body") -> Paragraph:
    return Paragraph(text, styles[style])


def section(text: str) -> Paragraph:
    return Paragraph(text, styles["Section"])


def table(rows: list[list[str]], widths: list[float]) -> Table:
    converted = [[p(cell, "Small") for cell in row] for row in rows]
    t = Table(converted, colWidths=widths)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E7F2EF")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D0D7DE")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


retrieval = load_json(PROJECT_ROOT / "domains" / "passport" / "data" / "evaluation" / "retrieval_summary.json")
generation = load_json(PROJECT_ROOT / "domains" / "passport" / "data" / "evaluation" / "generation_summary.json")

story = [
    Paragraph("Civic.ai RAG Progress Report", styles["ReportTitle"]),
    Paragraph(
        "Current implementation status for the Bangla-English government-service RAG thesis prototype.",
        styles["ReportSubtitle"],
    ),
    section("1. Project Goal"),
    p(
        "Civic.ai is being developed as a citizen-facing government service assistant for Bangladesh. "
        "The implementation follows the broad NextRAG idea, but adapts it from financial PDFs to government-service guidance, starting with passport FAQ data."
    ),
    section("2. Current Dataset"),
    p(
        "The active dataset is a manually curated passport FAQ JSON file. Raw PDFs are preserved as source artifacts, but the RAG index is built from structured FAQ records because they are better for retrieval, metadata, evaluation, and citation."
    ),
    table(
        [
            ["Artifact", "Path / Description"],
            ["Processed FAQ", "domains/passport/data/processed/passport_rag_clean.json"],
            ["Raw PDF", "domains/passport/data/raw/Passport.pdf"],
            ["Generated chunks", "domains/passport/data/interim/passport_faq_chunks.jsonl"],
            ["Vector index", "domains/passport/data/processed/chroma_passport_bge_m3"],
        ],
        [1.7 * inch, 4.9 * inch],
    ),
    section("3. Implemented Pipeline"),
    p(
        "The current pipeline is: processed FAQ JSON -> metadata-rich chunks -> BGE-M3 dense embeddings -> ChromaDB -> BM25 -> weighted RRF fusion -> reranking -> local Ollama generation -> chatbot UI."
    ),
    table(
        [
            ["Layer", "Current Implementation"],
            ["Ingestion", "Loads structured FAQ records from JSON."],
            ["Chunking", "One metadata-rich chunk per FAQ record."],
            ["Dense retrieval", "BAAI/bge-m3 embeddings stored in ChromaDB."],
            ["Sparse retrieval", "BM25 over the same chunk text."],
            ["Fusion", "Weighted RRF, currently dense=0.6 and BM25=0.4."],
            ["Reranking", "Cross-encoder hook implemented; lexical fallback active if model is not cached."],
            ["Generation", "Local Ollama models through LangChain."],
            ["Deployment", "Local browser chatbot at http://127.0.0.1:7860."],
        ],
        [1.45 * inch, 5.15 * inch],
    ),
    section("4. Local LLMs"),
    p("The chatbot is not tied to one LLM. It can compare multiple local generators while using the same retrieved evidence."),
    table(
        [
            ["Model", "Role"],
            ["llama3.2", "Fast local baseline."],
            ["llama3", "Stronger LLaMA-family baseline; prompt was adjusted to improve source use."],
            ["qwen2.5:7b", "Alternative model-family baseline; early sample performed strongly."],
        ],
        [1.45 * inch, 5.15 * inch],
    ),
    section("5. Implemented Files"),
    table(
        [
            ["File", "Purpose"],
            ["app.py", "Local web chatbot and /chat API."],
            ["src/pipeline.py", "Shared RAG pipeline wrapper."],
            ["src/retrieval/hybrid_retriever.py", "Dense + BM25 retrieval and RRF fusion."],
            ["src/reranking/reranker.py", "Cross-encoder reranker with lexical fallback."],
            ["src/generation/ollama_generator.py", "Grounded prompt and local LLM generation."],
            ["scripts/build_index.py", "Builds ChromaDB index from processed FAQ JSON."],
            ["scripts/query_rag.py", "Command-line query script."],
            ["scripts/compare_models.py", "Runs the same evidence through multiple LLMs."],
            ["scripts/evaluate_retrieval.py", "Numeric retrieval evaluation."],
            ["scripts/evaluate_generation.py", "Numeric generated-answer evaluation."],
        ],
        [2.25 * inch, 4.35 * inch],
    ),
    section("6. Current Numeric Evaluation"),
]

if retrieval:
    rows = [["Method", "N", "Recall@1", "Recall@5", "MRR", "nDCG@5"]]
    for method, values in retrieval.items():
        rows.append(
            [
                method,
                str(values["num_questions"]),
                f"{values['recall@1']:.3f}",
                f"{values['recall@5']:.3f}",
                f"{values['mrr']:.3f}",
                f"{values['ndcg@5']:.3f}",
            ]
        )
    story += [p("Retrieval smoke-test results using the indexed FAQ questions:"), table(rows, [1.6 * inch, 0.55 * inch, 1.0 * inch, 1.0 * inch, 0.8 * inch, 1.0 * inch])]

if generation:
    rows = [["Model", "N", "Semantic Similarity", "Token F1", "Source Acc.", "Citation Acc."]]
    for model, values in generation.items():
        rows.append(
            [
                model,
                str(values["num_questions"]),
                f"{values['mean_semantic_similarity']:.3f}",
                f"{values['mean_token_f1']:.3f}",
                f"{values['source_retrieval_accuracy']:.3f}",
                f"{values['citation_accuracy']:.3f}",
            ]
        )
    story += [Spacer(1, 0.12 * inch), p("Generated-answer sample results:"), table(rows, [1.3 * inch, 0.45 * inch, 1.35 * inch, 0.95 * inch, 1.0 * inch, 1.0 * inch])]

story += [
    p(
        "Important limitation: the current retrieval benchmark is a smoke test because it uses the same FAQ questions that are indexed. "
        "For thesis-quality results, the next dataset should include paraphrased English, Bangla, and code-mixed questions with expected source IDs."
    ),
    section("7. Next Steps"),
    table(
        [
            ["Priority", "Next Work"],
            ["1", "Curate a stronger JSON/JSONL dataset with service, category, language, source, keywords, and Bangla fields."],
            ["2", "Create a separate evaluation set with paraphrased English, Bangla, and code-mixed questions."],
            ["3", "Download/cache BGE reranker or evaluate a lighter reranker alternative."],
            ["4", "Run full Simple RAG vs CivicRAG comparisons for llama3.2, llama3, and qwen2.5:7b."],
            ["5", "Add citation/faithfulness review and final thesis tables."],
        ],
        [0.75 * inch, 5.85 * inch],
    ),
]

doc = SimpleDocTemplate(
    str(OUTPUT_PATH),
    pagesize=LETTER,
    leftMargin=0.75 * inch,
    rightMargin=0.75 * inch,
    topMargin=0.65 * inch,
    bottomMargin=0.65 * inch,
)
doc.build(story)
print(OUTPUT_PATH)
