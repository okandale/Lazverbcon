"""Transactional editorial data. Generation proposes; approval changes records."""

import csv
import gzip
import hashlib
import io
import json
import os
import re
import shutil
import sqlite3
import threading
import uuid
from contextlib import closing, contextmanager
from dataclasses import asdict
from datetime import datetime, timezone
from importlib.resources import files
from pathlib import Path

from laz_api.catalog import canonical
from laz_engine.engine import conjugate, select_rule
from laz_engine.enumeration import iter_features
from laz_engine.lexicon import load_entries
from laz_engine.models import Entry, Features
from pydantic import TypeAdapter

VERSION = 1
FEATURE_ADAPTER = TypeAdapter(Features)
ENTRY_ADAPTER = TypeAdapter(Entry)
SCHEMA = """
CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE entries(id TEXT PRIMARY KEY,data TEXT NOT NULL);
CREATE TABLE records(key TEXT PRIMARY KEY,entry_id TEXT NOT NULL REFERENCES entries(id),
 features TEXT NOT NULL,value TEXT NOT NULL);
CREATE INDEX records_entry ON records(entry_id);
CREATE TABLE proposals(id TEXT PRIMARY KEY,key TEXT NOT NULL,entry_id TEXT NOT NULL,
 features TEXT NOT NULL,before_hash TEXT NOT NULL,value TEXT,actor TEXT NOT NULL,
 reason TEXT NOT NULL,batch TEXT NOT NULL,state TEXT NOT NULL DEFAULT 'pending',created TEXT NOT NULL);
CREATE INDEX proposals_state ON proposals(state,batch);
CREATE TABLE history(id INTEGER PRIMARY KEY,revision INTEGER NOT NULL,entity TEXT NOT NULL,
 key TEXT NOT NULL,before_value TEXT,after_value TEXT,actor TEXT NOT NULL,
 reason TEXT NOT NULL,created TEXT NOT NULL);
"""


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def features(value):
    if set(value) - set(Features.__dataclass_fields__):
        raise ValueError("Unknown grammatical field")
    return asdict(FEATURE_ADAPTER.validate_python(value))


def entry_data(value):
    if set(value) - set(Entry.__dataclass_fields__):
        raise ValueError("Unknown entry field")
    e = ENTRY_ADAPTER.validate_python(value)
    if not e.id or not e.infinitive.strip() or not e.dialects:
        raise ValueError("An entry needs an ID, infinitive and at least one dialect")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,99}", e.id) or e.id.upper() in {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }:
        raise ValueError(
            "Use an ID of 1–100 ASCII letters, numbers, hyphens or underscores; Windows device names are reserved"
        )
    return ENTRY_ADAPTER.dump_python(e, mode="json")


def result_data(value):
    if value is None:
        return None  # removal, held as a proposal until approved
    if value.get("status") not in ("ok", "unsupported"):
        raise ValueError("Status must be ok or unsupported")
    out = []
    for form in value.get("forms", []):
        if set(form) - {"spelling", "frame", "subject_pronoun", "object_pronoun", "rule"}:
            raise ValueError("Unknown form field")
        if not isinstance(form.get("spelling"), str) or not form["spelling"].strip():
            raise ValueError("Each form needs a spelling")
        if form["spelling"].startswith("N/A"):
            raise ValueError("Use unsupported status instead of an N/A spelling")
        if form.get("frame") not in ("Dative", "Ergative", "Nominative"):
            raise ValueError("Choose Dative, Ergative or Nominative")
        item = {
            k: form.get(k, "")
            for k in ("spelling", "frame", "subject_pronoun", "object_pronoun", "rule")
        }
        if not all(isinstance(v, str) and len(v) <= 2000 for v in item.values()):
            raise ValueError("Form values must be text of at most 2000 characters")
        item["rule"] = item["rule"] or "editorial"
        if item not in out:
            out.append(item)
    if (value["status"] == "ok") != bool(out):
        raise ValueError("Approved results need forms; unsupported results must have none")
    return {
        "status": value["status"],
        "forms": sorted(out, key=canonical),
        "reason": str(value.get("reason") or ""),
        "source": str(value.get("source") or ""),
    }


