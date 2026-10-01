"""Expected outputs copied from the maintainer's corrected database, not the engine."""

import json
from dataclasses import replace
from pathlib import Path

import pytest
from laz_engine.engine import conjugate
from laz_engine.lexicon import entries_by_id
from laz_engine.models import Features
from pydantic import TypeAdapter

FIXTURE = json.loads((Path(__file__).parent / "fixtures/maintainer-corrections.json").read_text())
ADAPTER = TypeAdapter(Features)


@pytest.mark.parametrize("case", FIXTURE["cases"])
def test_maintainer_spellings_and_frames(case):
    result = conjugate(entries_by_id()[case["entry_id"]], ADAPTER.validate_python(case["features"]))
    assert result.status == "ok", (case["legacy_row_ids"], result)
    assert sorted(form.spelling for form in result.forms) == case["expected"]
    assert {form.frame for form in result.forms} == {case["frame"]}


def test_evidence_has_unique_requests_and_source_rows():
    keys = [(c["entry_id"], json.dumps(c["features"], sort_keys=True)) for c in FIXTURE["cases"]]
    assert len(keys) == len(set(keys))
    assert all(c["legacy_row_ids"] for c in FIXTURE["cases"])
    assert sum(c["basis"] == "dump" for c in FIXTURE["cases"]) == 283


def test_optional_setting_keeps_corrected_hopa_ending():
    # Dump row 575832 explicitly stores this ko-prefixed spelling.
    case = next(
        c
        for c in FIXTURE["cases"]
        if c["entry_id"] == "verb-0070"
        and c["features"]["subject"] == "3pl"
        and c["basis"] == "dump"
    )
    features = replace(ADAPTER.validate_python(case["features"]), optional_preverb=True)
    result = conjugate(entries_by_id()[case["entry_id"]], features)
    assert [form.spelling for form in result.forms] == ["kogvaşinert̆es"]


def test_recognized_echopu_preverb_survives_optional_setting():
    case = next(
        c
        for c in FIXTURE["cases"]
        if c["entry_id"] == "verb-0040"
        and c["features"]["dialect"] == "FA"
        and c["basis"] == "dump"
    )
    features = replace(ADAPTER.validate_python(case["features"]), optional_preverb=True)
    result = conjugate(entries_by_id()[case["entry_id"]], features)
    assert [form.spelling for form in result.forms] == case["expected"]
