"""Validate a static release before unpacking it for preview or deployment."""

import hashlib
import json
import zipfile
from pathlib import PurePosixPath


def unpack(archive, destination):
    with zipfile.ZipFile(archive) as source:
        members = source.infolist()
        if len(members) > 19000 or sum(m.file_size for m in members) > 1024**3:
            raise ValueError("Export exceeds supported size")
        names = set()
        for member in members:
            path = PurePosixPath(member.filename)
            if (
                path.is_absolute()
                or ".." in path.parts
                or "\\" in member.filename
                or ":" in member.filename
                or member.filename in names
                or member.is_dir()
                or path.suffix != ".json"
                or member.file_size > 25 * 1024**2
                or (member.external_attr >> 16) & 0o170000 == 0o120000
            ):
                raise ValueError("Unsafe export path or asset")
            names.add(member.filename)
        source.extractall(destination)
    manifest = json.loads((destination / "manifest.json").read_text(encoding="utf-8"))
    for name, details in manifest["files"].items():
        if (
            name not in names
            or hashlib.sha256((destination / name).read_bytes()).hexdigest() != details["sha256"]
        ):
            raise ValueError("Export integrity check failed")
    if set(manifest["files"]) | {"manifest.json"} != names:
        raise ValueError("Archive contains unlisted assets")
    return manifest
