from .common import Person, extract_prefix
from .verbs import Verb

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .conjugator import Conjugator


class VerbRule:
    def matches(self, conjugator: "Conjugator", verb: Verb) -> bool:
        raise NotImplementedError(
            "Please call this method from a concrete rule."
        )

    def apply(self, conjugator: "Conjugator", verb: Verb) -> str:
        raise NotImplementedError(
            "Please call this method from a concrete rule."
        )


class RuleWithMarkersAndSuffixes(VerbRule):
    def __init__(self, markers, suffixes):
        self.markers = markers
        self.suffixes = suffixes


class NsEndingRule(RuleWithMarkersAndSuffixes):

    def matches(self, conjugator: "Conjugator", verb: Verb):
        return verb.present_third.endswith("ns")

    def apply(self, conjugator: "Conjugator", verb: Verb):
        stem = (
            verb.present_third[:-1]
            if conjugator.subject.is_plural()
            else verb.present_third
        )
        return (
            self.markers[conjugator.subject]
            + stem
            + self.suffixes[conjugator.subject]
        )


class UStartingRule(RuleWithMarkersAndSuffixes):

    def matches(self, conjugator: "Conjugator", verb: Verb):
        return (
            verb.present_third.startswith("u")
            and not conjugator.subject.is_third_person()
        )

    def apply(self, conjugator: "Conjugator", verb: Verb):
        stem = f"i{verb.present_third[1:]}"
        return (
            self.markers[conjugator.subject]
            + stem
            + self.suffixes[conjugator.subject]
        )


class DoPreverbPresent(RuleWithMarkersAndSuffixes):
    def matches(self, conjugator: "Conjugator", verb: Verb):
        prefix = extract_prefix(verb.infinitive)
        return prefix == "do" and verb.present_third.startswith("di")

    def apply(self, conjugator: "Conjugator", verb: Verb):
        extended_stem = verb.present_third[:-1]
        if conjugator.subject.is_first_person():
            stem = extended_stem[1:]
            conjugation = conjugator.apply_epenthetic_segment(
                stem + self.suffixes[conjugator.region][conjugator.subject]
            )
            conjugation = "do{conjugation}"
        else:
            stem = extended_stem
            conjugation = (
                stem + self.suffixes[conjugator.region][conjugator.subject]
            )
        return conjugation
