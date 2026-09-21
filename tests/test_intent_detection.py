from src.generation.ollama_generator import detect_answer_language
from src.pipeline import CivicRAGPipeline


def test_bangla_queries_reject_chinese_model_output():
    assert CivicRAGPipeline._violates_answer_language(
        "গাড়ির ফিটনেস সনদ নবায়ন কীভাবে করব?",
        "根据提供的信息，您需要完成车辆检查。",
    )


def test_bangla_language_safety_answer_never_exposes_invalid_output():
    answer = CivicRAGPipeline._bangla_language_safety_answer([{"id": "brta_example"}])
    assert "নির্ভরযোগ্য বাংলায় উত্তর" in answer
    assert "brta_example" in answer


def test_bangla_query_with_official_latin_terms_still_requests_bangla_output():
    assert detect_answer_language("BRTA রেকর্ডে রং পরিবর্তন কীভাবে করব?") == "Bangla"


def test_bangla_query_rejects_mostly_english_answer_prose():
    assert CivicRAGPipeline._violates_answer_language(
        "পাসপোর্টের পাসওয়ার্ড কীভাবে রিসেট করব?",
        "Use the account page and select forgot password to receive a reset email.\n\nSources: passport_example",
    )


def test_dominant_context_is_used_alone_for_single_topic_question():
    contexts = [
        {"id": "fitness", "score": 0.65},
        {"id": "rule", "score": 0.12},
    ]
    assert CivicRAGPipeline._has_dominant_single_topic_context(
        "ফিটনেস সনদ নবায়নের প্রক্রিয়া কী?", contexts
    )


def test_multi_part_question_keeps_multiple_contexts():
    contexts = [
        {"id": "fee", "score": 0.80},
        {"id": "office", "score": 0.15},
    ]
    assert not CivicRAGPipeline._has_dominant_single_topic_context(
        "পাসপোর্টের ফি কত আর কোথায় যেতে হবে?", contexts
    )


def test_cross_domain_aggregate_question_is_detected():
    assert CivicRAGPipeline._is_cross_domain_aggregate_query(
        "জন্ম নিবন্ধন, পাসপোর্ট এবং ড্রাইভিং লাইসেন্স একসাথে করতে মোট কত টাকা লাগবে?"
    )


def test_single_domain_fee_question_is_not_cross_domain_aggregate():
    assert not CivicRAGPipeline._is_cross_domain_aggregate_query(
        "ই-পাসপোর্টের জন্য মোট কত টাকা লাগবে?"
    )


def test_lost_certificate_paraphrases_are_detected() -> None:
    queries = [
        "জন্ম নিবন্ধন হারালে কী করব?",
        "আমার জন্মসনদ হারিয়ে গেছে, নতুন কপি পেতে হলে কোথায় যেতে হবে?",
        "জন্ম সনদ নষ্ট হয়ে গেছে, প্রতিলিপি কীভাবে পাব?",
    ]

    for query in queries:
        assert CivicRAGPipeline._is_lost_certificate_query(query)


def test_plain_birth_application_is_not_lost_certificate() -> None:
    assert not CivicRAGPipeline._is_lost_certificate_query("জন্ম নিবন্ধনের জন্য আবেদন করব কীভাবে?")
