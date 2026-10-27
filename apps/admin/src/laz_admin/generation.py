"""Editor-specified generation choices; approved conjugations are unaffected."""

from dataclasses import asdict

from laz_engine.models import Features
from pydantic import TypeAdapter

ADAPTER = TypeAdapter(Features)
FIELDS = set(Features.__dataclass_fields__) - {"optional_preverb"}


def options(value=None):
    value = {} if value is None else value
    if not isinstance(value, dict) or set(value) - {"preverb_lookalike", "excluded_combinations"}:
        raise ValueError("Unknown generation option")
    lookalike = value.get("preverb_lookalike", False)
    excluded = value.get("excluded_combinations", [])
    if not isinstance(lookalike, bool) or not isinstance(excluded, list) or len(excluded) > 200:
        raise ValueError("Choose a preverb checkbox value and up to 200 exclusion rows")
    rows = []
    for rule in excluded:
        if not isinstance(rule, dict) or not rule or set(rule) - FIELDS:
            raise ValueError("Each exclusion needs at least one supported grammatical feature")
        normalized = asdict(ADAPTER.validate_python({"dialect": "AS", "subject": "1sg", **rule}))
        row = {key: normalized[key] for key in rule}
        if row not in rows:
            rows.append(row)
    return {"preverb_lookalike": lookalike, "excluded_combinations": rows}


def excluded(features, choices):
    return any(
        all(getattr(features, field) == value for field, value in row.items())
        for row in choices["excluded_combinations"]
    )
