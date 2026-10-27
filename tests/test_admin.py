"""Editorial safety tests: proposals, restoration and approved-only publication."""

import base64
import gzip
import hashlib
import json
import sqlite3
import time
import zipfile
from dataclasses import asdict
from itertools import islice, product
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from laz_admin.app import create_app
from laz_admin.archive import unpack
from laz_admin.publish import export_release, publish, snapshot
from laz_admin.store import Store, features, parse_import
from laz_api.catalog import Catalog
from laz_engine.engine import conjugate
from laz_engine.models import Derivation, Dialect, Features, Person, Tense


@pytest.fixture
def project(tmp_path, verb):
    store = Store(tmp_path / "project")
    store.save_entry(asdict(verb("doguru")), "Author", "Existing verb")
    return store


def item(store, spelling="author form", **fields):
    return {
        "entry_id": store.entries()[0]["id"],
        "features": features({"dialect": "AS", "subject": "1sg", **fields}),
        "value": {
            "status": "ok",
            "forms": [
                {
                    "spelling": spelling,
                    "frame": "Nominative",
                    "subject_pronoun": "author pronoun",
                    "object_pronoun": "",
                    "rule": "editorial",
                }
            ],
        },
    }


def approve(store, value):
    result = store.propose([value], "Author", "Linguistic correction")
    ids = [r["id"] for r in store.proposals(result["batch"])["proposals"]]
    store.review(ids, True, "Reviewer")
    return store.history()[0]["id"]


def test_project_creation_closes_database_connections(tmp_path, monkeypatch):
    connections = []
    connect = sqlite3.connect

    class TrackedConnection(sqlite3.Connection):
        closed = False

        def close(self):
            self.closed = True
            super().close()

    def tracked_connect(*args, **kwargs):
        db = connect(*args, **kwargs, factory=TrackedConnection)
        connections.append(db)
        return db

    monkeypatch.setattr(sqlite3, "connect", tracked_connect)
    Store(tmp_path / "project")
    assert connections and all(db.closed for db in connections)


def test_draft_approval_removal_and_undo(project):
    value = item(project)
    project.propose([value], "Author", "First form")
    assert project.status()["records"] == 0
    project.review([project.proposals()["proposals"][0]["id"]], True, "Reviewer")
    assert (
        project.records(value["entry_id"])["records"][0]["value"]["forms"][0]["spelling"]
        == "author form"
    )
    changed = approve(project, item(project, "corrected form"))
    project.undo(changed, "Author")
    assert (
        project.records(value["entry_id"])["records"][0]["value"]["forms"][0]["spelling"]
        == "author form"
    )
    removed = approve(project, {**value, "value": None})
    assert project.status()["records"] == 0
    project.undo(removed, "Author")
    assert project.status()["records"] == 1
    assert project.history()[0]["reason"].startswith("Undo")


def test_conflicting_approvals_are_atomic_and_can_be_rejected(project):
    a, b = item(project, "one"), item(project, "two")
    project.propose([a, b], "Author", "Conflicting alternatives")
    proposals = project.proposals()["proposals"]
    with pytest.raises(ValueError, match="Conflicting"):
        project.review([p["id"] for p in proposals], True, "Reviewer")
    assert project.status()["records"] == 0
    project.review([proposals[0]["id"]], True, "Reviewer")
    stale = project.proposals()["proposals"][0]
    assert stale["conflict"]
    project.review([stale["id"]], False, "Reviewer")
    assert project.status()["pending"] == 0


def test_entry_metadata_change_invalidates_open_forms_and_proposals(project):
    approve(project, item(project))
    row = project.records(project.entries()[0]["id"])["records"][0]
    with project.db() as db:
        expected = project.before_hash(db, row["entry_id"], row["key"])
    project.propose([item(project, "pending")], "Author", "Pending")
    original = project.entries()[0]
    project.save_entry({**original, "english": "new meaning"}, "Author", "Meaning", original)
    assert project.proposals()["proposals"][0]["conflict"]
    with pytest.raises(ValueError, match="changed since"):
        project.propose(
            [{**item(project, "stale edit"), "expected_hash": expected}], "Author", "Edit"
        )
    with pytest.raises(ValueError, match="changed since"):
        project.save_entry(original, "Author", "", original)


