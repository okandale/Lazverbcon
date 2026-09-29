"""Compare every request in an earlier SQLite release with the current engine.

This deliberately permits a different engine revision. It does not change either
the release or the fixtures. New constructions absent from the release need their
own reference tests.
"""

import argparse
import json
import sqlite3
import sys
from contextlib import closing
from dataclasses import asdict
from itertools import groupby
from pathlib import Path
from time import perf_counter

from laz_api.catalog import unpack_features, unpack_form
from laz_engine.engine import conjugate
from laz_engine.lexicon import entries_by_id
from laz_engine.models import Features
from pydantic import TypeAdapter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("database", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    adapter = TypeAdapter(Features)
    entries = entries_by_id()
    checked = 0
    mismatch_count = 0
    examples = []
    started = perf_counter()
    with closing(sqlite3.connect(args.database.resolve().as_uri() + "?mode=ro", uri=True)) as db:
        db.row_factory = sqlite3.Row
        rows = db.execute(
            """SELECT r.id,r.entry_id,r.features,r.status,r.reason,f.data
               FROM requests r LEFT JOIN forms f ON f.request_id=r.id ORDER BY r.id"""
        )
        for _, group in groupby(rows, key=lambda row: row["id"]):
            group = list(group)
            row = group[0]
            features = unpack_features(row["features"])
            expected = sorted(
                (unpack_form(r["data"], features) for r in group if r["data"] is not None),
                key=lambda form: form["spelling"],
            )
            try:
                result = conjugate(entries[row["entry_id"]], adapter.validate_python(features))
                actual = [asdict(form) for form in result.forms]
                same = (
                    result.status == row["status"]
                    and result.reason == row["reason"]
                    and actual == expected
                )
                detail = asdict(result)
            except Exception as exc:
                same = False
                detail = {"error": f"{type(exc).__name__}: {exc}"}
            if not same:
                mismatch_count += 1
                if len(examples) < 30:
                    examples.append(
                        {
                            "entry_id": row["entry_id"],
                            "features": features,
                            "expected": expected,
                            "expected_status": row["status"],
                            "expected_reason": row["reason"],
                            "actual": detail,
                        }
                    )
            checked += 1
            if checked % 100000 == 0:
                print(
                    f"{checked:,} requests checked; {mismatch_count:,} differences", file=sys.stderr
                )
    report = {
        "requests": checked,
        "mismatches": mismatch_count,
        "examples": examples,
        "seconds": round(perf_counter() - started, 3),
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "examples"}))
    raise SystemExit(1 if mismatch_count else 0)


if __name__ == "__main__":
    main()
