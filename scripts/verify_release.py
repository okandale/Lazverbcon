"""Compare a generated catalog to the independently captured original outputs."""

import argparse
import json
import time
from pathlib import Path

from laz_api.catalog import Catalog
from laz_engine.models import Features
from pydantic import TypeAdapter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("database", type=Path)
    args = parser.parse_args()
    catalog = Catalog(args.database)
    fixture = Path(__file__).resolve().parents[1] / "tests/fixtures/reference.json"
    cases = json.loads(fixture.read_text())["cases"]
    adapter = TypeAdapter(Features)
    mismatches = []
    started = time.perf_counter()
    for case in cases:
        features = adapter.validate_python(case["features"])
        result = catalog.lookup(case["entry_id"], features)
        expected = case["expected"]
        expected_status = "unsupported" if all("N/A" in form for form in expected) else "ok"
        actual = sorted(form["spelling"] for form in result["forms"])
        if result["status"] != expected_status or (expected_status == "ok" and actual != expected):
            mismatches.append(
                {
                    "entry_id": case["entry_id"],
                    "features": case["features"],
                    "expected": expected,
                    "actual": result,
                }
            )
    report = {
        "cases": len(cases),
        "mismatches": mismatches,
        "seconds": round(time.perf_counter() - started, 3),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
