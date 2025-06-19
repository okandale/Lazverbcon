from .common import Person, Region
from .errors import ConjugatorError
from .present_conjugator import PresentConjugator

NEGATIVE_IMPERATIVE_PREFIXES = {
    Region.ARDESEN: "mo",
    Region.FINDIKLI_ARHAVI: "mot",
    Region.HOPA: "mo",
    Region.PAZAR: "mot",
}


class NegativeImperativeConjugator(PresentConjugator):

    def __init__(self, subject: Person, region: Region, object: Person = None):
        if not subject.is_second_person():
            raise ConjugatorError(
                "The Negative Imperative mood only works "
                "for the second person."
            )
        super().__init__(subject, region, object)

    def conjugate_default_nominative_verb(self, verb):
        return (
            NEGATIVE_IMPERATIVE_PREFIXES[self.region]
            + " "
            + super().conjugate_default_nominative_verb(verb)
        )
