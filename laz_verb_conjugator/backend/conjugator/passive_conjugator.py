from .conjugator import Conjugator
from .common import (
    PassiveSuffixTable,
    Person,
    Region,
    Tense,
    extract_prefix,
    extract_root,
)
from .verbs import Verb


SUFFIXES: PassiveSuffixTable = {
    Tense.PAST: {
        Region.ARDESEN: {
            Person.FIRST_PERSON_SINGULAR: "i",
            Person.SECOND_PERSON_SINGULAR: "i",
            Person.THIRD_PERSON_SINGULAR: "u",
            Person.FIRST_PERSON_PLURAL: "it",
            Person.SECOND_PERSON_PLURAL: "it",
            Person.THIRD_PERSON_PLURAL: "ey",
        },
        Region.FINDIKLI_ARHAVI: {
            Person.FIRST_PERSON_SINGULAR: "i",
            Person.SECOND_PERSON_SINGULAR: "i",
            Person.THIRD_PERSON_SINGULAR: "u",
            Person.FIRST_PERSON_PLURAL: "it",
            Person.SECOND_PERSON_PLURAL: "it",
            Person.THIRD_PERSON_PLURAL: "es",
        },
        Region.HOPA: {
            Person.FIRST_PERSON_SINGULAR: "i",
            Person.SECOND_PERSON_SINGULAR: "i",
            Person.THIRD_PERSON_SINGULAR: "u",
            Person.FIRST_PERSON_PLURAL: "it",
            Person.SECOND_PERSON_PLURAL: "it",
            Person.THIRD_PERSON_PLURAL: "es",
        },
        Region.PAZAR: {
            Person.FIRST_PERSON_SINGULAR: "i",
            Person.SECOND_PERSON_SINGULAR: "i",
            Person.THIRD_PERSON_SINGULAR: "u",
            Person.FIRST_PERSON_PLURAL: "it",
            Person.SECOND_PERSON_PLURAL: "it",
            Person.THIRD_PERSON_PLURAL: "es",
        },
    }
}

SUBJECT_MARKERS = {
    Person.FIRST_PERSON_SINGULAR: "v",
    Person.SECOND_PERSON_SINGULAR: "",
    Person.THIRD_PERSON_SINGULAR: "",
    Person.FIRST_PERSON_PLURAL: "v",
    Person.SECOND_PERSON_PLURAL: "",
    Person.THIRD_PERSON_PLURAL: "",
}


class PassiveConjugator(Conjugator):

    def __init__(
        self, subject: Person, region: Region, object: Person, tense: Tense
    ):
        self.tense: Tense = tense
        super().__init__(subject, region, object)

    def conjugate_nominative_verb(self, verb: Verb) -> str:
        prefix = extract_prefix(verb.infinitive)
        stem = extract_root(verb.infinitive, 1, 1)
        suffix = SUFFIXES[self.tense][self.region][self.subject]

        conjugation = f"{SUBJECT_MARKERS[self.subject]}{stem}{suffix}"
        if prefix:
            conjugation = prefix + conjugation
        return conjugation
