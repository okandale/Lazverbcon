from backend.conjugator.verb_rules import DoPreverb

from .common import Person, Region
from .conjugator import Conjugator
from .nominative_verbs import ConjugateNominativeVerbMixin
from .verbs import Verb

PAST_PROGRESSIVE_TENSE_SUFFIXES = {
    Region.ARDESEN: {
        Person.FIRST_SINGULAR: "rt̆i",
        Person.SECOND_SINGULAR: "rt̆i",
        Person.THIRD_SINGULAR: "rt̆u",
        Person.FIRST_PLURAL: "rt̆it",
        Person.SECOND_PLURAL: "rt̆it",
        Person.THIRD_PLURAL: "rt̆ey",
    },
    Region.PAZAR: {
        Person.FIRST_SINGULAR: "rt̆i",
        Person.SECOND_SINGULAR: "rt̆i",
        Person.THIRD_SINGULAR: "rt̆u",
        Person.FIRST_PLURAL: "rt̆it",
        Person.SECOND_PLURAL: "rt̆it",
        Person.THIRD_PLURAL: "t̆es",
    },
    Region.FINDIKLI_ARHAVI: {
        Person.FIRST_SINGULAR: "rt̆i",
        Person.SECOND_SINGULAR: "rt̆i",
        Person.THIRD_SINGULAR: "rt̆u",
        Person.FIRST_PLURAL: "rt̆it",
        Person.SECOND_PLURAL: "rt̆it",
        Person.THIRD_PLURAL: "t̆es",
    },
    Region.HOPA: {
        Person.FIRST_SINGULAR: "rt̆i",
        Person.SECOND_SINGULAR: "rt̆i",
        Person.THIRD_SINGULAR: "rt̆u",
        Person.FIRST_PLURAL: "rt̆it",
        Person.SECOND_PLURAL: "rt̆it",
        Person.THIRD_PLURAL: "t̆es",
    },
}


class PastProgressiveConjugator(Conjugator, ConjugateNominativeVerbMixin):

    NOMINATIVE_RULES = [
        DoPreverb(ending_len=2, suffixes=PAST_PROGRESSIVE_TENSE_SUFFIXES)
    ]

    def conjugate_ergative_verb(self, verb):
        pass

    def conjugate_default_nominative_verb(self, verb: Verb) -> str:
        return ConjugateNominativeVerbMixin.conjugate_nominative_verb(
            self,
            verb,
            region_suffix_table=PAST_PROGRESSIVE_TENSE_SUFFIXES,
            ending_len=2,
        )

    def conjugate_dative_verb(self, verb):
        pass
