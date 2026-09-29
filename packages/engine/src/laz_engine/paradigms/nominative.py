"""Nominative morphology. See docs/rules.md for stage ordering and source provenance."""

from ..rules.endings import endings_for
from ..rules.phonology import (
    adjust_prefix,
    get_first_letter,
    get_first_word,
    is_vowel,
    process_compound_verb,
)
from ..rules.preverbs import find_preverb, get_preverbs_rules
from .state import Morphology, RuleRequest

preverbs_rules = get_preverbs_rules("tvm_tense")


def conjugate(request: RuleRequest, principal_part: str) -> str:
    """Conjugate one lexical variant; rule stages run in the order shown."""
    form = Morphology(request, principal_part)
    _prepare_stem(form)
    _apply_markers(form)
    _apply_preverbs(form)
    _adjust_stem(form)
    _select_ending(form)
    return _finish_form(form)


def get_phonetic_rules(region):
    if region == "FA":
        phonetic_rules_v = {
            "p": ["t", "k", "ʒ", "ç", "f", "s", "ş", "x", "h", "p"],
            "b": ["a", "e", "i", "o", "u", "d", "g", "ž", "c", "v", "z", "j", "ğ"],
            "p̌": ["ç̌", "ǩ", "q", "ǯ", "t̆"],
            "m": ["n"],
        }
    else:
        phonetic_rules_v = {
            "v": ["a", "e", "i", "o", "u"],
            "p": ["p", "t", "k", "ʒ", "ç", "f", "s", "ş", "x", "h"],
            "b": ["d", "g", "ž", "c", "v", "z", "j", "ğ"],
            "p̌": ["ç̌", "ǩ", "q", "ǯ", "t̆"],
            "m": ["n"],
        }
    phonetic_rules_g = {
        "k": ["t", "k", "ʒ", "ç", "f", "s", "ş", "x", "h"],
        "g": ["d", "g", "ž", "c", "v", "z", "j", "ğ"],
        "ǩ": ["ç̌", "ǩ", "q", "ǯ", "t̆"],
    }
    return (phonetic_rules_v, phonetic_rules_g)


def determine_marker(subject, obj, marker_type):
    if marker_type == "applicative":
        if (
            subject
            in ["S1_Singular", "S2_Singular", "S1_Plural", "S2_Plural", "S3_Singular", "S3_Plural"]
            and obj in ["O1_Singular", "O2_Singular", "O1_Plural", "O2_Plural"]
            or (
                obj in ["S1_Singular", "S2_Singular", "S1_Plural", "S2_Plural"]
                and subject
                in [
                    "O1_Singular",
                    "O2_Singular",
                    "O1_Plural",
                    "O2_Plural",
                    "S3_Singular",
                    "S3_Plural",
                ]
            )
        ):
            return "i"
        elif "O3" in obj:
            return "u"
        else:
            return ""
    elif marker_type == "causative":
        return "o"
    return ""


def handle_marker(infinitive, root, marker):
    if infinitive == "doguru":
        root = root[1:]
    elif root.startswith("i") or root.startswith("o"):
        if marker in ["i", "o"]:
            root = marker + root[1:]
        elif marker == "u":
            root = "u" + root[1:]
    else:
        root = marker + root
    return root


def _prepare_stem(form: Morphology) -> None:
    """Prepare stem for nominative."""
    request = form.request
    form.phonetic_rules_v, form.phonetic_rules_g = get_phonetic_rules(request.region)
    form.root = process_compound_verb(form.principal_part)
    form.first_word = get_first_word(form.principal_part)
    form.root = process_compound_verb(form.root)
    form.suffixes = endings_for("nominative", request.tense, request.region)
    form.preverb = ""
    preverb_exceptions = {"gonǯǩu"}
    form.preverb = find_preverb(
        request.main_infinitive, preverbs_rules, excluded=request.infinitive in preverb_exceptions
    )
    form.root = process_compound_verb(form.principal_part)
    if form.root in ("imxors", "ipxors") and request.infinitive == "oç̌ǩomu":
        form.root = "ç̌ǩomums"
    elif form.root in "imxors" and request.infinitive == "oşǩomu":
        form.root = "şǩomums"
    if form.preverb and form.root.startswith(form.preverb) and (request.infinitive != "gonǯǩu"):
        form.root = form.root[len(form.preverb) :]


