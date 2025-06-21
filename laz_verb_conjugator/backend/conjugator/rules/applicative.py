from typing import TYPE_CHECKING

from ..common import Mood, Person, Region, extract_prefix
from ..verbs import Verb
from .common import VerbRule, VerbRuleWithSuffixes

if TYPE_CHECKING:
    from ..conjugator import Conjugator


class ApplicativePresentFirstPersonObject(VerbRuleWithSuffixes):
    def matches(self, conjugator: "Conjugator", verb: Verb) -> bool:
        return (
            Mood.APPLICATIVE in conjugator.moods
            and conjugator.object.is_first_person()
        )

    def apply(self, conjugator: "Conjugator", verb: Verb) -> str:
        prefix = extract_prefix(verb.infinitive)
        extended_stem = verb.present_third[:-1]
        stem = (
            extended_stem[len(prefix) :]
            if prefix is not None
            else extended_stem
        )
        conjugation = f"{stem}{self.suffixes[self.subject]}"
        if conjugator.subject.is_first_person():
            conjugation = conjugator.apply_epenthetic_segment(conjugation)
        else:
            conjugation = f"m{conjugation}"
        # Put back the prefix if it exists.
        if prefix is not None:
            conjugation = f"{prefix}{conjugation}"
        
        # Special case for Ardeşen and third person.
        if (
            conjugator.region == Region.ARDESEN
            and conjugator.subject == Person.THIRD_SINGULAR
        ):
            # Replace the suffix.
            conjugation = f"{conjugation[:-2]}y"
        return conjugation


class ApplicativePresentSecondPersonObject(VerbRuleWithSuffixes):
    def matches(self, conjugator: "Conjugator", verb: Verb) -> bool:
        return (
            Mood.APPLICATIVE in conjugator.moods
            and conjugator.object.is_second_person()
        )

    def apply(self, conjugator: "Conjugator", verb: Verb) -> str:
        prefix = extract_prefix(verb.infinitive)
        extended_stem = verb.present_third[:-1]
        stem = (
            extended_stem[len(prefix) :]
            if prefix is not None
            else extended_stem
        )
        conjugation = f"{stem}{self.suffixes[conjugator.subject]}"
        if conjugator.subject != Person.SECOND_SINGULAR:
            conjugation = conjugator.apply_epenthetic_segment(conjugation)
        # Put back the prefix if it exists.
        if prefix is not None:
            conjugation = f"{prefix}{conjugation}"
        # Special case for Ardeşen and third person.
        if (
            conjugator.region == Region.ARDESEN
            and conjugator.subject == Person.THIRD_SINGULAR
        ):
            # Replace the suffix.
            conjugation = f"{conjugation[:-2]}y"
        return conjugation
