"""Load the versioned lexicon without merging homographs or source records."""

import json
import unicodedata
from functools import lru_cache
from importlib.resources import files

from .models import Dialect, Entry, PrincipalPart, VerbClass


def search_key(value: str) -> str:
    return unicodedata.normalize("NFC", value.strip().casefold())


@lru_cache(maxsize=1)
def load_entries() -> tuple[Entry, ...]:
    rows = json.loads(files("laz_engine").joinpath("data/entries.json").read_text(encoding="utf-8"))
    return tuple(
        Entry(
            id=r["id"],
            infinitive=r["infinitive"],
            verb_class=VerbClass(r["verb_class"]),
            english=r["english"],
            turkish=r["turkish"],
            source_row=r["source_row"],
            issues=tuple(r["issues"]),
            variants=tuple(
                PrincipalPart(form=v["form"], dialects=tuple(Dialect(d) for d in v["dialects"]))
                for v in r["variants"]
            ),
        )
        for r in rows
    )


@lru_cache(maxsize=1)
def entries_by_id() -> dict[str, Entry]:
    return {e.id: e for e in load_entries()}


def search_entries(query: str = "") -> list[Entry]:
    key = search_key(query)
    return [
        e for e in load_entries() if key in search_key(f"{e.infinitive} {e.english} {e.turkish}")
    ]