def test_generation_preserves_corrections_and_skips_provenance_only_changes(project):
    value = item(project)
    approve(project, value)
    value["value"]["source"] = "different source"
    value["value"]["forms"][0]["rule"] = "generated"
    assert project.propose([value], "Author", "")["proposals"] == 0
    result = project.generate(value["entry_id"], "Author", profile="core")
    assert result["proposals"] > 0
    assert project.status()["records"] == 1
    assert (
        project.records(value["entry_id"])["records"][0]["value"]["forms"][0]["spelling"]
        == "author form"
    )
    repeated = project.generate(value["entry_id"], "Author", profile="core")
    assert repeated["proposals"] == repeated["superseded"] == 1
    assert project.status()["pending"] == 1
    pending = project.proposals()["proposals"]
    project.review([p["id"] for p in pending], True, "Author")
    matching = project.generate(value["entry_id"], "Author")
    assert matching["proposals"] == 0 and matching["unchanged"] == 1


def test_new_verb_defaults_to_standard_without_optional_variants(project):
    result = project.generate(project.entries()[0]["id"], "Author")
    assert result["scope"] == "standard" and result["proposals"] > 0
    with project.db() as db:
        rows = [
            json.loads(r[0])
            for r in db.execute("SELECT features FROM proposals WHERE state='pending'")
        ]
    assert len(rows) == result["proposals"]
    assert all(
        not f["optional_preverb"]
        and f["optional_prefix"] == "none"
        and not f["applicative"]
        and f["causative"] == "none"
        and f["derivation"] == "none"
        for f in rows
    )
    expanded = project.generate(project.entries()[0]["id"], "Author", scope="expanded")
    assert expanded["proposals"] > result["proposals"]
    assert expanded["superseded"] == result["proposals"]
    with project.db() as db:
        assert not db.execute(
            "SELECT 1 FROM proposals WHERE state='pending' AND "
            "(json_extract(features,'$.optional_preverb')=1 OR json_extract(features,'$.optional_prefix')!='none')"
        ).fetchone()


def test_recorded_generation_does_not_expand_optional_preverbs_or_rejected_combinations(project):
    # This local verb ID has no engine prefix metadata; approved data is the evidence.
    original = project.entries()[0]
    local = project.save_entry({**original, "id": "local-verb"}, "Author", "Local verb")
    base = {**item(project), "entry_id": local["id"]}
    optional = {**item(project, dialect="FA", optional_prefix="ko"), "entry_id": local["id"]}
    rejected = {
        **item(project, subject="2sg"),
        "entry_id": local["id"],
        "value": {"status": "unsupported", "forms": []},
    }
    for value in (base, optional, rejected):
        approve(project, value)
    result = project.generate(local["id"], "Author")
    assert result["scope"] == "recorded" and result["requests"] == 2
    proposed = project.proposals(result["batch"])["proposals"]
    assert {json.dumps(p["features"], sort_keys=True) for p in proposed} == {
        json.dumps(v["features"], sort_keys=True) for v in (base, optional)
    }
    prefixed = next(p for p in proposed if p["features"]["optional_prefix"] == "ko")
    assert prefixed["value"]["forms"][0]["spelling"].startswith("ko")
    assert project.records(local["id"])["unavailable"] == 1


def test_regeneration_replaces_old_generated_drafts_and_keeps_manual_work(project):
    legacy = item(project, optional_preverb=True)
    legacy["value"]["source"] = "Generated proposal"
    project.propose([legacy], "Author", "Old generation")
    old = project.proposals()["proposals"][0]
    with pytest.raises(ValueError, match="Regenerate"):
        project.review([old["id"]], True, "Author")
    manual = item(project, "Manual draft")
    project.propose([manual], "Author", "Keep my draft")
    result = project.generate(project.entries()[0]["id"], "Author", profile="core")
    assert result["superseded"] == 1
    pending = project.proposals()["proposals"]
    assert any(p["reason"] == "Keep my draft" for p in pending)
    assert not any(p["features"]["optional_preverb"] for p in pending)
    with project.db() as db:
        assert (
            db.execute("SELECT state FROM proposals WHERE id=?", (old["id"],)).fetchone()[0]
            == "superseded"
        )


