"""Loopback-only admin HTTP interface; all project access needs a session token."""

import json
import secrets
import sqlite3
import threading
import uuid
from contextlib import asynccontextmanager
from importlib.resources import files
from pathlib import Path
from urllib.parse import unquote

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from laz_api.static_export import DIMENSIONS
from laz_engine.models import Features
from starlette.concurrency import run_in_threadpool

from .preview import Preview
from .publish import export_release, publish
from .store import Store, parse_import


class Jobs:
    def __init__(self):
        self.lock = threading.Lock()
        self.current = None
        self.cancel = threading.Event()

    def start(self, name, fn):
        with self.lock:
            if self.current and self.current["state"] == "running":
                raise ValueError("A job is already running")
            self.cancel.clear()
            job = {"id": str(uuid.uuid4()), "name": name, "state": "running", "progress": 0}
            self.current = job

        def progress(n):
            job["progress"] = n

        def run():
            try:
                job["result"] = fn(progress, self.cancel.is_set)
                job["state"] = "complete"
            except Exception as exc:
                job["error"] = str(exc)
                job["state"] = "failed"

        threading.Thread(target=run, daemon=True).start()
        return job


def create_app(
    store: Store, token=None, seed_path=None, shutdown=lambda: None, preview_assets=None
):
    token = token or secrets.token_urlsafe(32)
    preview = Preview(store, preview_assets)

    @asynccontextmanager
    async def lifespan(app):
        yield
        preview.close()

    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)
    app.state.token = token
    jobs = Jobs()
    app.state.jobs = jobs
    assets = Path(str(files("laz_admin").joinpath("assets")))

    @app.middleware("http")
    async def protect(request, call_next):
        if request.url.hostname not in ("127.0.0.1", "localhost"):
            return JSONResponse({"detail": "Invalid host"}, status_code=403)
        origin = request.headers.get("origin")
        if origin and origin != f"{request.url.scheme}://{request.headers.get('host')}":
            return JSONResponse({"detail": "Invalid origin"}, status_code=403)
        if request.url.path.startswith("/api/"):
            if not secrets.compare_digest(request.headers.get("X-Laz-Session", ""), token):
                return JSONResponse(
                    {"detail": "Open the editor using its launcher"}, status_code=403
                )
            if request.method != "GET" and request.url.path != "/api/restore":
                size = 0
                chunks = []
                async for chunk in request.stream():
                    size += len(chunk)
                    if size > 24 * 1024**2:
                        return JSONResponse(
                            {"detail": "Split imports into files under 20 MiB"}, status_code=413
                        )
                    chunks.append(chunk)
                request._body = b"".join(chunks)
            if request.method != "GET" and request.url.path not in ("/api/cancel",):
                if jobs.current and jobs.current["state"] == "running":
                    return JSONResponse(
                        {"detail": "Wait for the current job or cancel it first"}, status_code=409
                    )
                # Consistent daily backup before writes; only the first request per day copies.
                try:
                    await run_in_threadpool(
                        store.backup, daily=True, copy_external=request.url.path != "/api/settings"
                    )
                except OSError:
                    return JSONResponse(
                        {"detail": "Backup failed. Check the configured backup folder."},
                        status_code=409,
                    )
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'"
        )
        return response

    @app.exception_handler(ValueError)
    async def invalid(request, exc):
        return JSONResponse({"detail": str(exc)}, status_code=400)

    @app.exception_handler(KeyError)
    async def missing(request, exc):
        return JSONResponse({"detail": f"Missing field: {exc}"}, status_code=400)

    @app.exception_handler(sqlite3.DatabaseError)
    async def database_error(request, exc):
        return JSONResponse(
            {
                "detail": "Database operation failed. Check that the file is a valid admin backup and the disk has space."
            },
            status_code=400,
        )

    @app.get("/")
    def index():
        return FileResponse(assets / "index.html")

    app.mount("/admin-assets", StaticFiles(directory=assets), name="admin-assets")

    @app.get("/api/status")
    def status():
        return {
            **store.status(),
            "settings": store.settings(),
            "seed_available": bool(seed_path and Path(seed_path).exists()),
            "preview_available": preview.available,
            "dimensions": dict(zip(Features.__dataclass_fields__, DIMENSIONS, strict=True)),
        }

    @app.get("/api/job")
    def job():
        return jobs.current

    @app.post("/api/cancel")
    def cancel():
        jobs.cancel.set()
        return {"message": "Cancellation requested; waiting for a safe stopping point"}

    @app.post("/api/settings")
    def settings(body: dict):
        store.settings(body)
        return {"saved": True}

    @app.get("/api/entries")
    def entries(q: str = ""):
        return store.entries(q)

    @app.post("/api/entry")
    def save_entry(body: dict):
        return store.save_entry(
            body["entry"], body["actor"], body.get("reason", ""), body.get("expected")
        )

    @app.get("/api/records/{entry_id}")
    def records(entry_id: str, q: str = "", offset: int = 0, filters: str = "{}"):
        result = store.records(entry_id, q, offset, filters=json.loads(filters))
        with store.db() as db:
            for row in result["records"]:
                row["expected_hash"] = store.before_hash(db, entry_id, row["key"])
        return result

    @app.post("/api/proposal")
    def proposal(body: dict):
        return store.propose(body["items"], body["actor"], body.get("reason", "Manual correction"))

    @app.get("/api/proposals")
    def proposals(offset: int = 0, batch: str | None = None):
        return store.proposals(batch, offset)

    @app.post("/api/review")
    def review(body: dict):
        return store.review(body["ids"], body["approve"], body["actor"])

    @app.get("/api/history")
    def history(offset: int = 0):
        return store.history(offset)

    @app.post("/api/undo")
    def undo(body: dict):
        store.undo(body["id"], body["actor"])
        return {"undone": body["id"]}

    @app.post("/api/seed")
    def seed(body: dict):
        if not seed_path or not Path(seed_path).exists():
            raise ValueError("Baseline not bundled. Use a project backup or the source checkout.")
        return jobs.start(
            "Import maintainer baseline", lambda p, c: store.seed(seed_path, body["actor"], p, c)
        )

    @app.post("/api/generate")
    def generate(body: dict):
        return jobs.start(
            "Generate proposals",
            lambda p, c: store.generate(
                body["entry_id"], body["actor"], body.get("profile", "full"), p, c
            ),
        )

    @app.post("/api/import-preview")
    def import_preview(body: dict):
        items = parse_import(body["text"], body["format"])
        return {"requests": len(items), "sample": items[:5]}

    @app.post("/api/import")
    def import_data(body: dict):
        items = parse_import(body["text"], body["format"])
        store.backup(label="before-import")
        return store.propose(items, body["actor"], body.get("reason", "Imported file"))

    @app.post("/api/backup")
    def backup():
        return {"path": store.backup()}

    @app.get("/api/backups")
    def backups():
        return [
            {"name": p.name, "bytes": p.stat().st_size}
            for p in sorted((store.directory / "backups").glob("*.sqlite"), reverse=True)
        ]

    @app.post("/api/restore")
    async def restore(request: Request):
        # Browser-selected file streamed to disk; never accept a path to an arbitrary DB.
        actor = unquote(request.headers.get("X-Laz-Actor", "")).strip()
        if not actor:
            raise ValueError("Enter your name before restoring")
        target = store.directory / ("upload-" + uuid.uuid4().hex + ".sqlite")
        size = 0
        try:
            with target.open("wb") as dest:
                async for chunk in request.stream():
                    size += len(chunk)
                    if size > 4 * 1024**3:
                        raise ValueError("Backup exceeds 4 GiB")
                    dest.write(chunk)
            return store.restore(target, actor)
        finally:
            target.unlink(missing_ok=True)

    @app.get("/api/download/{kind}/{name}")
    def download(kind: str, name: str):
        if kind not in ("backups", "exports") or Path(name).name != name:
            raise HTTPException(404)
        path = store.directory / kind / name
        if not path.is_file() or path.suffix not in (".sqlite", ".zip"):
            raise HTTPException(404)
        return FileResponse(path, filename=name)

    @app.post("/api/export")
    def export(body: dict):
        return jobs.start(
            "Export approved data", lambda p, c: export_release(store, body["actor"], p, c)
        )

    @app.get("/api/exports")
    def exports():
        return [
            json.loads(p.read_text(encoding="utf-8"))
            for p in sorted((store.directory / "exports").glob("*.json"), reverse=True)
        ]

    @app.post("/api/publish")
    def publish_release(body: dict):
        return jobs.start(
            "Publish to GitHub",
            lambda p, c: publish(
                store,
                body["filename"],
                body["actor"],
                body["token"],
                body["repository"],
                body["branch"],
            ),
        )

    @app.post("/api/preview")
    def preview_release(body: dict):
        return jobs.start("Prepare website preview", lambda p, c: preview.open(body["filename"]))

    @app.post("/api/shutdown")
    def stop():
        threading.Timer(0.5, shutdown).start()
        return {"message": "Admin app stopped. You can close this tab."}

    return app
