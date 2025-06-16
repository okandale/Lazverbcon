import pytest

from backend.conjugator.builder import ConjugatorBuilder
from backend.conjugator.common import Aspect, Mood, Person, Region, Tense
from backend.conjugator.verbs import DativeVerb, NominativeVerb

# Expected full conjugated forms
expected_forms = {
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="oskidu", present_third="skidun"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "pskidi",
        Person.SECOND_PERSON_SINGULAR: "skidi",
        Person.THIRD_PERSON_SINGULAR: "skidu",
        Person.FIRST_PERSON_PLURAL: "pskidit",
        Person.SECOND_PERSON_PLURAL: "skidit",
        Person.THIRD_PERSON_PLURAL: "skidey",
    },
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="oputxu", present_third="putxun"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "putxi",
        Person.SECOND_PERSON_SINGULAR: "putxi",
        Person.THIRD_PERSON_SINGULAR: "putxu",
        Person.FIRST_PERSON_PLURAL: "putxit",
        Person.SECOND_PERSON_PLURAL: "putxit",
        Person.THIRD_PERSON_PLURAL: "putxey",
    },
    (
        Region.HOPA,
        NominativeVerb(infinitive="oputxu", present_third="putxun"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "putxi",
        Person.SECOND_PERSON_SINGULAR: "putxi",
        Person.THIRD_PERSON_SINGULAR: "putxu",
        Person.FIRST_PERSON_PLURAL: "putxit",
        Person.SECOND_PERSON_PLURAL: "putxit",
        Person.THIRD_PERSON_PLURAL: "putxes",
    },
    (
        Region.PAZAR,
        NominativeVerb(infinitive="cexunu", present_third="cexedun"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "cepxedi",
        Person.SECOND_PERSON_SINGULAR: "cexedi",
        Person.THIRD_PERSON_SINGULAR: "cexedu",
        Person.FIRST_PERSON_PLURAL: "cepxedit",
        Person.SECOND_PERSON_PLURAL: "cexedit",
        Person.THIRD_PERSON_PLURAL: "cexedes",
    },
}

prefixed_forms = {
    (
        Region.FINDIKLI_ARHAVI,
        NominativeVerb(infinitive="doskidu", present_third="doskidun"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "dopskidi",
        Person.SECOND_PERSON_SINGULAR: "doskidi",
        Person.THIRD_PERSON_SINGULAR: "doskidu",
        Person.FIRST_PERSON_PLURAL: "dopskidit",
        Person.SECOND_PERSON_PLURAL: "doskidit",
        Person.THIRD_PERSON_PLURAL: "doskides",
    },
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="dobadu", present_third="dibaden"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "dovibadi",
        Person.SECOND_PERSON_SINGULAR: "dibadi",
        Person.THIRD_PERSON_SINGULAR: "dibadu",
        Person.FIRST_PERSON_PLURAL: "dovibadit",
        Person.SECOND_PERSON_PLURAL: "dibadit",
        Person.THIRD_PERSON_PLURAL: "dibadey",
    },
}

mutated_prefix_past_tense = {
    (
        Region.HOPA,
        NominativeVerb(infinitive="dobadu", present_third="dibaden"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "dovibadi",
        Person.SECOND_PERSON_SINGULAR: "dibadi",
        Person.THIRD_PERSON_SINGULAR: "dibadu",
        Person.FIRST_PERSON_PLURAL: "dovibadit",
        Person.SECOND_PERSON_PLURAL: "dibadit",
        Person.THIRD_PERSON_PLURAL: "dibades",
    }
}


@pytest.mark.parametrize(
    "region_and_verb,conjugations", expected_forms.items()
)
def test_conjugate_nominative_past_tense_all_persons(
    region_and_verb, conjugations
):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .set_tense(Tense.PAST)
            .build()
        )
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"


@pytest.mark.parametrize(
    "region_and_verb,conjugations", prefixed_forms.items()
)
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
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"


@pytest.mark.parametrize(
    "region_and_verb,conjugations", mutated_prefix_past_tense.items()
)
def test_conjugate_mutated_prefix_past_tense(region_and_verb, conjugations):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .set_tense(Tense.PAST)
            .build()
        )
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"


