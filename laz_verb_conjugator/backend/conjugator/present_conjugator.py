from .common import Person, Region, extract_prefix, extract_root
from .conjugator import Conjugator
from .ergative_verbs import ConjugateErgativeVerbMixin
from .nominative_verbs import ConjugateNominativeVerbMixin
from .rules.applicative import (ApplicativePresentFirstPersonObject,
                                ApplicativePresentSecondPersonObject)
from .rules.common import (DoPreverb, NsEndingRule,
                           SubjectObjectNsOrRsEndingRule, UStartingRule)
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
    Person.FIRST_SINGULAR: "",
    Person.SECOND_SINGULAR: "",
    Person.THIRD_SINGULAR: "s",
    Person.FIRST_PLURAL: "t",
    Person.SECOND_PLURAL: "t",
    Person.THIRD_PLURAL: "an",
}

APPLICATIVE_SUFFIXES = {()}


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
        conjugation = ConjugateErgativeVerbMixin.conjugate_ergative_verb(
            self,
            verb,
            suffix_table=PRESENT_ERGATIVE_SUFFIXES,
            ending_len=1,
        )

        # Special case for Ardeşen and third person.
        if (
            self.region == Region.ARDESEN
            and self.subject == Person.THIRD_SINGULAR
        ):
            # Replace the suffix.
            conjugation = f"{conjugation[:-2]}y"
        return conjugation
