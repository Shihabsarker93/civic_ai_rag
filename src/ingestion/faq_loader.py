from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {"id", "category", "subcategory", "question", "answer", "tags"}


def load_faq_records(path: Path) -> list[dict[str, Any]]:
    """Load the manually curated government-service FAQ dataset."""
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError(f"Expected a JSON list in {path}")

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"Record {index} is not an object")
        missing = REQUIRED_FIELDS.difference(record)
        if missing:
            raise ValueError(f"Record {index} is missing fields: {sorted(missing)}")

    return records
