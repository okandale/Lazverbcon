from .common import Person, Region
from .conjugator import Conjugator
from .verbs import Verb

PRESENT_TENSE_SUFFIXES = {
    Region.ARDESEN: {
        Person.FIRST_PERSON_SINGULAR: "r",
        Person.SECOND_PERSON_SINGULAR: "r",
        Person.THIRD_PERSON_SINGULAR: "n",
        Person.FIRST_PERSON_PLURAL: "rt",
        Person.SECOND_PERSON_PLURAL: "rt",
        Person.THIRD_PERSON_PLURAL: "nan",
    },
    Region.PAZAR: {
        Person.FIRST_PERSON_SINGULAR: "r",
        Person.SECOND_PERSON_SINGULAR: "r",
        Person.THIRD_PERSON_SINGULAR: "n",
        Person.FIRST_PERSON_PLURAL: "rt",
        Person.SECOND_PERSON_PLURAL: "rt",
        Person.THIRD_PERSON_PLURAL: "nan",
    },
    Region.FINDIKLI_ARHAVI: {
        Person.FIRST_PERSON_SINGULAR: "r",
        Person.SECOND_PERSON_SINGULAR: "r",
        Person.THIRD_PERSON_SINGULAR: "n",
        Person.FIRST_PERSON_PLURAL: "rt",
        Person.SECOND_PERSON_PLURAL: "rt",
        Person.THIRD_PERSON_PLURAL: "nan",
    },
    Region.HOPA: {
        Person.FIRST_PERSON_SINGULAR: "r",
        Person.SECOND_PERSON_SINGULAR: "r",
        Person.THIRD_PERSON_SINGULAR: "n",
        Person.FIRST_PERSON_PLURAL: "rt",
        Person.SECOND_PERSON_PLURAL: "rt",
        Person.THIRD_PERSON_PLURAL: "nan",
    },
}


class PresentConjugator(Conjugator):
    def conjugate_nominative_verb(self, verb: Verb) -> str:
        return super()._conjugate_nominative_verb(
            verb, PRESENT_TENSE_SUFFIXES, ending_len=1
        )
