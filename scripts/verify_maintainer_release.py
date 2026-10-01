"""Exhaustively verify every canonical request and source row from lazverbcon2.

The fixture was captured from the archive, independently of generated output.
For each attested request compare the complete spelling/frame set, not merely
whether one expected form is present. N/A rows must be rejected, not searchable.
"""

import argparse
import gzip
import json
import sqlite3
import sys
from pathlib import Path
from time import perf_counter

from laz_api.catalog import Catalog, request_id
from laz_engine.engine import conjugate
from laz_engine.lexicon import entries_by_id
from laz_engine.models import Features
from laz_engine.validation import validate
from pydantic import TypeAdapter

DEFAULT_FIXTURE = Path(__file__).resolve().parents[1] / "tests/fixtures/maintainer-release.jsonl.gz"


def verify(database=None, fixture=DEFAULT_FIXTURE):
    started = perf_counter()
    entries = entries_by_id()
    adapter = TypeAdapter(Features)
    connection = None
    if database is not None:
        catalog = Catalog(database)
        connection = sqlite3.connect(catalog.path.as_uri() + "?mode=ro", uri=True)
    rows = checked = mismatches = rejected = 0
    examples = []
    try:
        with gzip.open(fixture, "rt", encoding="utf-8") as source:
            header = json.loads(next(source))
            if header["feature_fields"] != list(Features.__dataclass_fields__):
                raise ValueError("Maintainer fixture feature schema differs from the engine")
            for line in source:
                entry_id, packed, expected, row_ids = json.loads(line)
                features = adapter.validate_python(
                    dict(zip(header["feature_fields"], packed, strict=True))
                )
                entry = entries[entry_id]
                if connection is None:
                    result = conjugate(entry, features)
                    status = result.status
                    actual = sorted([form.spelling, form.frame] for form in result.forms)
                else:
                    key = request_id(entry_id, features)
                    request = connection.execute(
                        "SELECT id,status FROM requests WHERE request_key=?", (key,)
                    ).fetchone()
                    if request is None:
                        problem = validate(entry, features)
                        status = "unsupported" if problem else "not_generated"
                        actual = []
                    else:
                        status = request[1]
                        actual = sorted(
                            json.loads(r[0])[:2]
                            for r in connection.execute(
                                "SELECT data FROM forms WHERE request_id=?", (request[0],)
                            )
                        )
                    # The HTTP layer validates before looking up SQLite.
                    if expected and validate(entry, features) is not None:
                        status = "api_rejected"
                expected_status = "ok" if expected else "unsupported"
                if actual != expected or status != expected_status:
                    mismatches += 1
                    if len(examples) < 20:
                        examples.append(
                            dict(
                                entry_id=entry_id,
                                features=packed,
                                row_ids=row_ids,
                                expected=expected,
                                actual=actual,
                                status=status,
                            )
                        )
                rows += len(row_ids)
                checked += 1
                rejected += len(row_ids) if not expected else 0
                if checked % 100000 == 0:
                    print(
                        f"{checked:,} requests checked; {mismatches:,} mismatches", file=sys.stderr
                    )
        if rows != header["rows"] or checked != header["requests"]:
            raise ValueError("Incomplete maintainer fixture")
    finally:
        if connection is not None:
            connection.close()
    return dict(
        source_sha256=header["source_sha256"],
        source_rows=rows,
        requests=checked,
        rejected_rows=rejected,
        mismatches=mismatches,
        examples=examples,
        source="database" if database is not None else "engine",
        seconds=round(perf_counter() - started, 3),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", nargs="?", type=Path, help="Omit to verify the pure engine")
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    args = parser.parse_args()
    report = verify(args.database, args.fixture)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(1 if report["mismatches"] else 0)


if __name__ == "__main__":
    main()
