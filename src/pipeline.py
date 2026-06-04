from __future__ import annotations

import json
import re
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

        self.chunks = self._load_jsonl(project_root / self.data_config["chunk_output_path"])
        self.chunks_by_id = {str(chunk["id"]): chunk for chunk in self.chunks}
        self.retriever = HybridRetriever(
            chunks=self.chunks,
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
            max_generation_contexts = self.generation_config.get("top_k_for_generation", len(contexts))
            generation_contexts = self._select_generation_contexts(query, contexts, max_generation_contexts)
            answer = self._safe_extractive_answer(query, generation_contexts, normalized_method)
            if not answer:
                answer = self._safe_fee_answer(query, generation_contexts, normalized_method)
            if not answer:
                answer = self._generator(selected_model).answer(query, generation_contexts)
                if self._violates_answer_language(query, answer):
                    answer = self._fallback_evidence_answer(query, generation_contexts) or answer

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
                repeat_last_n=self.generation_config.get("repeat_last_n"),
                repeat_penalty=self.generation_config.get("repeat_penalty"),
            )
        return self._generators[model]

    def _select_generation_contexts(
        self,
        query: str,
        contexts: list[dict[str, Any]],
        max_contexts: int,
    ) -> list[dict[str, Any]]:
        query_lc = query.lower()
        is_procedure_query = (
            any(term in query for term in ["কীভাবে", "কিভাবে", "করতে পারি", "করবো", "করব", "ধাপ", "আবেদন"])
            or any(term in query_lc for term in ["how", "apply", "procedure", "process", "steps", "register"])
        )
        is_duplicate_cancel = (
            any(term in query for term in ["একাধিক", "বাতিল"])
            or any(term in query_lc for term in ["duplicate", "cancel"])
        )
        if is_duplicate_cancel:
            notice_contexts = [
                context
                for context in contexts
                if context["metadata"].get("document_type") == "correction_notice_ocr"
            ]
            if notice_contexts:
                return notice_contexts[:max_contexts]
        if is_procedure_query:
            expanded = self._expanded_procedure_context(contexts)
            if expanded:
                remaining = [context for context in contexts if context["id"] != expanded["id"]]
                return [expanded, *remaining[: max(max_contexts - 1, 0)]]
        return contexts[:max_contexts]

    def _safe_extractive_answer(
        self,
        query: str,
        contexts: list[dict[str, Any]],
        method: str,
    ) -> str:
        if method != "civic" or not contexts:
            return ""
        if not self._is_bangla_query(query) or not self._is_procedure_query(query):
            return ""

        top_context = contexts[0]
        doc_type = top_context["metadata"].get("document_type")
        if doc_type not in {"application_process", "correction_notice_ocr"}:
            return ""

        sections = self._extract_sections(top_context["content"])
        if not sections:
            return ""

        if doc_type == "correction_notice_ocr":
            sections = [
                section
                for section in sections
                if any(term in section["title"] for term in ["ধাপ", "শর্ত"])
            ] or sections[:2]

        if doc_type == "application_process":
            sections = [
                section
                for section in sections
                if any(
                    term in section["title"]
                    for term in ["পূর্ব প্রস্তুতি", "ধাপ", "সংযুক্ত করতে হবে", "OTP", "পরবর্তী করণীয়"]
                )
            ]

        if not sections:
            return ""

        lines: list[str] = []
        for section in sections[:10]:
            body = self._clean_evidence_body(section["body"])
            if not body:
                continue
            if section["title"].startswith("ধাপ"):
                lines.append(f"{section['title']}: {body}")
            else:
                lines.append(f"{section['title']}: {body}")

        if not lines:
            return ""

        source_ids = [str(context["id"]) for context in contexts[:3]]
        return "\n\n".join(lines).strip() + f"\n\nSources: {', '.join(source_ids)}"

    def _safe_fee_answer(
        self,
        query: str,
        contexts: list[dict[str, Any]],
        method: str,
    ) -> str:
        if method != "civic" or not contexts or not self._is_bangla_query(query) or not self._is_fee_query(query):
            return ""

        source_ids = [str(context["id"]) for context in contexts[:3]]
        waiver_context = next(
            (
                context
                for context in contexts
                if context["metadata"].get("document_type") == "legal_rules"
                and context["metadata"].get("section_title") == "ফিস"
                and any(term in str(context.get("content", "")) for term in ["এতিম", "প্রতিবন্ধী", "সহায় সম্বলহীন", "সহায় সম্বলহীন"])
            ),
            None,
        )
        if self._is_fee_waiver_query(query) and waiver_context:
            body = self._extract_labeled_value(str(waiver_context["content"]), "Content")
            if body:
                waiver_rule = re.split(r"\s*\(৫\)", body, maxsplit=1)[0].strip()
                return (
                    "সরাসরি সব ক্ষেত্রে ফি লাগবে না বলা যায় না। তবে বিধি ২১ অনুযায়ী, ১৮ বছরের কম বয়সী এতিমের জন্ম নিবন্ধনের ক্ষেত্রে "
                    "যথাযথভাবে ক্ষমতাপ্রাপ্ত কর্তৃপক্ষের সনদের ভিত্তিতে আবেদন করলে নিবন্ধক প্রদেয় ফি সম্পূর্ণ বা আংশিক মওকুফ করার বিষয়টি বিবেচনা করতে পারেন। "
                    "ফি মওকুফের বিষয়ে নিবন্ধকের সিদ্ধান্ত চূড়ান্ত।\n\n"
                    f"প্রাসঙ্গিক বিধি: {waiver_rule}\n\n"
                    f"Sources: {', '.join(source_ids)}"
                )

        fee_row = next((context for context in contexts if context["metadata"].get("document_type") == "fee_row"), None)
        if fee_row:
            item = self._extract_labeled_value(str(fee_row["content"]), "Fee item")
            amount = self._extract_labeled_value(str(fee_row["content"]), "Fee amount")
            if item and amount:
                return f"{item}: {amount}\n\nSources: {', '.join(source_ids)}"

        fee_table = next((context for context in contexts if context["metadata"].get("document_type") == "fees_table"), None)
        if fee_table:
            table = self._extract_fee_table(str(fee_table["content"]))
            if table:
                return f"{table}\n\nSources: {', '.join(source_ids)}"
        return ""

    def _fallback_evidence_answer(self, query: str, contexts: list[dict[str, Any]]) -> str:
        if not self._is_bangla_query(query) or not contexts:
            return ""

        top_context = contexts[0]
        doc_type = top_context["metadata"].get("document_type")
        content = str(top_context.get("content", ""))
        source_ids = [str(context["id"]) for context in contexts[:3]]

        if doc_type == "faq":
            question = self._extract_labeled_value(content, "Question")
            answer = self._extract_labeled_value(content, "Answer")
            if answer:
                prefix = f"{question}\n\n" if question else ""
                return f"{prefix}{answer}\n\nSources: {', '.join(source_ids)}"

        if doc_type == "fee_row":
            item = self._extract_labeled_value(content, "Fee item")
            amount = self._extract_labeled_value(content, "Fee amount")
            if item and amount:
                return f"{item}: {amount}\n\nSources: {', '.join(source_ids)}"

        if doc_type == "fees_table":
            table = self._extract_fee_table(content)
            if table:
                return f"{table}\n\nSources: {', '.join(source_ids)}"

        body = self._extract_labeled_value(content, "Content")
        if body:
            return f"{body}\n\nSources: {', '.join(source_ids)}"
        return ""

    @staticmethod
    def _is_bangla_query(query: str) -> bool:
        return bool(re.search(r"[\u0980-\u09FF]", query))

    @staticmethod
    def _violates_answer_language(query: str, answer: str) -> bool:
        if not CivicRAGPipeline._is_bangla_query(query):
            return False
        if re.search(r"[\u3400-\u9FFF\u3040-\u30FF\uAC00-\uD7AF]", answer):
            return True
        lowered = answer.lower()
        bad_markers = [
            "translated to english",
            "translate to english",
            "翻译",
            "plaintext",
            "```",
        ]
        return any(marker in lowered for marker in bad_markers)

    @staticmethod
    def _is_procedure_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            any(term in query for term in ["কীভাবে", "কিভাবে", "করতে পারি", "করবো", "করব", "ধাপ", "আবেদন", "বাতিল"])
            or any(term in query_lc for term in ["how", "apply", "procedure", "process", "steps", "register", "cancel"])
        )

    @staticmethod
    def _is_fee_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            any(term in query for term in ["ফি", "ফিস", "টাকা", "লাগবে", "খরচ", "বিনামূল্যে", "বিনা ফিসে"])
            or any(term in query_lc for term in ["fee", "fees", "cost", "charge", "payment", "free"])
        )

    @staticmethod
    def _is_fee_waiver_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            any(term in query for term in ["এতিম", "প্রতিবন্ধী", "সহায়", "সহায়", "মওকুফ", "মাফ"])
            or any(term in query_lc for term in ["orphan", "disabled", "waiver", "exempt"])
        )

    @staticmethod
    def _extract_sections(content: str) -> list[dict[str, str]]:
        blocks = re.split(r"\n\n(?=Service: )", content.strip())
        sections: list[dict[str, str]] = []
        for block in blocks:
            title_match = re.search(r"(?m)^Section:\s*(.+)$", block)
            body_match = re.search(r"(?s)^Content:\s*(.+)$", block, flags=re.MULTILINE)
            if title_match and body_match:
                sections.append(
                    {
                        "title": title_match.group(1).strip(),
                        "body": body_match.group(1).strip(),
                    }
                )
        return sections

    @staticmethod
    def _clean_evidence_body(body: str) -> str:
        body = re.sub(r"\n-{3,}\s*$", "", body.strip())
        body = re.sub(r"\n{3,}", "\n\n", body)
        return body.strip()

    @staticmethod
    def _extract_labeled_value(content: str, label: str) -> str:
        match = re.search(rf"(?ms)^{re.escape(label)}:\s*(.+?)(?=^[A-Z][A-Za-z ]*:\s|\Z)", content)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_fee_table(content: str) -> str:
        lines = []
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped.startswith("|"):
                continue
            if "---" in stripped or "ক্রম" in stripped or "বাবদ" in stripped:
                continue
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if len(cells) >= 3:
                lines.append(f"{cells[1]}: {cells[2]}")
        return "\n".join(lines)

    def _expanded_procedure_context(self, contexts: list[dict[str, Any]]) -> dict[str, Any] | None:
        seed = next(
            (
                context
                for context in contexts
                if context["metadata"].get("document_type") == "application_process"
            ),
            None,
        )
        if not seed:
            return None

        source_path = seed["metadata"].get("source_path")
        if not source_path:
            return None

        sibling_chunks = [
            chunk
            for chunk in self.chunks
            if chunk.get("metadata", {}).get("source_path") == source_path
            and chunk.get("metadata", {}).get("document_type") == "application_process"
        ]
        if not sibling_chunks:
            return None

        def section_index(chunk: dict[str, Any]) -> int:
            value = chunk.get("metadata", {}).get("section_index", 0)
            try:
                return int(value)
            except (TypeError, ValueError):
                return 0

        useful_sections = []
        for chunk in sorted(sibling_chunks, key=section_index):
            section_title = str(chunk.get("metadata", {}).get("section_title", ""))
            if any(
                term in section_title
                for term in [
                    "পূর্ব প্রস্তুতি",
                    "ধাপ",
                    "সংযুক্ত করতে হবে",
                    "OTP",
                    "পরবর্তী করণীয়",
                ]
            ):
                useful_sections.append(chunk)

        if not useful_sections:
            return None

        expanded_content = "\n\n".join(str(chunk["content"]) for chunk in useful_sections)
        expanded = dict(seed)
        expanded["content"] = expanded_content
        expanded["metadata"] = dict(seed["metadata"])
        expanded["metadata"]["expanded_context"] = True
        expanded["metadata"]["expanded_chunk_count"] = len(useful_sections)
        expanded["metadata"]["expanded_from_source_path"] = str(source_path)
        return expanded

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
