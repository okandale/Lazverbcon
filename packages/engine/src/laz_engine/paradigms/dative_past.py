"""Dative past morphology. See docs/rules.md for stage ordering and source provenance."""

from ..rules.markers import ivd_subject_markers as subject_markers
from ..rules.phonology import (
    adjust_prefix,
    get_first_letter,
    get_first_word,
    get_phonetic_rules,
    handle_special_case_coz,
    handle_special_case_gy,
    handle_special_case_u,
    process_compound_verb,
)
from ..rules.preverbs import find_preverb, get_preverbs_rules
from .dative_preverbs import _preverb_do as _preverb_do
from .dative_preverbs import _preverb_me as _preverb_me
from .state import Morphology, RuleRequest

preverbs_rules = get_preverbs_rules("ivd_past")


def conjugate(request: RuleRequest, principal_part: str) -> str:
    """Conjugate one lexical variant; rule stages run in the order shown."""
    form = Morphology(request, principal_part)
    _prepare_stem(form)
    _apply_agreement(form)
    _select_ending(form)
    return _finish_form(form)


def _prepare_stem(form: Morphology) -> None:
    """Prepare stem for dative past."""
    request = form.request
    form.phonetic_rules_v, form.phonetic_rules_g = get_phonetic_rules(request.region)
    form.root = process_compound_verb(form.principal_part)
    form.first_word = get_first_word(form.principal_part)
    form.root = process_compound_verb(form.root)
    form.first_word = request.first_word_infinitive
    form.suffixes = {
        "S1_Singular": "u",
        "S2_Singular": "u",
        "S3_Singular": "u",
        "S1_Plural": "ey" if request.region == "AŞ" else "es",
        "S2_Plural": "ey" if request.region == "AŞ" else "es",
        "S3_Plural": "ey" if request.region == "AŞ" else "es",
    }
    form.preverb = ""
    preverb_exceptions = {"oǩomandu"}
    form.preverb = find_preverb(
        request.main_infinitive,
        preverbs_rules,
        excluded=request.main_infinitive in preverb_exceptions,
    )
    form.root = process_compound_verb(form.principal_part)
    if form.preverb and form.root.startswith(form.preverb):
        form.root = form.root[len(form.preverb) :]
    form.root = handle_special_case_u(form.root, request.subject, form.preverb)
    if form.preverb == "gy":
        form.root = handle_special_case_gy(form.root, request.subject)
    if form.preverb == "coz":
        form.root = handle_special_case_coz(form.root, request.subject)


def _apply_agreement(form: Morphology) -> None:
    """Apply agreement for dative past."""
    request = form.request
    form.first_letter = get_first_letter(form.root)
    form.adjusted_prefix = ""
    form.preverb_form = form.preverb
    if form.preverb:
        form.preverb_form = preverbs_rules.get((form.preverb,), {}).get(
            request.subject, form.preverb
        )
    else:
        form.prefix = subject_markers[request.subject]
    form.prefix = ""
    if (
        form.preverb.endswith(("a", "e", "i", "o", "u"))
        and form.root.startswith(("a", "e", "i", "o", "u"))
        and (request.subject not in ("S1_Singular", "S1_Plural"))
        and (form.preverb == "e")
    ):
        form.preverb = "ey" if request.region == "PZ" else "y"
    if (
        form.preverb.endswith(("a", "e", "i", "o", "u"))
        and form.root.startswith(("a", "e", "i", "o", "u"))
        and (form.preverb not in "me")
    ):
        form.preverb = form.preverb[:-1]
    if form.preverb == "me" or (request.use_optional_preverb and (not form.preverb)):
        _preverb_me(form)
    elif form.preverb == "do":
        _preverb_do(form)
    elif form.preverb == "go":
        _preverb_go(form)
    elif form.preverb == "gy":
        if request.subject in ["S1_Singular", "S1_Plural"]:
            form.prefix = form.preverb[:1] + "em"
        elif request.subject in ["S2_Singular", "S2_Plural"]:
            form.prefix = form.preverb[:1] + "eg"
        else:
            form.prefix = form.preverb[:1] + "y"
    elif form.preverb == "coz":
        if request.subject in ["S1_Singular", "S1_Plural"]:
            form.prefix = "cem"
        elif request.subject in ["S2_Singular", "S2_Plural"]:
            form.prefix = "ceg"
        else:
            form.prefix = "c"
    if not form.preverb:
        _unprefixed_agreement(form)
    elif form.preverb:
        _general_preverb_agreement(form)
    if request.use_optional_preverb and (not form.preverb):
        form.prefix = "ko" + form.prefix
        if request.subject in ["O3_Singular", "O3_Plural"]:
            form.prefix = "k" + form.prefix


