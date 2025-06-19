from .common import Person, Region, SuffixTable, extract_prefix, extract_root
from .conjugator import Conjugator
from .verb_rules import VerbRuleWithSuffixes
from .verbs import Verb

PRESENT_PERFECT_SUFFIXES: SuffixTable = {
    Region.ARDESEN: {
        Person.FIRST_SINGULAR: "apun",
        Person.SECOND_SINGULAR: "apun",
        Person.THIRD_SINGULAR: "apun",
        Person.FIRST_PLURAL: "apunan",
        Person.SECOND_PLURAL: "apunan",
        Person.THIRD_PLURAL: "apunan",
    },
    Region.PAZAR: {
        Person.FIRST_SINGULAR: "apun",
        Person.SECOND_SINGULAR: "apun",
        Person.THIRD_SINGULAR: "apun",
        Person.FIRST_PLURAL: "apuran",
        Person.SECOND_PLURAL: "apuran",
        Person.THIRD_PLURAL: "apuran",
    },
    Region.FINDIKLI_ARHAVI: {
        Person.FIRST_SINGULAR: "un",
        Person.SECOND_SINGULAR: "un",
        Person.THIRD_SINGULAR: "un",
        Person.FIRST_PLURAL: "unan",
        Person.SECOND_PLURAL: "unan",
        Person.THIRD_PLURAL: "unan",
    },
    Region.HOPA: {
        Person.FIRST_SINGULAR: "apun",
        Person.SECOND_SINGULAR: "apun",
        Person.THIRD_SINGULAR: "apun",
        Person.FIRST_PLURAL: "apunan",
        Person.SECOND_PLURAL: "apunan",
        Person.THIRD_PLURAL: "apunan",
    },
}

SUBJECT_MARKERS = {
    Person.FIRST_SINGULAR: "mi",
    Person.SECOND_SINGULAR: "gi",
    Person.THIRD_SINGULAR: "u",
    Person.FIRST_PLURAL: "mi",
    Person.SECOND_PLURAL: "gi",
    Person.THIRD_PLURAL: "u",
}


PREVERB_HANDLERS = {}


def handle_preverb(preverb):
    def wrapper(func):
        PREVERB_HANDLERS[preverb] = func

    return wrapper


class PresentPerfectDoPreverbRule(VerbRuleWithSuffixes):
    def matches(self, conjugator: "Conjugator", verb: Verb):
        prefix = extract_prefix(verb.infinitive)
        return prefix == "do" and verb.present_third.startswith("di")

    def apply(self, conjugator: "Conjugator", verb: Verb):
        prefix = extract_prefix(verb.infinitive)
        subject_marker = SUBJECT_MARKERS[conjugator.subject]
        # Remove the first "do" before applying the subject marker.
        stem = extract_root(verb.infinitive, 2, 1)
        conjugation = (
            subject_marker
            + stem
            + PRESENT_PERFECT_SUFFIXES[conjugator.region][conjugator.subject]
        )
        if prefix[:-1] in "aeiou" or subject_marker[0] in "aeiou":
            return f"d{conjugation}"
        else:
            return f"do{conjugation}"


class PresentPerfectConjugator(Conjugator):

    NOMINATIVE_RULES = [
        PresentPerfectDoPreverbRule(suffixes=PRESENT_PERFECT_SUFFIXES)
    ]

    def conjugate_default_nominative_verb(self, verb: Verb) -> str:
        prefix = extract_prefix(verb.infinitive)
        stem = extract_root(verb.infinitive, 1, 1)
        conjugation = (
            SUBJECT_MARKERS[self.subject]
            + stem
            + PRESENT_PERFECT_SUFFIXES[self.region][self.subject]
        )
        if prefix:
            return prefix + conjugation
        else:
            return conjugation
