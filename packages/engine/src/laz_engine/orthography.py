"""Search equivalences are separate from displayed spelling and rule input."""

import re

from .lexicon import search_key

ALTERNATES = {
    "3'": "ǯ",
    "ts": "ʒ",
    "tz": "ǯ",
    "dz": "ž",
    "z'": "ž",
    "k'": "ǩ",
    "p'": "p̌",
    "t'": "t̆",
    "ç'": "ç̌",
    "h": "x",
    "ğ": "x",
    "c": "ʒ",
    "3": "ʒ",
    "z": "ž",
}
PATTERN = re.compile("|".join(re.escape(k) for k in sorted(ALTERNATES, key=len, reverse=True)))


def strict_key(value: str) -> str:
    return search_key(PATTERN.sub(lambda m: ALTERNATES[m.group()], search_key(value)))


def broad_key(value: str) -> str:
    # Preserve already-marked ç̌ rather than adding a second combining caron.
    return re.sub("ç(?!\u030c)", "ç̌", strict_key(value).replace("k", "ǩ"))
