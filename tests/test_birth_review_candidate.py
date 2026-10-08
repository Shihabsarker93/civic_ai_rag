import json
from pathlib import Path

import pytest

from scripts.prepare_birth_review_candidate import ROOT, apply_changes


def test_repair_requires_unique_anchor():
    changes = [{"id": "example", "before": "old", "after": "new"}]
    assert apply_changes("old value", changes) == "new value"
    with pytest.raises(ValueError):
        apply_changes("old old", changes)
    with pytest.raises(ValueError):
        apply_changes("missing", changes)


def test_reviewed_repairs_match_baseline_and_preserve_limits():
    repairs = json.loads((ROOT / "docs/data_cleanup/birth_review_20261008/repairs.json").read_text())
    for record in repairs["files"]:
        original = (ROOT / "domains/birth_death_registration/data/raw" / record["prepared_file"]).read_text()
        candidate = apply_changes(original, record["changes"])
        assert candidate != original
        if "notice_" in record["prepared_file"]:
            assert "শুধুমাত্র দিন ও মাসের" in candidate
            assert "উপপরিচালক স্থানীয় সরকার ও উপজেলা প্রশাসনের আইডি" in candidate
            assert "০১-০১-২০১৩" in candidate
            assert "প্রথম রেজিস্ট্রেশন সনদটি বহাল রাখতে হবে" in candidate
            assert "নিবন্ধক সহকারী তার আইডি দিয়ে প্রবেশ করবে" in candidate


def test_existing_output_is_not_overwritten(tmp_path):
    from scripts.prepare_birth_review_candidate import build

    marker = tmp_path / "keep.txt"
    marker.write_text("keep")
    with pytest.raises(ValueError, match="Output exists"):
        build(tmp_path, tmp_path, Path("unused"))
    assert marker.read_text() == "keep"
