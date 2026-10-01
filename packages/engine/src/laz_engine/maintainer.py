"""Attested optional-prefix availability from the corrected maintainer database."""

import json
from functools import lru_cache
from importlib.resources import files

from .models import OptionalPrefix


@lru_cache(maxsize=1)
def data():
    path = files("laz_engine").joinpath("data/maintainer.json")
    if not path.is_file():
        raise FileNotFoundError("Missing packaged maintainer prefix metadata")
    return json.loads(path.read_text(encoding="utf-8"))


def prefixes(entry_id: str, dialect) -> tuple[OptionalPrefix, ...]:
    return tuple(OptionalPrefix(p) for p in data()["prefixes"].get(entry_id, {}).get(dialect, []))
