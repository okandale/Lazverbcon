"""Capture the authoritative dump as reproducible rules metadata and test evidence.

Exports selected COPY data from the fingerprinted archive. SQL is parsed,
never executed. The full dump remains ignored; only conjugation test evidence,
prefix availability and an explicit identity mapping are versioned.
"""

import argparse
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import asdict, replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from laz_engine.engine import conjugate_regular  # noqa: E402
from laz_engine.lexicon import load_entries  # noqa: E402
from laz_engine.models import OptionalPrefix  # noqa: E402

from scripts.compare_legacy_database import (  # noqa: E402
    DIALECTS,
    TABLES,
    copy_rows,
    features_for,
    normalized,
)

SOURCE_SHA256 = "54964059bff2c7dbd5ae465235ce649f1a49491299116ccbf51757d0a280c35d"
FRAME_CLASS = {"Dative": "IVD", "Ergative": "TVE", "Nominative": "TVM"}
# Record 617 combines dative 'ache' with the ergative uǯǩunaps paradigm.
# Its entire ergative paradigm agrees with 0309 (762 forms differ from 0308).
IDENTITY_OVERRIDES = {("617", "TVE"): "verb-0309"}


def feature_key(features):
    return json.dumps(list(asdict(features).values()), ensure_ascii=False, separators=(",", ":"))


def choose_entry(old, category, dialect, index):
    candidates = index[normalized(old["infinitive"]), category, dialect]
    override = IDENTITY_OVERRIDES.get((old["verb_id"], category))
    if override:
        return next(e for e in candidates if e.id == override), "reviewed_paradigm_mapping"
    if not candidates:
        raise ValueError(f"No entry for {old['verb_id']}/{category}/{dialect}")

    def score(entry):
        return (
            (normalized(entry.english) == normalized(old["meaning_english"]))
            + (normalized(entry.turkish) == normalized(old["meaning_turkish"])),
            any(
                normalized(p.form) == normalized(old["present_3sg"]) and dialect in p.dialects
                for p in entry.variants
            ),
        )

    best = max(map(score, candidates))
    candidates = [e for e in candidates if score(e) == best]
    if len(candidates) > 1:
        identities = {
            (e.english, e.turkish, tuple(p.form for p in e.variants if dialect in p.dialects))
            for e in candidates
        }
        if len(identities) != 1:
            raise ValueError(f"Ambiguous identity for {old['verb_id']}/{category}/{dialect}")
        return max(candidates, key=lambda e: (len(e.dialects), e.id)), "equivalent_duplicate"
    return candidates[0], "metadata_and_frame"


