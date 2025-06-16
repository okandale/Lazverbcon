from .common import Person
from .verbs import Verb


class VerbRule:
    def matches(self, verb: Verb, subject: Person) -> bool:
        raise NotImplementedError(
            "Please call this method from a concrete rule."
        )

    def apply(
        self, verb: Verb, subject: Person, suffixes: dict, markers: dict
    ) -> str:
        raise NotImplementedError(
            "Please call this method from a concrete rule."
        )


class NsEndingRule(VerbRule):
    def matches(self, verb: Verb, subject: Person):
        return verb.present_third.endswith("ns")

    def apply(self, verb: Verb, subject: Person, suffixes, markers):
        stem = (
            verb.present_third[:-1]
            if subject.is_plural()
            else verb.present_third
        )
        return markers[subject] + stem + suffixes[subject]


class UStartingRule(VerbRule):
    def matches(self, verb: Verb, subject: Person):
        return (
            verb.present_third.startswith("u")
            and not subject.is_third_person()
        )

    def apply(self, verb: Verb, subject: Person, suffixes, markers):
        stem = f"i{verb.present_third[1:]}"
        return markers[subject] + stem + suffixes[subject]
