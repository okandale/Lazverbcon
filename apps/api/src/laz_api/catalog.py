"""Build and query immutable SQLite releases. No runtime writes."""

import hashlib
import json
import os
import sqlite3
import tempfile
from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone
from importlib.resources import files
from pathlib import Path

from laz_engine.engine import conjugate
from laz_engine.enumeration import iter_features
from laz_engine.lexicon import load_entries, search_key
from laz_engine.models import EngineFailure, Entry, Features
from laz_engine.orthography import broad_key, strict_key

SCHEMA_VERSION = 1
SCHEMA = """
CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE entries (id TEXT PRIMARY KEY, data TEXT NOT NULL, search TEXT NOT NULL);
CREATE TABLE requests (
 id INTEGER PRIMARY KEY, request_key BLOB UNIQUE NOT NULL,
 entry_id TEXT NOT NULL REFERENCES entries(id),
 features TEXT NOT NULL, status TEXT NOT NULL, reason TEXT, message TEXT
);
CREATE TABLE forms (
 id INTEGER PRIMARY KEY, request_id INTEGER NOT NULL REFERENCES requests(id),
 data TEXT NOT NULL, exact_key TEXT NOT NULL, strict_key TEXT NOT NULL, broad_key TEXT NOT NULL
);
CREATE INDEX forms_request ON forms(request_id);
CREATE INDEX forms_exact ON forms(exact_key);
CREATE INDEX forms_strict ON forms(strict_key);
CREATE INDEX forms_broad ON forms(broad_key);
"""


