from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.generation.ollama_generator import OllamaAnswerGenerator
from src.reranking.reranker import HybridReranker
from src.retrieval.hybrid_retriever import HybridRetriever, RetrievalResult


class CivicRAGPipeline:
    def __init__(self, project_root: Path, config_path: Path) -> None:
        self.project_root = project_root
        self.config = json.loads(config_path.read_text(encoding="utf-8"))
        self.data_config = self.config["data"]
        self.embedding_config = self.config["embedding"]
        self.retrieval_config = self.config["retrieval"]
        self.reranking_config = self.config["reranking"]
        self.generation_config = self.config["generation"]

        chunks = self._load_jsonl(project_root / self.data_config["chunk_output_path"])
        self.retriever = HybridRetriever(
            chunks=chunks,
            chroma_dir=str(project_root / self.data_config["chroma_persist_dir"]),
            collection_name=self.data_config["collection_name"],
            embedding_model_name=self.embedding_config["model"],
            embedding_device=self.embedding_config["device"],
            local_files_only=self.embedding_config.get("local_files_only", True),
            rrf_k=self.retrieval_config["rrf_k"],
            rrf_weights=self.retrieval_config["rrf_weights"],
        )
        self.reranker = HybridReranker(
            enabled=self.reranking_config.get("enabled", True),
            model_name=self.reranking_config["model"],
            device=self.reranking_config["device"],
            local_files_only=self.reranking_config.get("local_files_only", True),
            fallback=self.reranking_config.get("fallback", "lexical_overlap"),
        )
        self._generators: dict[str, OllamaAnswerGenerator] = {}

    def ask(
        self,
        query: str,
        model: str | None = None,
        generate: bool = True,
        method: str = "civic",
    ) -> dict[str, Any]:
        normalized_method = self._normalize_method(method)
        final_results = self.retrieve(query, method=normalized_method)
        contexts = [self._context_from_result(result) for result in final_results]

        answer = ""
        selected_model = model or self.generation_config["default_model"]
        if generate:
            answer = self._generator(selected_model).answer(query, contexts)

        return {
            "query": query,
            "model": selected_model,
            "method": normalized_method,
            "answer": answer,
            "sources": contexts,
        }

    def retrieve(self, query: str, method: str = "civic") -> list[RetrievalResult]:
        normalized_method = self._normalize_method(method)
        if normalized_method == "simple":
            return self.retriever.dense_only_search(
                query,
                top_k=self.reranking_config["top_k"],
            )

        initial_results = self.retriever.search(
            query,
            top_k_dense=self.retrieval_config["top_k_dense"],
            top_k_bm25=self.retrieval_config["top_k_bm25"],
            top_k_final=self.retrieval_config["top_k_final"],
        )
        return self.reranker.rerank(
            query,
            initial_results,
            top_k=self.reranking_config["top_k"],
        )

    @staticmethod
    def _normalize_method(method: str) -> str:
        normalized = method.strip().lower()
        if normalized in {"simple", "simple_rag", "simple rag"}:
            return "simple"
        return "civic"

    def _generator(self, model: str) -> OllamaAnswerGenerator:
        if model not in self._generators:
            self._generators[model] = OllamaAnswerGenerator(
                model=model,
                base_url=self.generation_config["ollama_base_url"],
                temperature=self.generation_config["temperature"],
                top_p=self.generation_config["top_p"],
                num_predict=self.generation_config["num_predict"],
            )
        return self._generators[model]

    @staticmethod
    def _load_jsonl(path: Path) -> list[dict[str, Any]]:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    @staticmethod
    def _context_from_result(result: RetrievalResult) -> dict[str, Any]:
        return {
            "id": result.chunk_id,
            "content": result.content,
            "metadata": result.metadata,
            "score": result.score,
            "retrievers": result.retrievers,
        }
