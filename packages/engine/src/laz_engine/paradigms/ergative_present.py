"""Ergative present morphology. See docs/rules.md for stage ordering and source provenance."""

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
from .ergative_preverbs import _preverb_ela_el as _preverb_ela_el
from .ergative_preverbs import _preverb_ge as _preverb_ge
from .ergative_preverbs import _preverb_gol as _preverb_gol
from .ergative_preverbs import _preverb_me as _preverb_me
from .ergative_preverbs import _preverb_mo as _preverb_mo
from .ergative_preverbs import _preverb_oxo as _preverb_oxo
from .state import Morphology, RuleRequest

preverbs_rules = get_preverbs_rules("tve_present")


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
    """Prepare stem for ergative present."""
    request = form.request
    form.phonetic_rules_v, form.phonetic_rules_g = get_phonetic_rules(request.region)
    form.original_root = process_compound_verb(form.principal_part)
    form.root = process_compound_verb(form.principal_part)
    form.first_word = get_first_word(form.principal_part)
    form.root = process_compound_verb(form.root)
    form.suffixes = {
        "S1_Singular": "",
        "S2_Singular": "",
        "S3_Singular": "s",
        "S1_Plural": "t",
        "S2_Plural": "t",
        "S3_Plural": "an",
    }
    form.preverb = ""
    preverb_exceptions = {"oǩoreʒxu", "oǩoru", "oxop̌u"}
    form.preverb = find_preverb(
        request.main_infinitive, preverbs_rules, excluded=request.infinitive in preverb_exceptions
    )
    form.root = process_compound_verb(form.principal_part)
    if form.preverb and form.root.startswith(form.preverb):
        form.root = form.root[len(form.preverb) :]


def _apply_markers(form: Morphology) -> None:
    """Apply markers for ergative present."""
    request = form.request
    form.marker = ""
    form.marker_type = ""
    if request.applicative:
        form.marker = determine_marker(request.subject, request.obj, "applicative")
        form.marker_type = "applicative"
    elif request.causative:
        form.marker = determine_marker(request.subject, request.obj, "causative")
        form.marker_type = "causative"
    elif request.simple_causative:
        form.marker = determine_marker(request.subject, request.obj, "simple_causative")
        form.marker_type = "simple_causative"
    if form.marker:
        form.root = handle_marker(
            request.main_infinitive, form.root, form.marker, request.subject, request.obj
        )
    if request.mood == "optative" and request.infinitive == "oç̌ǩomu":
        form.root = form.marker + "ç̌ǩomum" if form.marker else "ç̌ǩomum"
    elif request.mood == "optative" and request.infinitive == "oşǩomu":
        form.root = form.marker + "şǩomum" if form.marker else "şǩomum"
    elif request.mood == "optative" and request.infinitive == "oxvenu":
        form.root = form.marker + "xvenams" if form.marker else "xvenams"
    elif request.mood == "optative" and request.infinitive == "oxenu":
        form.root = form.marker + "xenams" if form.marker else "xenams"
    form.first_letter = get_first_letter(form.root)
    form.adjusted_prefix = ""
    form.handled_gontzku = False


def _apply_preverbs(form: Morphology) -> None:
    """Apply preverbs for ergative present."""
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
        elif form.preverb == "gelo":
            _preverb_gelo(form)
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
        elif form.preverb:
            _general_preverb_agreement(form)
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
            elif request.obj in ["O2_Singular", "O2_Plural"] and request.subject not in [
                "S2_Singular",
                "S2_Plural",
            ]:
                if form.root.startswith("n"):
                    form.root = form.root[1:]
                    form.first_letter = get_first_letter(form.root)
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
            else:
                form.prefix = subject_markers[request.subject]


def _adjust_stem(form: Morphology) -> None:
    """Adjust stem for ergative present."""
    request = form.request
    if form.principal_part.endswith("y"):
        if request.subject == "S3_Singular":
            form.root = form.root
        else:
            form.root = form.root[:-1] + "m"
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
        elif request.infinitive == "doguru":
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
    if request.mood == "optative" and request.infinitive in ("oşu", "dodvu", "otku"):
        if request.applicative and request.causative:
            form.root = form.root[:-2]
        elif request.applicative:
            form.root = form.root[:-3] + "v"
        elif request.causative:
            form.root = form.root[:-2]
        else:
            form.root = form.root[:-3] + "v"
    elif request.mood == "optative" and form.root.endswith(("ms", "ps")):
        form.root = form.root[:-3]
    elif request.mood == "optative" and form.root.endswith(("umers", "amers")):
        form.root = form.root[:-5]
    elif request.mood == "optative" and form.root.endswith("ums"):
        form.root = form.root[:-3]
    elif request.mood == "optative" and form.root.endswith("ams"):
        form.root = form.root[:-3]
    elif request.mood == "optative" and form.root.endswith(("um", "am")):
        form.root = form.root[:-2]
    elif request.mood == "optative" and form.root.endswith("y"):
        form.root = form.root[:-2]
    elif request.mood == "optative" and form.root.endswith("rs"):
        form.root = form.root[:-1]
    elif request.mood == "optative":
        form.root = form.root[:-2]