def test_unrecorded_generated_ko_do_drafts_cannot_be_approved(project):
    optional = item(project, optional_prefix="do")
    optional["value"]["source"] = "Generated proposal"
    project.propose([optional], "Author", "Old extrapolated prefix")
    with pytest.raises(ValueError, match="Regenerate"):
        project.review([], True, "Author", selection_hash=project.proposals()["selection_hash"])
    assert project.status()["records"] == 0


def test_bulk_review_spans_pages_but_respects_verb_and_batch_filters(project):
    values = [
        item(project, dialect=d, subject=s, tense=t, object=o)
        for d, s, t, o in islice(
            product(
                ("AS", "PZ", "FA", "HO"),
                ("1sg", "2sg", "3sg", "1pl", "2pl", "3pl"),
                ("present", "past", "future", "past_progressive", "present_perfect"),
                (None, "3sg"),
            ),
            150,
        )
    ]
    project.propose(values, "Author", "Large import", batch="large")
    project.propose([item(project, "Other batch")], "Author", "Leave pending", batch="other")
    selected = project.proposals("large", entry_id=project.entries()[0]["id"])
    assert selected["total"] == 150 and len(selected["proposals"]) == 100
    assert (
        project.review(
            [], True, "Reviewer", batch="large", selection_hash=selected["selection_hash"]
        )["reviewed"]
        == 150
    )
    assert project.status()["records"] == 150
    assert project.status()["pending"] == 1
    with project.db() as db:
        assert (
            db.execute(
                "SELECT count(*) FROM history WHERE entity='record' AND actor='Reviewer'"
            ).fetchone()[0]
            == 150
        )


def test_bulk_review_refuses_a_changed_selection_and_rolls_back_conflicts(project):
    project.propose([item(project)], "Author", "Initial")
    selection = project.proposals()["selection_hash"]
    project.propose([item(project, "Other", subject="2sg")], "Author", "Added later")
    with pytest.raises(ValueError, match="Pending proposals changed"):
        project.review([], True, "Reviewer", selection_hash=selection)
    project.propose([item(project, "Conflicting")], "Author", "Alternative")
    with pytest.raises(ValueError, match="Conflicting"):
        project.review([], True, "Reviewer", selection_hash=project.proposals()["selection_hash"])
    assert project.status()["records"] == 0 and project.status()["pending"] == 3
    rejected = project.review(
        [], False, "Reviewer", selection_hash=project.proposals()["selection_hash"]
    )
    assert rejected["reviewed"] == 3 and project.status()["pending"] == 0


def test_record_counts_distinguish_spellings_requests_and_unavailable_rows(project):
    approve(project, item(project, "same"))
    approve(project, item(project, "same", subject="2sg"))
    approve(
        project, {**item(project, subject="3sg"), "value": {"status": "unsupported", "forms": []}}
    )
    rows = project.records(project.entries()[0]["id"])
    assert (rows["total"], rows["available"], rows["unique_spellings"], rows["unavailable"]) == (
        3,
        2,
        1,
        1,
    )
    assert project.records(project.entries()[0]["id"], filters={"subject": "2sg"})["total"] == 1


def test_generation_api_can_run_repeatedly_and_bulk_review_its_batch(project):
    with TestClient(create_app(project, "secret"), base_url="http://127.0.0.1") as client:
        headers = {"X-Laz-Session": "secret"}
        results = []
        for _ in range(2):
            response = client.post(
                "/api/generate",
                headers=headers,
                json={"entry_id": project.entries()[0]["id"], "actor": "Author", "profile": "core"},
            )
            assert response.status_code == 200
            started = response.json()
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                job = client.get("/api/job", headers=headers).json()
                if job["state"] != "running":
                    break
                time.sleep(0.01)
            assert job["state"] == "complete", job
            assert job["id"] == started["id"]
            results.append(job)
        assert results[0]["id"] != results[1]["id"]
        assert results[1]["result"]["superseded"] == results[0]["result"]["proposals"]
        batch = results[1]["result"]["batch"]
        pending = client.get("/api/proposals", headers=headers, params={"batch": batch}).json()
        response = client.post(
            "/api/review",
            headers=headers,
            json={
                "approve": True,
                "actor": "Author",
                "batch": batch,
                "selection_hash": pending["selection_hash"],
            },
        )
        assert response.status_code == 200 and response.json()["reviewed"] == pending["total"]


