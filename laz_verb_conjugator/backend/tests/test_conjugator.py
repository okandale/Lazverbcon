from backend.conjugator.conjugator import Conjugator
import pytest

from backend.conjugator.builder import ConjugatorBuilder
from backend.conjugator.common import Aspect, Mood, Person, Region, Tense
from backend.conjugator.verbs import DativeVerb, ErgativeVerb, NominativeVerb

# Expected full conjugated forms
expected_forms = {
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="oskidu", present_third="skidun"),
    ): {
        Person.FIRST_SINGULAR: "pskidi",
        Person.SECOND_SINGULAR: "skidi",
        Person.THIRD_SINGULAR: "skidu",
        Person.FIRST_PLURAL: "pskidit",
        Person.SECOND_PLURAL: "skidit",
        Person.THIRD_PLURAL: "skidey",
    },
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="oputxu", present_third="putxun"),
    ): {
        Person.FIRST_SINGULAR: "putxi",
        Person.SECOND_SINGULAR: "putxi",
        Person.THIRD_SINGULAR: "putxu",
        Person.FIRST_PLURAL: "putxit",
        Person.SECOND_PLURAL: "putxit",
        Person.THIRD_PLURAL: "putxey",
    },
    (
        Region.HOPA,
        NominativeVerb(infinitive="oputxu", present_third="putxun"),
    ): {
        Person.FIRST_SINGULAR: "putxi",
        Person.SECOND_SINGULAR: "putxi",
        Person.THIRD_SINGULAR: "putxu",
        Person.FIRST_PLURAL: "putxit",
        Person.SECOND_PLURAL: "putxit",
        Person.THIRD_PLURAL: "putxes",
    },
    (
        Region.PAZAR,
        NominativeVerb(infinitive="cexunu", present_third="cexedun"),
    ): {
        Person.FIRST_SINGULAR: "cepxedi",
        Person.SECOND_SINGULAR: "cexedi",
        Person.THIRD_SINGULAR: "cexedu",
        Person.FIRST_PLURAL: "cepxedit",
        Person.SECOND_PLURAL: "cexedit",
        Person.THIRD_PLURAL: "cexedes",
    },
}

prefixed_forms = {
    (
        Region.FINDIKLI_ARHAVI,
        NominativeVerb(infinitive="doskidu", present_third="doskidun"),
    ): {
        Person.FIRST_SINGULAR: "dopskidi",
        Person.SECOND_SINGULAR: "doskidi",
        Person.THIRD_SINGULAR: "doskidu",
        Person.FIRST_PLURAL: "dopskidit",
        Person.SECOND_PLURAL: "doskidit",
        Person.THIRD_PLURAL: "doskides",
    },
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="dobadu", present_third="dibaden"),
    ): {
        Person.FIRST_SINGULAR: "dovibadi",
        Person.SECOND_SINGULAR: "dibadi",
        Person.THIRD_SINGULAR: "dibadu",
        Person.FIRST_PLURAL: "dovibadit",
        Person.SECOND_PLURAL: "dibadit",
        Person.THIRD_PLURAL: "dibadey",
    },
}