def _select_ending(form: Morphology) -> None:
    """Select ending for ergative present."""
    request = form.request
    if (
        request.subject == "S3_Singular"
        and request.obj in ["O1_Singular", "O3_Singular", "O2_Singular"]
        and form.root.endswith("ms")
        and (request.mood == "optative")
    ):
        form.suffix = "ay" if request.region == "AŞ" else "as"
    elif (
        request.subject == "S3_Singular"
        and (request.obj in ["O1_Singular", "O3_Singular", "O2_Singular"] or request.obj is None)
        and form.root.endswith(("ms", "rs"))
    ):
        if request.region == "AŞ":
            if form.root.endswith(("ms", "rs")):
                form.root = form.root[:-2]
            else:
                form.root = form.root[:-1]
            form.suffix = "y"
        else:
            form.suffix = "s"
    elif (
        request.subject == "S3_Singular"
        and request.obj in ["O2_Plural", "O1_Plural"]
        and form.root.endswith("ms")
        and (request.region == "AŞ")
    ):
        form.suffix = "man"
    elif (
        request.subject == "S3_Singular"
        and request.obj in ["O1_Plural", "O3_Plural", "O2_Plural"]
        and form.root.endswith("ms")
    ):
        form.root = form.root[:-1]
        form.suffix = "an"
    elif (
        request.subject == "S3_Singular"
        and request.obj in ["O1_Singular", "O3_Singular", "O2_Singular"]
        and form.root.endswith("y")
        and (request.mood == "optative")
    ):
        form.suffix = "ay"
    elif (
        request.subject == "S3_Singular"
        and (request.obj in ["O1_Singular", "O3_Singular", "O2_Singular"] or request.obj is None)
        and form.root.endswith("y")
    ):
        form.suffix = ""
    elif request.subject == "S3_Singular" and request.obj in ["O1_Plural", "O2_Plural"]:
        form.suffix = "man" if form.root.endswith("m") and request.region == "AŞ" else "an"
    elif request.subject in ("S1_Singular", "S2_Singular") and request.mood == "optative":
        form.suffix = "a"
    elif request.subject in ("S1_Plural", "S2_Plural") and request.mood == "optative":
        form.suffix = "at" if request.region == "AŞ" else "at"
    elif request.subject in ["S1_Singular", "S1_Plural"] and request.obj == "O2_Plural":
        form.suffix = "t"
    elif request.subject in ["S2_Singular", "S2_Plural"] and request.obj == "O1_Plural":
        form.suffix = "t"
    elif request.subject == "S3_Singular" and request.mood == "optative":
        form.suffix = "ay" if request.region == "AŞ" else "as"
    elif request.subject == "S3_Singular" and form.root.endswith(("um", "am", "ms")):
        if request.region == "AŞ":
            if form.root.endswith("ms"):
                form.root = form.root[:-2]
            else:
                form.root = form.root[:-1]
            form.suffix = "y"
        else:
            form.suffix = "s"
    else:
        form.suffix = form.suffixes[request.subject]


def _finish_form(form: Morphology) -> str:
    """Finish form for ergative present."""
    request = form.request
    if request.region == "AŞ" and form.root.endswith("apam") and (request.subject == "S3_Singular"):
        form.final_root = form.root[:-1]
    elif request.region == "AŞ" and form.root.endswith("ms") and (request.subject == "S3_Singular"):
        form.final_root = form.root[:-2]
    elif form.root.endswith("s"):
        form.final_root = form.root[:-1]
    else:
        form.final_root = form.root
    if form.prefix and form.final_root and (form.prefix[-1] == form.final_root[0]):
        form.final_root = form.final_root[1:]
    form.conjugated_verb = f"{form.prefix}{form.final_root}{form.suffix}"
    if (
        request.mood == "optative"
        and request.infinitive in ("oxvenu", "oxenu")
        and (request.obj is None)
    ):
        form.conjugated_verb = (
            "p̌a"
            if request.subject == "S1_Singular"
            else "p̌at"
            if request.subject == "S1_Plural"
            else "N/A - geçersiz kombinasyon"
        )
    return f"{form.first_word} {form.conjugated_verb}".strip()


