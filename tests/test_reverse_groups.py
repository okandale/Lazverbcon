"""Reverse cards group equivalent spellings without losing valid requests."""

from dataclasses import replace

import pytest
from fastapi.testclient import TestClient
from laz_api.app import create_app
from laz_api.catalog import Catalog, build_catalog
from laz_engine.lexicon import load_entries
from laz_engine.models import Features
from pydantic import TypeAdapter


def test_identical_grammar_keeps_separate_lexical_entries(tmp_path, verb):
    entry = verb("osinapu")
    homograph = replace(entry, id="test-homograph", english="another meaning")
    path = tmp_path / "homographs.sqlite"
    build_catalog(path, "core", (entry, homograph))
    result = Catalog(path).reverse("visinapam")
    assert result["total"] == 2
    assert {m["entry"]["id"] for m in result["matches"]} == {entry.id, homograph.id}


@pytest.fixture(scope="module")
def catalog(tmp_path_factory):
    path = tmp_path_factory.mktemp("reverse") / "catalog.sqlite"
    entries = tuple(e for e in load_entries() if e.infinitive in ("dobalu", "osinapu"))
    build_catalog(path, "full", entries)
    return Catalog(path)


def test_doviba_groups_before_counting_and_pagination(catalog):
    result = catalog.reverse("doviba")
    assert result["total"] == len(result["matches"]) == 3
    assert sum(len(m["variants"]) for m in result["matches"]) == 18
    assert {m["entry"]["english"] for m in result["matches"]} == {
        "to pour",
        "to flow, to leak",
    }
    for offset, expected in enumerate(result["matches"]):
        page = catalog.reverse("doviba", limit=1, offset=offset)
        assert page["total"] == 3
        assert page["matches"] == [expected]
        assert len(expected["variants"]) == 6
        assert {v["features"]["dialect"] for v in expected["variants"]} == {"AS", "PZ", "HO"}
        assert expected["features"]["optional_preverb"] is False
    # An empty page of exact matches must not fall through to a looser spelling tier.
    assert catalog.reverse("doviba", offset=3) == {
        "match_type": "exact",
        "total": 3,
        "matches": [],
    }


def test_every_grouped_variant_round_trips_to_forward_lookup(catalog):
    adapter = TypeAdapter(Features)
    for match in catalog.reverse("doviba")["matches"]:
        for variant in match["variants"]:
            features = adapter.validate_python(variant["features"])
            result = catalog.lookup(match["entry"]["id"], features)
            assert variant["form"] in result["forms"]


def test_object_number_and_markers_remain_distinct(catalog):
    matches = catalog.reverse("visinapam", limit=100)["matches"]
    ordinary = [
        m
        for m in matches
        if not m["features"]["applicative"] and m["features"]["causative"] == "none"
    ]
    assert {m["features"]["object"] for m in ordinary} >= {None, "3sg", "3pl"}
    pouring = [
        m for m in catalog.reverse("doviba")["matches"] if m["entry"]["english"] == "to pour"
    ]
    assert {m["features"]["causative"] for m in pouring} == {"none", "simple"}
    for match in matches:
        assert {v["features"]["object"] for v in match["variants"]} == {
            match["features"]["object"],
        }


def test_grouped_api_contract_and_missing_spelling(catalog):
    with TestClient(create_app(catalog.path)) as client:
        response = client.get("/api/v1/reverse", params={"q": "doviba", "limit": 1})
        assert response.status_code == 200
        assert response.json()["total"] == 3
        assert len(response.json()["matches"][0]["variants"]) == 6
        assert client.get("/api/v1/reverse", params={"q": "zzzzzzzz"}).json() == {
            "match_type": "none",
            "total": 0,
            "matches": [],
        }