def canonical(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def request_id(entry_id: str, features: Features) -> bytes:
    return hashlib.sha256(canonical([entry_id, asdict(features)]).encode()).digest()


FEATURE_FIELDS = tuple(Features.__dataclass_fields__)
FORM_FIELDS = ("spelling", "frame", "subject_pronoun", "object_pronoun", "rule")


def unpack_features(encoded: str) -> dict:
    return dict(zip(FEATURE_FIELDS, json.loads(encoded), strict=True))


def unpack_form(encoded: str, features: dict) -> dict:
    return {
        **dict(zip(FORM_FIELDS, json.loads(encoded), strict=True)),
        "subject": features["subject"],
        "object": features["object"],
    }


def engine_revision() -> str:
    digest = hashlib.sha256()
    root = Path(str(files("laz_engine")))
    for path in sorted(root.rglob("*.py")):
        digest.update(str(path.relative_to(root)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def lexicon_revision() -> str:
    return hashlib.sha256(
        files("laz_engine").joinpath("data/entries.json").read_bytes()
    ).hexdigest()


class BuildFailed(RuntimeError):
    pass


def build_catalog(
    output: Path, profile: str = "full", entries: tuple[Entry, ...] | None = None, progress=None
) -> dict:
    """Publish only after all requests succeed or explicitly return unsupported.

    An interrupted or failed build never overwrites the previous release.
    The report records all failed requests, plus grouped expected exclusions.
    """
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError("Choose a new release filename; existing releases are immutable.")
    chosen = entries if entries is not None else load_entries()
    handle, staging_name = tempfile.mkstemp(
        prefix=output.stem + "-", suffix=".building", dir=output.parent
    )
    os.close(handle)
    staging = Path(staging_name)
    report = {
        "schema_version": SCHEMA_VERSION,
        "profile": profile,
        "engine_revision": engine_revision(),
        "lexicon_revision": lexicon_revision(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "entry_count": len(chosen),
        "request_count": 0,
        "form_count": 0,
        "errors": [],
        "unsupported": {},
        "data_issues": [{"entry_id": e.id, "issues": e.issues} for e in chosen if e.issues],
        "complete_lexicon": {e.id for e in chosen} == {e.id for e in load_entries()},
    }
    counts = Counter()
    try:
        with sqlite3.connect(staging) as db:
            db.execute("PRAGMA foreign_keys=ON")
            db.executescript(SCHEMA)
            db.executemany(
                "INSERT INTO entries VALUES (?, ?, ?)",
                [
                    (
                        e.id,
                        canonical(asdict(e)),
                        search_key(f"{e.infinitive} {e.english} {e.turkish}"),
                    )
                    for e in chosen
                ],
            )
            for number, entry in enumerate(chosen, 1):
                for features in iter_features(entry, profile):
                    report["request_count"] += 1
                    try:
                        result = conjugate(entry, features)
                    except EngineFailure as exc:
                        report["errors"].append(
                            {"entry_id": entry.id, "features": asdict(features), "error": str(exc)}
                        )
                        continue
                    key = request_id(entry.id, features)
                    cursor = db.execute(
                        "INSERT INTO requests(request_key,entry_id,features,status,reason,message) VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            key,
                            entry.id,
                            canonical(list(asdict(features).values())),
                            result.status,
                            result.reason,
                            result.message,
                        ),
                    )
                    row_id = cursor.lastrowid
                    if result.status != "ok":
                        counts[result.reason] += 1
                    for form in result.forms:
                        db.execute(
                            "INSERT INTO forms(request_id,data,exact_key,strict_key,broad_key) VALUES (?,?,?,?,?)",
                            (
                                row_id,
                                canonical([getattr(form, name) for name in FORM_FIELDS]),
                                search_key(form.spelling),
                                strict_key(form.spelling),
                                broad_key(form.spelling),
                            ),
                        )
                        report["form_count"] += 1
                if progress:
                    progress(number, len(chosen), report)
            report["unsupported"] = dict(counts)
            report["status"] = "failed" if report["errors"] else "ready"
            report["coverage"] = (
                "full" if profile == "full" and report["complete_lexicon"] else "partial"
            )
            db.execute("INSERT INTO metadata VALUES ('manifest', ?)", (canonical(report),))
            db.commit()
            if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise BuildFailed("SQLite integrity check failed")
            if db.execute("PRAGMA foreign_key_check").fetchone():
                raise BuildFailed("SQLite foreign key check failed")
        output.with_suffix(".report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        )
        if report["errors"]:
            raise BuildFailed(
                f"{len(report['errors'])} rule failures; see {output.with_suffix('.report.json')}. No database published."
            )
        staging.replace(output)
        return report
    finally:
        if staging.exists():
            staging.unlink()


class Catalog:
    def __init__(self, path: Path):
        self.path = path.resolve()
        with self.connect() as db:
            self.manifest = json.loads(
                db.execute("SELECT value FROM metadata WHERE key='manifest'").fetchone()[0]
            )
        if self.manifest["schema_version"] != SCHEMA_VERSION or self.manifest["status"] != "ready":
            raise ValueError("Unsupported or unpublished database")

    def connect(self):
        # sqlite Connection.__exit__ does not close the handle; use closing below.
        from contextlib import closing

        db = sqlite3.connect(self.path.as_uri() + "?mode=ro", uri=True)
        db.row_factory = sqlite3.Row
        return closing(db)

    def entries(self, query: str = "", limit: int = 30, offset: int = 0):
        with self.connect() as db:
            key = search_key(query)
            count = db.execute(
                "SELECT count(*) FROM entries WHERE instr(search, ?) > 0", (key,)
            ).fetchone()[0]
            rows = db.execute(
                "SELECT data FROM entries WHERE instr(search, ?) > 0 ORDER BY id LIMIT ? OFFSET ?",
                (key, limit, offset),
            )
            return [json.loads(r[0]) for r in rows], count

    def entry(self, entry_id: str):
        with self.connect() as db:
            row = db.execute("SELECT data FROM entries WHERE id=?", (entry_id,)).fetchone()
            return json.loads(row[0]) if row else None

    def lookup(self, entry_id: str, features: Features):
        key = request_id(entry_id, features)
        with self.connect() as db:
            row = db.execute(
                "SELECT id,status,reason,message FROM requests WHERE request_key=?", (key,)
            ).fetchone()
            if not row:
                return {
                    "status": "not_generated",
                    "forms": [],
                    "reason": "not_generated",
                    "message": "This combination is not included in this database release.",
                }
            forms = [
                unpack_form(r[0], asdict(features))
                for r in db.execute(
                    "SELECT data FROM forms WHERE request_id=? ORDER BY data", (row["id"],)
                )
            ]
            return {k: row[k] for k in ("status", "reason", "message")} | {"forms": forms}

    def reverse(self, spelling: str, limit: int = 50, offset: int = 0):
        tiers = (
            ("exact", "exact_key", search_key(spelling)),
            ("alternate", "strict_key", strict_key(spelling)),
            ("broad", "broad_key", broad_key(spelling)),
        )
        with self.connect() as db:
            for tier, column, key in tiers:
                # Column names come exclusively from the fixed table above.
                count = db.execute(
                    f"SELECT count(*) FROM forms WHERE {column}=?", (key,)
                ).fetchone()[0]
                if not count:
                    continue
                rows = db.execute(
                    f"""SELECT f.data AS form, r.features, e.data AS entry
                    FROM forms f JOIN requests r ON r.id=f.request_id JOIN entries e ON e.id=r.entry_id
                    WHERE f.{column}=? ORDER BY e.id,r.features,f.data LIMIT ? OFFSET ?""",
                    (key, limit, offset),
                )
                matches = []
                for row in rows:
                    features = unpack_features(row["features"])
                    matches.append(
                        {
                            "features": features,
                            "entry": json.loads(row["entry"]),
                            "form": unpack_form(row["form"], features),
                        }
                    )
                return {"match_type": tier, "total": count, "matches": matches}
        return {"match_type": "none", "total": 0, "matches": []}

    def suggestions(self, prefix: str, limit: int = 8) -> list[str]:
        key = search_key(prefix)
        if not key:
            return []
        with self.connect() as db:
            rows = db.execute(
                """SELECT min(data) FROM forms WHERE exact_key >= ? AND exact_key < ?
                   GROUP BY exact_key ORDER BY exact_key LIMIT ?""",
                (key, key + "\U0010ffff", limit),
            )
            return [json.loads(row[0])[0] for row in rows]
