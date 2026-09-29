"""Ergative progressive morphology. See docs/rules.md for stage ordering and source provenance."""

from ..rules.markers import determine_marker, handle_marker
from ..rules.markers import tve_subject_markers as subject_markers
from ..rules.phonology import (
    adjust_prefix,
    get_first_letter,
    get_first_word,
    get_phonetic_rules,
    process_compound_verb,
)
from ..rules.preverbs import find_preverb, get_preverbs_rules
from .ergative_preverbs import _preverb_ce as _preverb_ce
from .ergative_preverbs import _preverb_cel as _preverb_cel
from .ergative_preverbs import _preverb_ela_el as _preverb_ela_el
from .ergative_preverbs import _preverb_ge as _preverb_ge
from .ergative_preverbs import _preverb_gelo_gel as _preverb_gelo_gel
from .ergative_preverbs import _preverb_gol as _preverb_gol
from .ergative_preverbs import _preverb_me as _preverb_me
from .ergative_preverbs import _preverb_mo as _preverb_mo
from .ergative_preverbs import _preverb_oxo as _preverb_oxo
from .ergative_preverbs import _preverb_oǩo as _preverb_oǩo
from .state import Morphology, RuleRequest

preverbs_rules = get_preverbs_rules("tve_pastpro")


def conjugate(request: RuleRequest, principal_part: str) -> str:
    """Conjugate one lexical variant; rule stages run in the order shown."""
    form = Morphology(request, principal_part)
    _prepare_stem(form)
    _apply_markers(form)
    _apply_preverbs(form)
    _adjust_stem(form)
    _select_ending(form)
    return _finish_form(form)


def _prepare_stem(form: Morphology) -> None:
    """Prepare stem for ergative progressive."""
    request = form.request
    form.phonetic_rules_v, form.phonetic_rules_g = get_phonetic_rules(request.region)
    form.original_root = process_compound_verb(form.principal_part)
    form.root = process_compound_verb(form.principal_part)
    form.first_word = get_first_word(form.principal_part)
    form.root = process_compound_verb(form.root)
    form.suffixes = {
        "S1_Singular": "t̆i",
        "S2_Singular": "t̆i",
        "S3_Singular": "t̆u",
        "S1_Plural": "t̆it",
        "S2_Plural": "t̆it",
        "S3_Plural": "t̆ey" if request.region == "AŞ" else "t̆es",
    }
    form.preverb = ""
    preverb_exceptions = {"oǩoreʒxu", "oǩoru", "oxop̌u"}
    form.preverb = find_preverb(
        request.main_infinitive, preverbs_rules, excluded=request.infinitive in preverb_exceptions
    )
    form.root = process_compound_verb(form.principal_part)
    if form.preverb and form.root.startswith(form.preverb) and (request.infinitive != "gonǯǩu"):
        form.root = form.root[len(form.preverb) :]


def _apply_markers(form: Morphology) -> None:
    """Apply markers for ergative progressive."""
    request = form.request
    form.marker = ""
    form.marker_type = ""
    if request.applicative:
        form.marker = determine_marker(request.subject, request.obj, "applicative")
        form.marker_type = "applicative"
    elif request.causative or request.simple_causative:
        form.marker = determine_marker(request.subject, request.obj, "causative")
        form.marker_type = "causative"
    if request.infinitive in "oxenu" and form.marker in ("u", "i", "o"):
        form.root = "xenums"
    if request.infinitive in "oxvenu" and form.marker in ("u", "i", "o"):
        form.root = "xenums"
    form.root = handle_marker(
        request.main_infinitive, form.root, form.marker, request.subject, request.obj
    )
    form.first_letter = get_first_letter(form.root)
    form.adjusted_prefix = ""
    form.handled_gontzku = False


