from scripts.audit_bangla_corpus_quality import text_flags


def test_amounts_and_dates_are_diagnostics_not_rewrites():
    text = 'ফি ১০০ টাকা; date 01/01/2001'
    assert text_flags(text) == ['mixed_digit_scripts_not_necessarily_error']
    assert '১০০' in text and '01/01/2001' in text


def test_broken_encoding_and_joiners_are_flagged():
    flags = text_flags('\ufffd\ue000\u200d\u200b')
    assert 'replacement_character' in flags
    assert 'private_use_character' in flags
    assert 'joiner_review_do_not_blindly_remove' in flags
    assert 'invisible_or_directional_control' in flags


def test_nfc_is_not_spelling_correction():
    assert text_flags('শর্ত এবং ব্যতিক্রম') == []
