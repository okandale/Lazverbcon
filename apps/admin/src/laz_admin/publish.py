"""Snapshot approved records, then publish a pinned static data release."""

import base64
import hashlib
import json
import re
import sqlite3
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from contextlib import closing
from importlib.metadata import version
from pathlib import Path

from laz_api.catalog import FEATURE_FIELDS, FORM_FIELDS, SCHEMA, SCHEMA_VERSION, canonical
from laz_api.static_export import export_catalog
from laz_engine.lexicon import search_key
from laz_engine.orthography import broad_key, strict_key

from .credentials import validate_token
from .store import now

POINTER = "published/catalog.json"


def snapshot(store, output, progress=lambda n: None, cancelled=lambda: False):
    """A single read transaction yields a coherent approved release."""
    if output.exists():
        raise ValueError("Snapshot already exists")
    with store.db() as source, closing(sqlite3.connect(output)) as target:
        source.execute("BEGIN")
        target.executescript(SCHEMA)
        entries = list(source.execute("SELECT * FROM entries ORDER BY id"))
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "app_version": version("lazverbcon"),
            "status": "ready",
            "coverage": "full",
            "profile": "editorial",
            "editorial": True,
            "complete_lexicon": False,
            "created_at": now(),
            "project": store.meta(source, "project"),
            "revision": int(store.meta(source, "revision")),
            "engine_revision": "editorial",
            "lexicon_revision": hashlib.sha256(
                canonical([r["data"] for r in entries]).encode()
            ).hexdigest(),
            "entry_count": len(entries),
            "request_count": 0,
            "form_count": 0,
            "errors": [],
            "data_issues": [],
            "unsupported": {},
        }
        for row in entries:
            e = json.loads(row["data"])
            target.execute(
                "INSERT INTO entries VALUES (?,?,?)",
                (
                    e["id"],
                    row["data"],
                    search_key(f"{e['infinitive']} {e['english']} {e['turkish']}"),
                ),
            )
        for i, row in enumerate(source.execute("SELECT * FROM records ORDER BY key")):
            f, value = json.loads(row["features"]), json.loads(row["value"])
            cursor = target.execute(
                "INSERT INTO requests(request_key,entry_id,features,status,reason,message) "
                "VALUES (?,?,?,?,?,?)",
                (
                    bytes.fromhex(row["key"]),
                    row["entry_id"],
                    canonical([f[k] for k in FEATURE_FIELDS]),
                    value["status"],
                    "editorial_rejection" if value["status"] != "ok" else None,
                    "Marked unavailable in approved data" if value["status"] != "ok" else None,
                ),
            )
            for form in value["forms"]:
                target.execute(
                    "INSERT INTO forms(request_id,data,exact_key,strict_key,broad_key) VALUES (?,?,?,?,?)",
                    (
                        cursor.lastrowid,
                        canonical([form[k] for k in FORM_FIELDS]),
                        search_key(form["spelling"]),
                        strict_key(form["spelling"]),
                        broad_key(form["spelling"]),
                    ),
                )
                manifest["form_count"] += 1
            manifest["request_count"] += 1
            if i % 2000 == 0:
                progress(i)
                if cancelled():
                    raise ValueError("Export cancelled")
        if not manifest["form_count"]:
            raise ValueError("Approve at least one form before exporting")
        target.execute("INSERT INTO metadata VALUES ('manifest', ?)", (canonical(manifest),))
        target.commit()
    return manifest


def export_release(store, actor, progress=lambda n: None, cancelled=lambda: False):
    folder = store.directory / "exports"
    folder.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=folder) as work:
        work = Path(work)
        manifest = snapshot(store, work / "snapshot.sqlite", progress, cancelled)
        if cancelled():
            raise ValueError("Export cancelled")
        report = export_catalog(work / "snapshot.sqlite", work / "data")
        if cancelled():
            raise ValueError("Export cancelled")
        target = folder / f"catalog-{report['release']}.zip"
        with zipfile.ZipFile(work / "release.zip", "w", zipfile.ZIP_DEFLATED) as archive:
            for path in sorted((work / "data").rglob("*.json")):
                archive.write(path, path.relative_to(work / "data").as_posix())
        (work / "release.zip").replace(target)
        sha = hashlib.sha256(target.read_bytes()).hexdigest()
        info = {
            **report,
            "project": manifest["project"],
            "revision": manifest["revision"],
            "sha256": sha,
            "filename": target.name,
        }
        target.with_suffix(".json").write_text(json.dumps(info, indent=2) + "\n")
    with store.db(True) as db:
        store.event(db, "export", info["release"], None, info, actor, "Exported approved snapshot")
    return info


