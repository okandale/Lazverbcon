from .common import Person, Region, extract_prefix
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
    },
}

PREVERB_HANDLERS = {}


def handle_preverb(preverb):
    def wrapper(func):
        PREVERB_HANDLERS[preverb] = func

    return wrapper


class PastConjugator(Conjugator):

    def conjugate_ergative_verb(self, verb):
        pass

    def conjugate_nominative_verb(self, verb: Verb) -> str:
        # Extract a potential verb prefix.
        prefix = extract_prefix(verb.infinitive)
        if prefix in PREVERB_HANDLERS:
            return PREVERB_HANDLERS[prefix](self, verb, prefix)
        else:
            return self.handle_default_nominative_verb(verb, prefix)

    def conjugate_dative_verb(self, verb):
        pass

    def handle_default_nominative_verb(self, verb, prefix):
        # Extract the "extended stem" (potential prefix + stem, if any)
        # from the present third form.
        extended_stem = verb.present_third[:-2]

        # If the extended stem contains the prefix, remove it: get the stem.
        # breakpoint()
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


@handle_preverb("do")
def handle_do_prefix(conjugator: Conjugator, verb: Verb, prefix):
    extended_stem = verb.present_third[:-2]
    if verb.present_third.startswith("di"):
        if conjugator.subject.is_first_person():
            # Remove the first "d" before applying the epenthetic segment.
            stem = extended_stem[1:]
            conjugation = conjugator.apply_epenthetic_segment(
                stem
                + PAST_TENSE_SUFFIXES[conjugator.region][conjugator.subject]
            )
            return f"do{conjugation}"
        else:
            stem = extended_stem
            conjugation = (
                stem
                + PAST_TENSE_SUFFIXES[conjugator.region][conjugator.subject]
            )
        return conjugation
    else:
        return conjugator.handle_default_nominative_verb(verb, prefix)
