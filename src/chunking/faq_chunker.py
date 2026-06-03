from __future__ import annotations

from typing import Any


def build_faq_chunk(record: dict[str, Any]) -> dict[str, Any]:
    """Convert one FAQ record into a retrieval chunk with strong metadata."""
    tags = record.get("tags") or []
    tag_text = ", ".join(str(tag) for tag in tags)

    content = "\n".join(
        [
            f"Service: passport",
            f"Category: {record['category']}",
            f"Subcategory: {record['subcategory']}",
            f"Question: {record['question']}",
            f"Answer: {record['answer']}",
            f"Tags: {tag_text}",
        ]
    )

    return {
        "id": str(record["id"]),
        "content": content,
        "question": str(record["question"]),
        "answer": str(record["answer"]),
        "metadata": {
            "source": "passport_rag_clean.json",
            "service": "passport",
            "category": str(record["category"]),
            "subcategory": str(record["subcategory"]),
            "tags": tag_text,
        },
    }


def build_faq_chunks(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    chunks = [build_faq_chunk(record) for record in records]
    overview = build_application_process_overview(records)
    if overview is not None:
        chunks.append(overview)
    return chunks


def build_application_process_overview(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    step_records = [
        record
        for record in records
        if record.get("category") == "application_process" and record.get("subcategory") == "steps"
    ]
    if not step_records:
        return None

    step_records = sorted(step_records, key=lambda record: str(record.get("id", "")))
    answer = " ".join(f"{index}. {record['answer']}" for index, record in enumerate(step_records, start=1))
    content = "\n".join(
        [
            "Service: passport",
            "Category: application_process",
            "Subcategory: overview",
            "Question: How can I apply for an e-Passport?",
            "Alternative questions: How can I do passport? How do I get a passport? What are the e-Passport application steps?",
            f"Answer: {answer}",
            "Tags: apply, application, process, steps, e-passport, passport, getting started",
        ]
    )

    return {
        "id": "application_process_overview",
        "content": content,
        "question": "How can I apply for an e-Passport?",
        "answer": answer,
        "metadata": {
            "source": "passport_rag_clean.json",
            "service": "passport",
            "category": "application_process",
            "subcategory": "overview",
            "tags": "apply, application, process, steps, e-passport, passport, getting started",
        },
    }
