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
            Person.FIRST_SINGULAR: "u",
            Person.SECOND_SINGULAR: "u",
            Person.THIRD_SINGULAR: "u",
            Person.FIRST_PLURAL: "ey",
            Person.SECOND_PLURAL: "ey",
            Person.THIRD_PLURAL: "ey",
        },
        Region.PAZAR: {
            Person.FIRST_SINGULAR: "u",
            Person.SECOND_SINGULAR: "u",
            Person.THIRD_SINGULAR: "u",
            Person.FIRST_PLURAL: "es",
            Person.SECOND_PLURAL: "es",
            Person.THIRD_PLURAL: "es",
        },
        Region.FINDIKLI_ARHAVI: {
            Person.FIRST_SINGULAR: "u",
            Person.SECOND_SINGULAR: "u",
            Person.THIRD_SINGULAR: "u",
            Person.FIRST_PLURAL: "es",
            Person.SECOND_PLURAL: "es",
            Person.THIRD_PLURAL: "es",
        },
        Region.HOPA: {
            Person.FIRST_SINGULAR: "u",
            Person.SECOND_SINGULAR: "u",
            Person.THIRD_SINGULAR: "u",
            Person.FIRST_PLURAL: "es",
            Person.SECOND_PLURAL: "es",
            Person.THIRD_PLURAL: "es",
        },
    }
}

SUBJECT_MARKERS = {
    Person.FIRST_SINGULAR: "ma",
    Person.SECOND_SINGULAR: "ga",
    Person.THIRD_SINGULAR: "a",
    Person.FIRST_PLURAL: "ma",
    Person.SECOND_PLURAL: "ga",
    Person.THIRD_PLURAL: "a",
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
