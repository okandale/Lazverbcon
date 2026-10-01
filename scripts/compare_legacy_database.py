"""Audit every legacy PostgreSQL form against a remake SQLite catalog.

Only COPY data is parsed; dumped SQL is never executed. Raw uploads and complete
reports belong in ignored directories. No source database or engine is changed.
"""

import argparse
import hashlib
import json
import re
import shutil
import sqlite3
import subprocess
import unicodedata
from collections import Counter
from dataclasses import asdict
from pathlib import Path

from laz_api.catalog import canonical, engine_revision, request_id
from laz_engine.models import (
    Causative,
    Derivation,
    Dialect,
    Entry,
    Features,
    Mood,
    OptionalPrefix,
    Person,
    Tense,
)
from laz_engine.validation import validate
from pydantic import TypeAdapter

TABLES = ("dialect", "verb_category", "verb", "verb_form")
DIALECTS = {"Ardeşen": "AS", "Pazar": "PZ", "Fındıklı/Arhavi": "FA", "Hopa": "HO"}
ESCAPE = re.compile(rb"\\(x[0-9a-fA-F]{1,2}|[0-7]{1,3}|.)")


def decode_copy(value):
    if value == r"\N":
        return None

    def replace(match):
        token = match[1]
        if token.startswith(b"x") and len(token) > 1:
            return bytes([int(token[1:], 16)])
        if token[0] in b"01234567":
            return bytes([int(token, 8)])
        return {b"b": b"\b", b"f": b"\f", b"n": b"\n", b"r": b"\r", b"t": b"\t", b"v": b"\v"}.get(
            token, token
        )

    return ESCAPE.sub(replace, value.encode("utf-8")).decode("utf-8")


def copy_rows(path):
    table = None
    columns = []
    with path.open(encoding="utf-8") as source:
        for line in source:
            line = line.rstrip("\n")
            if table:
                if line == r"\.":
                    table = None
                    continue
                values = [decode_copy(v) for v in line.split("\t")]
                if len(values) != len(columns):
                    raise ValueError(f"Invalid COPY row in {table}")
                yield table, dict(zip(columns, values, strict=True))
            elif line.startswith("COPY "):
                header = re.fullmatch(r"COPY public\.([a-z_]+) \(([^)]+)\) FROM stdin;", line)
                if not header or header[1] not in TABLES:
                    raise ValueError(f"Unsupported COPY header: {line}")
                table = header[1]
                columns = header[2].split(", ")
    if table:
        raise ValueError(f"Incomplete COPY data: {table}")


def normalized(value):
    return unicodedata.normalize("NFC", value or "").strip()


def map_verb(old, entries, dialect, category):
    candidates = [
        e
        for e in entries
        if normalized(e["infinitive"]) == normalized(old["infinitive"])
        and e["verb_class"] == category
        and any(dialect in p["dialects"] for p in e["variants"])
    ]
    exact = [
        e
        for e in candidates
        if normalized(e["english"]) == normalized(old["meaning_english"])
        and normalized(e["turkish"]) == normalized(old["meaning_turkish"])
        and any(
            dialect in p["dialects"] and normalized(p["form"]) == normalized(old["present_3sg"])
            for p in e["variants"]
        )
    ]
    if len(exact) == 1:
        return exact[0]["id"], "exact_metadata", [e["id"] for e in candidates]
    if len(candidates) == 1:
        return candidates[0]["id"], "identity_only_metadata_difference", [candidates[0]["id"]]
    return (
        None,
        "ambiguous_entry" if candidates else "unmapped_entry",
        [e["id"] for e in candidates],
    )


