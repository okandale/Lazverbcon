"""Stable domain types. No HTTP, database, or filesystem dependencies."""

from dataclasses import dataclass
from enum import StrEnum


class Dialect(StrEnum):
    AS = "AS"
    PZ = "PZ"
    FA = "FA"
    HO = "HO"

    @property
    def legacy(self) -> str:
        return "AŞ" if self == Dialect.AS else self.value


class Person(StrEnum):
    FIRST_SINGULAR = "1sg"
    SECOND_SINGULAR = "2sg"
    THIRD_SINGULAR = "3sg"
    FIRST_PLURAL = "1pl"
    SECOND_PLURAL = "2pl"
    THIRD_PLURAL = "3pl"

    def legacy(self, role: str) -> str:
        return f"{role}{self.value[0]}_{'Singular' if self.value.endswith('sg') else 'Plural'}"


class VerbClass(StrEnum):
    DATIVE = "IVD"
    ERGATIVE = "TVE"
    NOMINATIVE = "TVM"


class Tense(StrEnum):
    PRESENT = "present"
    PAST = "past"
    FUTURE = "future"
    PAST_PROGRESSIVE = "past_progressive"
    PRESENT_PERFECT = "present_perfect"


class Mood(StrEnum):
    INDICATIVE = "indicative"
    OPTATIVE = "optative"
    IMPERATIVE = "imperative"
    NEGATIVE_IMPERATIVE = "negative_imperative"


class Derivation(StrEnum):
    NONE = "none"
    POTENTIAL = "potential"
    PASSIVE = "passive"


class Causative(StrEnum):
    NONE = "none"
    SIMPLE = "simple"
    DOUBLE = "double"


@dataclass(frozen=True)
class PrincipalPart:
    form: str
    dialects: tuple[Dialect, ...]


@dataclass(frozen=True)
class Entry:
    id: str
    infinitive: str
    verb_class: VerbClass
    english: str
    turkish: str
    variants: tuple[PrincipalPart, ...]
    source_row: int
    issues: tuple[str, ...] = ()

    @property
    def dialects(self) -> tuple[Dialect, ...]:
        return tuple(d for d in Dialect if any(d in v.dialects for v in self.variants))


@dataclass(frozen=True)
class Features:
    dialect: Dialect
    subject: Person
    object: Person | None = None
    tense: Tense = Tense.PRESENT
    mood: Mood = Mood.INDICATIVE
    derivation: Derivation = Derivation.NONE
    applicative: bool = False
    causative: Causative = Causative.NONE
    optional_preverb: bool = False


@dataclass(frozen=True, order=True)
class Form:
    spelling: str
    frame: str
    subject: Person
    object: Person | None
    subject_pronoun: str
    object_pronoun: str
    rule: str


@dataclass(frozen=True)
class Result:
    status: str  # ok | unsupported; unexpected failures raise EngineFailure
    forms: tuple[Form, ...] = ()
    reason: str | None = None
    message: str | None = None


class EngineFailure(RuntimeError):
    """A rule failed unexpectedly; never treat this as an unavailable form."""
