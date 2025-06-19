from .common import Person, Region, SuffixTable, extract_prefix
from .conjugator import Conjugator
from .nominative_verbs import ConjugateNominativeVerbMixin
from .verb_rules import DoPreverbOptative
from .verbs import Verb

OPTATIVE_SUFFIXES = {
    Person.FIRST_SINGULAR: "a",
    Person.SECOND_SINGULAR: "a",
    Person.THIRD_SINGULAR: "as",
    Person.FIRST_PLURAL: "at",
    Person.SECOND_PLURAL: "at",
    Person.THIRD_PLURAL: "an",
}


class OptativeConjugator(Conjugator):

    NOMINATIVE_RULES = [
        DoPreverbOptative(ending_len=2, suffixes=OPTATIVE_SUFFIXES)
    ]

    def conjugate_default_nominative_verb(self, verb: Verb) -> str:
        return ConjugateNominativeVerbMixin.conjugate_nominative_verb(
            self, verb, suffix_table=OPTATIVE_SUFFIXES, ending_len=2
        )
