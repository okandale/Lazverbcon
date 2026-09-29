import json
import sqlite3
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from laz_api.app import create_app
from laz_api.catalog import BuildFailed, Catalog, build_catalog
from laz_engine.engine import conjugate
from laz_engine.models import Dialect, EngineFailure, Features, Person, Tense
from laz_engine.orthography import broad_key, strict_key


def test_round_trip_catalog_and_reverse(tmp_path, verb):
    entry = verb("osinapu")
    path = tmp_path / "release.sqlite"
    manifest = build_catalog(path, "core", (entry,))
    assert manifest["status"] == "ready" and manifest["coverage"] == "partial"
    catalog = Catalog(path)
    features = Features(Dialect.AS, Person.FIRST_SINGULAR)
    result = catalog.lookup(entry.id, features)
    assert result["forms"][0]["spelling"] == conjugate(entry, features).forms[0].spelling
    reverse = catalog.reverse("visinapam")
    assert reverse["match_type"] == "exact"
    assert "visinapam" in catalog.suggestions("visina")
    assert len(catalog.suggestions("v", limit=2)) <= 2
    assert catalog.suggestions("") == []
    assert any(
        m["features"]["subject"] == "1sg" and m["entry"]["id"] == entry.id
        for m in reverse["matches"]
    )
    assert (
        catalog.lookup(entry.id, Features(Dialect.AS, Person.FIRST_SINGULAR, tense=Tense.PAST))[
            "status"
        ]
        == "not_generated"
    )
    with catalog.connect() as db, pytest.raises(sqlite3.OperationalError):
        db.execute("DELETE FROM forms")


def test_failed_build_does_not_publish_or_overwrite(tmp_path, verb):
    output = tmp_path / "failed.sqlite"
    with patch("laz_api.catalog.conjugate", side_effect=EngineFailure("broken rule")):
        with pytest.raises(BuildFailed):
            build_catalog(output, "core", (verb("osinapu"),))
    assert not output.exists()
    assert not list(tmp_path.glob("*.building"))
    assert json.loads(output.with_suffix(".report.json").read_text())["errors"]
    output.write_bytes(b"existing release")
    with pytest.raises(FileExistsError):
        build_catalog(output, "core", (verb("osinapu"),))
    assert output.read_bytes() == b"existing release"


def test_unicode_and_search_tiers():
    assert strict_key("k'oru") == strict_key("ǩoru")
    assert broad_key("koru") == broad_key("ǩoru")
    assert broad_key("ç̌") == "ç̌"
    assert strict_key("t\u0306axu") == strict_key("t'axu")


@pytest.mark.parametrize("use_database", [False, True])
def test_api_contract_in_both_modes(tmp_path, verb, use_database):
    entry = verb("osinapu")
    path = tmp_path / "api.sqlite"
    if use_database:
        build_catalog(path, "core", (entry,))
    with TestClient(create_app(path if use_database else None)) as client:
        data = client.get("/api/v1/verbs", params={"q": "osinapu"}).json()
        assert data["total"] == 1
        response = client.post(
            "/api/v1/conjugations", json={"entry_id": entry.id, "dialects": ["AS"], "object": None}
        )
        assert response.status_code == 200
        assert len(response.json()["cells"]) == 6
        assert response.json()["cells"][0]["forms"][0]["spelling"] == "visinapam"
        assert (
            client.post(
                "/api/v1/conjugations", json={"entry_id": entry.id, "tense": "typo"}
            ).status_code
            == 422
        )
        assert (
            client.post(
                "/api/v1/conjugations", json={"entry_id": entry.id, "dialects": []}
            ).status_code
            == 422
        )
        assert client.get("/api/v1/verbs/no-such-entry").status_code == 404
        reverse = client.get("/api/v1/reverse", params={"q": "visinapam"})
        assert reverse.status_code == (200 if use_database else 503)
        if use_database:
            match = reverse.json()["matches"][0]
            assert match["features"]["subject"]


def test_options_and_failures_are_explicit(verb):
    entry = verb("osinapu")
    with TestClient(create_app()) as client:
        response = client.post("/api/v1/conjugation-options", json={"entry_id": entry.id})
        assert response.status_code == 200
        options = response.json()["options"]["causative"]
        assert next(o for o in options if o["value"] == "simple")["enabled"] is False
        with patch("laz_api.app.conjugate", side_effect=EngineFailure("failure")):
            response = client.post(
                "/api/v1/conjugations", json={"entry_id": entry.id, "dialects": ["AS"]}
            )
        assert all(c["status"] == "error" and not c["forms"] for c in response.json()["cells"])


def test_missing_database_never_silently_falls_back(tmp_path):
    with pytest.raises(sqlite3.OperationalError):
        create_app(tmp_path / "missing.sqlite")


def test_potential_optative_and_aggregate_options(verb):
    with TestClient(create_app()) as client:
        entry = verb("osinapu")
        request = {"entry_id": entry.id, "dialects": ["AS"], "subject": "all", "object": "2sg"}
        options = client.post("/api/v1/conjugation-options", json=request).json()["options"]
        # A second-person representative would falsely reject this aggregate.
        assert next(o for o in options["subject"] if o["value"] == "all")["enabled"]
        request.update(object=None, mood="optative", derivation="potential")
        forms = client.post("/api/v1/conjugations", json=request).json()["cells"]
        assert len(forms) == 6 and all(c["status"] == "ok" for c in forms)
        request.update(derivation="passive")
        options = client.post("/api/v1/conjugation-options", json=request).json()["options"]
        optative = next(o for o in options["mood"] if o["value"] == "optative")
        assert optative["reason_code"] == "derivation_construction"
