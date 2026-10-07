"""Cloudflare build: download the pinned approved data, never regenerate it."""

import argparse
import hashlib
import json
import re
import tempfile
import urllib.request
from pathlib import Path

from build_static import build
from laz_admin.archive import unpack


def download(pointer, destination):
    if not re.fullmatch(
        r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/releases/download/[^/]+/catalog\.zip",
        pointer["url"],
    ):
        raise ValueError("Expected a public GitHub release asset URL")
    if not re.fullmatch(r"[a-f0-9]{64}", pointer["sha256"]):
        raise ValueError("Invalid checksum")
    digest = hashlib.sha256()
    count = 0
    with (
        urllib.request.urlopen(pointer["url"], timeout=180) as response,
        destination.open("wb") as target,
    ):
        while chunk := response.read(1024 * 1024):
            count += len(chunk)
            if count > 1024**3:
                raise ValueError("Archive exceeds 1 GiB")
            digest.update(chunk)
            target.write(chunk)
    if digest.hexdigest() != pointer["sha256"]:
        raise ValueError("Published archive checksum differs from the pinned release")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pointer", type=Path, default=Path("published/catalog.json"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/pages"))
    args = parser.parse_args()
    if not args.pointer.is_file():
        parser.error(
            "Publish an approved export from Lazuri Admin first; no generated fallback is used."
        )
    pointer = json.loads(args.pointer.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as work:
        work = Path(work)
        download(pointer, work / "catalog.zip")
        data = work / "data"
        data.mkdir()
        manifest = unpack(work / "catalog.zip", data)
        if (
            manifest["release"] != pointer["release"]
            or manifest["catalog"].get("project") != pointer["project"]
            or manifest["catalog"].get("revision") != pointer["revision"]
        ):
            raise ValueError("Pinned release identity differs from the archive")
        print(json.dumps(build(None, args.output, data), indent=2))


if __name__ == "__main__":
    main()
