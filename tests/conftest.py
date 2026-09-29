import pytest
from laz_engine.lexicon import load_entries


@pytest.fixture
def verb():
    def find(infinitive, category="TVE"):
        return next(
            e for e in load_entries() if e.infinitive == infinitive and e.verb_class == category
        )

    return find
