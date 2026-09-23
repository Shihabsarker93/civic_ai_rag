from types import SimpleNamespace

from scripts.run_simple_matched import answer


def test_dense_only_uses_matched_generator_and_preserves_order():
    rows = [{'id': str(i), 'content': 'Evidence', 'metadata': {}} for i in range(8)]
    calls = []
    def retrieve(query, method):
        assert method == 'simple'
        return rows
    def generator(model, **kwargs):
        assert model == 'qwen3:8b'
        assert kwargs == {'selected_evidence': True}
        return SimpleNamespace(answer=lambda q, contexts: calls.append(contexts) or 'answer', last_metadata={})
    pipeline = SimpleNamespace(_normalize_query_text=lambda q: q, retrieve=retrieve,
        _context_from_result=lambda r: r, _generator=generator,
        _violates_answer_language=lambda q, a: False, domain_id='passport')
    result = answer(pipeline, 'question')
    assert calls == [rows[:6]]
    assert result['answer_contexts'] == rows[:6]
    assert result['method'] == 'simple_matched'


def test_empty_evidence_does_not_call_generator():
    pipeline = SimpleNamespace(_normalize_query_text=lambda q: q,
        retrieve=lambda q, method: [], domain_id='brta')
    assert answer(pipeline, 'question')['answer_route'] == 'no_applicable_evidence'
