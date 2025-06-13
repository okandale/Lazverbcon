from .conjugator import Conjugator
from .verbs import Verb
from .common import PHONETIC_PREFIXES_FIRST_PERSON, Person, extract_initial_cluster

SUFFIXES = {
    Person.FIRST_PERSON_SINGULAR: 'i',
    Person.SECOND_PERSON_SINGULAR: 'i',
    Person.THIRD_PERSON_SINGULAR: 'u',
    Person.FIRST_PERSON_PLURAL: 'it',
    Person.SECOND_PERSON_PLURAL: 'it',
    Person.THIRD_PERSON_PLURAL: 'es' # XXX: can be "ey" sometimes given the region.
}

class PastConjugator(Conjugator):

    def conjugate_ergative_verb(self, verb):
        pass
    
    def conjugate_nominative_verb(self, verb: Verb) -> str:
        stem = verb.present_third[:-2]
        conjugation = f"{stem}{SUFFIXES[self.subject]}"
        if self.subject.is_first_person():
            conjugation = self.apply_prothesis(conjugation)
        return conjugation
    
    def conjugate_dative_verb(self, verb):
        pass
        