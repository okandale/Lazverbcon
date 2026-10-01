"""Explicit optional prefixes, preserving the maintainer's attachment convention."""

from ..models import OptionalPrefix


def attach(spelling: str, prefix: OptionalPrefix) -> str:
    if prefix == OptionalPrefix.NONE:
        return spelling
    if spelling.startswith(f"({prefix.value})"):
        spelling = spelling[len(prefix.value) + 2 :]
    # Both prefixes lose o before a vowel. The dump attaches the prefix before
    # a negative particle too (e.g. komot giğur); preserve that stored order.
    surface = prefix.value[:-1] if spelling.startswith(("a", "e", "i", "o", "u")) else prefix.value
    return surface + spelling