def _preverb_gelo(form: Morphology) -> None:
    """Apply the gelo preverb branch."""
    request = form.request
    if form.root.endswith("ams"):
        if (
            request.subject in ["S1_Singular", "S1_Plural"]
            or request.obj in ["O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural"]
            or (request.obj in ["O3_Singular", "O3_Plural"] and form.marker)
        ):
            if request.applicative and request.causative:
                form.root = form.root
            if request.applicative:
                form.root = form.root
            elif request.causative or request.simple_causative:
                form.root = form.root
            else:
                form.root = "o" + form.root
        else:
            form.root = form.root
            form.preverb = form.preverb
    elif form.marker and request.obj in ["O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural"]:
        form.root = form.root
    else:
        form.root = form.root
    form.first_letter = get_first_letter(form.root)
    if request.obj in ["O2_Singular", "O2_Plural"] and request.subject not in [
        "S2_Singular",
        "S2_Plural",
    ]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"] and request.subject not in [
        "S1_Singular",
        "S1_Plural",
    ]:
        form.prefix = form.preverb + "m"
    elif form.marker_type == "causative":
        form.prefix = form.preverb
    else:
        form.prefix = form.preverb


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
            if form.root.startswith("n"):
                form.root = form.root[1:]
            form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
            form.prefix = form.preverb + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"] and request.subject not in [
        "S1_Singular",
        "S1_Plural",
    ]:
        if form.root.startswith("n"):
            form.root = form.root[1:]
        form.prefix = form.preverb + "m"
    elif form.marker_type == "causative" or request.main_infinitive == "doguru":
        form.prefix = "d"
    else:
        form.prefix = form.preverb


def _preverb_cel(form: Morphology) -> None:
    """Apply the cel preverb branch."""
    request = form.request
    if request.infinitive.startswith("cela"):
        if (
            request.subject in ["S1_Singular", "S1_Plural"]
            or request.obj in ["O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural"]
            or (request.obj in ["O3_Singular", "O3_Plural"] and form.marker)
        ):
            if request.applicative and request.causative:
                form.root = "i" + form.root[2:]
            if request.applicative:
                form.root = "i" + form.root[2:]
            elif request.causative or request.simple_causative:
                form.root = "o" + form.root[2:]
            else:
                form.root = "o" + form.root[1:]
        else:
            form.root = form.root[1:]
            form.preverb = form.preverb
    elif form.marker and request.obj in ["O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural"]:
        form.root = form.root
    else:
        form.root = form.root
    form.first_letter = get_first_letter(form.root)
    if request.obj in ["O2_Singular", "O2_Plural"] and request.subject not in [
        "S2_Singular",
        "S2_Plural",
    ]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = form.preverb + "e" + form.adjusted_prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
        form.prefix = form.preverb + "e" + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"] and request.subject not in [
        "S1_Singular",
        "S1_Plural",
    ]:
        form.prefix = form.preverb + "em"
    elif form.marker_type == "causative":
        form.prefix = form.preverb
    else:
        form.prefix = form.preverb + "a"


def _preverb_oǩo(form: Morphology) -> None:
    """Apply the oǩo preverb branch."""
    request = form.request
    if request.infinitive.startswith("oǩo"):
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
                else form.root
            )
        else:
            form.root = "o" + form.root
    elif form.marker and request.obj in ["O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural"]:
        form.root = form.root
    else:
        form.root = form.root
    form.first_letter = get_first_letter(form.root)
    if request.obj in ["O2_Singular", "O2_Plural"] and request.subject not in [
        "S2_Singular",
        "S2_Plural",
    ]:
        form.first_letter = get_first_letter(form.root)
        form.root = (
            form.root[1:]
            if form.marker and request.subject == "S3_Singular" and (request.obj == "O2_Plural")
            else form.root
        )
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = "oǩo" + form.adjusted_prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
        if form.root.startswith("n"):
            form.root = form.root[1:]
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"] and request.subject not in [
        "S1_Singular",
        "S1_Plural",
    ]:
        if form.root.startswith("n"):
            form.root = form.root[1:]
        form.prefix = form.preverb + "m"
    elif form.marker_type in ("causative", "applicative"):
        form.prefix = form.preverb
    else:
        form.prefix = form.preverb


def _general_preverb_agreement(form: Morphology) -> None:
    """Apply agreement after the specific preverb cases."""
    request = form.request
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
            form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
            form.prefix = form.preverb + "n" + form.adjusted_prefix
        else:
            form.first_letter = get_first_letter(form.root)
            form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
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
