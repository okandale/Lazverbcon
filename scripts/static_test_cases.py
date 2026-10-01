"""Generate independent API expectations for the browser's static query tests."""

import argparse
import json
from pathlib import Path

from fastapi.testclient import TestClient
from laz_api.app import create_app
from laz_api.catalog import Catalog, build_catalog
from laz_api.static_export import export_catalog
from laz_engine.lexicon import load_entries


def create(output, database=None):
    output.mkdir(parents=True, exist_ok=True)
    if database is None:
        database = output / "catalog.sqlite"
        wanted = {"doguru", "dobalu", "guri mentxu", "coxons", "gexvamu", "otebriǩu"}
        entries = tuple(e for e in load_entries() if e.infinitive in wanted)
        build_catalog(database, entries=entries)
        export_catalog(database, output / "data", allow_partial=True, shard_bytes=2048)
    catalog = Catalog(database)
    client = TestClient(create_app(database))
    entries, _ = catalog.entries(limit=1000)
    cases = []

    def add(method, path, body=None):
        response = client.request(method, path, json=body)
        response.raise_for_status()
        cases.append({"method": method, "path": path, "body": body, "expected": response.json()})

    for query in (
        "",
        "learn",
        "DO",
        "pour",
        "öğren",
        "xyzabc",
        "  DOBALU  ",
        "ß",
        "İ",
        "\u001cdo\u001f",
    ):
        from urllib.parse import urlencode

        add("GET", "/api/v1/verbs?" + urlencode({"q": query, "limit": 3, "offset": 1}))
    for entry in entries:
        add("GET", f"/api/v1/verbs/{entry['id']}")
        default = {"entry_id": entry["id"], "dialects": ["AS", "PZ", "FA", "HO"], "subject": "all"}
        variations = [
            {},
            {"mood": "optative"},
            {"tense": "present_perfect"},
            {"object": "all", "applicative": True},
            {"mood": "imperative", "tense": "past"},
            {"derivation": "passive", "causative": "double", "tense": "future"},
            {"derivation": "potential", "mood": "optative"},
            {"optional_prefix": "ko"},
            {"optional_prefix": "do"},
            {"optional_prefix": "ko", "optional_preverb": True},
            {"optional_preverb": True},
            {"subject": "1sg", "object": "1pl"},
            {"dialects": ["HO", "HO", "AS"]},
        ]
        for variation in variations:
            body = {**default, **variation}
            add("POST", "/api/v1/conjugations", body)
            add("POST", "/api/v1/conjugation-options", body)
    words = {"doviba", "DOGURU", "xyzabc", "", "  doviba  ", "cexv", "k", "ç", "ç̌"}
    with catalog.connect() as db:
        words.update(
            r[0]
            for r in db.execute(
                "SELECT exact_key FROM forms GROUP BY exact_key ORDER BY exact_key LIMIT 60"
            )
        )
        words.update(
            r[0]
            for r in db.execute(
                "SELECT exact_key FROM forms GROUP BY exact_key ORDER BY exact_key DESC LIMIT 60"
            )
        )
        for entry in entries:
            row = db.execute(
                "SELECT f.exact_key FROM forms f JOIN requests r ON r.id=f.request_id WHERE r.entry_id=? LIMIT 1",
                (entry["id"],),
            ).fetchone()
            if row:
                words.add(row[0])
    for word in sorted(words):
        if word:
            for query in (
                word,
                word.replace("x", "h").replace("ʒ", "ts"),
                word.replace("ǩ", "k").replace("ç̌", "ç"),
            ):
                add("GET", "/api/v1/reverse?" + urlencode({"q": query, "limit": 3, "offset": 0}))
            add("GET", "/api/v1/reverse?" + urlencode({"q": word, "limit": 2, "offset": 2}))
        for query in (word, word[:2]):
            add("GET", "/api/v1/reverse/suggestions?" + urlencode({"q": query}))
    (output / "cases.json").write_text(json.dumps(cases, ensure_ascii=False, separators=(",", ":")))
    print(f"Wrote {len(cases)} API expectations to {output / 'cases.json'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--database", type=Path)
    args = parser.parse_args()
    create(args.output, args.database)
