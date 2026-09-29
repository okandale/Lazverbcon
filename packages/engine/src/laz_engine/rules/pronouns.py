"""Display pronouns by rule family and dialect, independent of person IDs."""

DIALECTS = ("AŞ", "PZ", "FA", "HO")


S1_SINGULAR = {
    (
        "ivd_present",
        "ivd_past",
        "ivd_future",
        "ivd_pastpro",
        "tve_present",
        "tve_past",
        "tve_future",
        "tve_pastpro",
        "tvm_tense",
        "tvm_tve_potential",
        "tvm_tve_passive",
        "tvm_tve_presentperf",
    ): ("ma", "ma", "ma", "ma")
}

S2_SINGULAR = {
    (
        "ivd_present",
        "ivd_past",
        "ivd_future",
        "ivd_pastpro",
        "tve_present",
        "tve_past",
        "tve_future",
        "tve_pastpro",
        "tvm_tense",
        "tvm_tve_potential",
        "tvm_tve_passive",
        "tvm_tve_presentperf",
    ): ("si", "si", "si", "si")
}

O1_SINGULAR = {
    (
        "ivd_present",
        "ivd_past",
        "ivd_future",
        "ivd_pastpro",
        "tve_present",
        "tve_past",
        "tve_future",
        "tve_pastpro",
        "tvm_tense",
        "tvm_tve_potential",
        "tvm_tve_passive",
        "tvm_tve_presentperf",
    ): ("ma", "ma", "ma", "ma")
}

O2_SINGULAR = {
    (
        "ivd_present",
        "ivd_past",
        "ivd_future",
        "ivd_pastpro",
        "tve_present",
        "tve_past",
        "tve_future",
        "tve_pastpro",
        "tvm_tense",
        "tvm_tve_potential",
        "tvm_tve_passive",
        "tvm_tve_presentperf",
    ): ("si", "si", "si", "si")
}

S1_PLURAL = {
    (
        "ivd_present",
        "ivd_past",
        "ivd_future",
        "ivd_pastpro",
        "tve_present",
        "tve_past",
        "tve_future",
        "tve_pastpro",
        "tvm_tense",
        "tvm_tve_potential",
        "tvm_tve_passive",
        "tvm_tve_presentperf",
    ): ("şǩu", "şǩu", "çku", "çkin")
}

S2_PLURAL = {
    (
        "ivd_present",
        "ivd_past",
        "ivd_future",
        "ivd_pastpro",
        "tve_present",
        "tve_past",
        "tve_future",
        "tve_pastpro",
        "tvm_tense",
        "tvm_tve_potential",
        "tvm_tve_passive",
        "tvm_tve_presentperf",
    ): ("t̆ǩva", "t̆ǩva", "tkva", "tkvan")
}

O1_PLURAL = {
    (
        "ivd_present",
        "ivd_past",
        "ivd_future",
        "ivd_pastpro",
        "tve_pastpro",
        "tvm_tense",
        "tvm_tve_potential",
        "tvm_tve_passive",
        "tvm_tve_presentperf",
    ): ("çku", "çku", "çku", "çku"),
    ("tve_present", "tve_past", "tve_future"): ("şǩu", "şǩu", "çku", "çkin"),
}

O2_PLURAL = {
    (
        "ivd_present",
        "ivd_past",
        "ivd_future",
        "ivd_pastpro",
        "tve_pastpro",
        "tvm_tense",
        "tvm_tve_potential",
        "tvm_tve_passive",
        "tvm_tve_presentperf",
    ): ("tkva", "tkva", "tkva", "tkva"),
    ("tve_present", "tve_past", "tve_future"): ("t̆ǩva", "t̆ǩva", "tkva", "tkvan"),
}

S3_SINGULAR = {
    ("ivd_present", "ivd_past", "ivd_future"): ("him", "himus", "heyas", "(h)emus"),
    ("ivd_pastpro",): ("him", "himus", "heyas", "hemus"),
    ("tve_present", "tve_past", "tve_future", "tve_pastpro"): ("him", "himuk", "heyak", "(h)emuk"),
    ("tvm_tense", "tvm_tve_passive"): ("him", "him", "heya", "(h)em"),
    ("tvm_tve_potential", "tvm_tve_presentperf"): ("himus", "himus", "heyas", "(h)emus"),
}

O3_SINGULAR = {
    (
        "ivd_present",
        "ivd_past",
        "ivd_future",
        "tvm_tense",
        "tvm_tve_potential",
        "tvm_tve_passive",
        "tvm_tve_presentperf",
    ): ("him", "him", "heya", "(h)em"),
    ("ivd_pastpro",): ("him", "him", "heya", "hem"),
    ("tve_present", "tve_past", "tve_future", "tve_pastpro"): ("him", "himus", "heyas", "(h)emus"),
}

S3_PLURAL = {
    ("ivd_present", "ivd_past", "ivd_future", "ivd_pastpro", "tvm_tve_presentperf"): (
        "hini",
        "hinis",
        "hentepes",
        "entepes",
    ),
    ("tve_present", "tve_past", "tve_future"): ("hini", "hinik", "hentepek", "entepek"),
    ("tve_pastpro",): ("hini", "hinik", "hentepek", "entepe"),
    ("tvm_tense", "tvm_tve_passive"): ("hini", "hini", "hentepe", "entepe"),
    ("tvm_tve_potential",): ("hinis", "hinis", "hentepes", "entepes"),
}

O3_PLURAL = {
    (
        "ivd_present",
        "ivd_past",
        "ivd_future",
        "ivd_pastpro",
        "tvm_tense",
        "tvm_tve_potential",
        "tvm_tve_passive",
        "tvm_tve_presentperf",
    ): ("hini", "hini", "hentepe", "entepe"),
    ("tve_present", "tve_past", "tve_future"): ("hini", "hinis", "hentepes", "entepes"),
    ("tve_pastpro",): ("hentepes", "hentepes", "hentepes", "hentepes"),
}


ROLE_TABLES = {
    "S1_Singular": S1_SINGULAR,
    "S2_Singular": S2_SINGULAR,
    "O1_Singular": O1_SINGULAR,
    "O2_Singular": O2_SINGULAR,
    "S1_Plural": S1_PLURAL,
    "S2_Plural": S2_PLURAL,
    "O1_Plural": O1_PLURAL,
    "O2_Plural": O2_PLURAL,
    "S3_Singular": S3_SINGULAR,
    "O3_Singular": O3_SINGULAR,
    "S3_Plural": S3_PLURAL,
    "O3_Plural": O3_PLURAL,
}


def get_personal_pronouns(region: str, mode: str) -> dict[str, str]:
    """Keep dialect spellings separate from the canonical grammatical codes."""
    column = DIALECTS.index(region)
    return {
        role: next(row[column] for modes, row in groups.items() if mode in modes)
        for role, groups in ROLE_TABLES.items()
    }