def test_saved_generation_exclusions_preserve_manual_forms_and_log_undo(project):
    manual = item(project, "Manually entered present")
    approve(project, manual)
    project.propose([item(project, "Other draft")], "Author", "Before options changed")
    original = project.entries()[0]
    defaults = project.generation_options(original["id"])
    choices = {
        "preverb_lookalike": True,
        "excluded_combinations": [{"tense": "present", "mood": "indicative"}],
    }
    project.save_entry(
        original,
        "Author",
        "Present is manual",
        original,
        options=choices,
        expected_options=defaults,
    )
    event = project.history()[0]
    assert event["entity"] == "entry_options"
    assert project.generation_options(original["id"]) == choices
    assert project.proposals()["proposals"][0]["conflict"]
    result = project.generate(original["id"], "Author")
    assert result["requests"] == 0 and result["excluded"] == 1
    assert (
        project.records(original["id"])["records"][0]["value"]["forms"][0]["spelling"]
        == "Manually entered present"
    )
    project.undo(event["id"], "Author")
    assert project.generation_options(original["id"]) == defaults
    assert not project.proposals()["proposals"][0]["conflict"]


def test_exclusion_rows_match_all_fields_and_cover_multiple_constructions(project):
    entry = project.entries()[0]
    before = project.generate(entry["id"], "Author")
    choices = {
        "excluded_combinations": [
            {"tense": "present", "mood": "indicative", "object": None},
            {"mood": "optative"},
        ]
    }
    project.save_entry(entry, "Author", "Manual exceptions", entry, options=choices)
    result = project.generate(entry["id"], "Author")
    assert result["excluded"] > 0 and result["requests"] == before["requests"] - result["excluded"]
    with project.db() as db:
        fs = [
            json.loads(r[0])
            for r in db.execute("SELECT features FROM proposals WHERE state='pending'")
        ]
    assert all(f["mood"] != "optative" for f in fs)
    assert all(
        not (f["tense"] == "present" and f["mood"] == "indicative" and f["object"] is None)
        for f in fs
    )
    assert any(
        f["tense"] == "present" and f["mood"] == "indicative" and f["object"] == "3sg" for f in fs
    )


def test_generation_options_validate_back_up_and_stay_private(project):
    entry = project.entries()[0]
    with pytest.raises(ValueError, match="at least one"):
        project.save_entry(entry, "Author", "", entry, options={"excluded_combinations": [{}]})
    with pytest.raises(ValueError):
        project.save_entry(
            entry, "Author", "", entry, options={"excluded_combinations": [{"tense": "invented"}]}
        )
    assert project.generation_options(entry["id"])["excluded_combinations"] == []
    choices = {"preverb_lookalike": False, "excluded_combinations": [{"tense": "future"}]}
    project.save_entry(entry, "Author", "Manual future", entry, options=choices)
    with pytest.raises(ValueError, match="options changed"):
        project.save_entry(entry, "Author", "Stale", entry, options={})
    backup = Path(project.backup())
    project.save_entry(entry, "Author", "Reset", entry, options={}, expected_options=choices)
    project.restore(backup, "Author")
    assert project.generation_options(entry["id"]) == choices
    approve(project, item(project))
    output = project.directory / "public.sqlite"
    snapshot(project, output)
    with Catalog(output).connect() as db:
        assert "excluded_combinations" not in db.execute("SELECT data FROM entries").fetchone()[0]


