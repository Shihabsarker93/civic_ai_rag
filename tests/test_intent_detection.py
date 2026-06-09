from src.pipeline import CivicRAGPipeline


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
