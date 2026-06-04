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
            pairs = [(query, result.retrieval_text) for result in results]
            scores = self.cross_encoder.predict(pairs)
            rescored = [
                replace(result, score=float(score), retrievers=[*result.retrievers, "cross_encoder"])
                for result, score in zip(results, scores)
            ]
            return self._apply_domain_boosts(query, rescored)[:top_k]

        if self.fallback == "lexical_overlap":
            return self._lexical_rerank(query, results, top_k)

        return self._apply_domain_boosts(query, results)[:top_k]

    def _lexical_rerank(self, query: str, results: list[RetrievalResult], top_k: int) -> list[RetrievalResult]:
        query_tokens = set(tokenize(query))
        rescored = []

        for result in results:
            content_tokens = set(tokenize(result.retrieval_text))
            overlap = len(query_tokens.intersection(content_tokens))
            coverage = overlap / max(len(query_tokens), 1)
            # Keep lexical fallback as a light tie-breaker; RRF should remain dominant.
            score = result.score + (0.05 * coverage)
            rescored.append(
                replace(result, score=score, retrievers=[*result.retrievers, "lexical_reranker"])
            )

        return self._apply_domain_boosts(query, rescored)[:top_k]

    def _apply_domain_boosts(self, query: str, results: Iterable[RetrievalResult]) -> list[RetrievalResult]:
        query_lc = query.lower()
        is_how_to_registration = (
            any(term in query for term in ["কীভাবে", "কিভাবে", "করতে পারি", "করবো", "করব", "আবেদন"])
            or any(term in query_lc for term in ["how", "apply", "application", "register", "registration"])
        ) and ("নিবন্ধন" in query or "registration" in query_lc or "certificate" in query_lc)
        is_correction = (
            any(term in query for term in ["সংশোধন", "বাতিল", "জাতীয়তা", "ইস্যু তারিখ", "রেজিস্ট্রেশন তারিখ"])
            or any(term in query_lc for term in ["correction", "correct", "fix", "amend", "cancel", "nationality", "issue date"])
        )
        is_duplicate_cancel = (
            any(term in query for term in ["একাধিক", "বাতিল"])
            or any(term in query_lc for term in ["duplicate", "cancel"])
        )
        is_fee_query = (
            any(term in query for term in ["ফি", "ফিস", "টাকা", "লাগবে", "খরচ", "বিনামূল্যে", "বিনা ফিসে"])
            or any(term in query_lc for term in ["fee", "fees", "cost", "charge", "payment", "free"])
        )
        is_fee_admin_query = (
            any(term in query for term in ["চালান", "জমা", "আপলোড"])
            or any(term in query_lc for term in ["challan", "upload", "deposit"])
        )
        is_fee_waiver_query = (
            any(term in query for term in ["এতিম", "প্রতিবন্ধী", "সহায়", "সহায়", "মওকুফ", "মাফ"])
            or any(term in query_lc for term in ["orphan", "disabled", "waiver", "exempt"])
        )

        rescored: list[RetrievalResult] = []
        for result in results:
            metadata = result.metadata
            doc_type = str(metadata.get("document_type", ""))
            category = str(metadata.get("category", ""))
            section_title = str(metadata.get("section_title", ""))
            score = result.score

            if is_how_to_registration:
                if doc_type == "application_process":
                    score += 0.08
                    if section_title.startswith("ধাপ"):
                        score += 0.02
                    if any(term in section_title for term in ["ওয়েবসাইটে প্রবেশ", "ওয়েবসাইটে প্রবেশ", "পূর্ব প্রস্তুতি", "প্রয়োজনীয়", "পরবর্তী করণীয়"]):
                        score += 0.03
                elif doc_type == "general_guidance" and any(term in section_title for term in ["পদ্ধতি", "প্রক্রিয়া", "প্রক্রিয়া"]):
                    score += 0.05
                elif doc_type == "portal_summary":
                    score += 0.02
                elif doc_type == "legal_rules":
                    score -= 0.03
                elif doc_type == "faq" and category in {"special_cases", "parents_registration"}:
                    score -= 0.06
                if any(term in section_title for term in ["যাচাই", "পরীক্ষা", "জমজ", "২০১৩", "বিদেশ", "প্রবাস", "বিশেষ"]):
                    score -= 0.04

            if is_correction and doc_type in {"correction_process", "correction_notice_ocr"}:
                score += 0.08
                if is_duplicate_cancel:
                    if doc_type == "correction_notice_ocr":
                        score += 0.08
                        if any(term in section_title for term in ["বাতিলের ধাপ", "বাতিলকরণের ধাপ", "বাতিল করার ধাপ"]):
                            score += 0.12
                        elif "বাতিল" in section_title:
                            score += 0.05
                        elif any(term in section_title for term in ["জাতীয়তা", "ইস্যু", "রেজিস্ট্রেশন তারিখ"]):
                            score -= 0.06
                    elif doc_type == "correction_process":
                        score -= 0.03

            if is_fee_query:
                if is_fee_waiver_query and doc_type == "legal_rules" and section_title == "ফিস":
                    score += 0.22
                    if any(term in result.retrieval_text for term in ["এতিম", "প্রতিবন্ধী", "সহায় সম্বলহীন", "সহায় সম্বলহীন"]):
                        score += 0.08
                    elif "মওকুফ" in result.retrieval_text:
                        score -= 0.03
                if doc_type in {"fees_table", "fee_row"}:
                    score += 0.16
                    if "বিনা ফিসে" in result.retrieval_text or "৪৫" in result.retrieval_text:
                        score += 0.03
                    if is_fee_waiver_query:
                        score -= 0.08
                elif not is_fee_admin_query and not is_fee_waiver_query and doc_type in {"faq", "legal_rules", "legal_act"}:
                    score -= 0.04

            rescored.append(replace(result, score=score))

        return sorted(rescored, key=lambda result: result.score, reverse=True)
