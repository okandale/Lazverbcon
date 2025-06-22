from .common import Person, Region, SuffixTable, extract_preverb
from .conjugator import Conjugator
from .nominative_verbs import ConjugateNominativeVerbMixin
from .rules.common import DoPreverb
from .verbs import Verb

PAST_TENSE_SUFFIXES: SuffixTable = {
    Region.ARDESEN: {
        Person.FIRST_SINGULAR: "i",
        Person.SECOND_SINGULAR: "i",
        Person.THIRD_SINGULAR: "u",
        Person.FIRST_PLURAL: "it",
        Person.SECOND_PLURAL: "it",
        Person.THIRD_PLURAL: "ey",
    },
    Region.PAZAR: {
        Person.FIRST_SINGULAR: "i",
        Person.SECOND_SINGULAR: "i",
        Person.THIRD_SINGULAR: "u",
        Person.FIRST_PLURAL: "it",
        Person.SECOND_PLURAL: "it",
        Person.THIRD_PLURAL: "es",
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
}


SUBJECT_MARKERS = {
    Person.FIRST_SINGULAR: "ma",
    Person.SECOND_SINGULAR: "ga",
    Person.THIRD_SINGULAR: "a",
    Person.FIRST_PLURAL: "ma",
    Person.SECOND_PLURAL: "ga",
    Person.THIRD_PLURAL: "a",
}


class PastConjugator(Conjugator, ConjugateNominativeVerbMixin):

    NOMINATIVE_RULES = [DoPreverb(ending_len=2, suffixes=PAST_TENSE_SUFFIXES)]

    def conjugate_ergative_verb(self, verb):
        pass

    def conjugate_default_nominative_verb(self, verb: Verb) -> str:
        return (
            ConjugateNominativeVerbMixin.conjugate_nominative_verb_region_wise(
                self,
                verb,
                region_suffix_table=PAST_TENSE_SUFFIXES,
                ending_len=2,
            )
        )

    def conjugate_dative_verb(self, verb):
        pass
