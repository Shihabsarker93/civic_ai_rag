import json
from types import SimpleNamespace

import pytest

from src.generation.evidence_contract import validate_output
from src.generation.applicability import filter_applicable
from src.generation.ollama_generator import OllamaAnswerGenerator
from src.pipeline import CivicRAGPipeline
from src.retrieval.hybrid_retriever import RetrievalResult


CONTEXTS = [{"id": "source_1", "content": "নবায়নের জন্য ফি ৫০০ টাকা। মূল সনদ সঙ্গে আনতে হবে।", "metadata": {}}]


def output():
    return {"decision": "answer", "items": [{"text": "নবায়নের জন্য ফি ৫০০ টাকা।",
            "supports": [{"source_id": "source_1", "quote": "নবায়নের জন্য ফি ৫০০ টাকা।"}]}], "clarification": ""}


def test_valid_support_only_cites_used_sources():
    result = validate_output(json.dumps(output()), CONTEXTS + [{"id": "unused", "content": "অন্য সেবা"}])
    assert result["answer"].endswith("Sources: source_1")
    assert "unused" not in result["answer"]
    assert result["evidence_check"]["semantic_verification"] is False


@pytest.mark.parametrize("fault", ["source", "quote", "number", "language", "empty", "schema"])
def test_invalid_output_fails_closed(fault):
    data = output()
    item = data["items"][0]
    if fault == "source":
        item["supports"][0]["source_id"] = "invented"
    elif fault == "quote":
        item["supports"][0]["quote"] = "এই উদ্ধৃতিটি উৎসে নেই।"
    elif fault == "number":
        item["text"] = "নবায়নের জন্য ফি ৯০০ টাকা।"
    elif fault == "language":
        item["text"] = "The fee is five hundred taka."
    elif fault == "empty":
        item["supports"] = []
    else:
        data = []
    result = validate_output(json.dumps(data), CONTEXTS)
    assert result["answer_route"] == "evidence_abstention"
    assert "Sources:" not in result["answer"]


def test_truncated_json_fails_closed():
    assert validate_output('{"decision":', CONTEXTS)["evidence_check"]["status"] == "invalid_json"


def test_clarification_and_partial():
    clarification = {"decision": "clarify", "items": [], "clarification": "আপনি নতুন আবেদন নাকি নবায়ন করতে চান?"}
    assert validate_output(json.dumps(clarification), CONTEXTS)["answer_route"] == "evidence_clarification"
    data = output()
    data["decision"] = "partial"
    assert "বাকি অংশ" in validate_output(json.dumps(data), CONTEXTS)["answer"]


def test_bangla_and_ascii_digits_can_match():
    data = output()
    data["items"][0]["text"] = "নবায়নের জন্য ফি 500 টাকা।"
    assert validate_output(json.dumps(data), CONTEXTS)["answer_route"] == "llm_evidence_answer"


def test_explicit_system_message_and_json_binding():
    generator = OllamaAnswerGenerator.__new__(OllamaAnswerGenerator)
    class FakeModel:
        def bind(self, **kwargs):
            assert kwargs["format"]["type"] == "object"
            assert kwargs["options"]["num_ctx"] == 16384
            return self
        def invoke(self, messages):
            assert [m.type for m in messages] == ["system", "human"]
            assert json.loads(messages[1].content)["question"] == "কত টাকা?"
            return SimpleNamespace(content=json.dumps(output()))
    generator.llm = FakeModel()
    assert generator.answer_grounded("কত টাকা?", CONTEXTS)["answer_route"] == "llm_evidence_answer"


def test_oversized_evidence_is_recorded_not_truncated():
    generator = OllamaAnswerGenerator.__new__(OllamaAnswerGenerator)
    result = generator.answer_grounded("কী করব?", [{"id": "too_long", "content": "শর্ত " * 20000}])
    assert result["evidence_check"]["status"] == "evidence_exceeds_context_budget"
    assert result["evidence_check"]["omitted_source_ids"] == ["too_long"]


@pytest.mark.parametrize("query,topic", [
    ("নতুন পাসপোর্ট করতে কী লাগবে?", "Documents Needed for Passport Collection"),
    ("নতুন লাইসেন্স করতে কী লাগবে?", "লাইসেন্স নবায়ন"),
    ("ফিটনেস নবায়ন করব", "ড্রাইভিং লাইসেন্স নবায়ন"),
    ("জন্মতারিখ ভুল হলে সংশোধন করব", "রেজিস্ট্রেশন ও ইস্যু তারিখ সংশোধন"),
    ("পাসপোর্ট বানাতে কত টাকা লাগে?", "বিদেশীদের পরিচিতি সনদ (Certificate of Identity)"),
])
def test_explicit_action_service_and_date_conflicts_are_excluded(query, topic):
    contexts = [{"id": "wrong", "content": "অন্য কাজের শর্তাবলি", "metadata": {"section_title": topic}},
                {"id": "unknown", "content": "অজানা শিরোনামের তথ্য", "metadata": {}}]
    kept, rejected = filter_applicable(query, contexts)
    assert [c["id"] for c in kept] == ["unknown"]
    assert rejected[0]["source_id"] == "wrong"


def test_matching_collection_and_renewal_are_not_excluded():
    for query, topic in [("পাসপোর্ট সংগ্রহ করতে কী লাগবে?", "Passport Collection"),
                         ("লাইসেন্স নবায়নের আবেদন করব", "লাইসেন্স নবায়ন")]:
        contexts = [{"id": "right", "content": "প্রাসঙ্গিক শর্তাবলি", "metadata": {"section_title": topic}}]
        assert filter_applicable(query, contexts) == (contexts, [])


@pytest.mark.parametrize("domain", ["passport", "brta", "birth_death_registration"])
def test_all_domains_bypass_unchecked_controlled_handlers(domain):
    pipeline = CivicRAGPipeline.__new__(CivicRAGPipeline)
    pipeline.domain_id = domain
    pipeline.birth_death_rules = domain == "birth_death_registration"
    pipeline.generation_config = {"default_model": "test", "evidence_contract": True}
    result = RetrievalResult(chunk_id="source_1", content=CONTEXTS[0]["content"], retrieval_text="aliases",
                             metadata={}, score=0.9, retrievers=["dense"])
    pipeline.retrieve = lambda *args, **kwargs: [result]
    def forbidden(*args, **kwargs):
        raise AssertionError("Unchecked controlled handler called")
    pipeline._safe_domain_answer = forbidden
    pipeline._safe_passport_fee_and_office_answer = forbidden
    pipeline._select_generation_contexts = forbidden
    pipeline._generator = lambda model: SimpleNamespace(answer_grounded=lambda q, c: validate_output(json.dumps(output()), c))
    answer = pipeline.ask("নবায়ন করতে কত টাকা?", method="civic")
    assert answer["answer_route"] == "llm_evidence_answer"
    assert answer["generation_sources"] == ["source_1"]
    assert pipeline.ask("নবায়ন করতে কত টাকা?", generate=False)["answer_route"] == "retrieval_only"
    pipeline.retrieve = lambda *args, **kwargs: []
    pipeline._generator = forbidden
    assert pipeline.ask("নবায়ন করতে কত টাকা?")["answer_route"] == "evidence_abstention"