future_tense_fixtures = {
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="oskidu", present_third="skidun"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "pskidare",
        Person.SECOND_PERSON_SINGULAR: "skidare",
        Person.THIRD_PERSON_SINGULAR: "skidasen",
        Person.FIRST_PERSON_PLURAL: "pskidaten",
        Person.SECOND_PERSON_PLURAL: "skidaten",
        Person.THIRD_PERSON_PLURAL: "skidanen",
    },
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="dobadu", present_third="dibaden"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "dovibadare",
        Person.SECOND_PERSON_SINGULAR: "dibadare",
        Person.THIRD_PERSON_SINGULAR: "dibadasen",
        Person.FIRST_PERSON_PLURAL: "dovibadaten",
        Person.SECOND_PERSON_PLURAL: "dibadaten",
        Person.THIRD_PERSON_PLURAL: "dibadanen",
    },
}


@pytest.mark.parametrize(
    "region_and_verb,conjugations", future_tense_fixtures.items()
)
def test_conjugate_nominative_future_tense(region_and_verb, conjugations):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .set_tense(Tense.FUTURE)
            .build()
        )
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"


present_tense_fixtures = {
    (
        Region.FINDIKLI_ARHAVI,
        NominativeVerb(infinitive="oskidu", present_third="skidun"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "pskidur",
        Person.SECOND_PERSON_SINGULAR: "skidur",
        Person.THIRD_PERSON_SINGULAR: "skidun",
        Person.FIRST_PERSON_PLURAL: "pskidurt",
        Person.SECOND_PERSON_PLURAL: "skidurt",
        Person.THIRD_PERSON_PLURAL: "skidunan",
    },
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="dobadu", present_third="dibaden"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "dovibader",
        Person.SECOND_PERSON_SINGULAR: "dibader",
        Person.THIRD_PERSON_SINGULAR: "dibaden",
        Person.FIRST_PERSON_PLURAL: "dovibadert",
        Person.SECOND_PERSON_PLURAL: "dibadert",
        Person.THIRD_PERSON_PLURAL: "dibadenan",
    },
}


@pytest.mark.parametrize(
    "region_and_verb,conjugations", present_tense_fixtures.items()
)
def test_conjugate_nominative_present_tense(region_and_verb, conjugations):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .set_tense(Tense.PRESENT)
            .build()
        )
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"


past_progressive_tense_fixtures = {
    (
        Region.FINDIKLI_ARHAVI,
        NominativeVerb(infinitive="oskidu", present_third="skidun"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "pskidurt̆i",
        Person.SECOND_PERSON_SINGULAR: "skidurt̆i",
        Person.THIRD_PERSON_SINGULAR: "skidurt̆u",
        Person.FIRST_PERSON_PLURAL: "pskidurt̆it",
        Person.SECOND_PERSON_PLURAL: "skidurt̆it",
        Person.THIRD_PERSON_PLURAL: "skidut̆es",
    },
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="dobadu", present_third="dibaden"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "dovibadert̆i",
        Person.SECOND_PERSON_SINGULAR: "dibadert̆i",
        Person.THIRD_PERSON_SINGULAR: "dibadert̆u",
        Person.FIRST_PERSON_PLURAL: "dovibadert̆it",
        Person.SECOND_PERSON_PLURAL: "dibadert̆it",
        Person.THIRD_PERSON_PLURAL: "dibadert̆ey",
    },
}


@pytest.mark.parametrize(
    "region_and_verb,conjugations", past_progressive_tense_fixtures.items()
)
def test_conjugate_nominative_past_progressive_tense(
    region_and_verb, conjugations
):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .set_tense(Tense.PAST_PROGRESSIVE)
            .build()
        )
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"


present_perfect_tense_fixtures = {
    (
        Region.FINDIKLI_ARHAVI,
        NominativeVerb(infinitive="oskidu", present_third="skidun"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "miskidun",
        Person.SECOND_PERSON_SINGULAR: "giskidun",
        Person.THIRD_PERSON_SINGULAR: "uskidun",
        Person.FIRST_PERSON_PLURAL: "miskidunan",
        Person.SECOND_PERSON_PLURAL: "giskidunan",
        Person.THIRD_PERSON_PLURAL: "uskidunan",
    },
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="dobadu", present_third="dibaden"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "domibadapun",
        Person.SECOND_PERSON_SINGULAR: "dogibadapun",
        Person.THIRD_PERSON_SINGULAR: "dubadapun",
        Person.FIRST_PERSON_PLURAL: "domibadapunan",
        Person.SECOND_PERSON_PLURAL: "dogibadapunan",
        Person.THIRD_PERSON_PLURAL: "dubadapunan",
    },
}


