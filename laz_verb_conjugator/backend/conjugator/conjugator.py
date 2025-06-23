from typing import Callable, List

from .common import (PROTHETIC_CONSONANTS_NO_OBJECT,
                     PROTHETIC_CONSONANTS_SECOND_PERSON_OBJECT, Mood, Person,
                     Region, extract_initial_cluster)
from .errors import ConjugatorError
from .rules.common import VerbRule
from .verbs import Verb

PREVERB_HANDLERS = {}

APPLICATIVE_INCOMPATIBLE_SUBJECT_OBJECT = {
    Person.FIRST_SINGULAR: Person.FIRST_PLURAL,
    Person.SECOND_SINGULAR: Person.SECOND_PLURAL,
    Person.FIRST_PLURAL: Person.FIRST_SINGULAR,
    Person.SECOND_PLURAL: Person.SECOND_SINGULAR,
}

OPTATIVE_INCOMPATIBLE_OBJECT_SUBJECT = {
    Person.FIRST_SINGULAR: [Person.FIRST_SINGULAR, Person.FIRST_PLURAL],
    Person.SECOND_SINGULAR: [Person.SECOND_SINGULAR, Person.SECOND_PLURAL],
    Person.FIRST_PLURAL: [Person.FIRST_SINGULAR, Person.FIRST_PLURAL],
    Person.SECOND_PLURAL: [Person.SECOND_SINGULAR, Person.SECOND_PLURAL],
}


def handle_preverb(preverb):
    def wrapper(func):
        PREVERB_HANDLERS[preverb] = func

    return wrapper


class Conjugator:

    NOMINATIVE_RULES: List[VerbRule] = []
    DATIVE_RULES: List[VerbRule] = []
    ERGATIVE_RULES: List[VerbRule] = []

    def __init__(
        self,
        subject: Person,
        region: Region,
        object: Person = None,
        moods: Mood = Mood.NONE,
    ):
        self.subject: Person = subject
        self.region: Region = region
        self.object: Person = object
        self.moods: Mood = moods

    def update_subject(self, subject):
        if (
            Mood.APPLICATIVE in self.moods
            and subject in APPLICATIVE_INCOMPATIBLE_SUBJECT_OBJECT
            and APPLICATIVE_INCOMPATIBLE_SUBJECT_OBJECT[subject] == self.object
        ):
            raise ConjugatorError("N/A")

        if (
            Mood.OPTATIVE in self.moods
            and self.object is not None
            and subject in OPTATIVE_INCOMPATIBLE_OBJECT_SUBJECT[self.object]
        ):
            raise ConjugatorError("N/A")

        self.subject = subject

    def conjugate(self, verb: Verb):
        return verb.accept_conjugator(self)

    def apply_rule_or_fallback(
        self, verb: Verb, rules: List[VerbRule], fallback: Callable
    ):
        for rule in rules:
            if rule.matches(self, verb):
                return rule.apply(self, verb)
        return fallback(verb)

    def conjugate_nominative_verb(self, verb: Verb) -> str:
        return self.apply_rule_or_fallback(
            verb, self.NOMINATIVE_RULES, self.conjugate_default_nominative_verb
        )

    def conjugate_dative_verb(self, verb: Verb) -> str:
        return self.apply_rule_or_fallback(
            verb, self.DATIVE_RULES, self.conjugate_default_dative_verb
        )

    def conjugate_ergative_verb(self, verb: Verb) -> str:
        return self.apply_rule_or_fallback(
            verb, self.ERGATIVE_RULES, self.conjugate_default_ergative_verb
        )

    def conjugate_default_nominative_verb(self, verb: Verb):
        raise NotImplementedError(
            "Please call this method from a concrete conjugator."
        )

    def conjugate_default_dative_verb(self, verb: Verb):
        raise NotImplementedError(
            "Please call this method from a concrete conjugator."
        )

    def conjugate_default_ergative_verb(self, verb: Verb):
        raise NotImplementedError(
            "Please call this method from a concrete conjugator."
        )

    def apply_epenthetic_segment(self, inflected_stem):
        """
        Apply an epenthetic segment to the inflected stem if required.

        This method inserts a consonantal segment at the beginning of the verb form
        according to phonological and morphological rules specific to the grammatical
        person and dialectal region.

        The inserted segment—commonly referred to as an *epenthetic segment*—serves to
        ease articulation or mark person agreement in certain Laz verb conjugations.
        It is typically inserted in first and second person forms when the stem
        begins with specific consonant clusters or vowels.

        Example:
            'skidu' → 'pskidu' (with 'p' as the epenthetic segment)
            'isinapam' → 'visinapam' (vowel-initial stem, epenthetic 'v')

        Args:
            inflected_stem (str): The already-inflected verb stem, before any epenthetic insertion.

        Returns:
            str: The verb form with the appropriate epenthetic segment, if applicable.
                Returns the original stem if no rule matches.
        """
        if self.object is None:
            epenthetic_segments_by_cluster = PROTHETIC_CONSONANTS_NO_OBJECT[
                self.region
            ]
        elif (
            self.object.is_first_person() and not self.object.is_first_person()
        ):
            return f"m{inflected_stem}"
        elif self.object.is_second_person():
            epenthetic_segments_by_cluster = (
                PROTHETIC_CONSONANTS_SECOND_PERSON_OBJECT[self.region]
            )
        else:
            epenthetic_segments_by_cluster = PROTHETIC_CONSONANTS_NO_OBJECT[
                self.region
            ]

        initial_cluster = extract_initial_cluster(inflected_stem)
        for (
            epenthetic_segment,
            initial_clusters,
        ) in epenthetic_segments_by_cluster.items():
            if initial_cluster in initial_clusters:
                return (
                    f"{epenthetic_segment}{inflected_stem}"
                    if epenthetic_segment != initial_cluster
                    else inflected_stem
                )
