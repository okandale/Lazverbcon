from .common import Person, Region, SuffixTable, extract_prefix
from .conjugator import Conjugator
from .verbs import Verb

PAST_TENSE_SUFFIXES: SuffixTable = {
    Region.ARDESEN: {
        Person.FIRST_PERSON_SINGULAR: "i",
        Person.SECOND_PERSON_SINGULAR: "i",
        Person.THIRD_PERSON_SINGULAR: "u",
        Person.FIRST_PERSON_PLURAL: "it",
        Person.SECOND_PERSON_PLURAL: "it",
        Person.THIRD_PERSON_PLURAL: "ey",
    },
    Region.PAZAR: {
        Person.FIRST_PERSON_SINGULAR: "i",
        Person.SECOND_PERSON_SINGULAR: "i",
        Person.THIRD_PERSON_SINGULAR: "u",
        Person.FIRST_PERSON_PLURAL: "it",
        Person.SECOND_PERSON_PLURAL: "it",
        Person.THIRD_PERSON_PLURAL: "es",
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
}


SUBJECT_MARKERS = {
    Person.FIRST_PERSON_SINGULAR: "ma",
    Person.SECOND_PERSON_SINGULAR: "ga",
    Person.THIRD_PERSON_SINGULAR: "a",
    Person.FIRST_PERSON_PLURAL: "ma",
    Person.SECOND_PERSON_PLURAL: "ga",
    Person.THIRD_PERSON_PLURAL: "a",
}


class PastConjugator(Conjugator):

    def conjugate_ergative_verb(self, verb):
        pass

    def conjugate_nominative_verb(self, verb: Verb) -> str:
        # Extract a potential verb prefix.
        return super().conjugate_nominative_verb(
            verb, PAST_TENSE_SUFFIXES, ending_len=2
        )

    def conjugate_dative_verb(self, verb):
        pass