def _apply_markers(form: Morphology) -> None:
    """Apply markers for nominative."""
    request = form.request
    form.marker = ""
    form.marker_type = ""
    if request.applicative:
        form.marker = determine_marker(request.subject, request.obj, "applicative")
        form.marker_type = "applicative"
    elif request.causative:
        form.marker = determine_marker(request.subject, request.obj, "causative")
        form.marker_type = "causative"
    elif request.infinitive == "oxoǯonu" and (
        request.subject in ["S1_Singular", "S1_Plural"]
        or request.obj in ["O2_Singular", "O2_Plural"]
    ):
        form.marker = "o"
    if request.infinitive == "oxenu" and form.marker in ("u", "i", "o"):
        form.root = "xenums"
    form.root = handle_marker(request.main_infinitive, form.root, form.marker)


def _apply_preverbs(form: Morphology) -> None:
    """Apply preverbs for nominative."""
    request = form.request
    form.first_letter = get_first_letter(form.root)
    if (
        form.preverb.endswith(("a", "e", "i", "o", "u"))
        and form.marker.startswith(("a", "e", "i", "o", "u"))
        and (request.subject not in ("S1_Singular", "S1_Plural"))
        and (request.obj not in ("O1_Singular", "O1_Plural", "O2_Plural", "O2_Singular"))
        and (form.preverb == "e")
    ):
        form.preverb = "ey" if request.region == "PZ" else "y"
    if (
        form.preverb.endswith(("a", "e", "i", "o", "u"))
        and form.marker.startswith(("a", "e", "i", "o", "u"))
        and (request.subject not in ("S1_Singular", "S1_Plural"))
        and (request.obj not in ("O1_Singular", "O1_Plural", "O2_Plural", "O2_Singular"))
        and (request.infinitive not in request.gyo_verbs)
        and (form.preverb != "me")
    ):
        form.preverb = form.preverb[:-1]
    form.prefix = ""
    if form.preverb == "me" or (request.use_optional_preverb and (not form.preverb)):
        _preverb_me(form)
    if request.use_optional_preverb and (not form.preverb):
        form.prefix = "ko" + form.prefix
        if request.subject in ["O3_Singular", "O3_Plural"]:
            form.prefix = "k"
    elif form.preverb == "do":
        _preverb_do(form)
    elif form.preverb == "ge":
        _preverb_ge(form)
    elif form.preverb == "ce":
        _preverb_ce(form)
    elif form.preverb == "oxo":
        _preverb_oxo(form)
    elif form.preverb == "oǩo":
        _preverb_oǩo(form)
    elif form.preverb:
        _general_preverb_agreement(form)
    elif request.obj in ["O2_Singular", "O2_Plural"]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"]:
        if form.root.startswith("n"):
            form.root = form.root[1:]
        form.prefix = "m" + form.prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.adjusted_prefix = adjust_prefix(form.prefix, form.first_letter, form.phonetic_rules_v)
        if form.root.startswith("n"):
            form.root = form.root[1:]
        form.prefix = form.adjusted_prefix


def _adjust_stem(form: Morphology) -> None:
    """Adjust stem for nominative."""
    request = form.request
    if form.principal_part.endswith("y"):
        if request.subject == "S3_Singular":
            form.root = form.root
        else:
            form.root = form.root[:-1] + "ms"
    if form.marker_type == "applicative" and form.root in ("işums", "işups", "idums"):
        form.root = form.root[:-3] + "vap"
    elif form.marker_type == "applicative" and (
        form.root.endswith("ums") or form.root.endswith("ams")
    ):
        form.root = form.root[:-3] + "ap"
    elif form.marker_type == "causative" and form.root == "digurams":
        form.root = form.root
    elif form.marker_type == "causative" and form.root in ("oşums", "oşups", "odums"):
        form.root = form.root[:-3] + "vap"
    elif form.marker_type == "causative" and (
        form.root.endswith("ums") or form.root.endswith("ams")
    ):
        form.root = form.root[:-3] + "ap"
    elif form.marker_type == "causative" and (
        form.root.endswith("umers") or form.root.endswith("amers")
    ):
        form.root = form.root[:-5] + "ap"
    elif form.marker_type == "causative" and form.root.endswith("rs"):
        form.root = form.root[:-1] + "ap"
    elif form.root in ("şums", "şups", "dums"):
        form.root = form.root[:-3] + "v"
    elif form.root.endswith(("ums", "ams", "ups", "aps")):
        form.root = form.root[:-3]
    elif form.root.endswith("y"):
        form.root = form.root[:-2]
    elif form.root.endswith(("umers", "amers")) and form.root == "dumers":
        form.root = form.root[:-5] + "v"
    else:
        form.root = form.root


def _select_ending(form: Morphology) -> None:
    """Select ending for nominative."""
    request = form.request
    if request.tense in ("future", "past", "optative"):
        form.root = form.root[:-2]
        form.suffix = form.suffixes[request.subject]
    else:
        form.root = form.root[:-1]
        form.suffix = form.suffixes[request.subject]


