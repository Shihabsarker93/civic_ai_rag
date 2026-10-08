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


def test_guideline_replacement_is_hash_gated():
    from scripts.prepare_birth_review_candidate import replacement_text

    repair = json.loads((ROOT / 'docs/data_cleanup/birth_review_20261008/guideline_review.json').read_text())['files'][0]
    assert 'পৃষ্ঠা ৬' in replacement_text(repair)
    with pytest.raises(ValueError, match='replacement changed'):
        replacement_text({**repair, 'replacement_sha256': 'wrong'})


def test_guideline_sections_preserve_membership_duties_and_pages():
    from domains.birth_death_registration.scripts import prepare_chunks as prep
    from scripts.prepare_birth_review_candidate import reviewed_rows

    repair = json.loads((ROOT / 'docs/data_cleanup/birth_review_20261008/guideline_review.json').read_text())['files'][0]
    rows, coverage = reviewed_rows(prep, ROOT / repair['replacement_file'], repair, 1400)
    retained = [s for s in coverage if s['status'] == 'retained']
    assert len(retained) == 23
    assert sum(s['section'].endswith('গঠন') for s in retained) == 8
    assert sum(s['section'].endswith(prep.normalize_text('দায়িত্ব')) for s in retained) == 8
    assert sum(s['status'] == 'provenance_only' for s in coverage) == 4
    assert {r['metadata']['source_page'] for r in rows} == {1, 2, 3, 4, 5}
    assert all(r['metadata']['current_applicability_verified'] is False for r in rows)
    assert all(r['id'].startswith('review_v2_') for r in rows)
    city = [r for r in rows if r['metadata']['section_title'] == prep.normalize_text('পৃষ্ঠা ২ | সিটি কর্পোরেশন জন্ম ও মৃত্যু নিবন্ধন টাস্ক ফোর্স: গঠন')]
    assert 'স্থানীয় সমাজ কর্মী ২ জন' in city[0]['content']
    with pytest.raises(ValueError, match='Excluded section missing'):
        reviewed_rows(prep, ROOT / repair['replacement_file'], {**repair, 'excluded_sections': ['missing']}, 1400)
