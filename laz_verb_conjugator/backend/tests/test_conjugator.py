import pytest

from backend.conjugator.builder import ConjugatorBuilder
from backend.conjugator.verbs import NominativeVerb
from backend.conjugator.common import Person, Tense, Region


# Expected full conjugated forms
expected_forms = {
    (Region.ARDESEN, NominativeVerb(infinitive="oskidu", present_third="skidun")): {
        Person.FIRST_PERSON_SINGULAR: "pskidi",
        Person.SECOND_PERSON_SINGULAR: "skidi",
        Person.THIRD_PERSON_SINGULAR: "skidu",
        Person.FIRST_PERSON_PLURAL: "pskidit",
        Person.SECOND_PERSON_PLURAL: "skidit",
        Person.THIRD_PERSON_PLURAL: "skidey",
    },
    (Region.ARDESEN, NominativeVerb(infinitive="oputxu", present_third="putxun")): {
        Person.FIRST_PERSON_SINGULAR: "putxi",
        Person.SECOND_PERSON_SINGULAR: "putxi",
        Person.THIRD_PERSON_SINGULAR: "putxu",
        Person.FIRST_PERSON_PLURAL: "putxit",
        Person.SECOND_PERSON_PLURAL: "putxit",
        Person.THIRD_PERSON_PLURAL: "putxey",
    },
    (Region.HOPA, NominativeVerb(infinitive="oputxu", present_third="putxun")): {
        Person.FIRST_PERSON_SINGULAR: "putxi",
        Person.SECOND_PERSON_SINGULAR: "putxi",
        Person.THIRD_PERSON_SINGULAR: "putxu",
        Person.FIRST_PERSON_PLURAL: "putxit",
        Person.SECOND_PERSON_PLURAL: "putxit",
        Person.THIRD_PERSON_PLURAL: "putxes",
    }
}

prefixed_forms = {
    (Region.FINDIKLI_ARHAVI, NominativeVerb(infinitive="doskidu", present_third="doskidun")): {
        Person.FIRST_PERSON_SINGULAR: "dopskidi",
        Person.SECOND_PERSON_SINGULAR: "doskidi",
        Person.THIRD_PERSON_SINGULAR: "doskidu",
        Person.FIRST_PERSON_PLURAL: "dopskidit",
        Person.SECOND_PERSON_PLURAL: "doskidit",
        Person.THIRD_PERSON_PLURAL: "doskides",
    },
}

@pytest.mark.parametrize("region_and_verb,conjugations", expected_forms.items())
def test_conjugate_nominative_past_tense_all_persons(region_and_verb, conjugations):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .set_tense(Tense.PAST)
            .build()
        )
        result = conjugator.conjugate_nominative_verb(verb)
        assert result == conjugation, \
            f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"


@pytest.mark.parametrize("region_and_verb,conjugations", prefixed_forms.items())
def test_conjugate_prefix_verbs_past_tense(region_and_verb, conjugations):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .set_tense(Tense.PAST)
            .build()
        )
        result = conjugator.conjugate_nominative_verb(verb)
        assert result == conjugation, \
            f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"