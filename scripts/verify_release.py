"""Check a catalog against historical fixtures and the maintainer's corrections."""

import argparse
import json
import time
from pathlib import Path

from laz_api.catalog import Catalog, canonical
from laz_engine.models import Features
from pydantic import TypeAdapter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("database", type=Path)
    args = parser.parse_args()
    catalog = Catalog(args.database)
    fixtures = Path(__file__).resolve().parents[1] / "tests/fixtures"
    baseline = json.loads((fixtures / "reference.json").read_text())["cases"]
    corrections = json.loads((fixtures / "maintainer-corrections.json").read_text())["cases"]
    # The authoritative dump supersedes an older expected spelling for the
    # same request. The original evidence file itself remains unchanged.
    cases = {
        (case["entry_id"], canonical(case["features"])): case for case in [*baseline, *corrections]
    }
    adapter = TypeAdapter(Features)
    mismatches = []
    started = time.perf_counter()
    for case in cases.values():
        features = adapter.validate_python(case["features"])
        result = catalog.lookup(case["entry_id"], features)
        expected = case["expected"]
        expected_status = "unsupported" if all("N/A" in form for form in expected) else "ok"
        actual = sorted(form["spelling"] for form in result["forms"])
        wrong_frame = "frame" in case and any(
            form["frame"] != case["frame"] for form in result["forms"]
        )
        if (
            result["status"] != expected_status
            or (expected_status == "ok" and actual != expected)
            or wrong_frame
        ):
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
        "maintainer_cases": len(corrections),
        "mismatches": mismatches,
        "seconds": round(time.perf_counter() - started, 3),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