def features_for(row, dialect):
    def boolean(field):
        if row[field] not in ("t", "f"):
            raise ValueError(f"Unknown boolean {field}: {row[field]}")
        return row[field] == "t"

    def person(value, role):
        if value is None:
            return None
        if not re.fullmatch(role + r"[123](SG|PL)", value):
            raise ValueError(f"Unknown person: {value}")
        return Person(value[1:].lower())

    simple, double = boolean("is_causative"), boolean("is_double_causative")
    if simple and double:
        raise ValueError("Both simple and double causative flags set")
    if row["optional_prefix"] not in (None, "ko", "do"):
        raise ValueError(f"Unknown optional prefix: {row['optional_prefix']}")
    subject = person(row["subject"], "S")
    if subject is None:
        raise ValueError("Missing subject")
    return Features(
        Dialect(dialect),
        subject,
        person(row["object"], "O"),
        Tense(row["tense"]),
        Mood(row["mood"]),
        Derivation(row["derivation"]),
        boolean("is_applicative"),
        Causative.DOUBLE if double else Causative.SIMPLE if simple else Causative.NONE,
        False,
        OptionalPrefix(row["optional_prefix"] or "none"),
    )


def sha256(path):
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def diagnose(db, entries, mappings):
    """Keep unresolved lexical alternatives visible without silently remapping."""
    db.execute("ALTER TABLE old_rows ADD COLUMN reason TEXT")
    db.execute("ALTER TABLE old_rows ADD COLUMN alternative_entries TEXT")
    adapter = TypeAdapter(Features)
    entry_adapter = TypeAdapter(Entry)
    entry_objects = {e["id"]: entry_adapter.validate_python(e) for e in entries}
    for row in db.execute("SELECT * FROM old_rows WHERE status='request_absent'").fetchall():
        problem = validate(entry_objects[row["entry_id"]], adapter.validate_json(row["features"]))
        if problem:
            status = "both_reject" if row["spelling"].startswith("N/A") else "unsupported_request"
            db.execute(
                "UPDATE old_rows SET status=?,reason=? WHERE id=?",
                (status, problem.reason, row["id"]),
            )
    for row in db.execute(
        "SELECT * FROM old_rows WHERE status IN ('spelling_difference','frame_difference','unsupported_request','ambiguous_entry')"
    ).fetchall():
        if row["spelling"].startswith("N/A") or not row["features"]:
            continue
        old = json.loads(mappings[row["verb_id"]]["legacy_data"])
        features = adapter.validate_json(row["features"])
        alternatives = []
        for entry in entries:
            if entry["id"] == row["entry_id"] or normalized(entry["infinitive"]) != normalized(
                old["infinitive"]
            ):
                continue
            hit = db.execute(
                """SELECT 1 FROM current.requests r JOIN current.forms f ON f.request_id=r.id
                WHERE r.request_key=? AND json_extract(f.data,'$[0]')=? AND json_extract(f.data,'$[1]')=?""",
                (request_id(entry["id"], features), row["spelling"], row["frame"]),
            ).fetchone()
            if hit:
                alternatives.append(entry["id"])
        if alternatives:
            db.execute(
                "UPDATE old_rows SET alternative_entries=? WHERE id=?",
                (canonical(alternatives), row["id"]),
            )


