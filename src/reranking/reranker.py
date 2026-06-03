from __future__ import annotations

import re
from dataclasses import replace
from typing import Iterable

from sentence_transformers import CrossEncoder

from src.retrieval.hybrid_retriever import RetrievalResult, tokenize


class HybridReranker:
    """Cross-encoder reranker with a deterministic lexical fallback."""

    def __init__(
        self,
        *,
        enabled: bool,
        model_name: str,
        device: str,
        local_files_only: bool,
        fallback: str,
    ) -> None:
        self.enabled = enabled
        self.model_name = model_name
        self.fallback = fallback
        self.cross_encoder: CrossEncoder | None = None

        if not enabled:
            return

        try:
            self.cross_encoder = CrossEncoder(
                model_name,
                device=device,
                model_kwargs={"local_files_only": local_files_only},
                tokenizer_kwargs={"local_files_only": local_files_only},
                config_kwargs={"local_files_only": local_files_only},
            )
        except Exception:
            self.cross_encoder = None

    def rerank(self, query: str, results: list[RetrievalResult], top_k: int) -> list[RetrievalResult]:
        if not results:
            return []

        if self.cross_encoder is not None:
            pairs = [(query, result.content) for result in results]
            scores = self.cross_encoder.predict(pairs)
            rescored = [
                replace(result, score=float(score), retrievers=[*result.retrievers, "cross_encoder"])
                for result, score in zip(results, scores)
            ]
            return sorted(rescored, key=lambda result: result.score, reverse=True)[:top_k]

        if self.fallback == "lexical_overlap":
            return self._lexical_rerank(query, results, top_k)

        return results[:top_k]

    def _lexical_rerank(self, query: str, results: list[RetrievalResult], top_k: int) -> list[RetrievalResult]:
        query_tokens = set(tokenize(query))
        rescored = []

        for result in results:
            content_tokens = set(tokenize(result.content))
            overlap = len(query_tokens.intersection(content_tokens))
            coverage = overlap / max(len(query_tokens), 1)
            # Keep lexical fallback as a light tie-breaker; RRF should remain dominant.
            score = result.score + (0.05 * coverage)
            rescored.append(
                replace(result, score=score, retrievers=[*result.retrievers, "lexical_reranker"])
            )

        return sorted(rescored, key=lambda result: result.score, reverse=True)[:top_k]
