from .common import Person, extract_prefix, Region
from .conjugator import Conjugator
from .verbs import Verb

PAST_TENSE_SUFFIXES = {
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
    }
}


class PastConjugator(Conjugator):

    def conjugate_ergative_verb(self, verb):
        pass

    def conjugate_nominative_verb(self, verb: Verb) -> str:
        # Extract a potential verb prefix.
        prefix = extract_prefix(verb.infinitive)

        # Extract the "extended stem" (stem + potential prefix, if any)
        # from the present third form.
        extended_stem = verb.present_third[:-2]

        # If the extended stem contains the prefix, remove it: get the stem.
        stem = (
            extended_stem[len(prefix) :]
            if prefix is not None
            else extended_stem
        )

        # Start actual conjugation.
        conjugation = f"{stem}{PAST_TENSE_SUFFIXES[self.region][self.subject]}"
        if self.subject.is_first_person():
            conjugation = self.apply_epenthetic_segment(conjugation)

        # Put back the prefix if it exists.
        if prefix is not None:
            conjugation = f"{prefix}{conjugation}"
        return conjugation

    def conjugate_dative_verb(self, verb):
        pass
