from .present_perfect_conjugator import PresentPerfectConjugator
from .past_progressive_conjugator import PastProgressiveConjugator
from .common import Mood, Person, Region, Tense
from .errors import ConjugatorError
from .future_conjugator import FutureConjugator
from .imperative_conjugator import ImperativeConjugator
from .past_conjugator import PastConjugator
from .present_conjugator import PresentConjugator


class ConjugatorBuilder:
    def __init__(self):
        self.subject = None
        self.object = None
        self.tense = None
        self.aspect = None
        self.moods = Mood.NONE
        self.region = None

    def build(self):
        if self.moods == Mood.IMPERATIVE:
            return ImperativeConjugator(
                subject=self.subject, region=self.region, object=self.object
            )
        elif self.tense == Tense.PAST:
            return PastConjugator(
                subject=self.subject, region=self.region, object=self.object
            )
        elif self.tense == Tense.FUTURE:
            return FutureConjugator(
                subject=self.subject, region=self.region, object=self.object
            )
        elif self.tense == Tense.PRESENT:
            return PresentConjugator(
                subject=self.subject, region=self.region, object=self.object
            )
        elif self.tense == Tense.PAST_PROGRESSIVE:
            return PastProgressiveConjugator(
                subject=self.subject, region=self.region, object=self.object
            )
        elif self.tense == Tense.PRESENT_PREFECT:
            return PresentPerfectConjugator(
                subject=self.subject, region=self.region, object=self.object
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
            Person.SECOND_PERSON_PLURAL,
            Person.SECOND_PERSON_SINGULAR,
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
