"""Prefix semantics, reviewed identity mapping and exhaustive-check failure detection."""

import gzip
import json
import sqlite3
import sys
from dataclasses import asdict, replace
from pathlib import Path

from fastapi.testclient import TestClient
from laz_api.app import create_app
from laz_api.catalog import build_catalog, request_id
from laz_engine.engine import conjugate
from laz_engine.lexicon import entries_by_id
from laz_engine.maintainer import data
from laz_engine.models import Dialect, Features, OptionalPrefix, Person
from laz_engine.rules.optional_prefixes import attach
from laz_engine.validation import validate

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.import_maintainer import choose_entry  # noqa: E402
from scripts.verify_maintainer_release import verify  # noqa: E402


def test_prefix_contraction_and_parentheses():
    assert attach("ikum", OptionalPrefix.DO) == "dikum"
    assert attach("uşǩur", OptionalPrefix.KO) == "kuşǩur"
    assert attach("vuşǩur", OptionalPrefix.KO) == "kovuşǩur"
    assert attach("(do)p̌it", OptionalPrefix.DO) == "dop̌it"
    # Preserve the dump's negative-particle order (row 568322 and neighbors).
    assert attach("mot giğur", OptionalPrefix.KO) == "komot giğur"


def test_explicit_prefix_does_not_enable_legacy_preverb_behavior():
    entry = entries_by_id()["verb-0123"]
    f = Features(
        Dialect.FA, Person.FIRST_SINGULAR, Person.SECOND_SINGULAR, optional_prefix=OptionalPrefix.DO
    )
    assert [x.spelling for x in conjugate(entry, f).forms] == ["doǩç̌arum"]
    assert validate(entry, replace(f, optional_preverb=True)).reason == "prefix_conflict"
    assert (
        validate(entry, replace(f, optional_prefix=OptionalPrefix.KO)).reason
        == "prefix_unavailable"
    )


def test_added_hopa_principal_part_and_equivalent_duplicate_mapping():
    entries = entries_by_id()
    assert any(
        p.form == "meǩorums" and Dialect.HO in p.dialects for p in entries["verb-0086"].variants
    )
    old = dict(
        verb_id="269",
        infinitive="oçindu",
        meaning_english="to sneeze",
        meaning_turkish="aksırmak",
        present_3sg="açinden",
    )
    target, basis = choose_entry(
        old, "IVD", "PZ", {("oçindu", "IVD", "PZ"): [entries["verb-0128"], entries["verb-0142"]]}
    )
    assert target.id == "verb-0142" and basis == "equivalent_duplicate"


def test_catalog_api_and_verifier_detect_extra_outputs(tmp_path):
    entry = entries_by_id()["verb-0123"]
    path = tmp_path / "catalog.sqlite"
    build_catalog(path, entries=(entry,))
    features = Features(
        Dialect.FA, Person.FIRST_SINGULAR, Person.SECOND_SINGULAR, optional_prefix=OptionalPrefix.DO
    )
    rejected = replace(features, object=Person.FIRST_SINGULAR)
    fixture = tmp_path / "evidence.gz"
    with gzip.open(fixture, "wt", encoding="utf-8") as file:
        header = dict(
            source_sha256=data()["source_sha256"],
            rows=2,
            requests=2,
            feature_fields=list(Features.__dataclass_fields__),
        )
        file.write(json.dumps(header) + "\n")
        file.write(
            json.dumps(
                [
                    entry.id,
                    list(asdict(features).values()),
                    [["doǩç̌arum", "Ergative"]],
                    ["example-positive"],
                ]
            )
            + "\n"
        )
        file.write(
            json.dumps([entry.id, list(asdict(rejected).values()), [], ["example-rejected"]]) + "\n"
        )
    assert verify(path, fixture)["mismatches"] == 0
    with TestClient(create_app(path)) as client:
        response = client.post(
            "/api/v1/conjugations",
            json=dict(
                entry_id=entry.id,
                dialects=["FA"],
                subject="1sg",
                object="2sg",
                optional_prefix="do",
            ),
        )
        assert response.status_code == 200
        assert response.json()["cells"][0]["forms"][0]["spelling"] == "doǩç̌arum"
        reverse = client.get("/api/v1/reverse", params={"q": "doǩç̌arum"}).json()
        assert any(
            v["features"]["optional_prefix"] == "do"
            for m in reverse["matches"]
            for v in m["variants"]
        )
    # A verifier must reject an extra generated spelling, even when the expected
    # spelling is also present. Presence-only comparisons conceal such errors.
    with sqlite3.connect(path) as db:
        rid = db.execute(
            "SELECT id FROM requests WHERE request_key=?", (request_id(entry.id, features),)
        ).fetchone()[0]
        db.execute(
            "INSERT INTO forms(request_id,data,exact_key,strict_key,broad_key) SELECT request_id,replace(data,'doǩç̌arum','wrong'), 'wrong','wrong','wrong' FROM forms WHERE request_id=?",
            (rid,),
        )
    result = verify(path, fixture)
    assert result["mismatches"] == 1
    assert result["examples"][0]["row_ids"] == ["example-positive"]
