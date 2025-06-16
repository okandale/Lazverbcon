from .common import Person, Region
from .errors import ConjugatorError
from .past_conjugator import PastConjugator


class ImperativeConjugator(PastConjugator):

    def __init__(self, subject: Person, region: Region, object: Person = None):
        if not subject.is_second_person():
            raise ConjugatorError(
                "The Imperative mood only works for the second person."
            )
        super().__init__(subject, region, object)
