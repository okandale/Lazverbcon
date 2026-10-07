"""Serve a frozen approved export on a separate loopback port."""

import hashlib
import json
import socket
import tempfile
import threading
import time
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from laz_api.website import WebsiteFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.staticfiles import StaticFiles

from .archive import unpack


class Preview:
    def __init__(self, store, assets):
        self.store = store
        self.assets = Path(assets) if assets else None
        self.available = bool(self.assets and (self.assets / "index.html").is_file())
        self.server = self.thread = self.work = None

    def close(self):
        if self.server:
            self.server.should_exit = True
            self.thread.join(timeout=10)
            if self.thread.is_alive():
                raise ValueError("Preview is still shutting down; retry shortly")
            self.server = self.thread = None
        if self.work:
            self.work.cleanup()
            self.work = None

    def open(self, filename):
        if not self.available:
            raise ValueError(
                "Build the public preview assets first (scripts/build_admin_preview.py)"
            )
        if Path(filename).name != filename or not filename.endswith(".zip"):
            raise ValueError("Choose an exported snapshot")
        archive = self.store.directory / "exports" / filename
        info = json.loads(archive.with_suffix(".json").read_text(encoding="utf-8"))
        if hashlib.sha256(archive.read_bytes()).hexdigest() != info["sha256"]:
            raise ValueError("Export checksum differs; export again")
        self.close()
        self.work = tempfile.TemporaryDirectory(prefix="lazuri-preview-")
        try:
            unpack(archive, Path(self.work.name))
            app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
            app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost"])
            app.mount("/data/current", StaticFiles(directory=self.work.name))
            app.mount("/", WebsiteFiles(directory=self.assets, html=True))
            sock = socket.socket()
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
            self.server = uvicorn.Server(uvicorn.Config(app, log_level="warning", access_log=False))
            self.thread = threading.Thread(
                target=self.server.run, kwargs={"sockets": [sock]}, daemon=True
            )
            self.thread.start()
            for _ in range(100):
                if self.server.started:
                    return {"preview_url": f"http://127.0.0.1:{port}/?lang=en"}
                if not self.thread.is_alive():
                    break
                time.sleep(0.05)
            raise ValueError("Preview server failed to start")
        except BaseException:
            self.close()
            raise