def capture(source, output, fixture, mapping_path):
    entries = load_entries()
    index = defaultdict(list)
    by_id = {e.id: e for e in entries}
    for entry in entries:
        for dialect in entry.dialects:
            index[normalized(entry.infinitive), entry.verb_class, dialect].append(entry)
    metadata = {name: {} for name in ("verb", "dialect", "verb_category")}
    for table, row in copy_rows(source):
        if table in metadata:
            metadata[table][row[table + "_id"]] = row
    groups = {}
    mappings = {}
    prefix_options = defaultdict(lambda: defaultdict(set))
    total = 0
    for table, row in copy_rows(source):
        if table != "verb_form":
            continue
        old = metadata["verb"][row["verb_id"]]
        dialect = DIALECTS[metadata["dialect"][old["dialect_id"]]["english_name"]]
        original_class = metadata["verb_category"][old["verb_category_id"]]["code"]
        f = replace(
            features_for(row, dialect),
            optional_preverb=False,
            optional_prefix=OptionalPrefix(row["optional_prefix"] or "none"),
        )
        ordinary = f.derivation == "none" and f.tense != "present_perfect"
        category = FRAME_CLASS[row["frame"]] if ordinary else original_class
        if not ordinary and category == "IVD":
            category = "TVE" if index[normalized(old["infinitive"]), "TVE", dialect] else "TVM"
        mapping_key = f"{old['verb_id']}:{category}"
        if mapping_key not in mappings:
            entry, basis = choose_entry(old, category, dialect, index)
            mappings[mapping_key] = dict(
                entry_id=entry.id,
                legacy_verb_id=old["verb_id"],
                infinitive=old["infinitive"],
                dialect=dialect,
                verb_class=category,
                basis=basis,
            )
        entry_id = mappings[mapping_key]["entry_id"]
        group = groups.setdefault((entry_id, f), dict(forms=set(), rejected=False, row_ids=[]))
        if row["spelling"].startswith("N/A"):
            group["rejected"] = True
        else:
            group["forms"].add((row["spelling"], row["frame"]))
        group["row_ids"].append(row["verb_form_id"])
        if f.optional_prefix != OptionalPrefix.NONE:
            prefix_options[entry_id][dialect].add(f.optional_prefix.value)
        total += 1
    exceptions = defaultdict(dict)
    counts = Counter()
    fixture.parent.mkdir(parents=True, exist_ok=True)
    # A deterministic gzip stream allows byte-for-byte reproduction from the upload.
    staging = fixture.with_suffix(".building")
    with (
        staging.open("wb") as raw,
        gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as zipped,
    ):
        header = dict(
            source_sha256=SOURCE_SHA256,
            rows=total,
            requests=len(groups),
            feature_fields=list(next(iter(groups))[1].__dataclass_fields__),
        )
        zipped.write((json.dumps(header, separators=(",", ":")) + "\n").encode())
        for (entry_id, features), group in sorted(
            groups.items(), key=lambda x: (x[0][0], feature_key(x[0][1]))
        ):
            if group["forms"] and group["rejected"]:
                raise ValueError(
                    f"Conflicting rejection and forms: {entry_id}/{features}/{group['row_ids']}"
                )
            expected = sorted(group["forms"])
            result = conjugate_regular(by_id[entry_id], features)
            actual = sorted((form.spelling, form.frame) for form in result.forms)
            if actual != expected or (result.status == "ok") != bool(expected):
                exceptions[entry_id][feature_key(features)] = dict(
                    forms=expected, row_ids=group["row_ids"]
                )
                counts["exceptions"] += 1
            counts["forms" if expected else "rejected"] += len(group["row_ids"])
            case = [entry_id, list(asdict(features).values()), expected, group["row_ids"]]
            zipped.write(
                (json.dumps(case, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
            )
    if exceptions:
        report = output.with_suffix(".differences.json")
        report.write_text(json.dumps(exceptions, ensure_ascii=False, indent=2) + "\n")
        raise ValueError(f"Implement or review the remaining rule differences first: {report}")
    staging.replace(fixture)
    runtime = dict(
        source_sha256=SOURCE_SHA256,
        prefixes={
            eid: {d: sorted(ps) for d, ps in ds.items()}
            for eid, ds in sorted(prefix_options.items())
        },
    )
    output.write_text(json.dumps(runtime, ensure_ascii=False, indent=2) + "\n")
    mapping_path.write_text(
        json.dumps(
            dict(source_sha256=SOURCE_SHA256, mappings=mappings), ensure_ascii=False, indent=2
        )
        + "\n"
    )
    print(
        json.dumps(
            dict(rows=total, requests=len(groups), mappings=len(mappings), **counts), indent=2
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dump", type=Path, help="Original archive, checked for provenance")
    parser.add_argument("--pg-restore", default=shutil.which("pg_restore"))
    parser.add_argument(
        "--output", type=Path, default=Path("packages/engine/src/laz_engine/data/maintainer.json")
    )
    parser.add_argument(
        "--fixture", type=Path, default=Path("tests/fixtures/maintainer-release.jsonl.gz")
    )
    parser.add_argument("--mappings", type=Path, default=Path("migration/maintainer-mappings.json"))
    args = parser.parse_args()
    with args.dump.open("rb") as source:
        if hashlib.file_digest(source, "sha256").hexdigest() != SOURCE_SHA256:
            parser.error(
                "This importer is reviewed for lazverbcon2.dump with the recorded SHA-256 only"
            )
    if not args.pg_restore:
        parser.error("Supply --pg-restore /path/to/pg_restore")
    with tempfile.TemporaryDirectory(prefix="laz-maintainer-") as temp:
        source = Path(temp) / "source.sql"
        subprocess.run(
            [
                args.pg_restore,
                "--data-only",
                "--no-owner",
                "--no-privileges",
                *(f"--table={t}" for t in TABLES),
                f"--file={source}",
                str(args.dump),
            ],
            check=True,
        )
        capture(source, args.output, args.fixture, args.mappings)


if __name__ == "__main__":
    main()