class GitHub:
    def __init__(self, token):
        self.token = validate_token(token)

    def request(self, method, path, data=None, binary=False):
        url = (
            path
            if path.startswith("https://uploads.github.com/")
            else "https://api.github.com" + path
        )
        body = data if binary else (json.dumps(data).encode() if data is not None else None)
        request = urllib.request.Request(
            url,
            data=body,
            method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/zip" if binary else "application/json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "Lazuri-Admin",
            },
        )
        try:
            # Refuse authenticated redirects rather than forward a token elsewhere.
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    return None

            with urllib.request.build_opener(NoRedirect()).open(request, timeout=180) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code == 404 and method == "GET":
                return None
            raise ValueError(
                f"GitHub returned HTTP {exc.code}. Check repository permissions and branch; retry after reviewing GitHub."
            ) from None


def publish(store, info_name, actor, token, repository, branch, github=None):
    if not actor.strip() or not token.strip():
        raise ValueError("Enter an editor name and GitHub token")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository) or not branch:
        raise ValueError("Enter owner/repository and a branch")
    if Path(info_name).name != info_name or not info_name.endswith(".zip"):
        raise ValueError("Choose a locally exported release")
    archive = store.directory / "exports" / info_name
    info = json.loads(archive.with_suffix(".json").read_text(encoding="utf-8"))
    if hashlib.sha256(archive.read_bytes()).hexdigest() != info["sha256"]:
        raise ValueError("Export checksum differs; export again")
    client = github or GitHub(token)
    root = f"/repos/{repository}"
    repo = client.request("GET", root)
    if not repo or repo.get("private", True):
        raise ValueError("Publishing currently requires an accessible public GitHub repository")
    pointer_path = f"{root}/contents/{POINTER}"
    pointer = client.request("GET", pointer_path + "?ref=" + urllib.parse.quote(branch, safe=""))
    current = json.loads(base64.b64decode(pointer["content"])) if pointer else None
    with store.db() as db:
        expected = json.loads(store.meta(db, "remote_base"))
        project = store.meta(db, "project")
    if info["project"] != project:
        raise ValueError("Export belongs to a different project")
    remote_id = current["release"] if current else None
    if (
        current
        and remote_id == info["release"]
        and current.get("sha256") == info["sha256"]
        and current.get("project") == project
    ):
        # Recover a publication that reached GitHub before this process stopped.
        with store.db(True) as db:
            store.set_meta(db, "remote_base", canonical(remote_id))
            store.event(
                db,
                "publish",
                remote_id,
                None,
                current,
                actor,
                "Verified existing GitHub publication",
            )
        store.backup(label="after-publish")
        return {
            "release": remote_id,
            "url": current["url"],
            "message": "This export is already published; local publication state recovered.",
        }
    if remote_id != expected or (current and current["project"] != project):
        raise ValueError(
            "GitHub has a different published revision. Restore the current master backup before publishing."
        )
    tag = "catalog-" + info["release"] + "-" + uuid.uuid4().hex[:8]
    release = client.request(
        "POST",
        root + "/releases",
        {
            "tag_name": tag,
            "target_commitish": branch,
            "name": f"Approved catalogue revision {info['revision']}",
            "draft": True,
            "body": "Approved public conjugation data. No drafts or editorial history.",
        },
    )
    upload = release["upload_url"].split("{", 1)[0] + "?name=catalog.zip"
    asset = client.request("POST", upload, archive.read_bytes(), binary=True)
    published = client.request("PATCH", root + "/releases/" + str(release["id"]), {"draft": False})
    # A draft upload can have an untagged-* URL that changes on publication.
    asset = next((a for a in published["assets"] if a["id"] == asset["id"]), None)
    if not asset or asset.get("state") != "uploaded":
        raise ValueError("Published archive is unavailable; do not update the release pointer")
    public = {k: info[k] for k in ("release", "project", "revision", "sha256")}
    public["url"] = asset["browser_download_url"]
    body = {
        "message": f"Publish approved catalogue {info['release']}",
        "branch": branch,
        "content": base64.b64encode((json.dumps(public, indent=2) + "\n").encode()).decode(),
    }
    if pointer:
        body["sha"] = pointer["sha"]  # GitHub rejects a concurrent publication.
    client.request("PUT", pointer_path, body)
    with store.db(True) as db:
        store.set_meta(db, "remote_base", canonical(info["release"]))
        store.event(
            db,
            "publish",
            info["release"],
            current,
            public,
            actor,
            f"Published to {repository}:{branch}",
        )
    store.backup(label="after-publish")
    return {
        "release": info["release"],
        "url": asset["browser_download_url"],
        "message": "GitHub updated. Check the Cloudflare deployment for completion.",
    }
