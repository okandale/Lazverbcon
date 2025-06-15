import re
from enum import Enum, IntFlag, auto
from typing import TypeAlias


class Mood(IntFlag):
    NONE = 0
    APPLICATIVE = 1
    CAUSATIVE = 2
    OPTATIVE = 4
    IMPERATIVE = 8
    NEGATIVE_IMPERATIVE = 16


class Person(Enum):
    FIRST_PERSON_SINGULAR = auto()
    SECOND_PERSON_SINGULAR = auto()
    THIRD_PERSON_SINGULAR = auto()
    FIRST_PERSON_PLURAL = auto()
    SECOND_PERSON_PLURAL = auto()
    THIRD_PERSON_PLURAL = auto()

    def is_singular(self):
        return (
            self.value >= Person.FIRST_PERSON_SINGULAR
            and self.value <= Person.THIRD_PERSON_SINGULAR
        )

    def is_plural(self):
        return (
            self.value >= Person.FIRST_PERSON_PLURAL
            and self.value <= Person.THIRD_PERSON_PLURAL
        )

    def is_first_person(self):
        return self in (
            Person.FIRST_PERSON_SINGULAR,
            Person.FIRST_PERSON_PLURAL,
        )

    def is_second_person(self):
        return self in (
            Person.SECOND_PERSON_SINGULAR,
            Person.SECOND_PERSON_PLURAL,
        )

    def is_third_person(self):
        return self in (
            Person.THIRD_PERSON_SINGULAR,
            Person.THIRD_PERSON_PLURAL,
        )


class Tense(Enum):
    PRESENT = auto()
    PAST = auto()
    FUTURE = auto()
    PRESENT_PREFECT = auto()
    PAST_PROGRESSIVE = auto()


def check_flags(flags):
    if Mood.IMPERATIVE | Mood.NEGATIVE_IMPERATIVE in flags:
        raise Exception(
            "The 'imperative' and 'negative imperative' modes are "
            "exclusive. Please select only one of them, or not at all."
        )


class Region(Enum):
    ARDESEN = auto()
    FINDIKLI_ARHAVI = auto()
    HOPA = auto()
    PAZAR = auto()


PROTHETIC_CONSONANTS_FIRST_PERSON_BY_CLUSTER_AND_REGION = {
    Region.FINDIKLI_ARHAVI: {
        "p": ["t", "k", "ʒ", "ç", "f", "s", "ş", "x", "h", "p"],
        "b": [
            "a",
            "e",
            "i",
            "o",
            "u",
            "d",
            "g",
            "ž",
            "c",
            "v",
            "z",
            "j",
            "ğ",
        ],
        "p̌": ["ç̌", "ǩ", "q", "ǯ", "t̆"],
        "m": ["n"],
    },
    Region.ARDESEN: {
        "v": ["a", "e", "i", "o", "u"],
        "p": ["p", "t", "k", "ʒ", "ç", "f", "s", "ş", "x", "h"],
        "b": ["d", "g", "ž", "c", "v", "z", "j", "ğ"],
        "p̌": ["ç̌", "ǩ", "q", "ǯ", "t̆"],
        "m": ["n"],
    },
    Region.HOPA: {
        "v": ["a", "e", "i", "o", "u"],
        "p": ["p", "t", "k", "ʒ", "ç", "f", "s", "ş", "x", "h"],
        "b": ["d", "g", "ž", "c", "v", "z", "j", "ğ"],
        "p̌": ["ç̌", "ǩ", "q", "ǯ", "t̆"],
        "m": ["n"],
    },
    Region.PAZAR: {
        "v": ["a", "e", "i", "o", "u"],
        "p": ["p", "t", "k", "ʒ", "ç", "f", "s", "ş", "x", "h"],
        "b": ["d", "g", "ž", "c", "v", "z", "j", "ğ"],
        "p̌": ["ç̌", "ǩ", "q", "ǯ", "t̆"],
        "m": ["n"],
    },
}

PROTHETIC_CONSONANTS_SECOND_PERSON_BY_CLUSTER = {
    "g": ["a", "e", "i", "o", "u"],
    "k": ["t", "k", "ʒ", "ç", "f", "s", "ş", "x", "h"],
    "g": ["d", "g", "ž", "c", "v", "z", "j", "ğ"],
    "ǩ": ["ç̌", "ǩ", "q", "ǯ", "t̆"],
}

VERB_PREFIXES = [
    "gelo",
    "ge",
    "e",
    "ce",
    "dolo",
    "do",
    "oxo",
    "me",
    "gol",
    "go",
    "oǩo",
    "gam",
    "mola",
    "ye",
    "mo",
    "ǩoǩo",
]
VERB_PREFIX_REGEX = (
    r"^(" + "|".join(sorted(VERB_PREFIXES, key=len, reverse=True)) + r")"
)

SuffixTable: TypeAlias = dict[Region, dict[Person, str]]


def extract_initial_cluster(verb_form: str) -> str:
    """Extracts the initial consonant cluster from a verb form.

    Some Laz roots begin with special digraphs (e.g., 't̆', 'ǩ') which must be
    treated as a single phonological unit. This function ensures the correct
    extraction of such clusters from the beginning of the verb stem.

    Args:
        verb_form (str): A verb form or root.

    Returns:
        str: The initial consonant or consonant cluster to be used
            in morphological rules.
    """
    if len(verb_form) > 1 and verb_form[:2] in ["t̆", "ç̌", "ǩ", "p̌", "ǯ"]:
        return verb_form[:2]
    elif verb_form.startswith("gyoç̌ǩams"):
        return verb_form[2:]
    return verb_form[0]


def extract_prefix(infinitive_form):
    matches = re.match(VERB_PREFIX_REGEX, infinitive_form)
    if matches is not None:
        return matches.group(1)
    else:
        return None
