import pytest

from backend.conjugator.builder import ConjugatorBuilder
from backend.conjugator.verbs import NominativeVerb
from backend.conjugator.common import Person, Tense, Region


# Expected full conjugated forms
expected_forms = {
    NominativeVerb(infinitive="oskidu", present_third="skidun", region=Region.ARDESEN): {
        Person.FIRST_PERSON_SINGULAR: "pskidi",
        Person.SECOND_PERSON_SINGULAR: "skidi",
        Person.THIRD_PERSON_SINGULAR: "skidu",
        Person.FIRST_PERSON_PLURAL: "pskidit",
        Person.SECOND_PERSON_PLURAL: "skidit",
        Person.THIRD_PERSON_PLURAL: "skides",
    },
    NominativeVerb(infinitive="oputxu", present_third="putxun", region=Region.ARDESEN): {
        Person.FIRST_PERSON_SINGULAR: "putxi",
        Person.SECOND_PERSON_SINGULAR: "putxi",
        Person.THIRD_PERSON_SINGULAR: "putxu",
        Person.FIRST_PERSON_PLURAL: "putxit",
        Person.SECOND_PERSON_PLURAL: "putxit",
        Person.THIRD_PERSON_PLURAL: "putxey",
    },
    NominativeVerb(infinitive="oputxu", present_third="putxun", region=Region.PAZAR): {
        Person.FIRST_PERSON_SINGULAR: "putxi",
        Person.SECOND_PERSON_SINGULAR: "putxi",
        Person.THIRD_PERSON_SINGULAR: "putxu",
        Person.FIRST_PERSON_PLURAL: "putxit",
        Person.SECOND_PERSON_PLURAL: "putxit",
        Person.THIRD_PERSON_PLURAL: "putxes",
    }
}

prefixed_forms = {
    NominativeVerb(infinitive="doskidu", present_third="doskidun", region=Region.FINDIKLI_ARHAVI): {
        Person.FIRST_PERSON_SINGULAR: "dopskidi",
        Person.SECOND_PERSON_SINGULAR: "doskidi",
        Person.THIRD_PERSON_SINGULAR: "doskidu",
        Person.FIRST_PERSON_PLURAL: "dopskidit",
        Person.SECOND_PERSON_PLURAL: "doskidit",
        Person.THIRD_PERSON_PLURAL: "doskides",
    },
}

@pytest.mark.parametrize("verb,conjugations", expected_forms.items())
def test_conjugate_nominative_past_tense_all_persons(verb, conjugations):
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(Region.ARDESEN)
            .set_tense(Tense.PAST)
            .build()
        )
        result = conjugator.conjugate_nominative_verb(verb)
        assert result == conjugation, \
            f"Expected {conjugation} but got {result} for {person} and {verb.region}"


@pytest.mark.parametrize("verb,conjugations", prefixed_forms.items())
def test_conjugate_prefix_verbs_past_tense(verb, conjugations):
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_tense(Tense.PAST)
            .build()
        )
        result = conjugator.conjugate_nominative_verb(verb)
        assert result == conjugation, \
            f"Expected {conjugation} but got {result} for {person} and {verb.region}"