def test_entry_options_api_and_per_base_dialects(project):
    entry = project.entries()[0]
    options = {
        "preverb_lookalike": True,
        "excluded_combinations": [{"tense": "present", "mood": "indicative"}],
    }
    edited = {
        **entry,
        "variants": [
            {"form": "first", "dialects": ["FA", "PZ"]},
            {"form": "second", "dialects": ["HO"]},
        ],
    }
    with TestClient(create_app(project, "secret"), base_url="http://127.0.0.1") as client:
        headers = {"X-Laz-Session": "secret"}
        response = client.post(
            "/api/entry",
            headers=headers,
            json={
                "entry": edited,
                "expected": entry,
                "actor": "Author",
                "generation_options": options,
                "expected_options": {},
            },
        )
        assert response.status_code == 200
        assert (
            client.get("/api/generation-options/" + entry["id"], headers=headers).json() == options
        )
        assert response.json()["variants"] == edited["variants"]


@pytest.mark.parametrize("tense", list(Tense))
def test_preverb_lookalike_skips_detection_without_changing_default_rules(verb, tense):
    entry = verb("doguru")
    f = Features(Dialect.FA, Person.FIRST_SINGULAR, Person.THIRD_SINGULAR, tense=tense)
    if tense == Tense.PRESENT_PERFECT:
        f = Features(Dialect.FA, Person.FIRST_SINGULAR, tense=tense)
    normal = conjugate(entry, f)
    lookalike = conjugate(entry, f, preverb_lookalike=True)
    assert normal.status == lookalike.status == "ok"
    assert all(form.spelling for form in lookalike.forms)
    assert lookalike != normal
    assert conjugate(entry, f) == normal


@pytest.mark.parametrize(
    "infinitive,category", [("dodginu", "IVD"), ("dobadu", "TVM"), ("doguru", "TVE")]
)
@pytest.mark.parametrize("tense", list(Tense)[:-1])
def test_preverb_lookalike_works_in_all_base_classes(verb, infinitive, category, tense):
    entry = verb(infinitive, category)
    f = Features(entry.dialects[0], Person.FIRST_SINGULAR, tense=tense)
    result = conjugate(entry, f, preverb_lookalike=True)
    assert result.status == "ok" and all(form.spelling for form in result.forms)


@pytest.mark.parametrize("derivation", [Derivation.PASSIVE, Derivation.POTENTIAL])
@pytest.mark.parametrize("tense", list(Tense)[:-1])
def test_preverb_lookalike_works_in_derived_constructions(verb, derivation, tense):
    entry = verb("doguru")
    f = Features(Dialect.FA, Person.FIRST_SINGULAR, tense=tense, derivation=derivation)
    assert conjugate(entry, f, preverb_lookalike=True).status == "ok"


def test_cancelled_generation_and_export_leave_no_partial_output(project):
    with pytest.raises(ValueError, match="Cancelled"):
        project.generate(project.entries()[0]["id"], "Author", cancelled=lambda: True)
    assert project.status()["pending"] == 0
    approve(project, item(project))
    with pytest.raises(ValueError, match="cancelled"):
        export_release(project, "Author", cancelled=lambda: True)
    assert not list((project.directory / "exports").iterdir())


def test_import_is_atomic_and_groups_alternatives(project):
    csv = (
        "entry_id,dialect,subject,applicative,spelling,frame\n"
        f"{project.entries()[0]['id']},AS,1sg,false,first,Nominative\n"
        f"{project.entries()[0]['id']},AS,1sg,false,second,Nominative\n"
    )
    rows = parse_import(csv, "csv")
    assert len(rows) == 1 and len(rows[0]["value"]["forms"]) == 2
    assert rows[0]["features"]["applicative"] is False
    with pytest.raises(ValueError, match="Unknown entry"):
        project.propose([*rows, {**rows[0], "entry_id": "missing"}], "Author", "Import")
    assert project.status()["pending"] == 0
    with pytest.raises(ValueError, match="Combine alternatives"):
        parse_import(json.dumps([rows[0], rows[0]]), "json")
    with pytest.raises(ValueError, match="true or false"):
        parse_import(csv.replace("false", "maybe"), "csv")


def test_feature_filters_distinguish_null_objects_and_false_markers(project):
    approve(project, item(project, "plain"))
    approve(project, item(project, "marked", object="3sg", applicative=True))
    rows = project.records(
        project.entries()[0]["id"], filters={"object": None, "applicative": False}
    )
    assert rows["total"] == 1 and rows["records"][0]["value"]["forms"][0]["spelling"] == "plain"
    with pytest.raises(ValueError, match="Unknown grammatical"):
        project.records(project.entries()[0]["id"], filters={"bad": 1})


