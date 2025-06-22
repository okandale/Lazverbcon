from .common import Mood, Person, Region, extract_preverb, extract_root
from .conjugator import Conjugator
from .ergative_verbs import ConjugateErgativeVerbMixin
from .nominative_verbs import ConjugateNominativeVerbMixin
from .rules.applicative import (
    ApplicativePresentFirstPersonObject,
    ApplicativePresentSecondPersonObject,
    ApplicativePresentThirdPersonObject,
)
from .rules.common import (
    DoPreverb,
    NsEndingRule,
    SubjectObjectNsOrRsEndingRule,
    UStartingRule,
)
from .verbs import Verb
from .tables.base import (
    APPLICATIVE_PREFIXES,
    CAUSATIVE_PREFIXES,
    OPTATIVE_SUFFIXES,
    APPLICATIVE_SUFFIXES,
    PRESENT_ERGATIVE_SUFFIXES
)

PRESENT_TENSE_SUFFIXES = {
    Region.ARDESEN: {
        Person.FIRST_SINGULAR: "r",
        Person.SECOND_SINGULAR: "r",
        Person.THIRD_SINGULAR: "n",
        Person.FIRST_PLURAL: "rt",
        Person.SECOND_PLURAL: "rt",
        Person.THIRD_PLURAL: "nan",
    },
    Region.PAZAR: {
        Person.FIRST_SINGULAR: "r",
        Person.SECOND_SINGULAR: "r",
        Person.THIRD_SINGULAR: "n",
        Person.FIRST_PLURAL: "rt",
        Person.SECOND_PLURAL: "rt",
        Person.THIRD_PLURAL: "nan",
    },
    Region.FINDIKLI_ARHAVI: {
        Person.FIRST_SINGULAR: "r",
        Person.SECOND_SINGULAR: "r",
        Person.THIRD_SINGULAR: "n",
        Person.FIRST_PLURAL: "rt",
        Person.SECOND_PLURAL: "rt",
        Person.THIRD_PLURAL: "nan",
    },
    Region.HOPA: {
        Person.FIRST_SINGULAR: "r",
        Person.SECOND_SINGULAR: "r",
        Person.THIRD_SINGULAR: "n",
        Person.FIRST_PLURAL: "rt",
        Person.SECOND_PLURAL: "rt",
        Person.THIRD_PLURAL: "nan",
    },
}

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

    NOMINATIVE_RULES = [
        DoPreverb(ending_len=1, suffixes=PRESENT_TENSE_SUFFIXES)
    ]

    ERGATIVE_RULES = []

    def conjugate_default_nominative_verb(self, verb: Verb) -> str:
        if Mood.OPTATIVE in self.moods:
            suffix_table = OPTATIVE_SUFFIXES[Person.THIRD_SINGULAR]
        else:
            suffix_table = PRESENT_TENSE_SUFFIXES
            
        
        #return (
        #    ConjugateNominativeVerbMixin.conjugate_nominative_verb_region_wise(
        #        self,
        #        verb,
        #        region_suffix_table=suffix_table,
        #        ending_len=1,
        #    )
        #)

    def conjugate_default_dative_verb(self, verb: Verb) -> str:
        return (
            DATIVE_SUBJECT_MARKERS[self.subject]
            + verb.present_third
            + DATIVE_SUFFIXES[self.subject]
        )

    def conjugate_default_ergative_verb(self, verb: Verb) -> str:

        if Mood.APPLICATIVE in self.moods:
            verb_prefix = APPLICATIVE_PREFIXES[self.object][self.region][
                self.subject
            ]
            conjugation = f"{verb_prefix}{verb.stem}"
        elif Mood.CAUSATIVE in self.moods:
            verb_prefix = CAUSATIVE_PREFIXES[self.object][self.region][
                self.subject
            ]
            conjugation = f"{verb_prefix}{verb.stem}"
            pass
        else:
            conjugation = f"{verb.prefix}{verb.stem}"

        if (
            conjugation.startswith(("a", "e", "i", "o", "u"))
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
        else:
            conjugation += PRESENT_ERGATIVE_SUFFIXES[verb.suffix][self.region][
                self.subject
            ]
        if verb.preverb is not None:
            conjugation = verb.preverb + conjugation

        return conjugation
