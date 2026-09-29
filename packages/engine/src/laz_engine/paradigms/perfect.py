"""Perfect morphology. See docs/rules.md for stage ordering and source provenance."""

from ..rules.endings import endings_for
from ..rules.markers import presentperf_subject_markers as subject_markers
from ..rules.phonology import (
    get_first_letter,
    get_first_word,
    get_phonetic_rules,
    process_compound_verb,
)
from ..rules.preverbs import find_preverb, get_preverbs_rules
from .state import Morphology, RuleRequest

preverbs_rules = get_preverbs_rules("tvm_tve_presentperf")


def conjugate(request: RuleRequest, principal_part: str) -> str:
    """Conjugate one lexical variant; rule stages run in the order shown."""
    form = Morphology(request, principal_part)
    _prepare_stem(form)
    _apply_preverbs(form)
    return _finish_form(form)


def _prepare_stem(form: Morphology) -> None:
    """Prepare stem for perfect."""
    request = form.request
    form.phonetic_rules_v, form.phonetic_rules_g = get_phonetic_rules(request.region, is_tvm=True)
    form.root = request.infinitive
    form.first_word = get_first_word(form.root)
    form.root = process_compound_verb(form.root)
    form.suffixes = endings_for("perfect", "present_perfect", request.region)
    form.preverb = ""
    preverb_exceptions = {"oǩoreʒxu", "oǩoru", "oxop̌u"}
    form.preverb = find_preverb(
        request.main_infinitive, preverbs_rules, excluded=request.infinitive in preverb_exceptions
    )
    if form.preverb and form.root.startswith(form.preverb):
        form.root = form.root[len(form.preverb) : -1]
    elif form.root in ("oşu", "dodumu", "otku"):
        form.root = request.infinitive[1:-1] + "v"
    else:
        form.root = form.root[1:-1]


def _apply_preverbs(form: Morphology) -> None:
    """Apply preverbs for perfect."""
    request = form.request
    form.first_letter = get_first_letter(form.root)
    if (
        form.preverb.endswith(("a", "e", "i", "o", "u"))
        and request.subject in subject_markers
        and subject_markers[request.subject].startswith(("a", "e", "i", "o", "u"))
        and (request.subject not in ("S1_Singular", "S1_Plural"))
        and (request.obj not in ("O1_Singular", "O1_Plural", "O2_Plural", "O2_Singular"))
        and (form.preverb == "e")
    ):
        form.preverb = "ey" if request.region == "PZ" else "y"
    if form.preverb.endswith(("a", "e", "i", "o", "u")) and subject_markers[
        request.subject
    ].startswith(("a", "e", "i", "o", "u")):
        if form.root.startswith("gyo"):
            form.preverb = form.preverb[:-1] + "y"
        else:
            form.preverb = form.preverb
    if form.preverb == "me" and subject_markers[request.subject].startswith(
        ("a", "e", "i", "o", "u")
    ):
        form.preverb = "n"
        form.prefix = form.preverb + subject_markers[request.subject]
    elif form.preverb == "ce" and request.subject in ["S3_Singular", "S3_Plural"]:
        form.prefix = "c" + subject_markers[request.subject]
    elif request.infinitive in "gamaçamu":
        form.root = "ç"
        form.preverb = "gam" if request.subject in ("S3_Singular", "S3_Plural") else "gamo"
        form.prefix = form.preverb + subject_markers[request.subject]
    elif (
        request.infinitive.startswith("gama")
        and (not form.root.startswith("gama"))
        and (
            request.subject in ["S1_Singular", "S1_Plural"]
            or request.obj in ["O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural"]
        )
    ):
        form.preverb = "gama"
        form.prefix = form.preverb + subject_markers[request.subject]
    elif form.preverb == "go" and request.subject in ("S3_Singular", "S3_Plural"):
        form.prefix = (
            "gv" + subject_markers[request.subject]
            if request.region in "HO"
            else "g" + subject_markers[request.subject]
        )
    elif form.preverb == "e" and request.subject in ("S3_Singular", "S3_Plural"):
        form.prefix = "y" + subject_markers[request.subject]
    elif form.preverb:
        if form.preverb.endswith(("a", "e", "i", "o", "u")) and subject_markers[
            request.subject
        ].startswith(("a", "e", "i", "o", "u")):
            form.preverb = form.preverb[:-1]
        form.prefix = form.preverb + subject_markers[request.subject]
    else:
        form.prefix = subject_markers[request.subject]


def _finish_form(form: Morphology) -> str:
    """Finish form for perfect."""
    request = form.request
    form.suffix = form.suffixes[request.subject]
    form.final_root = form.root
    form.conjugated_verb = f"{form.prefix}{form.final_root}{form.suffix}"
    return f"{form.first_word} {form.conjugated_verb}".strip()
