from .verbs import Verb
from .common import Person, Region, SuffixTable, extract_prefix, extract_root
from .conjugator import Conjugator

PRESENT_PERFECT_SUFFIXES: SuffixTable = {
    Region.ARDESEN: {
        Person.FIRST_PERSON_SINGULAR: "apun",
        Person.SECOND_PERSON_SINGULAR: "apun",
        Person.THIRD_PERSON_SINGULAR: "apun",
        Person.FIRST_PERSON_PLURAL: "apunan",
        Person.SECOND_PERSON_PLURAL: "apunan",
        Person.THIRD_PERSON_PLURAL: "apunan",
    },
    Region.PAZAR: {
        Person.FIRST_PERSON_SINGULAR: "apun",
        Person.SECOND_PERSON_SINGULAR: "apun",
        Person.THIRD_PERSON_SINGULAR: "apun",
        Person.FIRST_PERSON_PLURAL: "apuran",
        Person.SECOND_PERSON_PLURAL: "apuran",
        Person.THIRD_PERSON_PLURAL: "apuran",
    },
    Region.FINDIKLI_ARHAVI: {
        Person.FIRST_PERSON_SINGULAR: "un",
        Person.SECOND_PERSON_SINGULAR: "un",
        Person.THIRD_PERSON_SINGULAR: "un",
        Person.FIRST_PERSON_PLURAL: "unan",
        Person.SECOND_PERSON_PLURAL: "unan",
        Person.THIRD_PERSON_PLURAL: "unan",
    },
    Region.HOPA: {
        Person.FIRST_PERSON_SINGULAR: "apun",
        Person.SECOND_PERSON_SINGULAR: "apun",
        Person.THIRD_PERSON_SINGULAR: "apun",
        Person.FIRST_PERSON_PLURAL: "apunan",
        Person.SECOND_PERSON_PLURAL: "apunan",
        Person.THIRD_PERSON_PLURAL: "apunan",
    },
}

SUBJECT_MARKERS = {
    Person.FIRST_PERSON_SINGULAR: "mi",
    Person.SECOND_PERSON_SINGULAR: "gi",
    Person.THIRD_PERSON_SINGULAR: "u",
    Person.FIRST_PERSON_PLURAL: "mi",
    Person.SECOND_PERSON_PLURAL: "gi",
    Person.THIRD_PERSON_PLURAL: "u",
}


PREVERB_HANDLERS = {}


def handle_preverb(preverb):
    def wrapper(func):
        PREVERB_HANDLERS[preverb] = func

    return wrapper



class PresentPerfectConjugator(Conjugator):
    def conjugate_nominative_verb(self, verb: Verb) -> str:
        
        prefix = extract_prefix(verb.infinitive)
        if prefix in PREVERB_HANDLERS:
            return PREVERB_HANDLERS[prefix](
                self, verb, prefix
            )
        else:
            return self.conjugate_default_nominative_verb(verb, prefix)

    def conjugate_default_nominative_verb(self, verb: Verb, prefix) -> str:
        stem = extract_root(verb.infinitive, 1, 1)
        conjugation = SUBJECT_MARKERS[self.subject] + stem + \
            PRESENT_PERFECT_SUFFIXES[self.region][self.subject]
        if prefix:
            return prefix + conjugation
        else:
            return conjugation
        

@handle_preverb("do")
def handle_do_prefix(
    conjugator: Conjugator,
    verb: Verb,
    prefix,
):
    if verb.present_third.startswith("di"):
        if conjugator.subject.is_first_person() or conjugator.subject.is_second_person():
            # Remove the first "do" before applying the subject marker.
            stem = extract_root(verb.infinitive, 2, 1)
            conjugation = SUBJECT_MARKERS[conjugator.subject] + stem + \
                PRESENT_PERFECT_SUFFIXES[conjugator.region][conjugator.subject]
            return f"do{conjugation}"
        else:
            # Remove the prefix completely.
            breakpoint()
            extended_stem = extract_root(verb.present_third, 2, 2)
            stem = extended_stem
            conjugation = (
                stem + PRESENT_PERFECT_SUFFIXES[
                    conjugator.region
                ][conjugator.subject]
            )
        return conjugation
    else:
        return conjugator.conjugate_default_nominative_verb(verb, prefix)