@pytest.mark.parametrize(
    "region_and_verb,conjugations", present_perfect_tense_fixtures.items()
)
def test_conjugate_nominative_past_progressive_tense(
    region_and_verb, conjugations
):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .set_tense(Tense.PRESENT_PREFECT)
            .build()
        )
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"


imperative_mood_fixtures = {
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="oskidu", present_third="skidun"),
    ): {
        Person.SECOND_PERSON_SINGULAR: "skidi",
        Person.SECOND_PERSON_PLURAL: "skidit",
    },
}


@pytest.mark.parametrize(
    "region_and_verb,conjugations", imperative_mood_fixtures.items()
)
def test_imperative_mood(region_and_verb, conjugations):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .add_mood(Mood.IMPERATIVE)
            .build()
        )
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"


negative_imperative_mood_fixtures = {
    (
        Region.HOPA,
        NominativeVerb(infinitive="oskidu", present_third="skidun"),
    ): {
        Person.SECOND_PERSON_SINGULAR: "mo skidur",
        Person.SECOND_PERSON_PLURAL: "mo skidurt",
    },
}


@pytest.mark.parametrize(
    "region_and_verb,conjugations", negative_imperative_mood_fixtures.items()
)
def test_negative_imperative_mood(region_and_verb, conjugations):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .add_mood(Mood.NEGATIVE_IMPERATIVE)
            .build()
        )
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"


past_potential_fixtures = {
    (
        Region.FINDIKLI_ARHAVI,
        NominativeVerb(infinitive="oskidu", present_third="skidun"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "maskidu",
        Person.SECOND_PERSON_SINGULAR: "gaskidu",
        Person.THIRD_PERSON_SINGULAR: "askidu",
        Person.FIRST_PERSON_PLURAL: "maskides",
        Person.SECOND_PERSON_PLURAL: "gaskides",
        Person.THIRD_PERSON_PLURAL: "askides",
    },
}


@pytest.mark.parametrize(
    "region_and_verb,conjugations", past_potential_fixtures.items()
)
def test_past_potential(region_and_verb, conjugations):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .set_tense(Tense.PAST)
            .set_aspect(Aspect.POTENTIAL)
            .build()
        )
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"


past_passive_fixtures = {
    (
        Region.FINDIKLI_ARHAVI,
        NominativeVerb(infinitive="oskidu", present_third="skidun"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "biskidi",
        Person.SECOND_PERSON_SINGULAR: "iskidi",
        Person.THIRD_PERSON_SINGULAR: "iskidu",
        Person.FIRST_PERSON_PLURAL: "biskidit",
        Person.SECOND_PERSON_PLURAL: "iskidit",
        Person.THIRD_PERSON_PLURAL: "iskides",
    },
}


@pytest.mark.parametrize(
    "region_and_verb,conjugations", past_passive_fixtures.items()
)
def test_past_potential(region_and_verb, conjugations):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .set_tense(Tense.PAST)
            .set_aspect(Aspect.PASSIVE)
            .build()
        )
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"


dative_present_fixtures = {
    (
        Region.ARDESEN,
        DativeVerb(infinitive="oropu", present_third="aoropen"),
    ): {
        Person.FIRST_PERSON_SINGULAR: "maoropen",
        Person.SECOND_PERSON_SINGULAR: "gaoropen",
        Person.THIRD_PERSON_SINGULAR: "aoropen",
        Person.FIRST_PERSON_PLURAL: "maoropenan",
        Person.SECOND_PERSON_PLURAL: "gaoropenan",
        Person.THIRD_PERSON_PLURAL: "aoropenan",
    },
}


@pytest.mark.parametrize(
    "region_and_verb,conjugations", dative_present_fixtures.items()
)
@pytest.mark.skip(reason="Being refactored")
def test_past_potential(region_and_verb, conjugations):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .set_tense(Tense.PRESENT)
            .build()
        )
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"
