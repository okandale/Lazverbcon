from .common import Person, Region
from .conjugator import Conjugator
from .verbs import Verb

PAST_PROGRESSIVE_TENSE_SUFFIXES = {
    Region.ARDESEN: {
        Person.FIRST_PERSON_SINGULAR: "rt̆i",
        Person.SECOND_PERSON_SINGULAR: "rt̆i",
        Person.THIRD_PERSON_SINGULAR: "rt̆u",
        Person.FIRST_PERSON_PLURAL: "rt̆it",
        Person.SECOND_PERSON_PLURAL: "rt̆it",
        Person.THIRD_PERSON_PLURAL: "rt̆ey",
    },
    Region.PAZAR: {
        Person.FIRST_PERSON_SINGULAR: "rt̆i",
        Person.SECOND_PERSON_SINGULAR: "rt̆i",
        Person.THIRD_PERSON_SINGULAR: "rt̆u",
        Person.FIRST_PERSON_PLURAL: "rt̆it",
        Person.SECOND_PERSON_PLURAL: "rt̆it",
        Person.THIRD_PERSON_PLURAL: "t̆es",
    },
    Region.FINDIKLI_ARHAVI: {
        Person.FIRST_PERSON_SINGULAR: "rt̆i",
        Person.SECOND_PERSON_SINGULAR: "rt̆i",
        Person.THIRD_PERSON_SINGULAR: "rt̆u",
        Person.FIRST_PERSON_PLURAL: "rt̆it",
        Person.SECOND_PERSON_PLURAL: "rt̆it",
        Person.THIRD_PERSON_PLURAL: "t̆es",
    },
    Region.HOPA: {
        Person.FIRST_PERSON_SINGULAR: "rt̆i",
        Person.SECOND_PERSON_SINGULAR: "rt̆i",
        Person.THIRD_PERSON_SINGULAR: "rt̆u",
        Person.FIRST_PERSON_PLURAL: "rt̆it",
        Person.SECOND_PERSON_PLURAL: "rt̆it",
        Person.THIRD_PERSON_PLURAL: "t̆es",
    },
}


class PastProgressiveConjugator(Conjugator):

    def conjugate_ergative_verb(self, verb):
        pass

    def conjugate_nominative_verb(self, verb: Verb) -> str:
        # Extract a potential verb prefix.
        return super().conjugate_nominative_verb(
            verb, PAST_PROGRESSIVE_TENSE_SUFFIXES, ending_len=1
        )

    def conjugate_dative_verb(self, verb):
        pass
