from .common import Aspect, Mood, Person, Region, Tense
from .conjugator import Conjugator
from .errors import ConjugatorError
from .future_conjugator import FutureConjugator
from .imperative_conjugator import ImperativeConjugator
from .negative_imperative_conjugator import NegativeImperativeConjugator
from .optative_conjugator import OptativeConjugator
from .passive_conjugator import PassiveConjugator
from .past_conjugator import PastConjugator
from .past_progressive_conjugator import PastProgressiveConjugator
from .potential_conjugator import PotentialConjugator
from .present_conjugator import PresentConjugator
from .present_perfect_conjugator import PresentPerfectConjugator

INCOMPATIBLE_APPLICATIVES = {
    Person.FIRST_SINGULAR: Person.FIRST_PLURAL,
    Person.SECOND_SINGULAR: Person.SECOND_PLURAL,
    Person.FIRST_PLURAL: Person.FIRST_SINGULAR,
    Person.SECOND_PLURAL: Person.SECOND_SINGULAR,
}


class ConjugatorBuilder:

    ASPECT_CONJUGATORS = {
        Aspect.POTENTIAL: PotentialConjugator,
        Aspect.PASSIVE: PassiveConjugator,
    }

    MOOD_CONJUGATORS = {
        Mood.IMPERATIVE: ImperativeConjugator,
        Mood.NEGATIVE_IMPERATIVE: NegativeImperativeConjugator,
        Mood.OPTATIVE: OptativeConjugator,
    }

    TENSE_CONJUGATORS = {
        Tense.PRESENT: PresentConjugator,
        Tense.PAST: PastConjugator,
        Tense.FUTURE: FutureConjugator,
        Tense.PAST_PROGRESSIVE: PastProgressiveConjugator,
        Tense.PRESENT_PREFECT: PresentPerfectConjugator,
    }

    def __init__(self):
        self.subject = None
        self.object = None
        self.tense = None
        self.aspect = None
        self.moods = Mood.NONE
        self.region = None

    def are_applicatives_incompatible(self):
        return (
            INCOMPATIBLE_APPLICATIVES[self.subject] == self.object
            if self.subject in INCOMPATIBLE_APPLICATIVES
            else False
        )

    def build(self) -> Conjugator:

        if (
            Mood.APPLICATIVE in self.moods
            and self.are_applicatives_incompatible()
        ):
            raise ConjugatorError(
                f"{self.subject} and {self.object} "
                "are not compatible in applicative mode."
            )

        if Mood.APPLICATIVE in self.moods and self.object is None:
            raise ConjugatorError(f"Applicative mood requires an object.")

        elif (
            self.subject == self.object and Mood.APPLICATIVE not in self.moods
        ):
            raise ConjugatorError(
                "You cannot have the same person for "
                "the subject and the object."
            )

        if self.aspect in self.ASPECT_CONJUGATORS:
            return self.ASPECT_CONJUGATORS[self.aspect](
                subject=self.subject,
                region=self.region,
                object=self.object,
                tense=self.tense,
                moods=self.moods,
            )
        elif self.moods in self.MOOD_CONJUGATORS:
            return self.MOOD_CONJUGATORS[self.moods](
                subject=self.subject,
                region=self.region,
                object=self.object,
            )
        elif self.tense in self.TENSE_CONJUGATORS:
            return self.TENSE_CONJUGATORS[self.tense](
                subject=self.subject,
                region=self.region,
                object=self.object,
                moods=self.moods,
            )
        raise ConjugatorError("Could not build the conjugator.")

    def set_region(self, region: Region):
        if self.region is not None:
            raise ConjugatorError("The region is already defined.")
        self.region = region
        return self

    def set_subject(self, subject: Person) -> "ConjugatorBuilder":
        if self.subject is not None:
            raise ConjugatorError("The subject is already defined.")
        self.subject = subject
        return self

    def set_object(self, object):
        if self.object is not None:
            raise ConjugatorError("The object is already defined.")
        self.object = object
        return self

    def set_tense(self, tense):
        if self.tense is not None:
            raise ConjugatorError("The tense is already defined")

        if self.moods & (
            Mood.OPTATIVE | Mood.IMPERATIVE | Mood.NEGATIVE_IMPERATIVE
        ):
            raise ConjugatorError(
                "You cannot set a tense while the optative/imperative/negative imperative mood is set."
            )

        self.tense = tense
        return self

    def add_mood(self, mood):
        if mood in self.moods:
            raise ConjugatorError("This mood has already been set.")

        # Guard check: if we add the (negative )imperative,
        # no tense must be set.
        if (
            mood in (Mood.IMPERATIVE, Mood.NEGATIVE_IMPERATIVE)
            and self.tense is not None
        ):
            raise ConjugatorError(
                "You cannot set the imperative mood with a tense."
            )

        if (
            mood == Mood.IMPERATIVE
            and Mood.NEGATIVE_IMPERATIVE in self.moods
            or mood == Mood.NEGATIVE_IMPERATIVE
            and Mood.IMPERATIVE in self.moods
        ):
            raise ConjugatorError(
                "The imperative and negative imperative moods "
                "are mutually exclusive"
            )

        if mood in (
            Mood.IMPERATIVE,
            Mood.NEGATIVE_IMPERATIVE,
        ) and self.subject not in (
            Person.SECOND_PLURAL,
            Person.SECOND_SINGULAR,
        ):
            raise ConjugatorError(
                "You must set either 2nd person of singular/plural to use the (negative) imperative mood."
            )

        if mood == Mood.CAUSATIVE and self.object is None:
            raise ConjugatorError(
                "An object must be set for the causative mood. "
                "Please call set_object() before adding this mood."
            )

        self.moods |= mood

        return self

    def set_aspect(self, aspect):
        if self.aspect is not None:
            raise ConjugatorError("The aspect has already been set.")

        if self.moods & (Mood.OPTATIVE | Mood.APPLICATIVE):
            raise ConjugatorError(
                "You cannot set an aspect while the optative/applicative mood is set."
            )

        self.aspect = aspect
        return self
