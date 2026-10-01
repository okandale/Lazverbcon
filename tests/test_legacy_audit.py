"""Validate the audit independently of the uploaded production data."""

import json
import sqlite3
import sys
from dataclasses import asdict
from pathlib import Path
from unittest.mock import patch

import pytest
from laz_api.catalog import build_catalog
from laz_engine.engine import conjugate
from laz_engine.models import Dialect, Features, Person

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.compare_legacy_database import (  # noqa: E402
    compare,
    copy_rows,
    decode_copy,
    features_for,
    map_verb,
    sha256,
)


def test_copy_escaping_and_nulls():
    assert decode_copy(r"\N") is None
    assert decode_copy(r"\\N") == r"\N"
    assert decode_copy(r"a\tb\nc\\d") == "a\tb\nc\\d"
    assert decode_copy(r"\303\247") == "ç"
    assert decode_copy(r"\xc3\xa7") == "ç"
    assert decode_copy("ç̌ǩt̆") == "ç̌ǩt̆"


def test_copy_parser_rejects_truncated_or_malformed_rows(tmp_path):
    path = tmp_path / "source.sql"
    path.write_text("COPY public.dialect (dialect_id, english_name) FROM stdin;\n1\n\\.\n")
    with pytest.raises(ValueError, match="Invalid COPY row"):
        list(copy_rows(path))
    path.write_text("COPY public.dialect (dialect_id) FROM stdin;\n1\n")
    with pytest.raises(ValueError, match="Incomplete COPY"):
        list(copy_rows(path))


def base_form(**overrides):
    return {
        "verb_form_id": "1",
        "verb_id": "old-verb",
        "frame": "Ergative",
        "subject": "S1SG",
        "object": None,
        "tense": "present",
        "derivation": "none",
        "mood": "indicative",
        "is_applicative": "f",
        "is_causative": "f",
        "is_double_causative": "f",
        "optional_prefix": None,
        "spelling": "visinapam",
        **overrides,
    }


def test_features_preserve_markers_and_reject_unknown_values():
    assert (
        features_for(base_form(optional_prefix="ko", is_double_causative="t"), "HO").optional_prefix
        == "ko"
    )
    assert not features_for(base_form(optional_prefix="do"), "AS").optional_preverb
    assert features_for(base_form(is_causative="t"), "AS").causative == "simple"
    assert features_for(base_form(is_double_causative="t"), "AS").causative == "double"
    for row in (
        base_form(subject="typo"),
        base_form(is_causative="t", is_double_causative="t"),
        base_form(optional_prefix="unknown"),
    ):
        with pytest.raises(ValueError):
            features_for(row, "AS")


def old_verb(entry):
    return {
        "verb_id": "old-verb",
        "dialect_id": "old-dialect",
        "verb_category_id": "old-class",
        "infinitive": entry.infinitive,
        "present_3sg": "isinapams",
        "meaning_english": entry.english,
        "meaning_turkish": entry.turkish,
    }


def test_identity_mapping_does_not_guess_between_homographs(verb):
    entry = verb("osinapu")
    candidates = [asdict(entry), {**asdict(entry), "id": "homograph"}]
    mapped, reason, ids = map_verb(old_verb(entry), candidates, "AS", "TVE")
    assert mapped is None and reason == "ambiguous_entry"
    assert set(ids) == {entry.id, "homograph"}


def write_table(file, table, rows):
    columns = list(rows[0])
    file.write(f"COPY public.{table} ({', '.join(columns)}) FROM stdin;\n")
    for row in rows:
        file.write("\t".join(r"\N" if row[c] is None else row[c] for c in columns) + "\n")
    file.write("\\.\n")


def test_full_comparison_accounts_for_all_rows_and_preserves_inputs(tmp_path, verb):
    entry = verb("osinapu")
    catalog = tmp_path / "catalog.sqlite"
    # A complete small lexicon makes the integration test fast and deterministic.
    with patch("laz_api.catalog.load_entries", return_value=(entry,)):
        manifest = build_catalog(catalog, "full")
    source = tmp_path / "source.sql"
    second = conjugate(entry, Features(Dialect.AS, Person.SECOND_SINGULAR)).forms[0].spelling
    with source.open("w") as file:
        file.write("DROP TABLE important_data;\n")  # Must be ignored, never executed.
        write_table(file, "dialect", [{"dialect_id": "old-dialect", "english_name": "Ardeşen"}])
        write_table(file, "verb_category", [{"verb_category_id": "old-class", "code": "TVE"}])
        write_table(file, "verb", [old_verb(entry)])
        write_table(
            file,
            "verb_form",
            [
                base_form(),
                base_form(verb_form_id="2", subject="S2SG", spelling="different spelling"),
                base_form(verb_form_id="3", subject="S2SG", spelling=second, frame="Nominative"),
                base_form(verb_form_id="4", object="O1SG", spelling="N/A - Geçersiz Kombinasyon"),
                base_form(verb_form_id="5", object="O1SG", spelling="stored-but-unsupported"),
            ],
        )
    hashes = (sha256(source), sha256(catalog))
    result = compare(source, catalog, tmp_path / "report")
    assert result["legacy_forms"] == 5
    assert result["old_row_status"] == {
        "exact": 1,
        "spelling_difference": 1,
        "frame_difference": 1,
        "both_reject": 1,
        "unsupported_request": 1,
    }
    assert sum(result["new_only_status"].values()) == manifest["form_count"] - 1
    assert result["legacy_rejection_messages"] == 1
    assert (sha256(source), sha256(catalog)) == hashes
    with sqlite3.connect(tmp_path / "report/audit.sqlite") as db:
        assert db.execute("SELECT count(*) FROM old_rows").fetchone()[0] == 5
        assert json.loads(db.execute("SELECT data FROM report").fetchone()[0]) == result
    with pytest.raises(FileExistsError):
        compare(source, catalog, tmp_path / "report")
