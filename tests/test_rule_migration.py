"""Cross-entry regression checks against the frozen, separately executed rules."""

import sys
from dataclasses import replace
from pathlib import Path

import pytest
from laz_engine.engine import conjugate
from laz_engine.lexicon import load_entries
from laz_engine.models import Causative, Derivation, Features, Mood, Person, Tense, VerbClass

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from migration.reference.engine import conjugate as reference_conjugate  # noqa: E402
from migration.reference.engine import context_for  # noqa: E402
from migration.reference.rules.tvm_tve_potential import conjugate_potential_form  # noqa: E402


@pytest.mark.parametrize("entry", load_entries(), ids=lambda entry: entry.id)
def test_all_entries_against_frozen_rules(entry):
    for dialect in entry.dialects:
        for subject in Person:
            base = Features(dialect, subject)
            scenarios = [replace(base, tense=tense) for tense in Tense]
            scenarios += [replace(base, mood=mood) for mood in Mood]
            scenarios += [replace(base, derivation=kind) for kind in Derivation]
            scenarios += [replace(base, optional_preverb=True)]
            if entry.verb_class == VerbClass.ERGATIVE:
                scenarios += [
                    replace(
                        base,
                        tense=tense,
                        object=Person.THIRD_SINGULAR,
                        applicative=app,
                        causative=cause,
                    )
                    for tense in (Tense.PRESENT, Tense.PAST, Tense.FUTURE, Tense.PAST_PROGRESSIVE)
                    for app in (False, True)
                    for cause in Causative
                ]
            for features in scenarios:
                expected = reference_conjugate(entry, features)
                actual = conjugate(entry, features)
                assert actual == expected, (entry.id, features, expected, actual)


@pytest.mark.parametrize(
    "entry",
    [e for e in load_entries() if e.verb_class != VerbClass.DATIVE],
    ids=lambda entry: entry.id,
)
def test_potential_optative_uses_original_ending_table(entry):
    for dialect in entry.dialects:
        for subject in Person:
            features = Features(
                dialect, subject, mood=Mood.OPTATIVE, derivation=Derivation.POTENTIAL
            )
            expected = conjugate_potential_form(
                entry.infinitive,
                "optative",
                subject=subject.legacy("S"),
                context=context_for(entry, dialect),
            )[dialect.legacy]
            actual = conjugate(entry, features)
            assert actual.status == "ok", (entry.id, features, actual)
            assert sorted(f.spelling for f in actual.forms) == sorted({f for _, _, f in expected})
