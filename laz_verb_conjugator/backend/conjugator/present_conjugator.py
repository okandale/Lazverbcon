from .common import Person, Region, extract_preverb, extract_root
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

PRESENT_ERGATIVE_SUFFIXES = {
    "ams": {
        Region.ARDESEN: {
            Person.FIRST_SINGULAR: "am",
            Person.SECOND_SINGULAR: "am",
            Person.THIRD_SINGULAR: "ay",
            Person.FIRST_PLURAL: "amt",
            Person.SECOND_PLURAL: "amt",
            Person.THIRD_PLURAL: "aman",
        },
        Region.PAZAR: {
            Person.FIRST_SINGULAR: "am",
            Person.SECOND_SINGULAR: "am",
            Person.THIRD_SINGULAR: "ams",
            Person.FIRST_PLURAL: "amt",
            Person.SECOND_PLURAL: "amt",
            Person.THIRD_PLURAL: "aman",
        },
        Region.FINDIKLI_ARHAVI: {
            Person.FIRST_SINGULAR: "am",
            Person.SECOND_SINGULAR: "am",
            Person.THIRD_SINGULAR: "ams",
            Person.FIRST_PLURAL: "amt",
            Person.SECOND_PLURAL: "amt",
            Person.THIRD_PLURAL: "aman",
        },
        Region.HOPA: {
            Person.FIRST_SINGULAR: "am",
            Person.SECOND_SINGULAR: "am",
            Person.THIRD_SINGULAR: "ams",
            Person.FIRST_PLURAL: "amt",
            Person.SECOND_PLURAL: "amt",
            Person.THIRD_PLURAL: "aman",
        },
    },
}

# In these prefixes, the key refers to the *object’s* person.
APPLICATIVE_PREFIXES = {
    Person.FIRST_SINGULAR: {
        
    }
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

    ERGATIVE_RULES = [
        ApplicativePresentFirstPersonObject(
            suffixes=PRESENT_ERGATIVE_SUFFIXES
        ),
        ApplicativePresentSecondPersonObject(
            suffixes=PRESENT_ERGATIVE_SUFFIXES
        ),
        ApplicativePresentThirdPersonObject(
            suffixes=PRESENT_ERGATIVE_SUFFIXES
        ),
    ]

    def conjugate_default_nominative_verb(self, verb: Verb) -> str:
        return (
            ConjugateNominativeVerbMixin.conjugate_nominative_verb_region_wise(
                self,
                verb,
                region_suffix_table=PRESENT_TENSE_SUFFIXES,
                ending_len=1,
            )
        )

    def conjugate_default_dative_verb(self, verb: Verb) -> str:
        return (
            DATIVE_SUBJECT_MARKERS[self.subject]
            + verb.present_third
            + DATIVE_SUFFIXES[self.subject]
        )

    def conjugate_default_ergative_verb(self, verb: Verb) -> str:
        conjugation = f"{verb.prefix}{verb.stem}"
        
        if (
            conjugation.startswith(("a", "e", "i", "o", "u"))
            and self.subject.is_first_person()
        ):
            conjugation = self.apply_epenthetic_segment(conjugation)

        conjugation = (
            conjugation +
            PRESENT_ERGATIVE_SUFFIXES[verb.suffix][self.region][self.subject]
        )
        if verb.preverb is not None:
            conjugation = verb.preverb + conjugation

        return conjugation