def compare(source, catalog, output, original_source=None):
    output.mkdir(parents=True, exist_ok=True)
    audit = output / "audit.sqlite"
    if audit.exists():
        raise FileExistsError(f"Use a new report directory: {audit}")
    db = sqlite3.connect(audit, uri=True)
    db.row_factory = sqlite3.Row
    reviewed = {}
    reviewed_path = Path(__file__).resolve().parents[1] / "migration/maintainer-mappings.json"
    if original_source and reviewed_path.exists():
        record = json.loads(reviewed_path.read_text())
        if sha256(original_source) == record["source_sha256"]:
            reviewed = record["mappings"]
    try:
        db.execute("ATTACH DATABASE ? AS current", (catalog.resolve().as_uri() + "?mode=ro",))
        manifest = json.loads(
            db.execute("SELECT value FROM current.metadata WHERE key='manifest'").fetchone()[0]
        )
        if manifest.get("status") != "ready" or manifest.get("coverage") != "full":
            raise ValueError("Comparison requires a ready full catalog")
        if manifest["engine_revision"] != engine_revision():
            raise ValueError("Catalog must match the current engine for request diagnostics")
        entries = [json.loads(r[0]) for r in db.execute("SELECT data FROM current.entries")]
        db.executescript("""
            CREATE TABLE verb_mapping (legacy_id TEXT PRIMARY KEY, entry_id TEXT, quality TEXT,
                                       dialect TEXT, category TEXT, candidates TEXT, legacy_data TEXT);
            CREATE TABLE old_rows (id TEXT PRIMARY KEY, verb_id TEXT, entry_id TEXT, features TEXT,
                                  request_key BLOB, frame TEXT, spelling TEXT, status TEXT,
                                  legacy_data TEXT);
        """)
        metadata = {t: {} for t in TABLES if t != "verb_form"}
        for table, row in copy_rows(source):
            if table != "verb_form":
                metadata[table][row[table + "_id"]] = row
        for old in metadata["verb"].values():
            dialect = DIALECTS[metadata["dialect"][old["dialect_id"]]["english_name"]]
            category = metadata["verb_category"][old["verb_category_id"]]["code"]
            entry_id, quality, candidates = map_verb(old, entries, dialect, category)
            db.execute(
                "INSERT INTO verb_mapping VALUES (?,?,?,?,?,?,?)",
                (
                    old["verb_id"],
                    entry_id,
                    quality,
                    dialect,
                    category,
                    canonical(candidates),
                    canonical(old),
                ),
            )
        mappings = {r["legacy_id"]: dict(r) for r in db.execute("SELECT * FROM verb_mapping")}
        counts = Counter()
        for table, row in copy_rows(source):
            if table != "verb_form":
                continue
            mapping = mappings[row["verb_id"]]
            entry_id = mapping["entry_id"]
            if reviewed:
                ordinary = row["derivation"] == "none" and row["tense"] != "present_perfect"
                category = (
                    {"Dative": "IVD", "Ergative": "TVE", "Nominative": "TVM"}[row["frame"]]
                    if ordinary
                    else mapping["category"]
                )
                if not ordinary and category == "IVD":
                    category = "TVE" if f"{row['verb_id']}:TVE" in reviewed else "TVM"
                entry_id = reviewed[f"{row['verb_id']}:{category}"]["entry_id"]
            features, key = None, None
            status = mapping["quality"] if not entry_id else "pending"
            try:
                features = features_for(row, mapping["dialect"])
                if entry_id:
                    key = request_id(entry_id, features)
            except ValueError as exc:
                status = "unmapped_features"
                row = {**row, "mapping_error": str(exc)}
            db.execute(
                "INSERT INTO old_rows VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    row["verb_form_id"],
                    row["verb_id"],
                    entry_id,
                    canonical(asdict(features)) if features else None,
                    key,
                    row["frame"],
                    row["spelling"],
                    status,
                    canonical(row),
                ),
            )
            counts["legacy_forms"] += 1
        if not counts["legacy_forms"]:
            raise ValueError("No legacy forms found")
        db.executescript("""
            CREATE INDEX old_request ON old_rows(request_key);
            CREATE INDEX old_output ON old_rows(request_key, spelling, frame);
            UPDATE old_rows SET status = CASE
              WHEN NOT EXISTS (SELECT 1 FROM current.requests r WHERE r.request_key=old_rows.request_key)
                THEN 'request_absent'
              WHEN EXISTS (SELECT 1 FROM current.requests r JOIN current.forms f ON f.request_id=r.id
                WHERE r.request_key=old_rows.request_key AND json_extract(f.data,'$[0]')=old_rows.spelling
                AND json_extract(f.data,'$[1]')=old_rows.frame) THEN 'exact'
              WHEN EXISTS (SELECT 1 FROM current.requests r JOIN current.forms f ON f.request_id=r.id
                WHERE r.request_key=old_rows.request_key AND json_extract(f.data,'$[0]')=old_rows.spelling)
                THEN 'frame_difference'
              WHEN EXISTS (SELECT 1 FROM current.requests r WHERE r.request_key=old_rows.request_key AND r.status='unsupported')
                THEN 'unsupported'
              ELSE 'spelling_difference' END WHERE status='pending';
            CREATE TABLE new_only AS
              SELECT f.id AS form_id, r.entry_id, r.features, f.data AS form,
                CASE WHEN EXISTS (SELECT 1 FROM old_rows o WHERE o.request_key=r.request_key)
                THEN 'different_output_for_shared_request' ELSE 'no_mapped_old_request' END AS status
              FROM current.forms f JOIN current.requests r ON r.id=f.request_id
              WHERE NOT EXISTS (SELECT 1 FROM old_rows o WHERE o.request_key=r.request_key
                AND o.spelling=json_extract(f.data,'$[0]') AND o.frame=json_extract(f.data,'$[1]'));
            CREATE INDEX old_status ON old_rows(status);
            CREATE INDEX new_status ON new_only(status);
        """)
        diagnose(db, entries, mappings)
        old_counts = dict(db.execute("SELECT status,count(*) FROM old_rows GROUP BY status"))
        new_counts = dict(db.execute("SELECT status,count(*) FROM new_only GROUP BY status"))
        examples = {}
        for status in old_counts:
            if status == "exact":
                continue
            examples[status] = []
            for r in db.execute(
                "SELECT * FROM old_rows WHERE status=? LIMIT 10", (status,)
            ).fetchall():
                actual = db.execute(
                    """SELECT f.data FROM current.requests r
                    JOIN current.forms f ON f.request_id=r.id WHERE r.request_key=?""",
                    (r["request_key"],),
                ).fetchall()
                examples[status].append(
                    {
                        "legacy_form_id": r["id"],
                        "legacy_verb": json.loads(mappings[r["verb_id"]]["legacy_data"]),
                        "entry_id": r["entry_id"],
                        "features": json.loads(r["features"]) if r["features"] else None,
                        "old_spelling": r["spelling"],
                        "old_frame": r["frame"],
                        "new_outputs": [json.loads(a[0])[:2] for a in actual],
                    }
                )
        report = {
            "input_sha256": sha256(original_source or source),
            "source_sha256": sha256(source),
            "catalog_sha256": sha256(catalog),
            "manifest": manifest,
            "legacy_verbs": len(mappings),
            "legacy_forms": counts["legacy_forms"],
            "reviewed_form_mappings": bool(reviewed),
            "new_forms": db.execute("SELECT count(*) FROM current.forms").fetchone()[0],
            "mapping_counts": dict(
                db.execute("SELECT quality,count(*) FROM verb_mapping GROUP BY quality")
            ),
            "old_row_status": old_counts,
            "new_only_status": new_counts,
            "unsupported_reasons": dict(
                db.execute(
                    "SELECT reason,count(*) FROM old_rows WHERE reason IS NOT NULL GROUP BY reason"
                )
            ),
            "alternative_entry_matches": db.execute(
                "SELECT count(*) FROM old_rows WHERE alternative_entries IS NOT NULL"
            ).fetchone()[0],
            "legacy_rejection_messages": db.execute(
                "SELECT count(*) FROM old_rows WHERE spelling LIKE 'N/A%'"
            ).fetchone()[0],
            "examples": examples,
        }
        assert sum(old_counts.values()) == counts["legacy_forms"]
        db.execute("CREATE TABLE report (data TEXT NOT NULL)")
        db.execute("INSERT INTO report VALUES (?)", (canonical(report),))
        db.commit()
        (output / "summary.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        )
        return report
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source", type=Path, help="PostgreSQL custom dump or selected COPY SQL export"
    )
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pg-restore", default=shutil.which("pg_restore"))
    args = parser.parse_args()
    if (args.output / "audit.sqlite").exists():
        parser.error("Use a new output directory; existing audits are preserved")
    source = args.source
    with source.open("rb") as file:
        custom = file.read(5) == b"PGDMP"
    if custom:
        if not args.pg_restore:
            parser.error("A PostgreSQL custom dump requires --pg-restore /path/to/pg_restore")
        args.output.mkdir(parents=True, exist_ok=True)
        source = args.output / "source.sql"
        subprocess.run(
            [
                args.pg_restore,
                "--data-only",
                "--no-owner",
                "--no-privileges",
                *(f"--table={t}" for t in TABLES),
                f"--file={source}",
                str(args.source),
            ],
            check=True,
        )
    report = compare(source, args.catalog, args.output, args.source)
    print(
        json.dumps({k: v for k, v in report.items() if k not in ("manifest", "examples")}, indent=2)
    )


if __name__ == "__main__":
    main()
