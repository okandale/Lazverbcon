from .conjugator import Conjugator
from .common import (
    Person,
    PotentialSuffixTable,
    Region,
    Tense,
    extract_prefix,
    extract_root,
)
from .verbs import Verb


SUFFIXES: PotentialSuffixTable = {
    Tense.PAST: {
        Region.ARDESEN: {
            Person.FIRST_PERSON_SINGULAR: "u",
            Person.SECOND_PERSON_SINGULAR: "u",
            Person.THIRD_PERSON_SINGULAR: "u",
            Person.FIRST_PERSON_PLURAL: "ey",
            Person.SECOND_PERSON_PLURAL: "ey",
            Person.THIRD_PERSON_PLURAL: "ey",
        },
        Region.PAZAR: {
            Person.FIRST_PERSON_SINGULAR: "u",
            Person.SECOND_PERSON_SINGULAR: "u",
            Person.THIRD_PERSON_SINGULAR: "u",
            Person.FIRST_PERSON_PLURAL: "es",
            Person.SECOND_PERSON_PLURAL: "es",
            Person.THIRD_PERSON_PLURAL: "es",
        },
        Region.FINDIKLI_ARHAVI: {
            Person.FIRST_PERSON_SINGULAR: "u",
            Person.SECOND_PERSON_SINGULAR: "u",
            Person.THIRD_PERSON_SINGULAR: "u",
            Person.FIRST_PERSON_PLURAL: "es",
            Person.SECOND_PERSON_PLURAL: "es",
            Person.THIRD_PERSON_PLURAL: "es",
        },
        Region.HOPA: {
            Person.FIRST_PERSON_SINGULAR: "u",
            Person.SECOND_PERSON_SINGULAR: "u",
            Person.THIRD_PERSON_SINGULAR: "u",
            Person.FIRST_PERSON_PLURAL: "es",
            Person.SECOND_PERSON_PLURAL: "es",
            Person.THIRD_PERSON_PLURAL: "es",
        },
    }
}

SUBJECT_MARKERS = {
    Person.FIRST_PERSON_SINGULAR: "ma",
    Person.SECOND_PERSON_SINGULAR: "ga",
    Person.THIRD_PERSON_SINGULAR: "a",
    Person.FIRST_PERSON_PLURAL: "ma",
    Person.SECOND_PERSON_PLURAL: "ga",
    Person.THIRD_PERSON_PLURAL: "a",
}


class PotentialConjugator(Conjugator):

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
