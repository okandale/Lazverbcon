from .common import Person, Region, extract_root
from .conjugator import Conjugator
from .verbs import Verb

PRESENT_TENSE_SUFFIXES = {
    Region.ARDESEN: {
        Person.FIRST_SINGULAR: "r",
        Person.SECOND_SINGULAR: "r",
        Person.THIRD_SINGULAR: "n",
        Person.FIRST_PLURAL: "rt",
        Person.SECOND_PLURAL: "rt",
        Person.THIRD_PLURAL: "nan",
    },
    Region.PAZAR: {
        Person.FIRST_SINGULAR: "r",
        Person.SECOND_SINGULAR: "r",
        Person.THIRD_SINGULAR: "n",
        Person.FIRST_PLURAL: "rt",
        Person.SECOND_PLURAL: "rt",
        Person.THIRD_PLURAL: "nan",
    },
    Region.FINDIKLI_ARHAVI: {
        Person.FIRST_SINGULAR: "r",
        Person.SECOND_SINGULAR: "r",
        Person.THIRD_SINGULAR: "n",
        Person.FIRST_PLURAL: "rt",
        Person.SECOND_PLURAL: "rt",
        Person.THIRD_PLURAL: "nan",
    },
    Region.HOPA: {
        Person.FIRST_SINGULAR: "r",
        Person.SECOND_SINGULAR: "r",
        Person.THIRD_SINGULAR: "n",
        Person.FIRST_PLURAL: "rt",
        Person.SECOND_PLURAL: "rt",
        Person.THIRD_PLURAL: "nan",
    },
}

DATIVE_SUFFIXES = {
    Person.FIRST_SINGULAR: "",
    Person.SECOND_SINGULAR: "",
    Person.THIRD_SINGULAR: "",
    Person.FIRST_PLURAL: "an",
    Person.SECOND_PLURAL: "an",
    Person.THIRD_PLURAL: "an",
}

DATIVE_SUBJECT_MARKERS = {
    Person.FIRST_SINGULAR: "m",
    Person.SECOND_SINGULAR: "g",
    Person.THIRD_SINGULAR: "",
    Person.FIRST_PLURAL: "m",
    Person.SECOND_PLURAL: "g",
    Person.THIRD_PLURAL: "",
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