def _finish_form(form: Morphology) -> str:
    """Finish form for nominative."""
    request = form.request
    form.final_root = form.root[:-1] if form.root.endswith("s") else form.root
    if (
        request.infinitive in ("oxtimu", "olva")
        and request.subject in ("S1_Singular", "S1_Plural")
        and (request.tense in ("past", "future", "optative"))
        and (not request.applicative)
        and (not request.causative)
    ):
        form.final_root = "id"
    elif (
        request.infinitive in ("oxtimu", "olva")
        and request.subject in ("S2_Singular", "S2_Plural")
        and (request.tense in ("past", "future", "optative"))
        and (not request.applicative)
        and (not request.causative)
    ):
        form.final_root = "id"
    elif (
        request.infinitive in ("oxtimu", "olva")
        and request.subject in ("S3_Singular", "S3_Plural")
        and (request.tense in ("past", "future", "optative"))
        and (not request.applicative)
        and (not request.causative)
    ):
        form.final_root = "id"
    elif (
        request.infinitive == "ren"
        and request.subject in "S1_Singular"
        and (request.tense == "present")
    ):
        if request.region in ("FA", "HO"):
            form.prefix = "b" if request.region == "FA" else "v"
        form.final_root = "ore"
        form.suffix = ""
    elif (
        request.infinitive == "ren"
        and request.subject in "S2_Singular"
        and (request.tense == "present")
    ):
        form.final_root = "(o)re"
        form.suffix = ""
    elif (
        request.infinitive == "ren"
        and request.subject in "S3_Singular"
        and (request.tense == "present")
    ):
        form.final_root = "on" if request.region in ("PZ", "AŞ") else "(o)ren"
        form.suffix = ""
    elif (
        request.infinitive == "ren"
        and request.subject in "S1_Plural"
        and (request.tense == "present")
    ):
        if request.region in ("FA", "HO"):
            form.prefix = "b" if request.region == "FA" else "v"
        form.final_root = "ore"
        form.suffix = "rtu" if request.region == "AŞ" else "t"
    elif (
        request.infinitive == "ren"
        and request.subject in "S2_Plural"
        and (request.tense == "present")
    ):
        form.final_root = "(o)re"
        form.suffix = "rtu" if request.region == "AŞ" else "t"
    elif (
        request.infinitive == "ren"
        and request.subject in "S3_Plural"
        and (request.tense == "present")
    ):
        form.final_root = (
            "on"
            if request.region in "AŞ"
            else "(o)ren"
            if request.region in ("FA", "HO")
            else "(o)"
        )
        form.suffix = "ran" if request.region == "PZ" else "an"
    if request.infinitive == "ren" and request.tense in ("past", "future"):
        if request.region in ("FA", "HO") and request.subject in ("S1_Singular", "S1_Plural"):
            form.prefix = "b" if request.region == "FA" else "v"
        form.final_root = "ort̆"
    if form.prefix and form.final_root and (form.prefix[-1] == form.final_root[0]):
        form.final_root = form.final_root[1:]
    form.conjugated_verb = f"{form.prefix}{form.final_root}{form.suffix}"
    return f"{form.first_word} {form.conjugated_verb}".strip()


def _preverb_me(form: Morphology) -> None:
    """Apply the me preverb branch."""
    request = form.request
    if form.root.startswith("no"):
        if request.subject in ("S1_Singular", "S1_Plural"):
            form.root = form.root[2:]
        else:
            form.root = form.root[1:]
            form.preverb = ""
    form.first_letter = get_first_letter(form.root)
    if request.obj in ["O2_Singular", "O2_Plural"]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"]:
        form.prefix = "mom"
    else:
        form.prefix = "me"
    if is_vowel(form.prefix[-1]) or (
        is_vowel(form.root[-1]) and request.subject not in ("S1_Singular", "S1_Plural")
    ):
        form.preverb = "n"
    else:
        form.preverb = "me"


def _preverb_do(form: Morphology) -> None:
    """Apply the do preverb branch."""
    request = form.request
    if form.root.startswith("di"):
        form.root = form.root[1:]
        form.prefix = (
            "do" + ("b" if request.region == "FA" else "v")
            if request.subject in ("S1_Singular", "S1_Plural")
            else "d"
        )
    elif request.obj in ["O2_Singular", "O2_Plural"]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = "do" + form.adjusted_prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
        form.prefix = "do" + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"]:
        form.prefix = "dom"
    elif form.marker_type == "causative" or request.main_infinitive == "doguru":
        form.prefix = "d"
    else:
        form.prefix = "do"