def _select_ending(form: Morphology) -> None:
    """Select ending for dative past."""
    request = form.request
    form.suffix = form.suffixes[request.subject]
    if form.root.endswith("en"):
        form.root = form.root[:-2]
    if form.root.endswith("s"):
        form.root = form.root[:-1] + "d" if request.infinitive.endswith("ndu") else form.root[:-1]
    if request.obj:
        if form.root.endswith("s"):
            form.root = (
                form.root[:-1] + "d" if request.infinitive.endswith("ndu") else form.root[:-1]
            )
        if form.root.endswith("en"):
            form.root = form.root[:-2]
        if request.subject == "S3_Singular" and request.obj == "O3_Singular":
            form.suffix = form.suffixes[request.subject]
        elif request.subject == "S3_Singular" and request.obj in ["O1_Plural", "O2_Plural"]:
            form.suffix = "it"
        elif request.subject in [
            "S1_Singular",
            "S2_Singular",
            "S3_Singular",
            "S3_Plural",
        ] and request.obj in ["O1_Singular", "O2_Singular"]:
            form.suffix = "i"
        elif request.subject in [
            "S1_Singular",
            "S1_Plural",
            "S2_Singular",
            "S2_Plural",
            "S3_Plural",
        ] and request.obj in ("O1_Plural", "O2_Plural"):
            form.suffix = "it"
        elif request.subject in ["S1_Plural", "S2_Plural"] and request.obj in (
            "O1_Singular",
            "O2_Singular",
        ):
            form.suffix = "it"
        elif request.subject in ["S1_Singular", "S2_Singular"] and request.obj in [
            "O3_Singular",
            "O3_Plural",
        ]:
            form.suffix = "u"
        elif request.subject in ["S1_Plural", "S2_Plural", "S3_Plural", "S3_Singular"] and (
            request.obj in ("O3_Singular", "O3_Plural") or request.obj is None
        ):
            form.suffix = "ey" if request.region in "AŞ" else "es"
        else:
            form.suffix = form.suffixes[request.subject]
        form.final_root = form.root


def _finish_form(form: Morphology) -> str:
    """Finish form for dative past."""
    request = form.request
    if form.preverb in ("go", "gy", "coz", "d"):
        if form.suffix == "r" and form.root.endswith("n"):
            form.final_root = form.root[:-1]
        elif request.subject in ["S1_Plural", "S2_Plural", "S3_Plural"] and form.root.endswith("s"):
            form.final_root = form.root[:-1]
        else:
            form.final_root = form.root
    elif request.subject in ["S1_Plural", "S2_Plural", "S3_Plural"] and form.root.endswith("s"):
        form.final_root = form.root[:-1]
    else:
        form.final_root = form.root
    form.conjugated_verb = f"{form.prefix}{form.final_root}{form.suffix}"
    return f"{form.first_word} {form.conjugated_verb}".strip()