def _apply_preverbs(form: Morphology) -> None:
    """Apply preverbs for ergative progressive."""
    request = form.request
    if (
        request.infinitive == "gonǯǩu"
        and (request.obj in ("O3_Singular", "O3_Plural") or request.obj is None)
        and (not form.marker)
    ):
        form.preverb = ""
        if request.subject in ("S1_Singular", "S1_Plural"):
            form.prefix = "bgo"
        else:
            form.prefix = "go"
        form.handled_gontzku = True
    if not form.handled_gontzku:
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
            form.preverb = form.preverb[:-1] + "y" if form.preverb == "ge" else form.preverb[:-1]
        if form.preverb == "mo" or request.infinitive.startswith("mo"):
            _preverb_mo(form)
        if form.preverb == "me" or (request.use_optional_preverb and (not form.preverb)):
            _preverb_me(form)
        if request.use_optional_preverb and (not form.preverb):
            form.prefix = "ko" + form.prefix
            if request.subject in ["O3_Singular", "O3_Plural"]:
                form.prefix = "k"
        elif form.preverb == "gol":
            _preverb_gol(form)
        elif form.preverb in ("gelo", "gel"):
            _preverb_gelo_gel(form)
        elif form.preverb == "do" or request.infinitive.startswith("do"):
            _preverb_do(form)
        elif (
            form.preverb == "ge"
            or request.infinitive.startswith("ge")
            or form.root.startswith(("igyu", "ugyu", "ogyu"))
        ):
            _preverb_ge(form)
        elif form.preverb in ("ela", "el"):
            _preverb_ela_el(form)
        elif form.preverb == "cel":
            _preverb_cel(form)
        elif form.preverb == "ce" or request.infinitive.startswith("ce"):
            _preverb_ce(form)
        elif form.preverb == "oxo":
            _preverb_oxo(form)
        elif form.preverb == "oǩo":
            _preverb_oǩo(form)
        elif form.preverb or request.infinitive.startswith("gama"):
            form.preverb_form = preverbs_rules.get(form.preverb, form.preverb)
            if isinstance(form.preverb_form, dict):
                form.preverb_form = form.preverb_form.get(request.subject, form.preverb)
            elif form.preverb in "gama" or (
                request.infinitive.startswith(("gama", "igama"))
                and (not form.root.startswith("gama"))
                and (
                    request.subject in ["S1_Singular", "S1_Plural"]
                    or request.obj in ["O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural"]
                )
            ):
                form.root = form.root[1:] if form.original_root.startswith("gamaça") else form.root
                if form.marker:
                    form.root = form.marker + form.root[1:]
                form.preverb = "gama"
                form.preverb_form = "gama"
            if request.obj in ["O2_Singular", "O2_Plural"] and request.subject not in [
                "S2_Singular",
                "S2_Plural",
            ]:
                if form.root.startswith("n"):
                    form.root = form.root[1:]
                    form.first_letter = get_first_letter(form.root)
                    form.adjusted_prefix = adjust_prefix(
                        "g", form.first_letter, form.phonetic_rules_g
                    )
                    form.prefix = form.preverb + "n" + form.adjusted_prefix
                else:
                    form.first_letter = get_first_letter(form.root)
                    form.adjusted_prefix = adjust_prefix(
                        "g", form.first_letter, form.phonetic_rules_g
                    )
                    form.prefix = form.preverb + form.adjusted_prefix
            elif request.obj in ["O1_Singular", "O1_Plural"] and request.subject not in [
                "S1_Singular",
                "S1_Plural",
            ]:
                if form.root.startswith("n"):
                    form.root = form.root[1:]
                form.prefix = form.preverb + "m"
            elif request.subject in ["S1_Singular", "S1_Plural"]:
                form.first_letter = get_first_letter(form.root)
                form.adjusted_prefix = adjust_prefix(
                    form.preverb_form, form.first_letter, form.phonetic_rules_v
                )
                if form.root.startswith("n"):
                    form.root = form.root[1:]
                form.prefix = form.preverb + form.adjusted_prefix
            else:
                form.prefix = form.preverb_form
        else:
            form.prefix = subject_markers[request.subject]
            if form.root == "oroms":
                if request.obj in ("O2_Singular", "O2_Plural") and request.subject not in [
                    "S2_Singular",
                    "S2_Plural",
                ]:
                    form.prefix = "ǩ"
                elif request.subject in ("S1_Singular", "S1_Plural") and request.obj in (
                    "O3_Singular",
                    "O3_Plural",
                ):
                    form.prefix = "p̌"
                elif request.subject in ("S1_Singular", "S1_Plural"):
                    form.prefix = "p̌"
                elif request.obj in ("O1_Singular", "O1_Plural") and request.subject not in [
                    "S1_Singular",
                    "S1_Plural",
                ]:
                    form.prefix = "p̌"
                else:
                    form.prefix = subject_markers[request.subject]
            if request.obj in ["O2_Singular", "O2_Plural"] and request.subject not in [
                "S2_Singular",
                "S2_Plural",
            ]:
                form.prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
            elif request.obj in ["O1_Singular", "O1_Plural"] and request.subject not in [
                "S1_Singular",
                "S1_Plural",
            ]:
                if form.root.startswith("n"):
                    form.root = form.root[1:]
                form.prefix = "m" + form.prefix
            elif request.subject in ["S1_Singular", "S1_Plural"]:
                form.adjusted_prefix = adjust_prefix(
                    form.prefix, form.first_letter, form.phonetic_rules_v
                )
                if form.root.startswith("n"):
                    form.root = form.root[1:]
                form.prefix = form.adjusted_prefix