def test_dump_baseline_files_match_recorded_provenance():
    root = Path(__file__).parents[1]
    folder = root / "apps/admin/src/laz_admin/data"
    provenance = json.loads((folder / "baseline.json").read_text(encoding="utf-8"))
    assert (
        hashlib.sha256((folder / "pronouns.json").read_bytes()).hexdigest()
        == provenance["pronouns_sha256"]
    )
    assert (
        hashlib.sha256(
            (root / "tests/fixtures/maintainer-release.jsonl.gz").read_bytes()
        ).hexdigest()
        == provenance["fixture_sha256"]
    )


def test_backup_restore_retains_history_and_refuses_new_schema(project, tmp_path):
    approve(project, item(project, "original"))
    project.settings({"backup_directory": str(tmp_path / "external")})
    saved = Path(project.backup())
    assert (tmp_path / "external" / project.status()["project"] / saved.name).is_file()
    approve(project, item(project, "later"))
    assert project.restore(saved, "Author")["previous_backup"]
    assert (
        project.records(project.entries()[0]["id"])["records"][0]["value"]["forms"][0]["spelling"]
        == "original"
    )
    assert project.history()[0]["entity"] == "restore"
    with sqlite3.connect(saved) as db:
        db.execute("UPDATE meta SET value='999' WHERE key='schema'")
    before = project.path.read_bytes()
    with pytest.raises(ValueError, match="different app version"):
        project.restore(saved, "Author")
    assert project.path.read_bytes() == before


def test_daily_retention_does_not_remove_manual_backups(project):
    manual = Path(project.backup())
    folder = manual.parent
    for day in range(1, 20):
        (folder / f"daily-2020-01-{day:02}.sqlite").write_bytes(b"old")
    daily = project.backup(daily=True)
    assert len(list(folder.glob("daily-*.sqlite"))) == 14
    assert manual.exists() and project.backup(daily=True) == daily


def test_restore_refuses_incomplete_metadata_without_replacing_project(project):
    saved = Path(project.backup())
    with sqlite3.connect(saved) as db:
        db.execute("DELETE FROM meta WHERE key='project'")
    before = project.path.read_bytes()
    with pytest.raises(ValueError, match="incomplete"):
        project.restore(saved, "Author")
    assert project.path.read_bytes() == before


def test_unavailable_external_backup_does_not_prevent_fixing_settings(project, tmp_path):
    invalid = tmp_path / "not-a-directory"
    invalid.write_text("file")
    project.settings({"backup_directory": str(invalid)})
    with TestClient(create_app(project, "secret"), base_url="http://127.0.0.1") as client:
        headers = {"X-Laz-Session": "secret"}
        assert (
            client.post(
                "/api/proposal", headers=headers, json={"items": [item(project)], "actor": "Author"}
            ).status_code
            == 409
        )
        assert (
            client.post("/api/settings", headers=headers, json={"backup_directory": ""}).status_code
            == 200
        )
        assert (
            client.post(
                "/api/proposal", headers=headers, json={"items": [item(project)], "actor": "Author"}
            ).status_code
            == 200
        )


def test_seed_uses_dump_pronouns_and_rolls_back_invalid_fixture(tmp_path):
    source = Path(__file__).parent / "fixtures/maintainer-release.jsonl.gz"
    with gzip.open(source, "rt") as stream:
        header = json.loads(next(stream))
        row = next(json.loads(line) for line in stream if json.loads(line)[2])
    header.update(requests=1, rows=len(row[3]))
    fixture = tmp_path / "baseline.gz"
    with gzip.open(fixture, "wt") as stream:
        stream.write(json.dumps(header) + "\n" + json.dumps(row) + "\n")
    store = Store(tmp_path / "seed")
    assert store.seed(fixture, "Author")["requests"] == 1
    record = store.records(row[0])["records"][0]
    f = record["features"]
    pronouns = json.loads(
        (Path(__file__).parents[1] / "apps/admin/src/laz_admin/data/pronouns.json").read_text(
            encoding="utf-8"
        )
    )
    form = record["value"]["forms"][0]
    assert (
        form["subject_pronoun"]
        == pronouns[f"{f['dialect']}|S{f['subject'].upper()}|{form['frame']}"]
    )
    with pytest.raises(ValueError, match="empty project"):
        store.seed(fixture, "Author")
    header["requests"] = 2
    with gzip.open(fixture, "wt") as stream:
        stream.write(json.dumps(header) + "\n" + json.dumps(row) + "\n")
    empty = Store(tmp_path / "failed")
    with pytest.raises(ValueError, match="incomplete"):
        empty.seed(fixture, "Author")
    assert empty.status()["entries"] == 0


