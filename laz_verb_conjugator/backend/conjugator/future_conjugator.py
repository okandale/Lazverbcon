from .common import Person, Region
from .conjugator import Conjugator
from .verbs import Verb

FUTURE_TENSE_SUFFIXES = {
    Region.ARDESEN: {
        Person.FIRST_PERSON_SINGULAR: "are",
        Person.SECOND_PERSON_SINGULAR: "are",
        Person.THIRD_PERSON_SINGULAR: "asen",
        Person.FIRST_PERSON_PLURAL: "aten",
        Person.SECOND_PERSON_PLURAL: "aten",
        Person.THIRD_PERSON_PLURAL: "anen",
    },
    Region.PAZAR: {
        Person.FIRST_PERSON_SINGULAR: "are",
        Person.SECOND_PERSON_SINGULAR: "are",
        Person.THIRD_PERSON_SINGULAR: "asere",
        Person.FIRST_PERSON_PLURAL: "asere",
        Person.SECOND_PERSON_PLURAL: "atere",
        Person.THIRD_PERSON_PLURAL: "anere",
    },
    Region.FINDIKLI_ARHAVI: {
        Person.FIRST_PERSON_SINGULAR: "are",
        Person.SECOND_PERSON_SINGULAR: "are",
        Person.THIRD_PERSON_SINGULAR: "asen",
        Person.FIRST_PERSON_PLURAL: "aten",
        Person.SECOND_PERSON_PLURAL: "aten",
        Person.THIRD_PERSON_PLURAL: "anen",
    },
    Region.HOPA: {
        Person.FIRST_PERSON_SINGULAR: "aminon",
        Person.SECOND_PERSON_SINGULAR: "aginon",
        Person.THIRD_PERSON_SINGULAR: "sunon",
        Person.FIRST_PERSON_PLURAL: "aminonan",
        Person.SECOND_PERSON_PLURAL: "aginonan",
        Person.THIRD_PERSON_PLURAL: "asunonan",
    },
}

class FutureConjugator(Conjugator):
    def conjugate_nominative_verb(self, verb: Verb) -> str:
        pass
