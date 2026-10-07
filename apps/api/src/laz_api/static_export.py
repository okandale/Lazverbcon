"""Publish a catalog as bounded, lazy-loaded files for the browser.

The engine remains the only rule implementation. Even validation is exported as
small, deduplicated decision tables. SQLite is a build input, never a web asset.
"""

import base64
import hashlib
import itertools
import json
import shutil
import tempfile
from dataclasses import asdict
from pathlib import Path

from laz_engine.lexicon import load_entries
from laz_engine.maintainer import prefixes
from laz_engine.models import (
    Causative,
    Derivation,
    Dialect,
    Features,
    Mood,
    OptionalPrefix,
    Person,
    Tense,
)
from laz_engine.orthography import ALTERNATES
from laz_engine.validation import validate_base

from .catalog import (
    FEATURE_FIELDS,
    FORM_FIELDS,
    Catalog,
    canonical,
    engine_revision,
    lexicon_revision,
)

DIMENSIONS = [
    list(Dialect),
    list(Person),
    [None, *Person],
    list(Tense),
    list(Mood),
    list(Derivation),
    [False, True],
    list(Causative),
    [False, True],
    list(OptionalPrefix),
]
SHARD_BYTES = 128 * 1024
MAX_FILE_BYTES = 25 * 1024 * 1024


def feature_code(values):
    code = 0
    for dimension, value in zip(DIMENSIONS, values, strict=True):
        code = code * len(dimension) + dimension.index(value)
    return code


def feature_values(code):
    values = []
    for dimension in reversed(DIMENSIONS):
        code, index = divmod(code, len(dimension))
        values.append(dimension[index])
    return list(reversed(values))


class Writer:
    def __init__(self, root):
        self.root = root
        self.files = {}

    def write(self, name, value):
        content = canonical(value).encode()
        if len(content) > MAX_FILE_BYTES:
            raise ValueError(f"Static asset exceeds 25 MiB: {name}")
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        self.files[name] = {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}

    def shards(self, name, rows, target_bytes):
        bounds, batch, size = [], [], 2

        def flush():
            filename = f"{name}/{len(bounds):04d}.json"
            self.write(filename, batch)
            bounds.append([batch[0][0], batch[-1][0], filename])

        for row in rows:
            length = len(canonical(row).encode()) + 1
            if batch and size + length > target_bytes:
                flush()
                batch, size = [], 2
            batch.append(row)
            size += length
        if batch:
            flush()
        return bounds


def validation_data(entries):
    reasons = [None]
    tables, entry_tables = [], {}
    table_ids = {}
    # Using every entry deliberately avoids a hand-maintained classification of
    # exceptions. Equal validation tables share one file representation.
    combinations = list(itertools.product(*DIMENSIONS[1:-1]))
    for entry in entries:
        codes = bytearray()
        for values in combinations:
            features = Features(entry.dialects[0], *values)
            result = validate_base(entry, features)
            reason = [result.reason, result.message] if result else None
            if reason not in reasons:
                reasons.append(reason)
            codes.append(reasons.index(reason))
        packed = bytes(codes)
        if packed not in table_ids:
            table_ids[packed] = len(tables)
            tables.append(base64.b64encode(packed).decode())
        entry_tables[entry.id] = {
            "table": table_ids[packed],
            "dialects": list(entry.dialects),
            "prefixes": {d: list(prefixes(entry.id, d)) for d in entry.dialects},
        }
    return {"reasons": reasons, "tables": tables, "entries": entry_tables}


