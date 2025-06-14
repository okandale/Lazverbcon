import pytest
from backend.conjugator.builder import ConjugatorBuilder
from backend.conjugator.verbs import NominativeVerb
from backend.conjugator.common import Person, Tense, Region
from backend.conjugator.past_conjugator import SUFFIXES


# Expected full conjugated forms
expected_forms = {
    Person.FIRST_PERSON_SINGULAR: "pskidi",
    Person.SECOND_PERSON_SINGULAR: "skidi",
    Person.THIRD_PERSON_SINGULAR: "skidu",
    Person.FIRST_PERSON_PLURAL: "pskidit",
    Person.SECOND_PERSON_PLURAL: "skidit",
    Person.THIRD_PERSON_PLURAL: "skides",  # or skidey depending on dialect
}

@pytest.mark.parametrize("person,expected", expected_forms.items())
def test_conjugate_nominative_past_tense_all_persons(person, expected):
    verb = NominativeVerb(infinitive="oskidu", present_third="skidun")
    conjugator = (
        ConjugatorBuilder()
        .set_subject(person)
        .set_region(Region.ARDESEN)
        .set_tense(Tense.PAST)
        .build()
    )
    result = conjugator.conjugate_nominative_verb(verb)
    assert result == expected, \
        f"Expected {expected} but got {result} for {person}"