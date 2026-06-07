from __future__ import annotations

import json
import re
import unicodedata
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
        search_query = self._normalize_query_text(query)
        final_results = self.retrieve(search_query, method=normalized_method)
        contexts = [self._context_from_result(result) for result in final_results]
        if normalized_method == "civic":
            contexts = self._augment_contexts(search_query, contexts)

        answer = ""
        selected_model = model or self.generation_config["default_model"]
        if generate:
            max_generation_contexts = self.generation_config.get("top_k_for_generation", len(contexts))
            decomposed_answer, decomposed_contexts = self._safe_decomposed_answer(search_query, normalized_method, contexts)
            if decomposed_answer:
                answer = decomposed_answer
                contexts = self._merge_contexts(contexts, decomposed_contexts)
            generation_contexts = self._select_generation_contexts(search_query, contexts, max_generation_contexts)
            if not answer:
                answer = self._safe_fee_answer(search_query, contexts, normalized_method)
            if not answer:
                answer = self._safe_domain_answer(search_query, contexts, normalized_method)
            if not answer:
                answer = self._safe_extractive_answer(search_query, generation_contexts, normalized_method)
            if not answer:
                answer = self._generator(selected_model).answer(search_query, generation_contexts)
                if self._violates_answer_language(search_query, answer):
                    answer = self._fallback_evidence_answer(search_query, generation_contexts) or answer

        return {
            "query": query,
            "model": selected_model,
            "method": normalized_method,
            "answer": answer,
            "sources": contexts,
        }

    def retrieve(self, query: str, method: str = "civic") -> list[RetrievalResult]:
        normalized_method = self._normalize_method(method)
        search_query = self._normalize_query_text(query)
        if normalized_method == "simple":
            return self.retriever.dense_only_search(
                search_query,
                top_k=self.reranking_config["top_k"],
            )

        initial_results = self.retriever.search(
            search_query,
            top_k_dense=self.retrieval_config["top_k_dense"],
            top_k_bm25=self.retrieval_config["top_k_bm25"],
            top_k_final=self.retrieval_config["top_k_final"],
        )
        return self.reranker.rerank(
            search_query,
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

    def _augment_contexts(self, query: str, contexts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        augmented = list(contexts)
        seen_ids = {str(context["id"]) for context in augmented}
        supplemental: list[dict[str, Any] | None] = []

        if self._is_birth_date_correction_query(query):
            supplemental.append(
                self._find_context(self.chunks, document_type="fee_row", content_contains="জন্ম তারিখ সংশোধন")
            )
        if self._is_data_correction_query(query):
            supplemental.append(
                self._find_context(self.chunks, document_type="fee_row", content_contains="জন্ম তারিখ ব্যতীত")
            )

        for context in supplemental:
            if not context or str(context["id"]) in seen_ids:
                continue
            augmented.append(context)
            seen_ids.add(str(context["id"]))
        return augmented

    def _safe_decomposed_answer(
        self,
        query: str,
        method: str,
        base_contexts: list[dict[str, Any]],
    ) -> tuple[str, list[dict[str, Any]]]:
        if method != "civic" or not self._is_bangla_query(query):
            return "", []

        intents = self._detect_query_intents(query)
        if len(intents) < 2:
            return "", []

        sections: list[tuple[str, str]] = []
        all_contexts: list[dict[str, Any]] = []
        for intent in intents:
            heading, answer, contexts = self._answer_intent(query, intent, method, base_contexts)
            if not answer:
                continue
            sections.append((heading, self._strip_sources(answer)))
            all_contexts.extend(contexts)

        if len(sections) < 2:
            return "", []

        merged_contexts = self._merge_contexts(all_contexts)
        source_ids = [str(context["id"]) for context in merged_contexts[:8]]
        lines = ["আপনার প্রশ্নে কয়েকটি আলাদা বিষয় আছে। প্রাপ্ত সরকারি/উৎস ডেটার ভিত্তিতে অংশভাগ করে উত্তর দিচ্ছি:"]
        for index, (heading, body) in enumerate(sections, start=1):
            lines.append(f"{index}. {heading}\n{body}")
        if source_ids:
            lines.append(f"Sources: {', '.join(source_ids)}")
        return "\n\n".join(lines), merged_contexts

    def _answer_intent(
        self,
        query: str,
        intent: str,
        method: str,
        base_contexts: list[dict[str, Any]],
    ) -> tuple[str, str, list[dict[str, Any]]]:
        subqueries = {
            "application": "জন্ম নিবন্ধনের আবেদন কীভাবে করতে হয় ধাপে ধাপে",
            "documents": "জন্ম নিবন্ধনের জন্য কী কী কাগজপত্র বা প্রমাণক প্রয়োজন",
            "status": "জন্ম নিবন্ধন আবেদন নম্বর আবেদন সম্পন্ন হওয়ার পর করণীয়",
            "upload_error": "জন্ম নিবন্ধন আবেদনে ফাইল সংযুক্তি আপলোড প্রমাণক সমস্যা",
            "manual_to_online": "ম্যানুয়াল জন্ম নিবন্ধন অনলাইনে করা হয়নি করণীয়",
            "online_visibility": "অনলাইনে জন্ম নিবন্ধন খুঁজে পাওয়া যাচ্ছে না জন্ম তথ্য যাচাই",
            "overseas": "দেশের বাইরে থাকি জন্ম নিবন্ধন অনলাইনে করণীয় প্রবাসী দূতাবাস",
            "single_parent": "বিবাহ বিচ্ছেদ পিতামাতার একজন তথ্য দিয়ে সন্তানের জন্ম নিবন্ধন",
            "parent_correction": "পিতা মাতার নাম ভুল জন্ম নিবন্ধন সংশোধন কীভাবে",
            "lost_certificate": "জন্ম নিবন্ধন সনদ হারিয়ে গেলে করণীয় প্রতিলিপি",
        }
        headings = {
            "application": "জন্ম নিবন্ধনের আবেদন",
            "documents": "প্রয়োজনীয় কাগজপত্র/প্রমাণক",
            "status": "আবেদন নম্বর, অগ্রগতি বা পরবর্তী করণীয়",
            "upload_error": "ফাইল সংযুক্তি/আপলোড সমস্যা",
            "manual_to_online": "পুরোনো/ম্যানুয়াল নিবন্ধন অনলাইনে না থাকলে",
            "online_visibility": "অনলাইনে নিবন্ধন খুঁজে না পেলে",
            "overseas": "দেশের বাইরে থাকলে",
            "single_parent": "বিবাহ বিচ্ছেদ বা একক পিতা/মাতার তথ্য",
            "parent_correction": "পিতা-মাতার নাম সংশোধন",
            "lost_certificate": "সনদ হারিয়ে গেলে",
        }
        subquery = subqueries.get(intent, query)
        contexts = self._contexts_for_intent(intent, base_contexts)

        answer = ""
        if intent == "application":
            generation_contexts = self._select_generation_contexts(subquery, contexts, 3)
            answer = self._safe_extractive_answer(subquery, generation_contexts, method)
        elif intent == "documents":
            answer = self._safe_domain_answer(subquery, contexts, method)
        elif intent == "status":
            answer = self._safe_application_status_answer(contexts)
        elif intent == "upload_error":
            answer = self._safe_upload_error_answer(contexts)
        elif intent == "manual_to_online":
            answer = self._safe_manual_to_online_answer(contexts)
        elif intent == "online_visibility":
            answer = self._safe_online_visibility_answer(contexts)
        elif intent == "overseas":
            answer = self._safe_overseas_answer(contexts)
        elif intent == "single_parent":
            answer = self._safe_single_parent_answer(contexts)
        elif intent == "parent_correction":
            answer = self._safe_domain_answer(subquery, contexts, method)
        elif intent == "lost_certificate":
            answer = self._safe_domain_answer(subquery, contexts, method)

        return headings.get(intent, intent), answer, contexts

    def _contexts_for_intent(self, intent: str, base_contexts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        curated_ids = {
            "application": [
                "birth_registration_application_process_cleaned_008_01",
                "birth_registration_application_process_cleaned_002_01",
                "birth_registration_application_process_cleaned_016_01",
                "birth_registration_application_process_cleaned_019_01",
                "birth_registration_application_process_cleaned_020_01",
            ],
            "documents": [
                "birth_registration_application_process_cleaned_002_01",
                "birth_registration_application_process_cleaned_016_01",
                "birth_registration_application_process_02_cleaned_010_01",
            ],
            "status": [
                "birth_registration_application_process_02_cleaned_013_01",
                "birth_registration_application_process_cleaned_019_01",
                "birth_registration_application_process_cleaned_020_01",
            ],
            "upload_error": [
                "birth_registration_application_process_cleaned_016_01",
                "birth_registration_application_process_cleaned_005_01",
            ],
            "manual_to_online": [
                "bdris_faq_01_q02",
            ],
            "online_visibility": [
                "know_this_01_cleaned_008_01",
                "bdris_faq_01_q02",
                "bdris_faq_02_q03",
            ],
            "overseas": [
                "birth_and_death_registration_rules_2018_বিধি_১০_01",
                "bdris_faq_01_q12",
                "birth_registration_application_process_cleaned_009_01",
                "birth_registration_application_process_cleaned_018_01",
            ],
            "single_parent": [
                "bdris_faq_02_q08",
                "bdris_faq_01_q10",
            ],
            "parent_correction": [
                "application_for_birth_information_correction_cleaned_002_01",
                "application_for_birth_information_correction_cleaned_003_01",
                "application_for_birth_information_correction_cleaned_004_01",
                "application_for_birth_information_correction_cleaned_006_01",
                "application_for_birth_information_correction_cleaned_007_01",
                "birth_and_death_registration_fees_cleaned_fee_row_05",
            ],
            "lost_certificate": [
                "birth_and_death_registration_rules_2018_বিধি_১৩_01",
            ],
        }
        curated_contexts = [
            context
            for context in (self._context_for_chunk_id(chunk_id) for chunk_id in curated_ids.get(intent, []))
            if context
        ]
        return self._merge_contexts(curated_contexts, base_contexts)

    def _context_for_chunk_id(self, chunk_id: str) -> dict[str, Any] | None:
        chunk = self.chunks_by_id.get(chunk_id)
        if not chunk:
            return None
        return {
            "id": str(chunk["id"]),
            "content": str(chunk["content"]),
            "metadata": dict(chunk.get("metadata", {})),
            "score": 0.0,
            "retrievers": ["safe_path"],
        }

    def _detect_query_intents(self, query: str) -> list[str]:
        intents: list[str] = []

        def add(intent: str) -> None:
            if intent not in intents:
                intents.append(intent)

        if self._is_lost_certificate_query(query):
            add("lost_certificate")
        if self._is_single_parent_registration_query(query):
            add("single_parent")
        if self._is_online_visibility_query(query):
            add("online_visibility")
        if self._is_overseas_query(query):
            add("overseas")
        if self._is_parent_name_correction_query(query) and self._is_data_correction_query(query):
            add("parent_correction")
        elif self._is_data_correction_query(query):
            add("parent_correction")
        if self._is_application_status_query(query):
            add("status")
        if self._is_upload_error_query(query):
            add("upload_error")
        if self._is_manual_to_online_query(query):
            add("manual_to_online")
        if self._is_birth_application_query(query):
            add("application")
        if self._is_document_requirement_query(query):
            add("documents")

        multi_signal = (
            len(query) > 180
            or query.count("?") + query.count("？") >= 2
            or query.count("।") >= 2
            or "\n" in query
        )
        if len(intents) >= 2 and multi_signal:
            return intents
        if len(intents) >= 3:
            return intents
        return []

    def _safe_application_status_answer(self, contexts: list[dict[str, Any]]) -> str:
        app_id = self._find_context(contexts, document_type="application_process", section_contains_any=["আবেদন নম্বর", "Application ID"])
        next_steps = self._find_context(contexts, document_type="application_process", section_contains="পরবর্তী করণীয়")
        complete = self._find_context(contexts, document_type="application_process", section_contains_any=["আবেদন সম্পন্ন", "সনদ গ্রহণ"])
        cited = [context for context in [app_id, complete, next_steps] if context]
        if not cited:
            return ""

        parts = []
        if app_id:
            body = self._clean_evidence_body(self._extract_labeled_value(str(app_id["content"]), "Content"))
            if body:
                parts.append(body)
        if complete:
            body = self._clean_evidence_body(self._extract_labeled_value(str(complete["content"]), "Content"))
            if body:
                parts.append(body)
        if next_steps:
            body = self._clean_evidence_body(self._extract_labeled_value(str(next_steps["content"]), "Content"))
            if body:
                parts.append(body)
        parts.append("এই ডেটাসেটে নির্দিষ্ট আবেদন নম্বর দিয়ে অনলাইন progress/status যাচাই করার আলাদা পদ্ধতি পাওয়া যায়নি। তাই নির্দিষ্ট আবেদন নম্বরের বর্তমান অবস্থা জানতে সংশ্লিষ্ট নিবন্ধন কার্যালয় বা BDRIS নির্দেশনা অনুসরণ করা উচিত।")
        return "\n\n".join(parts) + f"\n\nSources: {', '.join(str(context['id']) for context in cited[:4])}"

    def _safe_upload_error_answer(self, contexts: list[dict[str, Any]]) -> str:
        attachments = self._find_context(contexts, document_type="application_process", section_contains_any=["সংযুক্ত", "প্রমাণক"])
        form_warning = self._find_context(contexts, document_type="application_process", section_contains="ফরম পূরণের সময় সতর্কতা")
        cited = [context for context in [attachments, form_warning] if context]
        if not cited:
            return ""

        parts = []
        for context in cited:
            section = context["metadata"].get("section_title", "")
            body = self._clean_evidence_body(self._extract_labeled_value(str(context["content"]), "Content"))
            if body:
                parts.append(f"{section}: {body}")
        parts.append("আপনার বর্ণিত `প্রয়োজনীয় ফাইল আপলোড করেননি` ধরনের নির্দিষ্ট error message-এর পূর্ণ troubleshooting এই ডেটাসেটে নেই। তবে প্রমাণকগুলো সঠিক আলাদা ঘরে যুক্ত হয়েছে কিনা, ফাইল ফরম্যাট/সাইজ গ্রহণযোগ্য কিনা, এবং সব বাধ্যতামূলক প্রমাণক সংযুক্ত হয়েছে কিনা যাচাই করা উচিত। সমস্যা চলতে থাকলে সংশ্লিষ্ট নিবন্ধন কার্যালয় বা BDRIS সহায়তার সঙ্গে যোগাযোগ করা নিরাপদ।")
        return "\n\n".join(parts) + f"\n\nSources: {', '.join(str(context['id']) for context in cited[:3])}"

    def _safe_manual_to_online_answer(self, contexts: list[dict[str, Any]]) -> str:
        migration = self._find_context(contexts, document_type="faq", category="manual_to_online_migration")
        if not migration:
            return ""
        answer = self._extract_labeled_value(str(migration["content"]), "Answer")
        return f"{answer}\n\nSources: {migration['id']}" if answer else ""

    def _safe_single_parent_answer(self, contexts: list[dict[str, Any]]) -> str:
        faq_contexts = [
            context
            for context in contexts
            if context["metadata"].get("document_type") == "faq"
            and context["metadata"].get("category") == "special_cases"
            and "পিতামাতার একজন" in str(context.get("content", ""))
        ]
        if not faq_contexts:
            return ""
        best = max(faq_contexts, key=lambda context: len(self._extract_labeled_value(str(context["content"]), "Answer")))
        answer = self._extract_labeled_value(str(best["content"]), "Answer")
        return f"{answer}\n\nSources: {best['id']}" if answer else ""

    def _safe_online_visibility_answer(self, contexts: list[dict[str, Any]]) -> str:
        verification = self._find_context(contexts, document_type="general_guidance", section_contains_any=["পরীক্ষা", "যাচাই"])
        migration = self._find_context(contexts, document_type="faq", category="manual_to_online_migration")
        discrepancy = self._find_context(contexts, document_type="faq", category="data_discrepancy")
        cited = [context for context in [verification, migration, discrepancy] if context]
        if not cited:
            return ""

        parts = []
        if verification:
            body = self._extract_labeled_value(str(verification["content"]), "Content")
            if body:
                parts.append(body)
        if migration:
            answer = self._extract_labeled_value(str(migration["content"]), "Answer")
            if answer:
                parts.append("যদি এটি পুরোনো/ম্যানুয়াল নিবন্ধন হয়ে থাকে: " + answer)
        if discrepancy:
            answer = self._extract_labeled_value(str(discrepancy["content"]), "Answer")
            if answer:
                parts.append(answer)
        parts.append("যদি সঠিক জন্ম নিবন্ধন নম্বর ও জন্ম তারিখ দিয়েও তথ্য না পাওয়া যায়, তাহলে সংশ্লিষ্ট নিবন্ধন কার্যালয়ের সংরক্ষিত রেকর্ড যাচাই করানো উচিত।")
        return "\n\n".join(parts) + f"\n\nSources: {', '.join(str(context['id']) for context in cited[:4])}"

    def _safe_overseas_answer(self, contexts: list[dict[str, Any]]) -> str:
        overseas_rule = self._find_context(contexts, document_type="legal_rules", section_contains="প্রবাসীগণের জন্ম নিবন্ধন")
        overseas_faq = self._find_context(contexts, document_type="faq", category="overseas_registration")
        embassy_place = self._find_context(contexts, document_type="application_process", content_contains="দূতাবাস")
        cited = [context for context in [overseas_rule, overseas_faq, embassy_place] if context]
        if not cited:
            return ""

        parts = []
        if overseas_rule:
            body = self._extract_labeled_value(str(overseas_rule["content"]), "Content")
            if body:
                parts.append("প্রবাসে জন্ম নিবন্ধনের ক্ষেত্রে বিধি ১০ অনুযায়ী বিদেশে অবস্থিত বাংলাদেশ দূতাবাসের নিবন্ধক প্রয়োজনীয় তথ্য/প্রমাণ পেলে জন্ম নিবন্ধন করতে পারেন।")
        if embassy_place:
            body = self._clean_evidence_body(self._extract_labeled_value(str(embassy_place["content"]), "Content"))
            if body:
                parts.append(body)
        if overseas_faq:
            answer = self._extract_labeled_value(str(overseas_faq["content"]), "Answer")
            if answer:
                parts.append("বিদেশে নিবন্ধন করে দেশে ফেরা বা মূল অফিস-সংক্রান্ত ক্ষেত্রে: " + answer)
        parts.append("তবে আপনি যদি বাংলাদেশে জন্মগ্রহণ করে থাকেন কিন্তু আগে অনলাইনে নিবন্ধন না হয়ে থাকে, তাহলে মূল/স্থানীয় নিবন্ধন কার্যালয়ের রেকর্ডও গুরুত্বপূর্ণ হতে পারে।")
        return "\n\n".join(parts) + f"\n\nSources: {', '.join(str(context['id']) for context in cited[:4])}"

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

    def _safe_domain_answer(
        self,
        query: str,
        contexts: list[dict[str, Any]],
        method: str,
    ) -> str:
        if method != "civic" or not contexts or not self._is_bangla_query(query):
            return ""

        source_ids = [str(context["id"]) for context in contexts[:3]]
        if self._is_single_parent_registration_query(query):
            answer = self._safe_single_parent_answer(contexts)
            if answer:
                return answer

        if self._is_overseas_query(query):
            answer = self._safe_overseas_answer(contexts)
            if answer:
                return answer

        if self._is_application_status_query(query):
            answer = self._safe_application_status_answer(contexts)
            if answer:
                return answer

        if self._is_upload_error_query(query):
            answer = self._safe_upload_error_answer(contexts)
            if answer:
                return answer

        if self._is_manual_to_online_query(query):
            answer = self._safe_manual_to_online_answer(contexts)
            if answer:
                return answer

        if self._is_registration_deadline_query(query):
            deadline = self._find_context(contexts, document_type="legal_act", content_contains="৪৫")
            if not deadline:
                deadline = self._find_context(contexts, document_type="legal_rules", content_contains="৪৫")
            if deadline:
                body = self._extract_labeled_value(str(deadline["content"]), "Content")
                return (
                    "জন্মের ৪৫ দিনের মধ্যে জন্ম সংক্রান্ত তথ্য নিবন্ধকের নিকট প্রদান করতে হবে।\n\n"
                    f"প্রাসঙ্গিক বিধি/আইন: {body}\n\n"
                    f"Sources: {', '.join(source_ids)}"
                )

        if self._is_document_requirement_query(query):
            app_prep = self._find_context(contexts, document_type="application_process", section_contains="পূর্ব প্রস্তুতি")
            attachments = self._find_context(contexts, document_type="application_process", section_contains_any=["সংযুক্ত", "প্রমাণক"])
            legal_docs = self._find_context(contexts, document_type="legal_rules", content_contains="প্রমাণাদি")
            parts = ["জন্ম নিবন্ধনের জন্য সাধারণত জন্মস্থান, স্থায়ী ঠিকানা এবং বর্তমান ঠিকানার তথ্য প্রস্তুত রাখতে হয়।"]
            if app_prep:
                body = self._clean_evidence_body(self._extract_labeled_value(str(app_prep["content"]), "Content"))
                if body:
                    parts.append(body)
            if attachments:
                body = self._clean_evidence_body(self._extract_labeled_value(str(attachments["content"]), "Content"))
                if body:
                    parts.append(body)
            if legal_docs:
                parts.append(
                    "বিধি ৯ অনুযায়ী প্রাসঙ্গিক প্রমাণের মধ্যে জন্মস্থান ও জন্ম তারিখের প্রমাণ, স্থায়ী ঠিকানার প্রমাণ, "
                    "এবং প্রযোজ্য ক্ষেত্রে পিতা-মাতার জন্ম নিবন্ধন নম্বর বা জাতীয় পরিচয়পত্রের তথ্য থাকতে পারে।"
                )
            return "\n\n".join(parts) + f"\n\nSources: {', '.join(source_ids)}"

        if self._is_lost_certificate_query(query):
            rule = self._find_context(contexts, document_type="legal_rules", section_contains="প্রতিলিপি")
            if rule:
                body = self._extract_labeled_value(str(rule["content"]), "Content")
                if body:
                    summary = (
                        "জন্ম নিবন্ধন সনদ হারিয়ে গেলে বা নষ্ট হলে নিবন্ধকের কাছে সনদের প্রতিলিপির জন্য আবেদন করতে হবে। "
                        "বিধি ১৩ অনুযায়ী, আবেদন পাওয়ার ৭ কার্য দিবসের মধ্যে জন্ম/মৃত্যু নিবন্ধন সনদের প্রতিলিপি প্রদান করা হয়। "
                        "প্রতিলিপির জন্য বিধি ২১ অনুযায়ী নির্ধারিত ফি প্রযোজ্য হতে পারে।"
                    )
                    return f"{summary}\n\nপ্রাসঙ্গিক বিধি: {body}\n\nSources: {', '.join(source_ids)}"

        if self._is_mixed_correction_query(query):
            return self._safe_mixed_correction_answer(contexts)

        if self._is_birth_date_correction_query(query):
            fee = self._find_context(contexts, document_type="fee_row", content_contains="জন্ম তারিখ সংশোধন")
            feature = self._find_context(contexts, document_type="correction_notice_ocr", content_contains="জন্ম তারিখ সংশোধন")
            legal = self._find_context(contexts, document_type="legal_rules", content_contains="ধারা ১৫")
            cited_contexts = list(contexts[:3])
            parts = [
                "জন্ম তারিখ ভুল হলে জন্ম নিবন্ধন তথ্য সংশোধনের আবেদন করতে হবে।",
            ]
            if legal:
                if legal not in cited_contexts:
                    cited_contexts.append(legal)
                parts.append("বিধিমালার প্রাসঙ্গিক অংশে বলা আছে, জন্ম তারিখ একবার নিবন্ধন করা হলে পরবর্তীতে আইনের ধারা ১৫ অনুযায়ী সংশোধন করা যায়।")
            if feature:
                if feature not in cited_contexts:
                    cited_contexts.append(feature)
                parts.append("BDRIS সংশোধন-সংক্রান্ত ফিচারের তালিকায় জন্ম তারিখ সংশোধন অন্তর্ভুক্ত আছে।")
            if fee:
                if fee not in cited_contexts:
                    cited_contexts.append(fee)
                amount = self._extract_labeled_value(str(fee["content"]), "Fee amount")
                if amount:
                    parts.append(f"জন্ম তারিখ সংশোধনের আবেদন ফি: {amount}।")
            parts.append("তবে এই ডেটাসেটে জন্ম তারিখ সংশোধনের সম্পূর্ণ ধাপে-ধাপে প্রক্রিয়া নেই; তাই সংশ্লিষ্ট নিবন্ধন কার্যালয়/BDRIS নির্দেশনা অনুসরণ করা উচিত।")
            cited_ids = [str(context["id"]) for context in cited_contexts[:5]]
            return "\n\n".join(parts) + f"\n\nSources: {', '.join(cited_ids)}"

        if self._is_online_visibility_query(query):
            answer = self._safe_online_visibility_answer(contexts)
            if answer:
                return answer

        if self._is_data_correction_query(query):
            correction_contexts = [
                context for context in contexts if context["metadata"].get("document_type") == "correction_process"
            ]
            fee = self._find_context(contexts, document_type="fee_row", content_contains="জন্ম তারিখ ব্যতীত")
            if correction_contexts:
                cited_contexts: list[dict[str, Any]] = []
                lines = ["নাম/ঠিকানা/তথ্য ভুল হলে জন্ম নিবন্ধন তথ্য সংশোধনের আবেদন করতে হবে।"]
                if self._is_parent_name_correction_query(query):
                    answer_contexts = self._sort_contexts_by_section_index(correction_contexts)[:4]
                else:
                    answer_contexts = [
                        context
                        for context in self._sort_contexts_by_section_index(correction_contexts)
                        if any(term in str(context["metadata"].get("section_title", "")) for term in ["যোগাযোগ", "তথ্য সংশোধন"])
                    ][:3]
                for context in answer_contexts:
                    section = context["metadata"].get("section_title", "")
                    body = self._clean_evidence_body(self._extract_labeled_value(str(context["content"]), "Content"))
                    if body:
                        if context not in cited_contexts:
                            cited_contexts.append(context)
                        lines.append(f"{section}: {body}")
                if fee:
                    if fee not in cited_contexts:
                        cited_contexts.append(fee)
                    amount = self._extract_labeled_value(str(fee["content"]), "Fee amount")
                    if amount:
                        lines.append(f"জন্ম তারিখ ব্যতীত নাম, পিতার নাম, মাতার নাম, ঠিকানা ইত্যাদি তথ্য সংশোধনের আবেদন ফি: {amount}।")
                if self._is_parent_name_correction_query(query) and self._is_document_requirement_query(query):
                    lines.append("পিতা-মাতার নাম সংশোধনের জন্য আপলোডযোগ্য সব কাগজপত্রের পূর্ণ তালিকা এই ডেটাসেটে নেই। তাই BDRIS সংশোধন পোর্টাল বা সংশ্লিষ্ট নিবন্ধন কার্যালয়ের নির্দেশনা অনুযায়ী প্রমাণপত্র প্রস্তুত করা উচিত।")
                if not self._is_parent_name_correction_query(query):
                    lines.append("এই ডেটাসেটে নাম/ঠিকানা সংশোধনের পূর্ণ ধাপে-ধাপে প্রক্রিয়া নেই; তাই সংশ্লিষ্ট নিবন্ধন কার্যালয় বা BDRIS সংশোধন পোর্টালের নির্দেশনা অনুসরণ করা উচিত।")
                cited_ids = [str(context["id"]) for context in cited_contexts[:5]]
                return "\n\n".join(lines) + f"\n\nSources: {', '.join(cited_ids)}"

        return ""

    def _safe_mixed_correction_answer(self, contexts: list[dict[str, Any]]) -> str:
        correction_contexts = [
            context for context in contexts if context["metadata"].get("document_type") == "correction_process"
        ]
        birth_date_fee = self._find_context(contexts, document_type="fee_row", content_contains="জন্ম তারিখ সংশোধন")
        other_info_fee = self._find_context(contexts, document_type="fee_row", content_contains="জন্ম তারিখ ব্যতীত")
        feature = self._find_context(contexts, document_type="correction_notice_ocr", content_contains="জন্ম তারিখ সংশোধন")
        legal = self._find_context(contexts, document_type="legal_rules", content_contains="ধারা ১৫")

        cited_contexts: list[dict[str, Any]] = []
        lines = [
            "নাম, ঠিকানা এবং জন্ম তারিখ একসাথে ভুল হলে এগুলোকে জন্ম নিবন্ধন তথ্য সংশোধনের বিষয় হিসেবে ধরতে হবে।",
            "তবে জন্ম তারিখ সংশোধন এবং জন্ম তারিখ ব্যতীত অন্যান্য তথ্য সংশোধনের ফি আলাদা।",
        ]
        if feature:
            if feature not in cited_contexts:
                cited_contexts.append(feature)
            lines.append("BDRIS সংশোধন-সংক্রান্ত ফিচারের তালিকায় জন্ম তারিখ সংশোধন অন্তর্ভুক্ত আছে।")
        if legal:
            if legal not in cited_contexts:
                cited_contexts.append(legal)
            lines.append("প্রাসঙ্গিক বিধি অনুযায়ী জন্ম তারিখ একবার নিবন্ধন করা হলে পরবর্তীতে আইনের ধারা ১৫ অনুযায়ী সংশোধন করা যায়।")
        if correction_contexts:
            lines.append("নাম/ঠিকানা/অন্যান্য তথ্য সংশোধনের জন্য জন্ম নিবন্ধন তথ্য সংশোধনের আবেদন করতে হবে।")
            general_contexts = [
                context
                for context in self._sort_contexts_by_section_index(correction_contexts)
                if any(term in str(context["metadata"].get("section_title", "")) for term in ["যোগাযোগ", "তথ্য সংশোধন"])
            ][:2]
            for context in general_contexts:
                section = context["metadata"].get("section_title", "")
                body = self._clean_evidence_body(self._extract_labeled_value(str(context["content"]), "Content"))
                if body:
                    if context not in cited_contexts:
                        cited_contexts.append(context)
                    lines.append(f"{section}: {body}")
        if birth_date_fee:
            if birth_date_fee not in cited_contexts:
                cited_contexts.append(birth_date_fee)
            amount = self._extract_labeled_value(str(birth_date_fee["content"]), "Fee amount")
            if amount:
                lines.append(f"জন্ম তারিখ সংশোধনের আবেদন ফি: {amount}।")
        if other_info_fee:
            if other_info_fee not in cited_contexts:
                cited_contexts.append(other_info_fee)
            amount = self._extract_labeled_value(str(other_info_fee["content"]), "Fee amount")
            if amount:
                lines.append(f"জন্ম তারিখ ব্যতীত নাম, পিতার নাম, মাতার নাম, ঠিকানা ইত্যাদি তথ্য সংশোধনের আবেদন ফি: {amount}।")
        lines.append("এই ডেটাসেটে সব ধরনের সংশোধনের সম্পূর্ণ ধাপে-ধাপে প্রক্রিয়া নেই; তাই সংশ্লিষ্ট নিবন্ধন কার্যালয়/BDRIS নির্দেশনা অনুসরণ করা উচিত।")

        cited_ids = [str(context["id"]) for context in cited_contexts[:6]]
        return "\n\n".join(lines) + f"\n\nSources: {', '.join(cited_ids)}"

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
    def _normalize_query_text(query: str) -> str:
        normalized = unicodedata.normalize("NFC", query)
        normalized = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", normalized)
        replacements = {
            "অনলাইনাে": "অনলাইনে",
            "অনলাইনাএ": "অনলাইনে",
            "অনলাই করা": "অনলাইনে করা",
            "অনলাই কর": "অনলাইনে কর",
            "ভোডার": "ভোটার",
            "চেয়ারম্যান": "চেয়ারম্যান",
            "প্রগ্রেস": "progress",
            "স্ট্যাটাস": "status",
        }
        for source, target in replacements.items():
            normalized = normalized.replace(source, target)
        return normalized.strip()

    @staticmethod
    def _merge_contexts(*context_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
        merged: list[dict[str, Any]] = []
        seen: set[str] = set()
        for contexts in context_groups:
            for context in contexts:
                context_id = str(context.get("id", ""))
                if not context_id or context_id in seen:
                    continue
                merged.append(context)
                seen.add(context_id)
        return merged

    @staticmethod
    def _strip_sources(answer: str) -> str:
        return re.sub(r"\n\nSources:\s*.+\Z", "", answer.strip(), flags=re.DOTALL).strip()

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
    def _is_birth_date_correction_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            "জন্ম তারিখ" in query and any(term in query for term in ["ভুল", "সংশোধন", "ঠিক"])
        ) or any(term in query_lc for term in ["date of birth correction", "birth date correction"])

    @staticmethod
    def _is_lost_certificate_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            any(term in query for term in ["হারিয়ে", "হারিয়ে", "হারাইয়া", "নষ্ট", "প্রতিলিপি", "নকল"])
            or any(term in query_lc for term in ["lost certificate", "duplicate certificate", "certificate copy", "reprint"])
        )

    @staticmethod
    def _is_online_visibility_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            any(
                term in query
                for term in [
                    "দেখাচ্ছে না",
                    "দেখাচ্ছেনা",
                    "খুঁজে পাচ্ছি না",
                    "খুঁজে পাচ্ছিনা",
                    "পাচ্ছি না",
                    "পাচ্ছিনা",
                    "অনলাইনে দেখ",
                    "অনলাইনে পাওয়া",
                    "অনলাইনে পাওয়া",
                    "জন্ম তথ্য যাচাই",
                ]
            )
            or any(term in query_lc for term in ["not showing online", "not found online", "online copy", "cannot find online"])
        )

    @staticmethod
    def _is_data_correction_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            any(term in query for term in ["নাম", "ঠিকানা", "সব ভুল", "তথ্য ভুল", "ঠিক করবে", "ঠিক করতে"])
            and any(term in query for term in ["সংশোধন", "ভুল", "ঠিক"])
        ) or any(term in query_lc for term in ["wrong name", "wrong address", "correct information", "data correction"])

    @staticmethod
    def _is_parent_name_correction_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            any(term in query for term in ["পিতার", "মাতার", "পিতা", "মাতা", "বাবার", "মায়ের", "মায়ের"])
            or any(term in query_lc for term in ["father", "mother", "parent"])
        )

    @staticmethod
    def _is_mixed_correction_query(query: str) -> bool:
        has_birth_date = CivicRAGPipeline._is_birth_date_correction_query(query)
        has_other_field = any(term in query for term in ["নাম", "ঠিকানা", "পিতার নাম", "মাতার নাম", "তথ্য"])
        return has_birth_date and has_other_field

    @staticmethod
    def _is_registration_deadline_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            "কত দিনের মধ্যে" in query
            or "কয় দিনের মধ্যে" in query
            or "কয় দিনের মধ্যে" in query
            or any(term in query_lc for term in ["within how many days", "registration deadline"])
        ) and ("জন্ম" in query or "birth" in query_lc)

    @staticmethod
    def _is_document_requirement_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            any(term in query for term in ["কাগজপত্র", "ডকুমেন্ট", "প্রমাণক", "দলিল", "কি কি লাগে", "কী কী লাগে"])
            or any(term in query_lc for term in ["documents", "required documents", "papers", "proof"])
        )

    @staticmethod
    def _is_birth_application_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            "জন্ম" in query
            and any(term in query for term in ["আবেদন", "করব", "করবো", "করতে", "কীভাবে", "কিভাবে", "অনলাইনে"])
        ) or any(term in query_lc for term in ["apply for birth", "birth registration application"])

    @staticmethod
    def _is_application_status_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            any(term in query for term in ["আবেদন নম্বর", "অ্যাপ্লিকেশন আইডি", "কতদিন", "কত দিন", "সময় লাগবে", "সময় লাগবে", "জন্ম নিবন্ধন নাম্বার", "বের করতে", "প্রগতি"])
            or any(term in query_lc for term in ["application id", "application number", "progress", "status", "how long"])
        )

    @staticmethod
    def _is_upload_error_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            any(term in query for term in ["ফাইল", "সংযোজন", "আপলোড", "সাবমিট", "এরর", "প্রয়োজনীয় ফাইল", "প্রয়োজনীয় ফাইল"])
            or any(term in query_lc for term in ["upload", "file", "submit", "error"])
        )

    @staticmethod
    def _is_manual_to_online_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            any(term in query for term in ["অনলাইনে করা নাই", "অনলাইন করা নাই", "অনলাইন করা হয়নি", "অনলাইনে জন্ম নিবন্ধন হয়নি", "ম্যানুয়াল", "হাতে লেখা"])
            or any(term in query_lc for term in ["manual registration", "not online", "not digitized"])
        )

    @staticmethod
    def _is_overseas_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            any(term in query for term in ["দেশের বাইরে", "বিদেশে", "প্রবাস", "দূতাবাস", "মিশন"])
            or any(term in query_lc for term in ["overseas", "abroad", "embassy", "mission"])
        )

    @staticmethod
    def _is_single_parent_registration_query(query: str) -> bool:
        query_lc = query.lower()
        return (
            any(term in query for term in ["ডিভোর্স", "বিবাহ বিচ্ছেদ", "তালাক", "শুধু পিতার", "শুধু মাতার", "পিতামাতার একজন", "নিখোঁজ"])
            or any(term in query_lc for term in ["divorce", "single parent", "missing parent"])
        ) and "জন্ম" in query

    @staticmethod
    def _find_context(
        contexts: list[dict[str, Any]],
        *,
        document_type: str | None = None,
        section_contains: str | None = None,
        section_contains_any: list[str] | None = None,
        category: str | None = None,
        content_contains: str | None = None,
    ) -> dict[str, Any] | None:
        for context in contexts:
            metadata = context.get("metadata", {})
            content = str(context.get("content", ""))
            section = str(metadata.get("section_title", ""))
            if document_type and metadata.get("document_type") != document_type:
                continue
            if category and metadata.get("category") != category:
                continue
            if section_contains and section_contains not in section:
                continue
            if section_contains_any and not any(term in section for term in section_contains_any):
                continue
            if content_contains and content_contains not in content:
                continue
            return context
        return None

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
    def _sort_contexts_by_section_index(contexts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        def section_index(context: dict[str, Any]) -> int:
            value = context.get("metadata", {}).get("section_index", 0)
            try:
                return int(value)
            except (TypeError, ValueError):
                return 0

        return sorted(contexts, key=section_index)

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
