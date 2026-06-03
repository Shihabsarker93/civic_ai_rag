from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_chunks(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(
            f"Chunk file not found: {path}. "
            "Run the domain chunk-preparation script before building the index."
        )
    chunks = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for index, chunk in enumerate(chunks):
        if not {"id", "content", "metadata"}.issubset(chunk):
            raise ValueError(f"Chunk {index} must contain id, content, and metadata")
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Civic.ai retrieval index from prepared domain chunks.")
    parser.add_argument("--config", default="domains/birth_death_registration/config.json")
    args = parser.parse_args()

    config = load_config(PROJECT_ROOT / args.config)
    data_config = config["data"]
    embedding_config = config["embedding"]

    chunk_path = PROJECT_ROOT / data_config["chunk_output_path"]
    chroma_dir = PROJECT_ROOT / data_config["chroma_persist_dir"]

    chunks = load_chunks(chunk_path)

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

    print(f"Loaded chunks: {len(chunks)}")
    print(f"Built Chroma collection: {data_config['collection_name']}")
    print(f"Chroma path: {chroma_dir}")


if __name__ == "__main__":
    main()