def export_catalog(database: Path, output: Path, *, allow_partial=False, shard_bytes=SHARD_BYTES):
    catalog = Catalog(database)
    manifest = catalog.manifest
    if manifest["coverage"] != "full" and not allow_partial:
        raise ValueError(
            "Static publishing requires a full catalog; use --allow-partial only for tests."
        )
    if not manifest.get("editorial") and (
        manifest["engine_revision"],
        manifest["lexicon_revision"],
    ) != (
        engine_revision(),
        lexicon_revision(),
    ):
        raise ValueError(
            "Catalog rules or lexicon are stale; rebuild before exporting validation tables."
        )
    if output.exists():
        raise FileExistsError(f"Choose a new output directory: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix="static-", dir=output.parent))
    writer = Writer(staging)
    try:
        with catalog.connect() as db:
            entries = [json.loads(r[0]) for r in db.execute("SELECT data FROM entries ORDER BY id")]
            entry_numbers = {entry["id"]: n for n, entry in enumerate(entries)}
            source_entries = {e.id: e for e in load_entries()}
            for entry in entries:
                if not manifest.get("editorial") and canonical(
                    asdict(source_entries[entry["id"]])
                ) != canonical(entry):
                    raise ValueError(
                        f"Catalog entry differs from the source lexicon: {entry['id']}"
                    )
            writer.write("entries.json", entries)
            if manifest.get("editorial"):
                approved = {}
                for e in entries:
                    dialects = sorted(
                        {
                            json.loads(r[0])[0]
                            for r in db.execute(
                                "SELECT DISTINCT features FROM requests WHERE entry_id=?",
                                (e["id"],),
                            )
                        }
                        | {d for p in e["variants"] for d in p["dialects"]}
                    )
                    approved[e["id"]] = {
                        "table": 0,
                        "dialects": dialects,
                        "prefixes": {d: [] for d in dialects},
                    }
                writer.write(
                    "validation.json",
                    {"mode": "approved", "reasons": [], "tables": [], "entries": approved},
                )
            else:
                writer.write(
                    "validation.json", validation_data([source_entries[e["id"]] for e in entries])
                )
            # Store reverse references on disk while streaming the catalog; the
            # exporter never needs all conjugations in Python memory at once.
            db.execute("PRAGMA temp_store=FILE")
            db.execute(
                "CREATE TEMP TABLE refs (id INTEGER PRIMARY KEY, entry INTEGER, code INTEGER, form INTEGER)"
            )
            rows = db.execute("""SELECT r.entry_id,r.id,r.features,r.status,r.reason,r.message,
                f.id AS form_id,f.data FROM requests r LEFT JOIN forms f ON f.request_id=r.id
                ORDER BY r.entry_id,json_extract(r.features,'$[0]'),r.id,f.data""")
            form_count = request_count = 0
            forward = {}
            for (entry_id, dialect), group in itertools.groupby(
                rows, lambda r: (r["entry_id"], json.loads(r["features"])[0])
            ):
                forms, form_ids, requests, unsupported, refs = [], {}, {}, {}, []
                for row in group:
                    code = feature_code(json.loads(row["features"]))
                    if str(code) not in requests and str(code) not in unsupported:
                        request_count += 1
                    if row["status"] == "unsupported":
                        unsupported[str(code)] = [row["reason"], row["message"]]
                    elif row["status"] != "ok":
                        raise ValueError(f"Unpublished request status: {row['status']}")
                    else:
                        targets = requests.setdefault(str(code), [])
                        if row["data"] is not None:
                            if row["data"] not in form_ids:
                                form_ids[row["data"]] = len(forms)
                                forms.append(json.loads(row["data"]))
                            form_id = form_ids[row["data"]]
                            targets.append(form_id)
                            refs.append((row["form_id"], entry_numbers[entry_id], code, form_id))
                            form_count += 1
                filename = f"verbs/{entry_id}/{dialect}.json"
                writer.write(
                    filename, {"forms": forms, "requests": requests, "unsupported": unsupported}
                )
                forward.setdefault(entry_id, {})[dialect] = filename
                db.executemany("INSERT INTO refs VALUES (?,?,?,?)", refs)
            if (request_count, form_count) != (manifest["request_count"], manifest["form_count"]):
                raise ValueError("Catalog counts do not match the exported rows")

            def exact_rows():
                rows = db.execute("""SELECT f.exact_key,f.data,x.entry,x.code,x.form FROM forms f
                    JOIN refs x ON x.id=f.id ORDER BY f.exact_key,f.data,x.entry,x.code,x.form""")
                for key, group in itertools.groupby(rows, lambda r: r[0]):
                    grouped = list(group)
                    yield [key, json.loads(grouped[0][1])[0], [[r[2], r[3], r[4]] for r in grouped]]

            indexes = {"exact": writer.shards("exact", exact_rows(), shard_bytes)}
            for name, column in (("alternate", "strict_key"), ("broad", "broad_key")):
                rows = db.execute(
                    f"SELECT DISTINCT {column},exact_key FROM forms ORDER BY {column},exact_key"
                )
                groups = itertools.groupby(rows, lambda r: r[0])
                indexes[name] = writer.shards(
                    name, ([key, [r[1] for r in group]] for key, group in groups), shard_bytes
                )
            # Full Unicode casefold parity, including characters that JavaScript's
            # lowercasing does not expand (e.g. ß). Trim uses Python's whitespace set.
            casefold = {
                chr(i): chr(i).casefold() for i in range(0x110000) if chr(i).casefold() != chr(i)
            }
            whitespace = "".join(chr(i) for i in range(0x110000) if chr(i).isspace())
            release = {
                "schema_version": 1,
                "catalog": manifest,
                "feature_fields": FEATURE_FIELDS,
                "form_fields": FORM_FIELDS,
                "dimensions": DIMENSIONS,
                "forward": forward,
                "indexes": indexes,
                "casefold": casefold,
                "whitespace": whitespace,
                "alternates": list(ALTERNATES.items()),
            }
            # Content identity covers every data file, not just a timestamp.
            release["release"] = hashlib.sha256(
                canonical([release, writer.files]).encode()
            ).hexdigest()[:20]
            release["files"] = dict(writer.files)
            writer.write("manifest.json", release)
            report = {
                "release": release["release"],
                "requests": request_count,
                "forms": form_count,
                "file_count": len(writer.files),
                "bytes": sum(f["bytes"] for f in writer.files.values()),
                "largest_file_bytes": max(f["bytes"] for f in writer.files.values()),
            }
            if report["file_count"] > 19000:
                raise ValueError(
                    "Export leaves insufficient room under the Pages 20,000-file limit"
                )
        staging.rename(output)
        return report
    finally:
        if staging.exists():
            shutil.rmtree(staging)
