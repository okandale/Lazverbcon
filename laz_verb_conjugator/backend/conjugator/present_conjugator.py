from .common import Person, Region, extract_prefix, extract_root
from .conjugator import Conjugator
from .nominative_verbs import ConjugateNominativeVerbMixin
from .verb_rules import DoPreverb, NsEndingRule, UStartingRule
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


class PresentConjugator(Conjugator, ConjugateNominativeVerbMixin):

    DATIVE_RULES = [
        NsEndingRule(DATIVE_SUBJECT_MARKERS, DATIVE_SUFFIXES),
        UStartingRule(DATIVE_SUBJECT_MARKERS, DATIVE_SUFFIXES),
    ]

    NOMINATIVE_RULES = [
        DoPreverb(ending_len=1, suffixes=PRESENT_TENSE_SUFFIXES)
    ]

    def conjugate_default_nominative_verb(self, verb: Verb) -> str:
        return ConjugateNominativeVerbMixin.conjugate_nominative_verb(
            self, verb, suffix_table=PRESENT_TENSE_SUFFIXES, ending_len=1
        )

    def conjugate_default_dative_verb(self, verb: Verb) -> str:
        return (
            DATIVE_SUBJECT_MARKERS[self.subject]
            + verb.present_third
            + DATIVE_SUFFIXES[self.subject]
        )
