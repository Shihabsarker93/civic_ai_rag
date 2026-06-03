from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.chunking.faq_chunker import build_faq_chunks
from src.ingestion.faq_loader import load_faq_records


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the Civic.ai passport FAQ retrieval index.")
    parser.add_argument("--config", default="domains/passport/config.json")
    args = parser.parse_args()

    config = load_config(PROJECT_ROOT / args.config)
    data_config = config["data"]
    embedding_config = config["embedding"]

    faq_path = PROJECT_ROOT / data_config["processed_faq_path"]
    chunk_path = PROJECT_ROOT / data_config["chunk_output_path"]
    chroma_dir = PROJECT_ROOT / data_config["chroma_persist_dir"]

    records = load_faq_records(faq_path)
    chunks = build_faq_chunks(records)
    write_jsonl(chunk_path, chunks)

    model = SentenceTransformer(
        embedding_config["model"],
        device=embedding_config["device"],
        local_files_only=embedding_config.get("local_files_only", False),
    )
    embeddings = model.encode(
        [chunk["content"] for chunk in chunks],
        normalize_embeddings=embedding_config.get("normalize_embeddings", True),
        show_progress_bar=True,
    ).tolist()

    client = chromadb.PersistentClient(path=str(chroma_dir))
    existing = [collection.name for collection in client.list_collections()]
    if data_config["collection_name"] in existing:
        client.delete_collection(data_config["collection_name"])
    collection = client.create_collection(name=data_config["collection_name"])

    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["content"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks],
        embeddings=embeddings,
    )

    print(f"Loaded FAQ records: {len(records)}")
    print(f"Wrote chunks: {chunk_path}")
    print(f"Built Chroma collection: {data_config['collection_name']}")
    print(f"Chroma path: {chroma_dir}")


if __name__ == "__main__":
    main()
