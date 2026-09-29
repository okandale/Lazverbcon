"""Endings in 1sg, 2sg, 3sg, 1pl, 2pl, 3pl order.

Only constructions whose endings depend on tense/dialect/causative belong here.
Root-dependent agreement remains with its paradigm.
"""

SUBJECTS = ("S1_Singular", "S2_Singular", "S3_Singular", "S1_Plural", "S2_Plural", "S3_Plural")

ENDINGS = {
    ("nominative", "present", False): {"default": ("r", "r", "n", "rt", "rt", "nan")},
    ("nominative", "past", False): {
        "default": ("i", "i", "u", "it", "it", "es"),
        "AŞ": ("i", "i", "u", "it", "it", "ey"),
    },
    ("nominative", "future", False): {
        "default": ("are", "are", "asen", "aten", "aten", "anen"),
        "PZ": ("are", "are", "asere", "asere", "atere", "anere"),
        "HO": ("aminon", "aginon", "sunon", "aminonan", "aginonan", "asunonan"),
    },
    ("nominative", "pastpro", False): {
        "default": ("rt̆i", "rt̆i", "rt̆u", "rt̆it", "rt̆it", "t̆es"),
        "AŞ": ("rt̆i", "rt̆i", "rt̆u", "rt̆it", "rt̆it", "rt̆ey"),
    },
    ("nominative", "optative", False): {"default": ("a", "a", "as", "at", "at", "an")},
    ("potential", "present", False): {"default": ("en", "en", "en", "enan", "enan", "enan")},
    ("potential", "past", False): {
        "default": ("u", "u", "u", "es", "es", "es"),
        "AŞ": ("u", "u", "u", "ey", "ey", "ey"),
    },
    ("potential", "future", False): {
        "default": ("asen", "asen", "asen", "anen", "anen", "anen"),
        "PZ": ("asere", "asere", "asere", "anere", "anere", "anere"),
        "HO": ("asinon", "asinon", "asinon", "asinonan", "asinonan", "asinonan"),
    },
    ("potential", "pastpro", False): {
        "default": ("ert̆u", "ert̆u", "ert̆u", "ert̆es", "ert̆es", "ert̆es")
    },
    ("potential", "optative", False): {"default": ("as", "as", "as", "an", "an", "an")},
    ("passive", "present", False): {"default": ("er", "er", "en", "ert", "ert", "enan")},
    ("passive", "present", True): {
        "default": ("apiner", "apiner", "apinen", "apinert", "apinert", "apinenan")
    },
    ("passive", "past", False): {
        "default": ("i", "i", "u", "it", "it", "es"),
        "AŞ": ("i", "i", "u", "it", "it", "ey"),
    },
    ("passive", "past", True): {
        "default": ("apineri", "apineri", "apinenu", "apinerit", "apinerit", "apinenanu")
    },
    ("passive", "future", False): {
        "default": ("are", "are", "asen", "aten", "aten", "anenan"),
        "PZ": ("are", "are", "asere", "atere", "atere", "aneran"),
        "HO": ("aminon", "aginon", "asinon", "aminonan", "aginonan", "asinonan"),
    },
    ("passive", "future", True): {
        "default": ("apare", "apare", "apasen", "apaten", "apaten", "apaten"),
        "PZ": ("apare", "apare", "apasere", "apaten", "apaten", "apaten"),
        "HO": ("apaminon", "apaginon", "apasinon", "apaminonan", "apaginonan", "apasinonan"),
    },
    ("passive", "pastpro", False): {"default": ("ert̆i", "ert̆i", "ert̆u", "ert̆it", "ert̆it", "ert̆es")},
    ("passive", "pastpro", True): {
        "default": ("apinert̆i", "apinert̆i", "apinert̆u", "apinert̆it", "apinert̆it", "apinent̆es")
    },
    ("perfect", "present_perfect", False): {
        "default": ("un", "un", "un", "unan", "unan", "unan"),
        "AŞ": ("apun", "apun", "apun", "apunan", "apunan", "apunan"),
        "PZ": ("apun", "apun", "apun", "apuran", "apuran", "apuran"),
        "HO": ("apun", "apun", "apun", "apunan", "apunan", "apunan"),
    },
}


def endings_for(
    construction: str, tense: str, region: str, causative: bool = False
) -> dict[str, str]:
    tense = "pastpro" if tense == "past progressive" else tense
    variants = ENDINGS[construction, tense, causative]
    return dict(zip(SUBJECTS, variants.get(region, variants["default"]), strict=True))