def _preverb_go(form: Morphology) -> None:
    """Apply the go preverb branch."""
    request = form.request
    if request.subject in ("S3_Singular", "S3_Plural") and (
        not request.obj or request.obj in ("O2_Singular", "O2_Plural", "O3_Singular", "O3_Plural")
    ):
        form.preverb = ""
    else:
        form.root = form.root[2:] if request.region in ("PZ", "AŞ", "HO") else form.root[1:]
    if request.subject in ("S3_Singular", "S3_Plural"):
        if request.obj in ("O1_Singular", "O1_Plural"):
            form.adjusted_prefix = "v" if request.region in ("PZ", "AŞ", "HO") else "b"
            form.prefix = form.preverb + form.adjusted_prefix
        else:
            form.prefix = "g" if request.region in "FA" else "gv"
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.prefix = form.preverb + "m"
    elif request.subject in ["S2_Singular", "S2_Plural"]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = form.preverb + form.adjusted_prefix
    else:
        form.prefix = form.preverb[:-1]


def _unprefixed_agreement(form: Morphology) -> None:
    """Apply agreement after the specific preverb cases."""
    request = form.request
    if form.root == "diç̌irs":
        form.root = "ç̌irs"
        if request.subject in ("S3_Singular", "S3_Plural"):
            if request.obj in ("O1_Singular", "O1_Plural"):
                form.adjusted_prefix = "dova" if request.region in ("PZ", "AŞ", "HO") else "doba"
            else:
                form.adjusted_prefix = "di"
            form.prefix = form.adjusted_prefix
        elif request.subject in ("S1_Singular", "S1_Plural"):
            form.adjusted_prefix = "doma"
            form.prefix = form.adjusted_prefix
        elif request.subject in ("S2_Singular", "S2_Plural"):
            form.adjusted_prefix = "doga"
            form.prefix = form.adjusted_prefix
        else:
            form.prefix = subject_markers[request.subject]
    elif form.root == "dvaç̌irs":
        form.root = "ç̌irs"
        if request.subject in ("S3_Singular", "S3_Plural"):
            if request.obj in ("O1_Singular", "O1_Plural"):
                form.adjusted_prefix = "dova" if request.region in ("PZ", "AŞ", "HO") else "doba"
            else:
                form.adjusted_prefix = "dva"
            form.prefix = form.adjusted_prefix
        elif request.subject in ("S1_Singular", "S1_Plural"):
            form.adjusted_prefix = "doma"
            form.prefix = form.adjusted_prefix
        elif request.subject in ("S2_Singular", "S2_Plural"):
            form.adjusted_prefix = "doga"
            form.prefix = form.adjusted_prefix
        else:
            form.prefix = subject_markers[request.subject]
    elif request.subject in ("S3_Singular", "S3_Plural") and request.obj in (
        "O1_Singular",
        "O1_Plural",
    ):
        form.adjusted_prefix = "v" if request.region in ("PZ", "AŞ", "HO") else "b"
        if request.infinitive in ("olimbu", "oropumu"):
            form.prefix = "(go)" + form.adjusted_prefix
        else:
            form.prefix = form.adjusted_prefix
    else:
        form.prefix = subject_markers[request.subject]


def _general_preverb_agreement(form: Morphology) -> None:
    """Apply agreement after the specific preverb cases."""
    request = form.request
    if form.root.startswith("ca"):
        if request.subject in ("S3_Singular", "S3_Plural"):
            form.preverb = "c"
        form.root = form.root[1:]
    if form.root.startswith(("ma", "mu")):
        form.root = form.root if request.subject in ("S3_Singular", "S3_Plural") else form.root[1:]
        form.preverb = "" if request.subject in ("S3_Singular", "S3_Plural") else form.preverb
    if request.subject in ["S1_Singular", "S1_Plural"]:
        form.prefix = form.preverb + "m"
    elif request.subject in ["S2_Singular", "S2_Plural"]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.subject in ("S3_Singular", "S3_Plural"):
        if request.obj in ("O1_Singular", "O1_Plural"):
            form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
            form.prefix = form.preverb + form.adjusted_prefix
        else:
            form.prefix = form.preverb
    else:
        form.prefix = form.preverb
