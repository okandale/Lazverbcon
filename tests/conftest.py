import json
from dataclasses import asdict
from pathlib import Path

import pytest
from laz_api.catalog import canonical
from laz_engine.lexicon import load_entries
from laz_engine.models import Features
from pydantic import TypeAdapter


@pytest.fixture(scope="session")
def maintainer_cases():
    path = Path(__file__).parent / "fixtures/maintainer-corrections.json"
    return {
        (
            case["entry_id"],
            canonical(asdict(TypeAdapter(Features).validate_python(case["features"]))),
        ): case
        for case in json.loads(path.read_text())["cases"]
    }


@pytest.fixture
def verb():
    def find(infinitive, category="TVE"):
        return next(
            e for e in load_entries() if e.infinitive == infinitive and e.verb_class == category
        )

    return find
