import re
from enum import Enum, IntFlag, auto
from typing import TypeAlias


class VerbType(Enum):
    NOMINATIVE = auto()
    DATIVE = auto()
    ERGATIVE = auto()


class Mood(IntFlag):
    NONE = 0
    APPLICATIVE = 1
    CAUSATIVE = 2
    OPTATIVE = 4
    IMPERATIVE = 8
    NEGATIVE_IMPERATIVE = 16


class Aspect(Enum):
    NONE = auto()
    POTENTIAL = auto()
    PASSIVE = auto()


class Person(Enum):
    FIRST_SINGULAR = auto()
    SECOND_SINGULAR = auto()
    THIRD_SINGULAR = auto()
    FIRST_PLURAL = auto()
    SECOND_PLURAL = auto()
    THIRD_PLURAL = auto()

    def is_singular(self):
        return self in (
            Person.FIRST_SINGULAR,
            Person.SECOND_SINGULAR,
            Person.THIRD_SINGULAR,
        )

    def is_plural(self):
        return self in (
            Person.FIRST_PLURAL,
            Person.SECOND_PLURAL,
            Person.THIRD_PLURAL,
        )

    def is_first_person(self):
        return self in (
            Person.FIRST_SINGULAR,
            Person.FIRST_PLURAL,
        )

    def is_second_person(self):
        return self in (
            Person.SECOND_SINGULAR,
            Person.SECOND_PLURAL,
        )

    def is_third_person(self):
        return self in (
            Person.THIRD_SINGULAR,
            Person.THIRD_PLURAL,
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


PROTHETIC_CONSONANTS_NO_OBJECT = {
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

PROTHETIC_CONSONANTS_SECOND_PERSON_OBJECT = {
    Region.FINDIKLI_ARHAVI: {
        "k": ["t", "k", "ʒ", "ç", "f", "s", "ş", "x", "h", "p"],
        "g": [
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
        "ǩ": ["ç̌", "ǩ", "q", "ǯ", "t̆"],
        "m": ["n"],
    },
    Region.ARDESEN: {
        "g": ["a", "e", "i", "o", "u"],
        "k": ["p", "t", "k", "ʒ", "ç", "f", "s", "ş", "x", "h"],
        "ǩ": ["ç̌", "ǩ", "q", "ǯ", "t̆"],
        "m": ["n"],
    },
    Region.HOPA: {
        "g": ["a", "e", "i", "o", "u"],
        "k": ["p", "t", "k", "ʒ", "ç", "f", "s", "ş", "x", "h"],
        "g": ["d", "g", "ž", "c", "v", "z", "j", "ğ"],
        "ǩ": ["ç̌", "ǩ", "q", "ǯ", "t̆"],
        "m": ["n"],
    },
    Region.PAZAR: {
        "g": ["a", "e", "i", "o", "u"],
        "k": ["p", "t", "k", "ʒ", "ç", "f", "s", "ş", "x", "h"],
        "g": ["d", "g", "ž", "c", "v", "z", "j", "ğ"],
        "ǩ": ["ç̌", "ǩ", "q", "ǯ", "t̆"],
        "m": ["n"],
    },
}

PROTHETIC_CONSONANTS_SECOND_PERSON = {
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

POTENTIAL_SUBJECT_MARKERS = {
    Person.FIRST_SINGULAR: "ma",
    Person.SECOND_SINGULAR: "ga",
    Person.THIRD_SINGULAR: "a",
    Person.FIRST_PLURAL: "ma",
    Person.SECOND_PLURAL: "ga",
    Person.THIRD_PLURAL: "a",
}

DATIVE_SUFFIXES = {
    Person.FIRST_SINGULAR: "",
    Person.SECOND_SINGULAR: "",
    Person.THIRD_SINGULAR: "",
    Person.FIRST_PLURAL: "an",
    Person.SECOND_PLURAL: "an",
    Person.THIRD_PLURAL: "an",
}

DATIVE_SUBJECT_MARKERS = {
    Person.FIRST_SINGULAR: "m",
    Person.SECOND_SINGULAR: "g",
    Person.THIRD_SINGULAR: "",
    Person.FIRST_PLURAL: "m",
    Person.SECOND_PLURAL: "g",
    Person.THIRD_PLURAL: "",
}


RegionSuffixTable: TypeAlias = dict[Region, dict[Person, str]]
SuffixTable: TypeAlias = dict[Person, str]
PotentialSuffixTable: TypeAlias = dict[Tense, dict[Region, dict[Person, str]]]
PassiveSuffixTable: TypeAlias = PotentialSuffixTable


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


def extract_preverb(infinitive_form: str) -> str | None:
    matches = re.match(VERB_PREFIX_REGEX, infinitive_form)
    if matches is not None:
        return matches.group(1)
    else:
        return None


def extract_root(word, start, end):
    """Extract the root of *word*.

    Remove *start* letters at the beginning and *end* letters at the end.

    Examples:
        - radicalize("oskidu", 1, 1) -> "skid".

    Returns:
        - str: the stem

    """
    return word[start:-end]
