"""Explicit inputs and local morphology used by the ordered rule stages.

Each principal part gets a fresh state. Stages mutate only that local state;
lexical entries and requests remain immutable. Intermediate fields deliberately
have no defaults: reading one before its preparation stage is an error.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class RuleRequest:
    infinitive: str
    main_infinitive: str
    first_word_infinitive: str
    region: str
    subject: str
    obj: str | None
    tense: str
    mood: str | None
    applicative: bool
    causative: bool
    simple_causative: bool
    use_optional_preverb: bool
    co_verbs: tuple[str, ...]
    gyo_verbs: tuple[str, ...]
    no_verbs: tuple[str, ...]


@dataclass(slots=True)
class Morphology:
    request: RuleRequest
    principal_part: str
    root: str = field(init=False)
    original_root: str = field(init=False)
    first_word: str = field(init=False)
    suffixes: dict[str, str] = field(init=False)
    preverb: str = field(init=False)
    prefix: str = field(init=False)
    preverb_form: str = field(init=False)
    marker: str = field(init=False)
    marker_type: str = field(init=False)
    first_letter: str = field(init=False)
    adjusted_prefix: str = field(init=False)
    handled_gontzku: bool = field(init=False)
    suffix: str = field(init=False)
    final_root: str = field(init=False)
    conjugated_verb: str = field(init=False)
    phonetic_rules_v: dict[str, list[str]] = field(init=False)
    phonetic_rules_g: dict[str, list[str]] = field(init=False)