def test_export_only_approved_including_new_entries_and_rule_exceptions(project, tmp_path):
    original = project.entries()[0]
    new = project.save_entry(
        {**original, "id": "new-verb", "infinitive": "New", "verb_class": "TVM"}, "Author", ""
    )
    # A nominative verb with an object is normally rejected by engine validation.
    approved = item(project, "approved exception", object="2sg", optional_prefix="ko")
    approved["entry_id"] = new["id"]
    approve(project, approved)
    approve(
        project,
        {
            **approved,
            "features": {**approved["features"], "subject": "2sg"},
            "value": {"status": "unsupported", "forms": [], "reason": "PRIVATE APPROVED REASON"},
        },
    )
    project.propose(
        [{**approved, "value": item(project, "private draft")["value"]}],
        "PRIVATE AUTHOR",
        "PRIVATE REASON",
    )
    manifest = snapshot(project, tmp_path / "snapshot.sqlite")
    assert manifest["form_count"] == 1
    with Catalog(tmp_path / "snapshot.sqlite").connect() as db:
        assert db.execute("SELECT count(*) FROM forms").fetchone()[0] == 1
    info = export_release(project, "Author")
    destination = tmp_path / "unpack"
    destination.mkdir()
    m = unpack(project.directory / "exports" / info["filename"], destination)
    assert m["catalog"]["editorial"]
    assert (
        json.loads((destination / "validation.json").read_text(encoding="utf-8"))["mode"]
        == "approved"
    )
    text = "".join(p.read_text(encoding="utf-8") for p in destination.rglob("*.json"))
    assert "approved exception" in text
    assert (
        "private draft" not in text
        and "PRIVATE AUTHOR" not in text
        and "PRIVATE REASON" not in text
    )
    assert "PRIVATE APPROVED REASON" not in text


class FakeGitHub:
    def __init__(self, pointer=None, fail=False):
        self.pointer, self.fail, self.calls = pointer, fail, []

    def request(self, method, path, data=None, binary=False):
        self.calls.append((method, path, data))
        if method == "GET":
            if "/contents/" not in path:
                return {"private": False}
            return (
                {
                    "content": base64.b64encode(json.dumps(self.pointer).encode()).decode(),
                    "sha": "existing-sha",
                }
                if self.pointer
                else None
            )
        if method == "POST" and not binary:
            return {
                "id": 1,
                "upload_url": "https://uploads.github.com/repos/owner/repo/releases/1/assets{?name}",
            }
        if binary:
            return {
                "id": 10,
                "browser_download_url": "https://github.com/owner/repo/releases/download/untagged-draft/catalog.zip",
            }
        if method == "PATCH":
            return {
                "assets": [
                    {
                        "id": 10,
                        "state": "uploaded",
                        "browser_download_url": "https://github.com/owner/repo/releases/download/test/catalog.zip",
                    }
                ]
            }
        if method == "PUT":
            if self.fail:
                raise ValueError("Concurrent pointer edit")
            self.pointer = json.loads(base64.b64decode(data["content"]))
        return {}


