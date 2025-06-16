from .common import Person, Region, extract_prefix
from .conjugator import Conjugator
from .verbs import Verb

FUTURE_TENSE_SUFFIXES = {
    Region.ARDESEN: {
        Person.FIRST_SINGULAR: "are",
        Person.SECOND_SINGULAR: "are",
        Person.THIRD_SINGULAR: "asen",
        Person.FIRST_PLURAL: "aten",
        Person.SECOND_PLURAL: "aten",
        Person.THIRD_PLURAL: "anen",
    },
    Region.PAZAR: {
        Person.FIRST_SINGULAR: "are",
        Person.SECOND_SINGULAR: "are",
        Person.THIRD_SINGULAR: "asere",
        Person.FIRST_PLURAL: "asere",
        Person.SECOND_PLURAL: "atere",
        Person.THIRD_PLURAL: "anere",
    },
    Region.FINDIKLI_ARHAVI: {
        Person.FIRST_SINGULAR: "are",
        Person.SECOND_SINGULAR: "are",
        Person.THIRD_SINGULAR: "asen",
        Person.FIRST_PLURAL: "aten",
        Person.SECOND_PLURAL: "aten",
        Person.THIRD_PLURAL: "anen",
    },
    Region.HOPA: {
        Person.FIRST_SINGULAR: "aminon",
        Person.SECOND_SINGULAR: "aginon",
        Person.THIRD_SINGULAR: "sunon",
        Person.FIRST_PLURAL: "aminonan",
        Person.SECOND_PLURAL: "aginonan",
        Person.THIRD_PLURAL: "asunonan",
    },
}


class FutureConjugator(Conjugator):
    def conjugate_nominative_verb(self, verb: Verb) -> str:
        return super()._conjugate_nominative_verb(
            verb, FUTURE_TENSE_SUFFIXES, ending_len=2
        )
