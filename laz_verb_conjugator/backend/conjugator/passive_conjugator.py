from .common import (Mood, PassiveSuffixTable, Person, Region, Tense,
                     extract_preverb, extract_root)
from .conjugator import Conjugator
from .verbs import Verb

SUFFIXES: PassiveSuffixTable = {
    Tense.PAST: {
        Region.ARDESEN: {
            Person.FIRST_SINGULAR: "i",
            Person.SECOND_SINGULAR: "i",
            Person.THIRD_SINGULAR: "u",
            Person.FIRST_PLURAL: "it",
            Person.SECOND_PLURAL: "it",
            Person.THIRD_PLURAL: "ey",
        },
        Region.FINDIKLI_ARHAVI: {
            Person.FIRST_SINGULAR: "i",
            Person.SECOND_SINGULAR: "i",
            Person.THIRD_SINGULAR: "u",
            Person.FIRST_PLURAL: "it",
            Person.SECOND_PLURAL: "it",
            Person.THIRD_PLURAL: "es",
        },
        Region.HOPA: {
            Person.FIRST_SINGULAR: "i",
            Person.SECOND_SINGULAR: "i",
            Person.THIRD_SINGULAR: "u",
            Person.FIRST_PLURAL: "it",
            Person.SECOND_PLURAL: "it",
            Person.THIRD_PLURAL: "es",
        },
        Region.PAZAR: {
            Person.FIRST_SINGULAR: "i",
            Person.SECOND_SINGULAR: "i",
            Person.THIRD_SINGULAR: "u",
            Person.FIRST_PLURAL: "it",
            Person.SECOND_PLURAL: "it",
            Person.THIRD_PLURAL: "es",
        },
    }
}

SUBJECT_MARKERS = {
    Person.FIRST_SINGULAR: "v",
    Person.SECOND_SINGULAR: "",
    Person.THIRD_SINGULAR: "",
    Person.FIRST_PLURAL: "v",
    Person.SECOND_PLURAL: "",
    Person.THIRD_PLURAL: "",
}


class PassiveConjugator(Conjugator):

    def __init__(
        self,
        subject: Person,
        region: Region,
        object: Person,
        tense: Tense,
        moods: Mood,
    ):
        self.tense: Tense = tense
        super().__init__(subject, region, object, moods)

    def conjugate_nominative_verb(self, verb: Verb) -> str:
        prefix = extract_preverb(verb.infinitive)
        stem = extract_root(verb.infinitive, 1, 1)
        suffix = SUFFIXES[self.tense][self.region][self.subject]

        conjugation = f"{SUBJECT_MARKERS[self.subject]}{stem}{suffix}"
        if prefix:
            conjugation = prefix + conjugation
        return conjugation
