"""Verify every seeded request against the maintainer fixture and pronoun table."""

import argparse
import gzip
import json
from importlib.resources import files
from pathlib import Path

from laz_admin.store import Store, digest, features


def verify(store, fixture):
    pronouns = json.loads(
        files("laz_admin").joinpath("data/pronouns.json").read_text(encoding="utf-8")
    )
    checked = forms_checked = 0
    with store.db() as db, gzip.open(fixture, "rt", encoding="utf-8") as source:
        header = json.loads(next(source))
        for line in source:
            entry_id, packed, expected, source_ids = json.loads(line)
            f = features(dict(zip(header["feature_fields"], packed, strict=True)))
            row = db.execute(
                "SELECT value FROM records WHERE key=?", (digest([entry_id, f]),)
            ).fetchone()
            if not row:
                raise ValueError(f"Missing request from source rows {source_ids}")
            actual = json.loads(row[0])
            if actual["status"] != ("ok" if expected else "unsupported"):
                raise ValueError(f"Status mismatch: {source_ids}")
            if sorted((r["spelling"], r["frame"]) for r in actual["forms"]) != sorted(
                map(tuple, expected)
            ):
                raise ValueError(f"Conjugation mismatch: {source_ids}")
            for form in actual["forms"]:
                for role, key in [("S", "subject"), ("O", "object")]:
                    want = (
                        pronouns[f"{f['dialect']}|{role}{f[key].upper()}|{form['frame']}"]
                        if f[key]
                        else ""
                    )
                    if form[f"{key}_pronoun"] != want:
                        raise ValueError(f"Pronoun mismatch: {source_ids}")
                forms_checked += 1
            checked += 1
        if (
            checked != header["requests"]
            or db.execute("SELECT count(*) FROM records").fetchone()[0] != checked
        ):
            raise ValueError("Request count differs from baseline")
    return {"requests_checked": checked, "forms_checked": forms_checked, "discrepancies": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument(
        "--fixture", type=Path, default=Path("tests/fixtures/maintainer-release.jsonl.gz")
    )
    args = parser.parse_args()
    print(json.dumps(verify(Store(args.project), args.fixture), indent=2))
