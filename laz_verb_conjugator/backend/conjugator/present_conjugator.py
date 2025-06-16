from .common import Person, Region, extract_root
from .conjugator import Conjugator
from .verbs import Verb

PRESENT_TENSE_SUFFIXES = {
    Region.ARDESEN: {
        Person.FIRST_PERSON_SINGULAR: "r",
        Person.SECOND_PERSON_SINGULAR: "r",
        Person.THIRD_PERSON_SINGULAR: "n",
        Person.FIRST_PERSON_PLURAL: "rt",
        Person.SECOND_PERSON_PLURAL: "rt",
        Person.THIRD_PERSON_PLURAL: "nan",
    },
    Region.PAZAR: {
        Person.FIRST_PERSON_SINGULAR: "r",
        Person.SECOND_PERSON_SINGULAR: "r",
        Person.THIRD_PERSON_SINGULAR: "n",
        Person.FIRST_PERSON_PLURAL: "rt",
        Person.SECOND_PERSON_PLURAL: "rt",
        Person.THIRD_PERSON_PLURAL: "nan",
    },
    Region.FINDIKLI_ARHAVI: {
        Person.FIRST_PERSON_SINGULAR: "r",
        Person.SECOND_PERSON_SINGULAR: "r",
        Person.THIRD_PERSON_SINGULAR: "n",
        Person.FIRST_PERSON_PLURAL: "rt",
        Person.SECOND_PERSON_PLURAL: "rt",
        Person.THIRD_PERSON_PLURAL: "nan",
    },
    Region.HOPA: {
        Person.FIRST_PERSON_SINGULAR: "r",
        Person.SECOND_PERSON_SINGULAR: "r",
        Person.THIRD_PERSON_SINGULAR: "n",
        Person.FIRST_PERSON_PLURAL: "rt",
        Person.SECOND_PERSON_PLURAL: "rt",
        Person.THIRD_PERSON_PLURAL: "nan",
    },
}

DATIVE_SUFFIXES = {
    Person.FIRST_PERSON_SINGULAR: "",
    Person.SECOND_PERSON_SINGULAR: "",
    Person.THIRD_PERSON_SINGULAR: "",
    Person.FIRST_PERSON_PLURAL: "an",
    Person.SECOND_PERSON_PLURAL: "an",
    Person.THIRD_PERSON_PLURAL: "an",
}

DATIVE_SUBJECT_MARKERS = {
    Person.FIRST_PERSON_SINGULAR: "m",
    Person.SECOND_PERSON_SINGULAR: "g",
    Person.THIRD_PERSON_SINGULAR: "",
    Person.FIRST_PERSON_PLURAL: "m",
    Person.SECOND_PERSON_PLURAL: "g",
    Person.THIRD_PERSON_PLURAL: "",
}


class PresentConjugator(Conjugator):
    def conjugate_nominative_verb(self, verb: Verb) -> str:
        return super()._conjugate_nominative_verb(
            verb, PRESENT_TENSE_SUFFIXES, ending_len=1
        )

    def conjugate_dative_verb(self, verb: Verb) -> str:
        if (verb.present_third.startswith("u")
                and not self.subject.is_third_person()
        ):
            stem = f"i{verb.present_third[1:]}"
        else:
            stem = verb.present_third
        return (
            DATIVE_SUBJECT_MARKERS[self.subject] +
            stem + DATIVE_SUFFIXES[self.subject]
        )