def linguistic_value(value):
    """Provenance changes alone are not a new conjugation proposal."""
    if value is None:
        return None
    return {
        "status": value["status"],
        "forms": sorted(
            [{k: v for k, v in form.items() if k != "rule"} for form in value["forms"]],
            key=canonical,
        ),
    }


class Store:
    def __init__(self, directory):
        self.directory = Path(directory).resolve()
        self.directory.mkdir(parents=True, exist_ok=True)
        self.path = self.directory / "master.sqlite"
        self.lock = threading.RLock()
        if not self.path.exists():
            with closing(sqlite3.connect(self.path)) as db, db:
                db.executescript(SCHEMA)
                db.executemany(
                    "INSERT INTO meta VALUES (?,?)",
                    [
                        ("schema", str(VERSION)),
                        ("project", str(uuid.uuid4())),
                        ("revision", "0"),
                        ("remote_base", "null"),
                        ("settings", "{}"),
                    ],
                )
        self.check(self.path)

    @staticmethod
    def check(path):
        with closing(sqlite3.connect(Path(path).resolve().as_uri() + "?mode=ro", uri=True)) as db:
            if db.execute("SELECT value FROM meta WHERE key='schema'").fetchone() != (
                str(VERSION),
            ):
                raise ValueError("This project needs a different app version; it was not modified")
            if db.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                raise ValueError("Database integrity check failed")
            if db.execute("PRAGMA foreign_key_check").fetchone():
                raise ValueError("Database has broken references")
            columns = {
                "entries": "id,data",
                "records": "key,entry_id,features,value",
                "proposals": "id,key,entry_id,features,before_hash,value,actor,reason,batch,state,created",
                "history": "id,revision,entity,key,before_value,after_value,actor,reason,created",
            }
            for table, fields in columns.items():
                db.execute(f"SELECT {fields} FROM {table} LIMIT 0")
            metadata = dict(db.execute("SELECT key,value FROM meta"))
            if not {"schema", "project", "revision", "settings", "remote_base"} <= metadata.keys():
                raise ValueError("Backup metadata is incomplete")
            uuid.UUID(metadata["project"])
            if int(metadata["revision"]) < 0 or not isinstance(
                json.loads(metadata["settings"]), dict
            ):
                raise ValueError("Backup metadata is invalid")
            base = json.loads(metadata["remote_base"])
            if base is not None and not isinstance(base, str):
                raise ValueError("Backup publication state is invalid")

    @contextmanager
    def db(self, write=False):
        with self.lock:
            db = sqlite3.connect(self.path, timeout=30)
            db.row_factory = sqlite3.Row
            db.execute("PRAGMA foreign_keys=ON")
            try:
                if write:
                    db.execute("BEGIN IMMEDIATE")
                yield db
                if write:
                    db.commit()
            except BaseException:
                db.rollback()
                raise
            finally:
                db.close()

    @staticmethod
    def meta(db, key):
        return db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()[0]

    @staticmethod
    def set_meta(db, key, value):
        db.execute("INSERT OR REPLACE INTO meta VALUES (?,?)", (key, value))

    def event(self, db, entity, key, before, after, actor, reason):
        if not actor.strip():
            raise ValueError("Enter your name for the change history")
        revision = int(self.meta(db, "revision")) + 1
        self.set_meta(db, "revision", str(revision))
        db.execute(
            "INSERT INTO history(revision,entity,key,before_value,after_value,actor,reason,created) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (
                revision,
                entity,
                key,
                canonical(before) if before is not None else None,
                canonical(after) if after is not None else None,
                actor,
                reason,
                now(),
            ),
        )
        return revision

    def status(self):
        with self.db() as db:
            return {
                **dict(db.execute("SELECT key,value FROM meta")),
                "entries": db.execute("SELECT count(*) FROM entries").fetchone()[0],
                "records": db.execute("SELECT count(*) FROM records").fetchone()[0],
                "pending": db.execute(
                    "SELECT count(*) FROM proposals WHERE state='pending'"
                ).fetchone()[0],
                "directory": str(self.directory),
            }

    def entries(self, query=""):
        with self.db() as db:
            rows = [json.loads(r[0]) for r in db.execute("SELECT data FROM entries ORDER BY id")]
            return [
                r
                for r in rows
                if query.casefold()
                in f"{r['infinitive']} {r['english']} {r['turkish']} {r['id']}".casefold()
            ]

    def save_entry(self, value, actor, reason, expected=None):
        value = entry_data(value)
        with self.db(True) as db:
            row = db.execute("SELECT data FROM entries WHERE id=?", (value["id"],)).fetchone()
            before = json.loads(row[0]) if row else None
            if before != expected:
                raise ValueError("Entry changed since it was opened. Reload before saving.")
            db.execute(
                "INSERT INTO entries VALUES (?,?) ON CONFLICT(id) DO UPDATE SET data=excluded.data",
                (value["id"], canonical(value)),
            )
            self.event(db, "entry", value["id"], before, value, actor, reason)
        return value

    def records(self, entry_id, query="", offset=0, limit=100, filters=None):
        with self.db() as db:
            args = (entry_id, f"%{query}%")
            where = "entry_id=? AND (value LIKE ?)"
            if filters:
                normalized = features({"dialect": "AS", "subject": "1sg", **filters})
                for key in filters:
                    where += " AND json_extract(features, ?) IS ?"
                    args += (f"$.{key}", normalized[key])
            count = db.execute(f"SELECT count(*) FROM records WHERE {where}", args).fetchone()[0]
            rows = db.execute(
                f"SELECT * FROM records WHERE {where} ORDER BY json_extract(features,'$.dialect'), json_extract(features,'$.tense'), json_extract(features,'$.subject'), key LIMIT ? OFFSET ?",
                (*args, min(limit, 200), max(offset, 0)),
            )
            return {
                "total": count,
                "records": [
                    {
                        **dict(r),
                        "features": json.loads(r["features"]),
                        "value": json.loads(r["value"]),
                    }
                    for r in rows
                ],
            }

    def before_hash(self, db, entry_id, key):
        entry = db.execute("SELECT data FROM entries WHERE id=?", (entry_id,)).fetchone()
        if not entry:
            raise ValueError("Unknown entry")
        row = db.execute("SELECT value FROM records WHERE key=?", (key,)).fetchone()
        return digest([entry[0], row[0] if row else None])

    def propose(self, items, actor, reason, batch=None):
        if not actor.strip():
            raise ValueError("Enter your name")
        batch = batch or str(uuid.uuid4())
        count = 0
        with self.db(True) as db:
            for item in items:
                f = features(item["features"])
                key = digest([item["entry_id"], f])
                value = result_data(item["value"])
                before = self.before_hash(db, item["entry_id"], key)
                if item.get("expected_hash") and item["expected_hash"] != before:
                    raise ValueError("The form changed since it was opened. Reload before saving.")
                current = db.execute("SELECT value FROM records WHERE key=?", (key,)).fetchone()
                encoded = canonical(value) if value is not None else None
                if linguistic_value(
                    json.loads(current[0]) if current else None
                ) == linguistic_value(value):
                    continue
                duplicate = db.execute(
                    "SELECT 1 FROM proposals WHERE key=? AND before_hash=? "
                    "AND value IS ? AND state='pending'",
                    (key, before, encoded),
                ).fetchone()
                if duplicate:
                    continue
                db.execute(
                    "INSERT INTO proposals(id,key,entry_id,features,before_hash,value,actor,reason,batch,created) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (
                        str(uuid.uuid4()),
                        key,
                        item["entry_id"],
                        canonical(f),
                        before,
                        encoded,
                        actor,
                        reason,
                        batch,
                        now(),
                    ),
                )
                count += 1
        return {"batch": batch, "proposals": count}

    def proposals(self, batch=None, offset=0):
        with self.db() as db:
            where = "state='pending'" + (" AND batch=?" if batch else "")
            args = (batch,) if batch else ()
            count = db.execute(f"SELECT count(*) FROM proposals WHERE {where}", args).fetchone()[0]
            rows = db.execute(
                f"SELECT * FROM proposals WHERE {where} ORDER BY created,id LIMIT 100 OFFSET ?",
                (*args, max(0, offset)),
            )
            out = []
            for r in rows:
                old = db.execute("SELECT value FROM records WHERE key=?", (r["key"],)).fetchone()
                out.append(
                    {
                        **dict(r),
                        "features": json.loads(r["features"]),
                        "before": json.loads(old[0]) if old else None,
                        "value": json.loads(r["value"]) if r["value"] else None,
                        "conflict": self.before_hash(db, r["entry_id"], r["key"])
                        != r["before_hash"],
                    }
                )
            return {"total": count, "proposals": out}

    def review(self, ids, approve, actor):
        if not isinstance(approve, bool):
            raise ValueError("Approval must be true or false")
        if not ids or len(ids) > 10000 or not actor.strip():
            raise ValueError("Select up to 10,000 proposals and enter your name")
        with self.db(True) as db:
            for ident in dict.fromkeys(ids):
                r = db.execute(
                    "SELECT * FROM proposals WHERE id=? AND state='pending'", (ident,)
                ).fetchone()
                if not r:
                    raise ValueError("Proposal has already been reviewed")
                if approve and self.before_hash(db, r["entry_id"], r["key"]) != r["before_hash"]:
                    raise ValueError("Conflicting proposal: approved data or entry has changed")
                old = db.execute("SELECT value FROM records WHERE key=?", (r["key"],)).fetchone()
                before = json.loads(old[0]) if old else None
                after = json.loads(r["value"]) if r["value"] else None
                if approve:
                    if after is None:
                        db.execute("DELETE FROM records WHERE key=?", (r["key"],))
                    else:
                        db.execute(
                            "INSERT OR REPLACE INTO records VALUES (?,?,?,?)",
                            (r["key"], r["entry_id"], r["features"], r["value"]),
                        )
                    # Include feature identity so removal can be undone without a side table.
                    self.event(
                        db,
                        "record",
                        r["key"],
                        {
                            "entry_id": r["entry_id"],
                            "features": json.loads(r["features"]),
                            "value": before,
                        },
                        {
                            "entry_id": r["entry_id"],
                            "features": json.loads(r["features"]),
                            "value": after,
                        },
                        actor,
                        f"{r['reason']} (proposal by {r['actor']}; batch {r['batch']})",
                    )
                else:
                    self.event(
                        db, "rejection", ident, None, {"batch": r["batch"]}, actor, r["reason"]
                    )
                db.execute(
                    "UPDATE proposals SET state=? WHERE id=?",
                    ("approved" if approve else "rejected", ident),
                )
        return {"reviewed": len(set(ids))}

    def history(self, offset=0):
        with self.db() as db:
            return [
                dict(r)
                for r in db.execute(
                    "SELECT * FROM history ORDER BY id DESC LIMIT 100 OFFSET ?", (max(offset, 0),)
                )
            ]

    def undo(self, ident, actor):
        with self.db(True) as db:
            event = db.execute("SELECT * FROM history WHERE id=?", (ident,)).fetchone()
            if not event or event["entity"] not in ("entry", "record"):
                raise ValueError("This history event cannot be reversed individually")
            before = json.loads(event["before_value"]) if event["before_value"] else None
            after = json.loads(event["after_value"]) if event["after_value"] else None
            if event["entity"] == "entry":
                current = db.execute(
                    "SELECT data FROM entries WHERE id=?", (event["key"],)
                ).fetchone()
                if (json.loads(current[0]) if current else None) != after:
                    raise ValueError("Later edits exist; review them before undoing")
                if before is None:
                    if db.execute(
                        "SELECT 1 FROM proposals WHERE entry_id=?", (event["key"],)
                    ).fetchone():
                        raise ValueError("Entry has proposals; retain it for their history")
                    db.execute("DELETE FROM entries WHERE id=?", (event["key"],))
                else:
                    db.execute(
                        "INSERT INTO entries VALUES (?,?) ON CONFLICT(id) DO UPDATE SET data=excluded.data",
                        (event["key"], canonical(before)),
                    )
            else:
                current = db.execute(
                    "SELECT value FROM records WHERE key=?", (event["key"],)
                ).fetchone()
                if (json.loads(current[0]) if current else None) != after["value"]:
                    raise ValueError("Later edits exist; review them before undoing")
                if before["value"] is None:
                    db.execute("DELETE FROM records WHERE key=?", (event["key"],))
                else:
                    db.execute(
                        "INSERT OR REPLACE INTO records VALUES (?,?,?,?)",
                        (
                            event["key"],
                            before["entry_id"],
                            canonical(before["features"]),
                            canonical(before["value"]),
                        ),
                    )
            self.event(
                db, event["entity"], event["key"], after, before, actor, f"Undo event {ident}"
            )

    def settings(self, value=None):
        with self.db(value is not None) as db:
            if value is not None:
                allowed = {"actor", "backup_directory", "repository", "branch"}
                if set(value) - allowed:
                    raise ValueError("Unknown setting; credentials are never saved here")
                if not all(isinstance(v, str) for v in value.values()):
                    raise ValueError("Settings must contain text values")
                self.set_meta(db, "settings", canonical(value))
            return json.loads(self.meta(db, "settings"))

    def backup(self, daily=False, label="manual", copy_external=True):
        with self.lock:
            folder = self.directory / "backups"
            folder.mkdir(exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime(
                "%Y-%m-%d" if daily else "%Y-%m-%d-%H%M%S-%f"
            )
            name = f"{'daily' if daily else label}-{stamp}.sqlite"
            target = folder / name
            if not target.exists():
                with self.db() as source:
                    dest = sqlite3.connect(str(target) + ".tmp")
                    try:
                        source.backup(dest)
                    finally:
                        dest.close()
                Path(str(target) + ".tmp").replace(target)
            external = self.settings().get("backup_directory")
            if external and copy_external:
                copy = Path(external).expanduser() / self.status()["project"] / name
                copy.parent.mkdir(parents=True, exist_ok=True)
                if not copy.exists():
                    shutil.copyfile(target, str(copy) + ".tmp")
                    Path(str(copy) + ".tmp").replace(copy)
                for old in sorted(copy.parent.glob("daily-*.sqlite"))[:-14]:
                    old.unlink()
            for old in sorted(folder.glob("daily-*.sqlite"))[:-14]:
                old.unlink()
            return str(target)

    def restore(self, source, actor):
        if not actor.strip():
            raise ValueError("Enter your name before restoring")
        source = Path(source).resolve()
        if source == self.path:
            raise ValueError("Choose a backup, not the open project")
        self.check(source)
        with self.lock:
            backup = self.backup(label="before-restore")
            staging = self.directory / "restore.sqlite"
            with closing(sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)) as src:
                with closing(sqlite3.connect(staging)) as dst:
                    src.backup(dst)
            self.check(staging)
            os.replace(staging, self.path)
            with self.db(True) as db:
                self.event(
                    db,
                    "restore",
                    "project",
                    None,
                    {"backup": source.name},
                    actor,
                    "Project restored",
                )
            return {"previous_backup": backup}

    def seed(self, fixture, actor, progress=lambda n: None, cancelled=lambda: False):
        pronouns = json.loads(
            files("laz_admin").joinpath("data/pronouns.json").read_text(encoding="utf-8")
        )
        entries = {e.id: e for e in load_entries()}
        with self.db(True) as db, gzip.open(fixture, "rt", encoding="utf-8") as stream:
            if (
                db.execute("SELECT count(*) FROM records").fetchone()[0]
                or db.execute("SELECT count(*) FROM entries").fetchone()[0]
            ):
                raise ValueError(
                    "Baseline import requires an empty project; existing data was retained"
                )
            header = json.loads(next(stream))
            if header["feature_fields"] != list(Features.__dataclass_fields__):
                raise ValueError("Baseline feature schema differs from this application")
            db.executemany(
                "INSERT INTO entries VALUES (?,?)",
                [(e.id, canonical(asdict(e))) for e in entries.values()],
            )
            count = rows = 0
            for line in stream:
                eid, packed, forms, source_ids = json.loads(line)
                f = features(dict(zip(header["feature_fields"], packed, strict=True)))
                typed = FEATURE_ADAPTER.validate_python(f)
                rule = select_rule(entries[eid], typed)[0]

                def pronoun(person, role, frame):
                    return (
                        pronouns[f"{f['dialect']}|{role}{person.upper()}|{frame}"] if person else ""
                    )

                value = {
                    "status": "ok" if forms else "unsupported",
                    "forms": [
                        {
                            "spelling": spelling,
                            "frame": frame,
                            "rule": rule,
                            "subject_pronoun": pronoun(f["subject"], "S", frame),
                            "object_pronoun": pronoun(f["object"], "O", frame),
                        }
                        for spelling, frame in forms
                    ],
                    "reason": "" if forms else "Rejected in maintainer database",
                    "source": "lazverbcon2.dump rows " + ",".join(source_ids),
                }
                db.execute(
                    "INSERT INTO records VALUES (?,?,?,?)",
                    (digest([eid, f]), eid, canonical(f), canonical(value)),
                )
                count += 1
                rows += len(source_ids)
                if count % 2000 == 0:
                    progress(count)
                    if cancelled():
                        raise ValueError("Cancelled; baseline import rolled back")
            if count != header["requests"] or rows != header["rows"]:
                raise ValueError("Baseline is incomplete")
            self.event(
                db,
                "baseline",
                "project",
                None,
                header,
                actor,
                "Imported authoritative maintainer data and pronouns",
            )
            return {"requests": count, "source_rows": rows}

    def generate(
        self, entry_id, actor, profile="full", progress=lambda n: None, cancelled=lambda: False
    ):
        with self.db() as db:
            row = db.execute("SELECT data FROM entries WHERE id=?", (entry_id,)).fetchone()
            if not row:
                raise ValueError("Unknown entry")
            entry = ENTRY_ADAPTER.validate_json(row[0])
            entry_hash = digest(json.loads(row[0]))
            revision = self.meta(db, "revision")
        items = []
        for i, f in enumerate(iter_features(entry, profile)):
            if cancelled():
                raise ValueError("Cancelled; no proposals saved")
            result = conjugate(entry, f)
            if result.status == "ok":
                forms = [
                    {k: v for k, v in asdict(form).items() if k not in ("subject", "object")}
                    for form in result.forms
                ]
                items.append(
                    {
                        "entry_id": entry_id,
                        "features": asdict(f),
                        "value": {"status": "ok", "forms": forms, "source": "Generated proposal"},
                    }
                )
            if i % 100 == 0:
                progress(i)
        with self.lock, self.db() as db:
            if self.meta(db, "revision") != revision:
                raise ValueError("Project changed during generation; run it again")
            if (
                digest(
                    json.loads(
                        db.execute("SELECT data FROM entries WHERE id=?", (entry_id,)).fetchone()[0]
                    )
                )
                != entry_hash
            ):
                raise ValueError("Entry changed during generation; run it again")
            return self.propose(items, actor, "Generated; requires linguistic review")