def test_publish_pins_public_archive_and_protects_against_stale_restore(project):
    approve(project, item(project))
    info = export_release(project, "Author")
    client = FakeGitHub()
    args = (
        project,
        info["filename"],
        "Author",
        "never-save-token",
        "owner/repo",
        "codex/static-export",
    )
    publish(*args, github=client)
    assert json.loads(project.status()["remote_base"]) == info["release"]
    assert client.pointer["sha256"] == info["sha256"]
    assert (
        client.pointer["url"] == "https://github.com/owner/repo/releases/download/test/catalog.zip"
    )
    assert set(client.pointer) == {"release", "project", "revision", "sha256", "url"}
    assert "never-save-token" not in str(project.history()) + str(project.settings())
    with project.db(True) as db:
        project.set_meta(db, "remote_base", "null")
    publish(*args, github=client)  # interrupted local bookkeeping can recover
    assert json.loads(project.status()["remote_base"]) == info["release"]
    client.pointer["release"] = "newer-release"
    mutations = len([c for c in client.calls if c[0] != "GET"])
    with pytest.raises(ValueError, match="different published revision"):
        publish(*args, github=client)
    assert len([c for c in client.calls if c[0] != "GET"]) == mutations


def test_failed_github_commit_does_not_advance_local_base(project):
    approve(project, item(project))
    info = export_release(project, "Author")
    client = FakeGitHub(fail=True)
    with pytest.raises(ValueError, match="Concurrent"):
        publish(project, info["filename"], "Author", "token", "owner/repo", "main", github=client)
    assert json.loads(project.status()["remote_base"]) is None


def test_missing_published_asset_does_not_commit_a_pointer(project):
    class MissingAsset(FakeGitHub):
        def request(self, method, path, data=None, binary=False):
            response = super().request(method, path, data, binary)
            return {"assets": []} if method == "PATCH" else response

    approve(project, item(project))
    info = export_release(project, "Author")
    client = MissingAsset()
    with pytest.raises(ValueError, match="Published archive is unavailable"):
        publish(project, info["filename"], "Author", "token", "owner/repo", "main", github=client)
    assert not any(method == "PUT" for method, _, _ in client.calls)
    assert json.loads(project.status()["remote_base"]) is None


def test_editor_rejects_foreign_origins_hosts_and_missing_tokens(project):
    with TestClient(create_app(project, "secret"), base_url="http://127.0.0.1") as client:
        assert client.get("/").status_code == 200
        assert client.get("/api/status").status_code == 403
        headers = {"X-Laz-Session": "secret"}
        assert client.get("/api/status", headers=headers).status_code == 200
        assert (
            client.get(
                "/api/status", headers={**headers, "Origin": "https://other.test"}
            ).status_code
            == 403
        )
        assert (
            client.get("/api/status", headers={**headers, "Host": "other.test"}).status_code == 403
        )
        assert (
            client.post(
                "/api/proposal", headers=headers, json={"items": [item(project)], "actor": "Author"}
            ).status_code
            == 200
        )
        assert client.get("/api/download/exports/absent.zip", headers=headers).status_code == 404
        assert (
            client.post(
                "/api/restore", headers={**headers, "X-Laz-Actor": "Author"}, content=b"invalid"
            ).status_code
            == 400
        )
        assert project.status()["pending"] == 1


@pytest.mark.parametrize(
    "name", ["../outside.json", "/absolute.json", "data\\outside.json", "C:bad.json"]
)
def test_archive_refuses_path_traversal(tmp_path, name):
    archive = tmp_path / "bad.zip"
    member = zipfile.ZipInfo(name)
    # Preserve a malformed raw name: ZipInfo normalizes backslashes on Windows.
    member.filename = name
    with zipfile.ZipFile(archive, "w") as dest:
        dest.writestr(member, "{}")
    with pytest.raises(ValueError, match="Unsafe"):
        unpack(archive, tmp_path / "unpack")


def test_archive_refuses_tampering(project, tmp_path):
    approve(project, item(project))
    info = export_release(project, "Author")
    archive = project.directory / "exports" / info["filename"]
    with zipfile.ZipFile(archive) as source, zipfile.ZipFile(tmp_path / "bad.zip", "w") as dest:
        for name in source.namelist():
            dest.writestr(name, b"[]" if name == "entries.json" else source.read(name))
    with pytest.raises(ValueError, match="integrity"):
        unpack(tmp_path / "bad.zip", tmp_path / "unpack")
