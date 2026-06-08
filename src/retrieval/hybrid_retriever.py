from __future__ import annotations

import math
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

import chromadb
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


TOKEN_PATTERN = re.compile(r"[\w\u0980-\u09FF]+", re.UNICODE)
ZERO_WIDTH_RE = re.compile(r"[\u200b\u200c\u200d\u200e\u200f\ufeff]")


def tokenize(text: str) -> list[str]:
    text = unicodedata.normalize("NFC", text)
    text = ZERO_WIDTH_RE.sub("", text)
    return [match.group(0).lower() for match in TOKEN_PATTERN.finditer(text)]


@dataclass(frozen=True)
class RetrievalResult:
    chunk_id: str
    content: str
    retrieval_text: str
    metadata: dict[str, Any]
    score: float
    retrievers: list[str]


class HybridRetriever:
    """Dense + BM25 retriever with weighted Reciprocal Rank Fusion."""

    def __init__(
        self,
        *,
        chunks: list[dict[str, Any]],
        chroma_dir: str,
        collection_name: str,
        embedding_model_name: str,
        embedding_device: str,
        local_files_only: bool,
        rrf_k: int,
        rrf_weights: dict[str, float],
    ) -> None:
        self.chunks = chunks
        self.chunk_by_id = {chunk["id"]: chunk for chunk in chunks}
        self.rrf_k = rrf_k
        self.rrf_weights = rrf_weights

        self.embedding_model = SentenceTransformer(
            embedding_model_name,
            device=embedding_device,
            local_files_only=local_files_only,
        )
        self.chroma_client = chromadb.PersistentClient(path=chroma_dir)
        self.collection = self.chroma_client.get_collection(collection_name)

        tokenized_corpus = [tokenize(chunk.get("retrieval_text", chunk["content"])) for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def _dense_search(self, query: str, top_k: int) -> list[str]:
        query_embedding = self.embedding_model.encode(
            [query],
            normalize_embeddings=True,
            show_progress_bar=False,
        )[0].tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["metadatas", "documents", "distances"],
        )
        return list(results.get("ids", [[]])[0])

    def _bm25_search(self, query: str, top_k: int) -> list[str]:
        scores = self.bm25.get_scores(tokenize(query))
        ranked = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)
        return [self.chunks[index]["id"] for index, score in ranked[:top_k] if score > 0]

    def dense_only_search(self, query: str, *, top_k: int) -> list[RetrievalResult]:
        """Simple RAG baseline: Chroma dense retrieval only."""
        chunk_ids = self._dense_search(query, top_k)
        results = []
        for rank, chunk_id in enumerate(chunk_ids, start=1):
            chunk = self.chunk_by_id[chunk_id]
            results.append(
                RetrievalResult(
                    chunk_id=chunk_id,
                    content=chunk["content"],
                    retrieval_text=chunk.get("retrieval_text", chunk["content"]),
                    metadata=chunk["metadata"],
                    score=1 / rank,
                    retrievers=["dense"],
                )
            )
        return results

    def bm25_only_search(self, query: str, *, top_k: int) -> list[RetrievalResult]:
        """Sparse lexical baseline: BM25 retrieval only."""
        chunk_ids = self._bm25_search(query, top_k)
        results = []
        for rank, chunk_id in enumerate(chunk_ids, start=1):
            chunk = self.chunk_by_id[chunk_id]
            results.append(
                RetrievalResult(
                    chunk_id=chunk_id,
                    content=chunk["content"],
                    retrieval_text=chunk.get("retrieval_text", chunk["content"]),
                    metadata=chunk["metadata"],
                    score=1 / rank,
                    retrievers=["bm25"],
                )
            )
        return results

    def _rrf_fuse(self, ranked_lists: dict[str, list[str]]) -> list[RetrievalResult]:
        scores: dict[str, float] = defaultdict(float)
        retriever_hits: dict[str, list[str]] = defaultdict(list)

        for retriever_name, chunk_ids in ranked_lists.items():
            weight = self.rrf_weights.get(retriever_name, 1.0)
            for rank, chunk_id in enumerate(chunk_ids, start=1):
                scores[chunk_id] += weight / (self.rrf_k + rank)
                retriever_hits[chunk_id].append(retriever_name)

        fused = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        results = []
        for chunk_id, score in fused:
            chunk = self.chunk_by_id[chunk_id]
            results.append(
                RetrievalResult(
                    chunk_id=chunk_id,
                    content=chunk["content"],
                    retrieval_text=chunk.get("retrieval_text", chunk["content"]),
                    metadata=chunk["metadata"],
                    score=score,
                    retrievers=retriever_hits[chunk_id],
                )
            )
        return results

    def search(
        self,
        query: str,
        *,
        top_k_dense: int,
        top_k_bm25: int,
        top_k_final: int,
        rrf_weights: dict[str, float] | None = None,
    ) -> list[RetrievalResult]:
        ranked_lists = {
            "dense": self._dense_search(query, top_k_dense),
            "bm25": self._bm25_search(query, top_k_bm25),
        }
        if rrf_weights is None:
            return self._rrf_fuse(ranked_lists)[:top_k_final]

        original_weights = self.rrf_weights
        try:
            self.rrf_weights = rrf_weights
            return self._rrf_fuse(ranked_lists)[:top_k_final]
        finally:
            self.rrf_weights = original_weights