mutated_prefix_past_tense = {
    (
        Region.HOPA,
        NominativeVerb(infinitive="dobadu", present_third="dibaden"),
    ): {
        Person.FIRST_SINGULAR: "dovibadi",
        Person.SECOND_SINGULAR: "dibadi",
        Person.THIRD_SINGULAR: "dibadu",
        Person.FIRST_PLURAL: "dovibadit",
        Person.SECOND_PLURAL: "dibadit",
        Person.THIRD_PLURAL: "dibades",
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
        Person.FIRST_SINGULAR: "pskidare",
        Person.SECOND_SINGULAR: "skidare",
        Person.THIRD_SINGULAR: "skidasen",
        Person.FIRST_PLURAL: "pskidaten",
        Person.SECOND_PLURAL: "skidaten",
        Person.THIRD_PLURAL: "skidanen",
    },
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="dobadu", present_third="dibaden"),
    ): {
        Person.FIRST_SINGULAR: "dovibadare",
        Person.SECOND_SINGULAR: "dibadare",
        Person.THIRD_SINGULAR: "dibadasen",
        Person.FIRST_PLURAL: "dovibadaten",
        Person.SECOND_PLURAL: "dibadaten",
        Person.THIRD_PLURAL: "dibadanen",
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
        Person.FIRST_SINGULAR: "pskidur",
        Person.SECOND_SINGULAR: "skidur",
        Person.THIRD_SINGULAR: "skidun",
        Person.FIRST_PLURAL: "pskidurt",
        Person.SECOND_PLURAL: "skidurt",
        Person.THIRD_PLURAL: "skidunan",
    },
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="dobadu", present_third="dibaden"),
    ): {
        Person.FIRST_SINGULAR: "dovibader",
        Person.SECOND_SINGULAR: "dibader",
        Person.THIRD_SINGULAR: "dibaden",
        Person.FIRST_PLURAL: "dovibadert",
        Person.SECOND_PLURAL: "dibadert",
        Person.THIRD_PLURAL: "dibadenan",
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
        Person.FIRST_SINGULAR: "pskidurt̆i",
        Person.SECOND_SINGULAR: "skidurt̆i",
        Person.THIRD_SINGULAR: "skidurt̆u",
        Person.FIRST_PLURAL: "pskidurt̆it",
        Person.SECOND_PLURAL: "skidurt̆it",
        Person.THIRD_PLURAL: "skidut̆es",
    },
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="dobadu", present_third="dibaden"),
    ): {
        Person.FIRST_SINGULAR: "dovibadert̆i",
        Person.SECOND_SINGULAR: "dibadert̆i",
        Person.THIRD_SINGULAR: "dibadert̆u",
        Person.FIRST_PLURAL: "dovibadert̆it",
        Person.SECOND_PLURAL: "dibadert̆it",
        Person.THIRD_PLURAL: "dibadert̆ey",
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
        Person.FIRST_SINGULAR: "miskidun",
        Person.SECOND_SINGULAR: "giskidun",
        Person.THIRD_SINGULAR: "uskidun",
        Person.FIRST_PLURAL: "miskidunan",
        Person.SECOND_PLURAL: "giskidunan",
        Person.THIRD_PLURAL: "uskidunan",
    },
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="dobadu", present_third="dibaden"),
    ): {
        Person.FIRST_SINGULAR: "domibadapun",
        Person.SECOND_SINGULAR: "dogibadapun",
        Person.THIRD_SINGULAR: "dubadapun",
        Person.FIRST_PLURAL: "domibadapunan",
        Person.SECOND_PLURAL: "dogibadapunan",
        Person.THIRD_PLURAL: "dubadapunan",
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
        Person.SECOND_SINGULAR: "skidi",
        Person.SECOND_PLURAL: "skidit",
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
        Person.SECOND_SINGULAR: "mo skidur",
        Person.SECOND_PLURAL: "mo skidurt",
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
        Person.FIRST_SINGULAR: "maskidu",
        Person.SECOND_SINGULAR: "gaskidu",
        Person.THIRD_SINGULAR: "askidu",
        Person.FIRST_PLURAL: "maskides",
        Person.SECOND_PLURAL: "gaskides",
        Person.THIRD_PLURAL: "askides",
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
        Person.FIRST_SINGULAR: "biskidi",
        Person.SECOND_SINGULAR: "iskidi",
        Person.THIRD_SINGULAR: "iskidu",
        Person.FIRST_PLURAL: "biskidit",
        Person.SECOND_PLURAL: "iskidit",
        Person.THIRD_PLURAL: "iskides",
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
        Person.FIRST_SINGULAR: "maoropen",
        Person.SECOND_SINGULAR: "gaoropen",
        Person.THIRD_SINGULAR: "aoropen",
        Person.FIRST_PLURAL: "maoropenan",
        Person.SECOND_PLURAL: "gaoropenan",
        Person.THIRD_PLURAL: "aoropenan",
    },
    (
        Region.ARDESEN,
        DativeVerb(infinitive="omşkorinu", present_third="amşkorinen"),
    ): {
        Person.FIRST_SINGULAR: "mamşkorinen",
        Person.SECOND_SINGULAR: "gamşkorinen",
        Person.THIRD_SINGULAR: "amşkorinen",
        Person.FIRST_PLURAL: "mamşkorinenan",
        Person.SECOND_PLURAL: "gamşkorinenan",
        Person.THIRD_PLURAL: "amşkorinenan",
    },
    (
        Region.PAZAR,
        DativeVerb(infinitive="olimbu", present_third="alimben"),
    ): {
        Person.FIRST_SINGULAR: "malimben",
        Person.SECOND_SINGULAR: "galimben",
        Person.THIRD_SINGULAR: "alimben",
        Person.FIRST_PLURAL: "malimbenan",
        Person.SECOND_PLURAL: "galimbenan",
        Person.THIRD_PLURAL: "alimbenan",
    },
    (
        Region.FINDIKLI_ARHAVI,
        DativeVerb(infinitive="oçkinu", present_third="uçkin"),
    ): {
        Person.FIRST_SINGULAR: "miçkin",
        Person.SECOND_SINGULAR: "giçkin",
        Person.THIRD_SINGULAR: "uçkin",
        Person.FIRST_PLURAL: "miçkinan",
        Person.SECOND_PLURAL: "giçkinan",
        Person.THIRD_PLURAL: "uçkinan",
    },
    (
        Region.HOPA,
        DativeVerb(infinitive="coxons", present_third="coxons"),
    ): {
        Person.FIRST_SINGULAR: "mcoxons",
        Person.SECOND_SINGULAR: "gcoxons",
        Person.THIRD_SINGULAR: "coxons",
        Person.FIRST_PLURAL: "mcoxonan",
        Person.SECOND_PLURAL: "gcoxonan",
        Person.THIRD_PLURAL: "coxonan",
    },
}


