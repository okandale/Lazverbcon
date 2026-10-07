"""Double-click launcher with persistent data outside the program directory."""

import argparse
import os
import socket
import sys
import threading
import webbrowser
from pathlib import Path

import uvicorn

from .app import create_app
from .store import Store


def data_directory():
    if sys.platform == "win32":
        return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / "LazuriAdmin"
    if sys.platform == "darwin":
        return Path.home() / "Library/Application Support/LazuriAdmin"
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "lazuri-admin"


def seed_file():
    bundled = Path(getattr(sys, "_MEIPASS", ".")) / "seed/maintainer-release.jsonl.gz"
    if bundled.is_file():
        return bundled
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "tests/fixtures/maintainer-release.jsonl.gz"
        if candidate.is_file():
            return candidate
    return None


def preview_files():
    bundled = Path(getattr(sys, "_MEIPASS", ".")) / "public-preview"
    if bundled.is_dir():
        return bundled
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "artifacts/admin-public"
        if candidate.is_dir():
            return candidate
    return None


def lock_instance(directory):
    directory.mkdir(parents=True, exist_ok=True)
    handle = (directory / "app.lock").open("a+b")
    handle.seek(0)
    if sys.platform == "win32":
        import msvcrt

        if not handle.read(1):
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
    else:
        import fcntl

        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    return handle


def main():
    parser = argparse.ArgumentParser(description="Local Lazuri editor")
    parser.add_argument("--data-dir", type=Path, default=data_directory())
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    try:
        instance = lock_instance(args.data_dir)
    except OSError:
        raise SystemExit("This project is already open. Use the existing admin window.") from None
    try:
        store = Store(args.data_dir)
        store.backup(daily=True)
        app = create_app(store, seed_path=seed_file())
        sock = socket.socket()
        sock.bind(("127.0.0.1", args.port))
        server = uvicorn.Server(uvicorn.Config(app, log_level="warning", access_log=False))
        # The callback is bound by recreating the app before startup.
        server.config.app = create_app(
            store,
            app.state.token,
            seed_file(),
            lambda: setattr(server, "should_exit", True),
            preview_files(),
        )
        url = f"http://127.0.0.1:{sock.getsockname()[1]}/#session={app.state.token}"
        print("Lazuri Admin:", url, flush=True)
        print("Data:", store.directory, flush=True)
        if not args.no_browser:
            threading.Timer(1, lambda: webbrowser.open(url)).start()
        server.run(sockets=[sock])
    finally:
        instance.close()


if __name__ == "__main__":
    main()
