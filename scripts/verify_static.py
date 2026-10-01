"""Verify every catalog row, search reference and maintainer request after export."""

import argparse
import base64
import gzip
import hashlib
import itertools
import json
from functools import lru_cache
from pathlib import Path

from laz_api.catalog import Catalog, canonical
from laz_api.static_export import DIMENSIONS, feature_code

ROOT = Path(__file__).resolve().parents[1]


def verify(data, database, fixture=ROOT / "tests/fixtures/maintainer-release.jsonl.gz"):
    manifest = json.loads((data / "manifest.json").read_text())
    for filename, expected in manifest["files"].items():
        content = (data / filename).read_bytes()
        assert len(content) == expected["bytes"]
        assert hashlib.sha256(content).hexdigest() == expected["sha256"], filename
    entries = json.loads((data / "entries.json").read_text())
    validation = json.loads((data / "validation.json").read_text())
    tables = [base64.b64decode(table) for table in validation["tables"]]

    @lru_cache(maxsize=32)
    def chunk(entry_id, dialect):
        filename = manifest["forward"].get(entry_id, {}).get(dialect)
        return (
            json.loads((data / filename).read_text())
            if filename
            else {"requests": {}, "unsupported": {}}
        )

    def lookup(entry_id, values):
        v = validation["entries"][entry_id]
        dialect, *_, legacy, prefix = values
        problem = (
            legacy
            and prefix != "none"
            or dialect not in v["dialects"]
            or (prefix != "none" and prefix not in v["prefixes"][dialect])
        )
        code = 0
        for dimension, value in zip(DIMENSIONS[1:-1], values[1:-1], strict=True):
            code = code * len(dimension) + dimension.index(value)
        if problem or tables[v["table"]][code]:
            return "unsupported", []
        part = chunk(entry_id, dialect)
        key = str(feature_code(values))
        if key in part["unsupported"]:
            return "unsupported", []
        if key not in part["requests"]:
            return "not_generated", []
        return "ok", [part["forms"][i] for i in part["requests"][key]]

    requests = forms = reverse_refs = 0
    with Catalog(database).connect() as db:
        assert manifest["catalog"] == Catalog(database).manifest
        assert entries == [
            json.loads(r[0]) for r in db.execute("SELECT data FROM entries ORDER BY id")
        ]
        rows = db.execute("""SELECT r.id,r.entry_id,r.features,r.status,f.data FROM requests r
            LEFT JOIN forms f ON f.request_id=r.id ORDER BY r.entry_id,json_extract(r.features,'$[0]'),r.id,f.data""")
        for _, group in itertools.groupby(rows, lambda r: r[0]):
            grouped = list(group)
            first = grouped[0]
            values = json.loads(first[2])
            status, actual = lookup(first[1], values)
            expected = [json.loads(r[4]) for r in grouped if r[4] is not None]
            assert (status, actual) == (first[3], expected), (first[1], values)
            requests += 1
            forms += len(actual)

        # Compare the full exact index against SQL, not only a sample of searches.
        def exported_exact():
            for _, _, filename in manifest["indexes"]["exact"]:
                for key, spelling, refs in json.loads((data / filename).read_text()):
                    values = []
                    for entry_number, code, form_id in refs:
                        from laz_api.static_export import feature_values

                        features = feature_values(code)
                        entry_id = entries[entry_number]["id"]
                        form = chunk(entry_id, features[0])["forms"][form_id]
                        values.append([entry_id, canonical(features), canonical(form)])
                    yield key, spelling, sorted(values)

        rows = db.execute("""SELECT f.exact_key,f.data,r.entry_id,r.features FROM forms f JOIN requests r ON r.id=f.request_id
            ORDER BY f.exact_key,f.data,r.entry_id,r.features""")
        expected_groups = itertools.groupby(rows, lambda r: r[0])
        for exported, (key, group) in itertools.zip_longest(exported_exact(), expected_groups):
            grouped = list(group)
            expected = sorted([r[2], r[3], r[1]] for r in grouped)
            assert exported == (key, json.loads(grouped[0][1])[0], expected), key
            reverse_refs += len(expected)
        for tier, column in (("alternate", "strict_key"), ("broad", "broad_key")):

            def actual_rows():
                for _, _, filename in manifest["indexes"][tier]:
                    for key, values in json.loads((data / filename).read_text()):
                        for value in values:
                            yield key, value

            expected = db.execute(
                f"SELECT DISTINCT {column},exact_key FROM forms ORDER BY {column},exact_key"
            )
            assert all(a == tuple(b) for a, b in itertools.zip_longest(actual_rows(), expected))
    checked = source_rows = 0
    with gzip.open(fixture, "rt") as source:
        header = json.loads(next(source))
        for line in source:
            entry_id, values, expected, ids = json.loads(line)
            status, actual = lookup(entry_id, values)
            assert status == ("ok" if expected else "unsupported"), (entry_id, values)
            assert sorted(form[:2] for form in actual) == expected, (entry_id, values)
            checked += 1
            source_rows += len(ids)
    assert (checked, source_rows) == (header["requests"], header["rows"])
    return {
        "release": manifest["release"],
        "requests": requests,
        "forms": forms,
        "reverse_references": reverse_refs,
        "maintainer_requests": checked,
        "maintainer_source_rows": source_rows,
        "mismatches": 0,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path)
    parser.add_argument("database", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.data, args.database), indent=2))
