"""Ergative past morphology. See docs/rules.md for stage ordering and source provenance."""

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

preverbs_rules = get_preverbs_rules("tve_past")


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
    """Prepare stem for ergative past."""
    request = form.request
    form.phonetic_rules_v, form.phonetic_rules_g = get_phonetic_rules(request.region)
    form.adjusted_prefix = ""
    form.original_root = process_compound_verb(form.principal_part)
    form.root = process_compound_verb(form.principal_part)
    form.first_word = get_first_word(form.principal_part)
    form.root = process_compound_verb(form.root)
    form.suffixes = {
        "S1_Singular": "i",
        "S2_Singular": "i",
        "S3_Singular": "u",
        "S1_Plural": "it",
        "S2_Plural": "it",
        "S3_Plural": "ey" if request.region == "AŞ" else "es",
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
    """Apply markers for ergative past."""
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
        form.root = "xvenums"
    if request.infinitive in "oxenu":
        form.root = "xenams"
    if request.infinitive in "oxvenu":
        form.root = "xvenams"
    if request.infinitive in "oç̌ǩomu":
        form.root = "ç̌ǩomums"
    if request.infinitive in "oşǩomu":
        form.root = "şǩomums"
    if form.root.endswith("rs") and request.infinitive.endswith("du"):
        form.root = form.root[:-2] + "d"
    form.root = handle_marker(
        request.main_infinitive, form.root, form.marker, request.subject, request.obj
    )
    form.adjusted_prefix = ""
    form.first_letter = get_first_letter(form.root)
    form.handled_gontzku = False


def _apply_preverbs(form: Morphology) -> None:
    """Apply preverbs for ergative past."""
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
                    form.prefix = "mp̌"
                else:
                    form.prefix = subject_markers[request.subject]
            if request.obj in ["O2_Singular", "O2_Plural"] and request.subject not in [
                "S2_Singular",
                "S2_Plural",
            ]:
                if form.root.startswith("n"):
                    form.root = form.root[1:]
                    form.first_letter = get_first_letter(form.root)
                form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
                form.prefix = form.preverb + form.adjusted_prefix
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
    """Adjust stem for ergative past."""
    request = form.request
    if form.principal_part.endswith("y"):
        if request.subject == "S3_Singular":
            form.root = form.root
        else:
            form.root = form.root[:-1] + "ms"
    if request.applicative and request.causative:
        if request.infinitive in ("oşu", "dodvu", "otku", "golusu", "meşǩvu"):
            form.root = (
                form.root[:-5] + "vap" if request.infinitive in "golusu" else form.root[:-3] + "vap"
            )
        elif form.root.endswith(("ms", "ps")):
            form.root = form.root[:-3] + "ap"
        elif form.root.endswith("umers") or form.root.endswith("amers"):
            form.root = form.root[:-5] + "ap"
        elif form.root.endswith("rs"):
            form.root = form.root[:-1] + "ap"
    elif request.applicative or request.simple_causative:
        if form.root in ("işums", "işups", "idums", "itkums", "itkups") or request.infinitive in (
            "golusu",
            "meşǩvu",
        ):
            form.root = (
                form.root[:-5] + "v" if request.infinitive in "golusu" else form.root[:-3] + "vap"
            )
        elif form.root.endswith(("ms", "ps")):
            form.root = form.root[:-3]
    elif request.causative:
        if form.root == "digurams":
            form.root = form.root
        elif form.root in ("oşums", "oşups", "odums", "otkums", "otkups") or request.infinitive in (
            "golusu",
            "meşǩvu",
        ):
            form.root = (
                form.root[:-5] + "v" if request.infinitive in "golusu" else form.root[:-3] + "vap"
            )
        elif form.root.endswith(("ms", "ps")):
            form.root = form.root[:-3] + "ap"
        elif form.root.endswith("umers") or form.root.endswith("amers"):
            form.root = form.root[:-5] + "ap"
        elif form.root.endswith("rs"):
            form.root = form.root[:-1] + "ap"
    elif form.root in ("şums", "şups", "dums", "tkums", "tkups") or request.infinitive in "meşǩvu":
        form.root = form.root[:-3] + "v"
        if request.subject == "S3_Singular":
            form.root = form.root[:-1]
    elif form.root.endswith(("ms", "ps")):
        form.root = form.root[:-3]
    elif form.root.endswith("y"):
        form.root = form.root[:-2]
    elif form.root.endswith(("umers", "amers")):
        form.root = form.root[:-5] + "v"
    else:
        form.root = form.root


def _select_ending(form: Morphology) -> None:
    """Select ending for ergative past."""
    request = form.request
    if request.subject in ("S1_Singular", "S2_Singular") and request.obj in (
        "O1_Plural",
        "O2_Plural",
    ):
        form.suffix = "it"
    elif request.subject == "S2_Singular" and request.obj == "S1_Plural":
        form.suffix = "it"
    elif request.subject == "S3_Singular" and request.obj in [
        "O1_Singular",
        "O3_Singular",
        "O2_Singular",
        "O3_Plural",
    ]:
        form.suffix = "u"
    elif request.subject in ("S1_Singular", "S2_Singular") and request.obj in (
        "O1_Singular",
        "O2_Singular",
        "O3_Singular",
        "O3_Plural",
    ):
        form.suffix = "i"
    elif request.subject == "S3_Singular" and request.obj in ["O1_Plural", "O2_Plural"]:
        form.suffix = "ey" if request.region == "AŞ" else "es"
    elif request.subject in ["S1_Plural", "S2_Plural"]:
        form.suffix = "it"
    elif request.subject == "S3_Plural":
        form.suffix = "ey" if request.region == "AŞ" else "es"
    else:
        form.suffix = form.suffixes[request.subject]


def _finish_form(form: Morphology) -> str:
    """Finish form for ergative past."""
    request = form.request
    form.final_root = form.root[:-1] if form.root.endswith("s") else form.root
    if (
        request.infinitive in ("oxenu", "oxvenu")
        and request.subject in ("S1_Singular", "S1_Plural")
        and (not request.applicative)
        and (not request.causative)
    ):
        form.prefix = "(do)p̌"
        # lazverbcon2 rows 362779/815/851 and 362995/363031/067 correct
        # only singular I -> you; the dump retains p̌ in plural requests.
        if (
            request.infinitive == "oxenu"
            and request.region in ("AŞ", "PZ", "FA")
            and request.subject == "S1_Singular"
            and request.obj == "O2_Singular"
        ):
            form.prefix = "(do)ǩ"
        form.final_root = "qv" if request.region in "HO" else ""
    elif (
        request.infinitive in ("oxenu", "oxvenu")
        and request.subject in ("S2_Singular", "S2_Plural")
        and (not request.applicative)
        and (not request.causative)
    ):
        form.prefix = ""
        form.final_root = (
            "" if request.region in ("AŞ", "PZ") else "v" if request.region in "FA" else "qv"
        )
    elif (
        request.infinitive in ("oxenu", "oxvenu")
        and request.subject in ("S3_Singular", "S3_Plural")
        and (not request.applicative)
        and (not request.causative)
    ):
        form.prefix = "q" if request.region == "HO" else ""
        form.final_root = (
            "" if request.region in ("AŞ", "PZ") else "v" if request.region in "HO" else "v"
        )
    if form.prefix and form.final_root and (form.prefix[-1] == form.final_root[0]):
        form.final_root = form.final_root[1:]
    form.conjugated_verb = f"{form.prefix}{form.final_root}{form.suffix}"
    if form.conjugated_verb == "p̌qvi":
        form.conjugated_verb = "(do)p̌qvi (dop̌i)"
    if form.conjugated_verb == "p̌qvit":
        form.conjugated_verb = "(do)p̌qvit (dop̌it)"
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
                form.root = form.marker + form.root[1:]
        if request.causative or request.simple_causative:
            form.root = form.marker + form.root[1:]
        else:
            form.root = (
                "i" + form.root[1:]
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