@pytest.mark.parametrize(
    "region_and_verb,conjugations", dative_present_fixtures.items()
)
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


optative_mood_fixtures = {
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="dobadu", present_third="dibaden"),
    ): {
        Person.FIRST_SINGULAR: "dovibada",
        Person.SECOND_SINGULAR: "dibada",
        Person.THIRD_SINGULAR: "dibadas",
        Person.FIRST_PLURAL: "dovibadat",
        Person.SECOND_PLURAL: "dibadat",
        Person.THIRD_PLURAL: "dibadan",
    },
    (
        Region.ARDESEN,
        NominativeVerb(infinitive="oskidu", present_third="skidun"),
    ): {
        Person.FIRST_SINGULAR: "pskida",
        Person.SECOND_SINGULAR: "skida",
        Person.THIRD_SINGULAR: "skidas",
        Person.FIRST_PLURAL: "pskidat",
        Person.SECOND_PLURAL: "skidat",
        Person.THIRD_PLURAL: "skidan",
    },
}


@pytest.mark.parametrize(
    "region_and_verb,conjugations", optative_mood_fixtures.items()
)
def test_optative(region_and_verb, conjugations):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .add_mood(Mood.OPTATIVE)
            .build()
        )
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"


# XXX: do Oropu, omşkorinu, olimbu
# XXX: Oçkinu, Then preverbs, then coxons/uğun/uyonun (verbs with no infinitive), then gyožin

dative_with_2nd_person_object_fixtures = {
    (
        Region.ARDESEN,
        DativeVerb(infinitive="oropu", present_third="aoropen"),
    ): {
        Person.FIRST_SINGULAR: "maoroper",
        Person.THIRD_SINGULAR: "aoroper",
        Person.FIRST_PLURAL: "maoropet",
        Person.THIRD_PLURAL: "aoroper",
    },
}


@pytest.mark.parametrize(
    "region_and_verb,conjugations",
    dative_with_2nd_person_object_fixtures.items(),
)
def test_dative_with_2nd_person(region_and_verb, conjugations):
    region, verb = region_and_verb
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .set_tense(Tense.PRESENT)
            .set_object(Person.SECOND_SINGULAR)
            .build()
        )
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, {person} and {region}"


ergative_fixtures = {
    (
        Region.ARDESEN,
        ErgativeVerb(infinitive="osinapu", present_third="isinapams"),
    ): {
        Person.FIRST_SINGULAR: "visinapam",
        Person.SECOND_SINGULAR: "isinapam",
        Person.THIRD_SINGULAR: "isinapay",
        Person.FIRST_PLURAL: "visinapamt",
        Person.SECOND_PLURAL: "isinapamt",
        Person.THIRD_PLURAL: "isinapaman",
    },
}


@pytest.mark.parametrize(
    "region_and_verb,conjugations",
    ergative_fixtures.items(),
)
def test_ergative(region_and_verb, conjugations):
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

ergative_applicative_fixtures = {
    (
        Region.ARDESEN,
        ErgativeVerb(infinitive="osinapu", present_third="isinapams"),
    ): {
        Person.FIRST_SINGULAR: "gisinapam",
        Person.SECOND_SINGULAR: "isinapam",
        Person.THIRD_SINGULAR: "gisinapay",
        Person.FIRST_PLURAL: "gisinapamt",
        Person.THIRD_PLURAL: "gisinapaman",
    },
}
@pytest.mark.parametrize(
    "region,object,verb,conjugations",
    [
        (Region.ARDESEN,
        Person.SECOND_SINGULAR,
        ErgativeVerb(infinitive="osinapu", present_third="isinapams"),
        {
        Person.FIRST_SINGULAR: "gisinapam",
        Person.SECOND_SINGULAR: "isinapam",
        Person.THIRD_SINGULAR: "gisinapay",
        Person.FIRST_PLURAL: "gisinapamt",
        Person.THIRD_PLURAL: "gisinapaman",
        }),
        (Region.ARDESEN,
        Person.FIRST_SINGULAR,
        ErgativeVerb(infinitive="osinapu", present_third="isinapams"),
        {
        Person.FIRST_SINGULAR: "visinapam",
        Person.SECOND_SINGULAR: "misinapam",
        Person.THIRD_SINGULAR: "misinapay",
        Person.SECOND_PLURAL: "misinapamt",
        Person.THIRD_PLURAL: "misinapaman",
        }),
    ],
)
def test_ergative_applicative(region, object, verb, conjugations):
    for person, conjugation in conjugations.items():
        conjugator = (
            ConjugatorBuilder()
            .set_subject(person)
            .set_region(region)
            .set_tense(Tense.PRESENT)
            .set_object(object)
            .add_mood(Mood.APPLICATIVE)
            .build()
        )
        result = conjugator.conjugate(verb)
        assert (
            result == conjugation
        ), f"Expected {conjugation} but got {result} for verb {verb}, object {object}, subject {person} and {region}"