def _preverb_ge(form: Morphology) -> None:
    """Apply the ge preverb branch."""
    request = form.request
    if request.infinitive in request.gyo_verbs or form.root.startswith("gya"):
        if request.subject in ["S1_Singular", "S1_Plural"]:
            form.root = form.root[2:]
        else:
            form.root = form.root
            form.preverb = ""
    else:
        form.root = form.root
    form.first_letter = get_first_letter(form.root)
    if request.obj in ["O2_Singular", "O2_Plural"]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"]:
        form.prefix = form.preverb + "m"
    elif form.marker_type == "causative":
        form.prefix = ""
    else:
        form.prefix = (
            form.preverb
            if request.subject in ("S1_Singular", "S1_Plural")
            or request.obj in ("O2_Singular", "O2_Plural")
            else form.preverb[:1]
            if request.infinitive in request.gyo_verbs
            else form.preverb
        )


def _preverb_ce(form: Morphology) -> None:
    """Apply the ce preverb branch."""
    request = form.request
    if request.infinitive in request.co_verbs:
        if (
            request.subject in ["S1_Singular", "S1_Plural"]
            and form.marker
            or (
                request.obj
                in ["O2_Singular", "O3_Singular", "O3_PluralO2_Plural", "O1_Singular", "O1_Plural"]
                and form.marker
            )
        ):
            form.root = (
                form.root
                if request.subject in ("S1_Singular", "S1_Plural") and form.marker == "u"
                else form.root[2:]
            )
        else:
            form.root = form.root[1:]
    elif form.root.startswith("ca"):
        if request.subject in ["S1_Singular", "S1_Plural"]:
            form.root = form.root[1:]
        else:
            form.root = form.root
            form.preverb = ""
    elif form.marker and request.obj in ["O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural"]:
        form.root = form.root
    else:
        form.root = form.root
    form.first_letter = get_first_letter(form.root)
    if request.infinitive in "ceyonu" and (not form.marker):
        form.root = (
            "i" + form.root[2:]
            if request.obj in ("O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural")
            else form.root[1:]
        )
    form.first_letter = get_first_letter(form.root)
    if request.obj in ["O2_Singular", "O2_Plural"]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"]:
        form.prefix = form.preverb + "m"
    elif form.marker_type == "causative":
        form.prefix = ""
    else:
        form.prefix = (
            form.preverb[:1] if form.root.startswith(("a", "e", "i", "o", "u")) else form.preverb
        )


def _preverb_oxo(form: Morphology) -> None:
    """Apply the oxo preverb branch."""
    request = form.request
    if form.marker:
        form.root = form.root
    else:
        form.root = form.root
    form.first_letter = get_first_letter(form.root)
    if request.obj in ["O2_Singular", "O2_Plural"]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = "oxo" + form.adjusted_prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
        form.prefix = "oxo" + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"]:
        if form.marker_type != "causative":
            form.root = "o" + form.root
        form.prefix = "oxom"
    elif form.marker_type == "causative":
        form.prefix = "oxo"
    else:
        form.prefix = "oxo"


def _preverb_oǩo(form: Morphology) -> None:
    """Apply the oǩo preverb branch."""
    request = form.request
    if form.marker:
        form.root = form.root
    else:
        form.root = form.root
    form.first_letter = get_first_letter(form.root)
    if request.obj in ["O2_Singular", "O2_Plural"]:
        if form.marker_type != "causative" and form.marker_type != "applicative":
            form.root = form.marker + form.root
        form.first_letter = get_first_letter(form.root)
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = "oǩo" + form.adjusted_prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        if form.marker_type != "causative" and form.marker_type != "applicative":
            form.root = form.marker + form.root
        form.first_letter = get_first_letter(form.root)
        form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
        form.prefix = "oǩo" + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"]:
        if form.marker_type != "causative":
            form.root = "o" + form.root
        form.prefix = "oǩom"
    elif form.marker_type == "causative":
        form.prefix = "oǩo"
    else:
        form.prefix = "oǩo"


def _general_preverb_agreement(form: Morphology) -> None:
    """Apply agreement after the specific preverb cases."""
    request = form.request
    if form.preverb == "mo" and form.root.startswith("ma"):
        if request.subject in ["S1_Singular", "S1_Plural"]:
            form.root = form.root[1:]
        else:
            form.root = form.root
            form.preverb = ""
    elif form.preverb == "gama":
        if request.subject in ("S1_Singular", "S1_Plural"):
            form.preverb = "gama"
            form.root = form.root[3:]
        else:
            form.preverb = "gam"
            form.root = form.root[3:]
    form.first_letter = get_first_letter(form.root)
    if request.obj in ["O2_Singular", "O2_Plural"]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"]:
        form.prefix = form.preverb + "m"
    elif form.marker_type == "causative":
        form.prefix = ""
    else:
        form.prefix = form.preverb