def _adjust_stem(form: Morphology) -> None:
    """Adjust stem for ergative progressive."""
    request = form.request
    if form.principal_part.endswith("y"):
        form.root = form.root[:-1] + "ms"
    if request.applicative and request.causative:
        if request.infinitive in ("oşu", "dodvu", "otku"):
            form.root = form.root[:-3] + ("vapap" if request.region == "HO" else "vapam")
        elif form.root.endswith(("umers", "omers")) or form.root.endswith("amers"):
            form.root = form.root[:-5] + "apam"
        elif form.root.endswith(("ms", "ps")):
            form.root = form.root[:-3] + ("apap" if request.region == "HO" else "apam")
        elif form.root.endswith("ams"):
            form.root = form.root[:-3] + "apam"
        elif form.root.endswith("rs"):
            form.root = form.root[:-1] + "apam"
        elif form.root.endswith(("um", "om", "op")) or form.root.endswith("am"):
            form.root = form.root[:-2] + ("apap" if request.region == "HO" else "apam")
        elif form.root.endswith("y"):
            form.root = form.root[:-2] + "apam"
    elif request.applicative or request.simple_causative:
        if request.infinitive in ("oşu", "dodvu", "otku"):
            form.root = form.root[:-3] + ("vaps" if request.region == "HO" else "vams")
        elif form.root.endswith(("ms", "ups")):
            form.root = form.root[:-3] + ("aps" if request.region == "HO" else "ams")
        elif form.root.endswith("um"):
            form.root = form.root[:-2] + "ams"
        elif form.root.endswith("y"):
            form.root = form.root[:-2] + "ams"
        elif form.root.endswith("rs"):
            form.root = form.root[:-1] + ("aps" if request.region == "HO" else "ams")
    elif request.causative:
        if form.root == "çams":
            form.root = form.root
        elif request.infinitive in ("oşu", "dodvu", "otku"):
            form.root = form.root[:-3] + ("vapap" if request.region == "HO" else "vapam")
        elif form.root.endswith("umers") or form.root.endswith("amers"):
            form.root = form.root[:-5] + "apam"
        elif form.root.endswith(("ms", "ps")):
            form.root = form.root[:-3] + ("apap" if request.region == "HO" else "apam")
        elif form.root.endswith("ams"):
            form.root = form.root[:-3] + "apam"
        elif form.root.endswith("rs"):
            form.root = form.root[:-1] + ("apap" if request.region == "HO" else "apam")
        elif form.root.endswith("um") or form.root.endswith("am"):
            form.root = form.root[:-2] + "apam"
        elif form.root.endswith("y"):
            form.root = form.root[:-2] + "apam"


def _select_ending(form: Morphology) -> None:
    """Select ending for ergative progressive."""
    request = form.request
    if request.subject == "S3_Singular" and request.obj in [
        "O1_Singular",
        "O3_Singular",
        "O2_Singular",
        "O3_Plural",
    ]:
        form.suffix = "t̆u"
    elif request.subject in ("S1_Singular", "S2_Singular") and request.obj in (
        "S1_Singular",
        "S2_Singular",
        "S3_Singular",
        "S3_Plural",
    ):
        form.suffix = "t̆i"
    elif request.subject == "S3_Singular" and request.obj in ["O1_Plural", "O2_Plural"]:
        form.suffix = "t̆es"
    elif request.subject in ["S1_Plural", "S2_Plural"]:
        form.suffix = "t̆it"
    elif request.subject == "S3_Plural":
        form.suffix = "t̆ey" if request.region == "AŞ" else "t̆es"
    else:
        form.suffix = form.suffixes[request.subject]


def _finish_form(form: Morphology) -> str:
    """Finish form for ergative progressive."""
    form.final_root = form.root[:-1] if form.root.endswith("s") else form.root
    if form.prefix and form.final_root and (form.prefix[-1] == form.final_root[0]):
        form.final_root = form.final_root[1:]
    form.conjugated_verb = f"{form.prefix}{form.final_root}{form.suffix}"
    return f"{form.first_word} {form.conjugated_verb}".strip()


def _preverb_do(form: Morphology) -> None:
    """Apply the do preverb branch."""
    request = form.request
    if form.root.startswith(("du", "idu", "udu", "odu")) and request.infinitive not in "dodumu":
        form.root = form.root[1:] if form.root.startswith("du") else form.root[2:]
        form.preverb = (
            "do"
            if request.subject in ["S1_Singular", "S1_Plural"]
            or request.obj in ["O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural"]
            else "d"
        )
        if request.applicative:
            if request.obj in ["O1_Singular", "O1_Plural", "O2_Singular", "O2_Plural"]:
                form.root = form.marker + form.root
        if request.causative or request.simple_causative:
            form.root = form.marker + form.root[1:]
        else:
            form.root = (
                "i" + form.root[2:]
                if request.subject in ["S1_Singular", "S1_Plural"]
                and request.obj in ["O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural"]
                or request.obj in ["O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural"]
                else form.root
            )
    form.first_letter = get_first_letter(form.root)
    if form.root.startswith("di"):
        form.root = form.root[1:]
    if request.obj in ["O2_Singular", "O2_Plural"] and request.subject not in [
        "S2_Singular",
        "S2_Plural",
    ]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        if form.root in ("iguraps", "igurams"):
            form.prefix = "do" + "b" if request.region == "FA" else "do" + "v"
        else:
            form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
            form.prefix = form.preverb + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"] and request.subject not in [
        "S1_Singular",
        "S1_Plural",
    ]:
        form.prefix = form.preverb + "m"
    elif form.marker_type == "causative" or request.main_infinitive == "doguru":
        form.prefix = "d"
    else:
        form.prefix = form.preverb
