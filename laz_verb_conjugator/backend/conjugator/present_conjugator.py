from .common import Aspect, Mood, Person, Region
from .conjugator import Conjugator
from .ergative_verbs import ConjugateErgativeVerbMixin
from .nominative_verbs import ConjugateNominativeVerbMixin
from .rules.applicative import (ApplicativePresentFirstPersonObject,
                                ApplicativePresentSecondPersonObject,
                                ApplicativePresentThirdPersonObject)
from .rules.common import (DoPreverb, NsEndingRule,
                           SubjectObjectNsOrRsEndingRule, UStartingRule)
from .tables.base import (APPLICATIVE_PREFIXES, APPLICATIVE_SUFFIXES,
                          CAUSATIVE_PREFIXES, OPTATIVE_SUFFIXES,
                          PRESENT_ERGATIVE_SUFFIXES,
                          PRESENT_NOMINATIVE_SUFFIXES,
                          PRESENT_PASSIVE_SUFFIXES, PRESENT_POTENTIAL_PREFIXES,
                          PRESENT_POTENTIAL_SUFFIXES)
from .tables.preverbs import (PREVERB_APPLICATIVE_PREFIXES_TABLE,
                              PREVERB_CAUSATIVE_PREFIXES_TABLE,
                              PREVERB_PREFIXES_TABLE)
from .verbs import Verb

DATIVE_SUFFIXES = {
    Person.FIRST_SINGULAR: "",
    Person.SECOND_SINGULAR: "",
    Person.THIRD_SINGULAR: "",
    Person.FIRST_PLURAL: "an",
    Person.SECOND_PLURAL: "an",
    Person.THIRD_PLURAL: "an",
}

DATIVE_SUBJECT_MARKERS = {
    Person.FIRST_SINGULAR: "m",
    Person.SECOND_SINGULAR: "g",
    Person.THIRD_SINGULAR: "",
    Person.FIRST_PLURAL: "m",
    Person.SECOND_PLURAL: "g",
    Person.THIRD_PLURAL: "",
}

DATIVE_SECOND_PERSON_SUFFIXES = {
    Person.FIRST_SINGULAR: "r",
    Person.THIRD_SINGULAR: "r",
    Person.FIRST_PLURAL: "t",
    Person.THIRD_PLURAL: "r",
}


class PresentConjugator(
    Conjugator, ConjugateNominativeVerbMixin, ConjugateErgativeVerbMixin
):

    DATIVE_RULES = [
        SubjectObjectNsOrRsEndingRule(
            DATIVE_SUBJECT_MARKERS, DATIVE_SECOND_PERSON_SUFFIXES
        ),
        NsEndingRule(DATIVE_SUBJECT_MARKERS, DATIVE_SUFFIXES),
        UStartingRule(DATIVE_SUBJECT_MARKERS, DATIVE_SUFFIXES),
        SubjectObjectNsOrRsEndingRule(
            DATIVE_SUBJECT_MARKERS, DATIVE_SECOND_PERSON_SUFFIXES
        ),
    ]

    ERGATIVE_RULES = []

    def conjugate_default_nominative_verb(self, verb: Verb) -> str:
        if Mood.OPTATIVE in self.moods:
            suffix_table = OPTATIVE_SUFFIXES[Person.THIRD_SINGULAR]
        else:
            suffix_table = PRESENT_NOMINATIVE_SUFFIXES[verb.suffix]

        conjugation = verb.stem + suffix_table[self.region][self.subject]
        if verb.preverb in PREVERB_PREFIXES_TABLE:
            conjugation = (
                PREVERB_PREFIXES_TABLE[verb.preverb][self.region][self.subject]
                + conjugation
            )
        elif self.subject.is_first_person():
            conjugation = self.apply_epenthetic_segment(conjugation)

        if Mood.NEGATIVE_IMPERATIVE in self.moods:
            return f"mo {conjugation}"
        else:
            return conjugation

    def conjugate_default_dative_verb(self, verb: Verb) -> str:
        conjugation = (
            DATIVE_SUBJECT_MARKERS[self.subject]
            + verb.present_third
            + DATIVE_SUFFIXES[self.subject]
        )
        if Mood.NEGATIVE_IMPERATIVE in self.moods:
            return f"mo {conjugation}"
        else:
            return conjugation

    def conjugate_default_ergative_verb(self, verb: Verb) -> str:
        if Mood.APPLICATIVE in self.moods and verb.preverb is None:
            verb_prefix = APPLICATIVE_PREFIXES[self.object][self.region][
                self.subject
            ]
            conjugation = f"{verb_prefix}{verb.stem}"
        elif Mood.CAUSATIVE in self.moods:
            verb_prefix = CAUSATIVE_PREFIXES[self.object][self.region][
                self.subject
            ]
            conjugation = f"{verb_prefix}{verb.stem}"
        elif self.aspect == Aspect.POTENTIAL and verb.preverb is None:
            verb_prefix = PRESENT_POTENTIAL_PREFIXES[self.region][self.subject]
            conjugation = f"{verb_prefix}{verb.stem}"
        elif verb.preverb is None:
            conjugation = f"{verb.prefix}{verb.stem}"
        else:
            conjugation = verb.stem

        if (
            verb.preverb is None
            and self.moods == Mood.NONE
            and self.subject.is_first_person()
        ):
            conjugation = self.apply_epenthetic_segment(conjugation)

        if Mood.CAUSATIVE in self.moods:
            conjugation += "ap"

        if Mood.OPTATIVE in self.moods:
            conjugation += OPTATIVE_SUFFIXES[self.object][self.region][
                self.subject
            ]
        elif Mood.APPLICATIVE in self.moods:
            conjugation += APPLICATIVE_SUFFIXES[self.object][self.region][
                self.subject
            ]
        elif self.aspect == Aspect.POTENTIAL:
            conjugation += PRESENT_POTENTIAL_SUFFIXES[self.region][
                self.subject
            ]
        elif self.aspect == Aspect.PASSIVE:
            conjugation += PRESENT_PASSIVE_SUFFIXES[self.region][self.subject]
        else:
            conjugation += PRESENT_ERGATIVE_SUFFIXES[verb.suffix][self.region][
                self.subject
            ]

        if verb.preverb is not None:
            if Mood.APPLICATIVE in self.moods:
                prefix_table = PREVERB_APPLICATIVE_PREFIXES_TABLE[
                    verb.preverb
                ][self.object]
            elif Mood.CAUSATIVE in self.moods:
                prefix_table = PREVERB_CAUSATIVE_PREFIXES_TABLE[verb.preverb][
                    self.object
                ]
            else:
                prefix_table = PREVERB_PREFIXES_TABLE[verb.preverb]
            conjugation = prefix_table[self.region][self.subject] + conjugation

        if Mood.NEGATIVE_IMPERATIVE in self.moods:
            return f"mo {conjugation}"
        else:
            return conjugation