def parse_import(text, kind):
    """Strict documented formats; parse the complete file before any writes."""
    if kind == "json":
        rows = json.loads(text)
        if not isinstance(rows, list):
            raise ValueError("JSON import must be a list of requests")
    elif kind == "csv":
        grouped = {}
        for row in csv.DictReader(io.StringIO(text)):
            f = {k: row[k] for k in Features.__dataclass_fields__ if row.get(k, "") != ""}
            for k in ("applicative", "optional_preverb"):
                if k in f:
                    if f[k].lower() not in ("true", "false"):
                        raise ValueError(f"{k} must be true or false")
                    f[k] = f[k].lower() == "true"
            f = features(f)
            key = digest([row["entry_id"], f])
            item = grouped.setdefault(
                key,
                {
                    "entry_id": row["entry_id"],
                    "features": f,
                    "value": {"status": "ok", "forms": [], "source": "CSV import"},
                },
            )
            item["value"]["forms"].append(
                {
                    k: row.get(k, "")
                    for k in ("spelling", "frame", "subject_pronoun", "object_pronoun", "rule")
                }
            )
        rows = list(grouped.values())
    else:
        raise ValueError("Choose json or csv")
    if not rows or len(rows) > 10000:
        raise ValueError("Import between 1 and 10,000 requests per file")
    normalized = [
        {
            "entry_id": r["entry_id"],
            "features": features(r["features"]),
            "value": result_data(r["value"]),
        }
        for r in rows
    ]
    if len({digest([r["entry_id"], r["features"]]) for r in normalized}) != len(normalized):
        raise ValueError("Combine alternatives for the same grammatical request into one JSON item")
    return normalized
