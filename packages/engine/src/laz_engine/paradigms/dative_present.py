"""Dative present morphology. See docs/rules.md for stage ordering and source provenance."""

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
from .dative_preverbs import _preverb_go as _preverb_go
from .state import Morphology, RuleRequest

preverbs_rules = get_preverbs_rules("ivd_present")


def conjugate(request: RuleRequest, principal_part: str) -> str:
    """Conjugate one lexical variant; rule stages run in the order shown."""
    form = Morphology(request, principal_part)
    _prepare_stem(form)
    _apply_agreement(form)
    _select_ending(form)
    return _finish_form(form)


def _prepare_stem(form: Morphology) -> None:
    """Prepare stem for dative present."""
    request = form.request
    form.phonetic_rules_v, form.phonetic_rules_g = get_phonetic_rules(request.region)
    form.root = process_compound_verb(form.principal_part)
    form.first_word = get_first_word(form.principal_part)
    form.root = process_compound_verb(form.root)
    if request.mood and request.obj:
        raise ValueError("Dative verbs cannot take an object in the optative.")
    form.first_word = request.first_word_infinitive
    form.suffixes = {
        "S1_Singular": "",
        "S2_Singular": "",
        "S3_Singular": "",
        "S1_Plural": "an",
        "S2_Plural": "an",
        "S3_Plural": "an",
    }
    form.preverb = ""
    form.prefix = ""
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
    """Apply agreement for dative present."""
    request = form.request
    form.first_letter = get_first_letter(form.root)
    form.adjusted_prefix = ""
    if form.preverb:
        form.preverb_form = preverbs_rules.get((form.preverb,), {}).get(
            request.subject, form.preverb
        )
    else:
        form.prefix = subject_markers[request.subject]
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
    elif form.preverb == "mo" or request.infinitive.startswith("mo"):
        _preverb_mo(form)
    elif form.preverb:
        _general_preverb_agreement(form)
    if not form.preverb:
        _unprefixed_agreement(form)
    if request.use_optional_preverb and (not form.preverb):
        form.prefix = "ko" + form.prefix
        if request.subject in ["O3_Singular", "O3_Plural"]:
            form.prefix = "k" + form.prefix


def _select_ending(form: Morphology) -> None:
    """Select ending for dative present."""
    request = form.request
    form.suffix = form.suffixes[request.subject]
    if request.mood == "optative":
        if request.infinitive in ("uğun", "oçkinu", "uyonun", "uqoun", "unon"):
            if request.infinitive == "unon":
                form.root = form.root[:-2]
            else:
                form.root = form.root[:-1]
            form.suffix = (
                "t̆az"
                if request.region == "FA"
                and request.subject in ("S1_Singular", "S2_Singular", "S3_Singular")
                else "t̆as"
                if request.subject in ("S1_Singular", "S2_Singular", "S3_Singular")
                else "t̆an"
            )
        else:
            form.root = form.root[:-2]
            form.suffix = (
                "az"
                if request.region in "FA"
                and request.subject in ("S1_Singular", "S2_Singular", "S3_Singular")
                else "as"
                if request.subject in ("S1_Singular", "S2_Singular", "S3_Singular")
                else "an"
            )
    elif request.subject == "S3_Singular" and (request.obj == "O3_Singular" or request.obj is None):
        form.suffix = ""
    elif request.subject == "S3_Singular" and request.obj == "O3_Plural":
        if form.root.endswith(("rs", "ns")):
            form.root = form.root
        form.suffix = ""
    elif request.subject == "S3_Singular" and request.obj in ["O1_Plural", "O2_Plural"]:
        if form.root.endswith(("en", "rs")):
            form.root = form.root[:-2] if request.infinitive.endswith("rs") else form.root[:-1]
        form.suffix = "rt"
        if form.root.endswith("ns"):
            form.root = form.root[:-1]
        form.suffix = "t"
    elif request.subject in [
        "S1_Singular",
        "S2_Singular",
        "S3_Singular",
        "S3_Plural",
    ] and request.obj in ["O1_Singular", "O2_Singular"]:
        if form.root.endswith(("n", "rs")):
            form.root = form.root[:-1]
            form.suffix = "" if request.infinitive.endswith("rs") else "r"
        if form.root.endswith("ns"):
            form.root = form.root[:-1]
            form.suffix = ""
    elif request.subject in [
        "S1_Singular",
        "S1_Plural",
        "S2_Singular",
        "S2_Plural",
        "S3_Plural",
    ] and request.obj in ("O1_Plural", "O2_Plural"):
        if form.root.endswith(("n", "rs")):
            form.root = form.root[:-2] if request.infinitive.endswith("rs") else form.root[:-1]
        form.suffix = "rt"
        if form.root.endswith("ns"):
            form.root = form.root[:-1]
        form.suffix = "t"
    elif request.subject in ["S1_Plural", "S2_Plural"] and request.obj in (
        "O1_Singular",
        "O2_Singular",
    ):
        if form.root.endswith(("n", "rs")):
            form.root = form.root[:-2] if request.infinitive.endswith("rs") else form.root[:-1]
        form.suffix = "rt"
        if form.root.endswith("ns"):
            form.root = form.root[:-1]
        form.suffix = "t"
    elif request.subject in ["S1_Singular", "S2_Singular"] and request.obj in [
        "O3_Singular",
        "O3_Plural",
    ]:
        form.suffix = ""
    elif request.subject in ["S1_Plural", "S2_Plural", "S3_Singular"] and (
        request.obj in ("O3_Singular", "O3_Plural") or request.obj is None
    ):
        if form.root.endswith("rs") or form.root.endswith("ns"):
            form.root = form.root[:-1]
        form.suffix = (
            ""
            if form.root.endswith("an")
            else "s"
            if request.infinitive == "coxons" and request.subject == "S3_Singular"
            else "an"
        )
    elif request.subject == "S3_Plural":
        if form.root.endswith("rs") or form.root.endswith("ns"):
            form.root = form.root[:-1]
        form.suffix = "an"


def _finish_form(form: Morphology) -> str:
    """Finish form for dative present."""
    request = form.request
    if form.preverb in ("go", "gy", "coz", "d"):
        if form.suffix == "r" and form.root.endswith("n"):
            form.final_root = form.root
        elif request.subject in ["S1_Plural", "S2_Plural", "S3_Plural"] and form.root.endswith("s"):
            form.final_root = form.root + "r"
        else:
            form.final_root = form.root
    elif request.subject in ["S1_Plural", "S2_Plural", "S3_Plural"] and form.root.endswith("s"):
        form.final_root = form.root
    else:
        form.final_root = form.root
    form.conjugated_verb = f"{form.prefix}{form.final_root}{form.suffix}"
    return f"{form.first_word} {form.conjugated_verb}".strip()


def _preverb_me(form: Morphology) -> None:
    """Apply the me preverb branch."""
    request = form.request
    if form.root.startswith("na") and request.subject not in ("S3_Singular", "S3_Plural"):
        form.root = form.root[1:]
        form.prefix = (
            form.preverb_form + "m"
            if request.subject in ("S1_Singular", "S1_Plural")
            else form.preverb + "g"
        )
    elif request.subject in ("S3_Singular", "S3_Plural"):
        if request.obj in ("O1_Singular", "O1_Plural"):
            form.adjusted_prefix = "v" if request.region in ("PZ", "AŞ", "HO") else "b"
            form.prefix = form.preverb + form.adjusted_prefix
            form.root = form.root[1:]


def _preverb_mo(form: Morphology) -> None:
    """Apply the mo preverb branch."""
    request = form.request
    if form.root.startswith("m") and request.subject not in ("S3_Singular", "S3_Plural"):
        form.root = form.root[1:]
    if request.subject in ("S3_Singular", "S3_Plural") and request.obj in (
        "O1_Singular",
        "O1_Plural",
    ):
        form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.subject in ("S2_Singular", "S2_Plural"):
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.subject in ("S1_Singular", "S1_Plural") and request.obj in (
        "O3_Singular",
        "O3_Plural",
    ):
        form.adjusted_prefix = "m"
        form.prefix = form.preverb + form.adjusted_prefix
    else:
        form.prefix = (
            form.preverb[2:] + subject_markers[request.subject]
            if form.root.startswith("m")
            else form.preverb + subject_markers[request.subject]
        )


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
    elif request.subject in ("S1_Singular", "S1_Plural") and request.obj in (
        "O3_Singular",
        "O3_Plural",
    ):
        form.adjusted_prefix = "m"
        form.prefix = form.adjusted_prefix
    else:
        form.prefix = subject_markers[request.subject]


def _general_preverb_agreement(form: Morphology) -> None:
    """Apply agreement after the specific preverb cases."""
    request = form.request
    if form.root.startswith(("ca", "adgi")):
        if request.subject in ("S3_Singular", "S3_Plural"):
            form.preverb = "c"
        form.root = form.root if request.infinitive == "cedginu" else form.root[1:]
        if request.subject in ("S1_Singular", "S2_Singular", "S1_Pural", "S2_Plural"):
            form.root = form.root[1:]
    if form.root.startswith(("ma", "mu")):
        form.root = form.root if request.subject in ("S3_Singular", "S3_Plural") else form.root[1:]
        form.preverb = "" if request.subject in ("S3_Singular", "S3_Plural") else form.preverb
    if request.subject in ["S1_Singular", "S1_Plural"]:
        form.prefix = form.preverb + "m"
    elif request.subject in ["S2_Singular", "S2_Plural"]:
        form.prefix = form.preverb + "g"
    elif request.subject in ("S3_Singular", "S3_Plural"):
        if request.obj in ("O1_Singular", "O1_Plural"):
            form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
            form.prefix = form.preverb + form.adjusted_prefix
    else:
        form.prefix = form.preverb
