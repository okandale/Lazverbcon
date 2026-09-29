"""Shared ergative preverb rules. Only identical source branches are shared."""

from ..rules.phonology import adjust_prefix, get_first_letter, is_vowel
from .state import Morphology


def _preverb_gol(form: Morphology) -> None:
    """Apply the gol preverb branch."""
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
        form.prefix = form.preverb + "o" + form.adjusted_prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
        form.prefix = form.preverb + "o" + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"] and request.subject not in [
        "S1_Singular",
        "S1_Plural",
    ]:
        form.prefix = form.preverb + "o" + "m"
    elif form.marker_type == "causative":
        form.prefix = form.preverb
    else:
        form.prefix = form.preverb


def _preverb_gelo_gel(form: Morphology) -> None:
    """Apply the gelo/gel preverb branch."""
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


def _preverb_ela_el(form: Morphology) -> None:
    """Apply the ela/el preverb branch."""
    request = form.request
    if (
        form.preverb in "ela"
        or (
            request.infinitive.startswith(("ela", "uela", "iela", "oel"))
            and (not form.root.startswith("ela"))
            and (
                request.subject in ["S1_Singular", "S1_Plural"]
                or request.obj in ["O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural"]
            )
        )
    ) or (request.obj in ["O3_Singular", "O3_Plural"] and form.marker):
        if form.marker:
            form.root = (
                form.marker + form.root[4:]
                if form.marker in ("u", "o")
                else form.marker + form.root[2:]
            )
        form.preverb = "ela"
        form.preverb_form = "el"
        form.root = form.root if form.marker in ("u", "o") else form.root[2:]
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


def _preverb_cel(form: Morphology) -> None:
    """Apply the cel preverb branch."""
    request = form.request
    if request.infinitive in "celabalu":
        if request.subject in ["S1_Singular", "S1_Plural"] or request.obj in [
            "O2_Singular",
            "O2_Plural",
            "O1_Singular",
            "O1_Plural",
        ]:
            if request.applicative and request.causative:
                form.root = "i" + form.root[5:]
            if request.applicative:
                form.root = "i" + form.root[5:]
            elif request.causative or request.simple_causative:
                form.root = "o" + form.root[5:]
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
        form.prefix = form.preverb + "a"
    else:
        form.prefix = form.preverb + "a"


def _preverb_ce(form: Morphology) -> None:
    """Apply the ce preverb branch."""
    request = form.request
    if request.infinitive in request.co_verbs or form.root.startswith(("icu", "ocu", "ucu", "u")):
        if (
            request.subject in ["S1_Singular", "S1_Plural"]
            and form.marker
            or (
                request.obj
                in [
                    "O2_Singular",
                    "O3_Singular",
                    "O3_Plural",
                    "O2_Plural",
                    "O1_Singular",
                    "O1_Plural",
                ]
                and form.marker
            )
        ):
            if form.root.startswith(("icu", "ucu", "ocu")):
                form.root = (
                    "c" + form.marker + form.root[3:]
                    if (request.applicative and request.causative or request.causative)
                    and request.subject in ("S2_Singular", "S3_Singular", "S3_Plural")
                    and (request.obj in ("O3_Singular", "O3_Plural"))
                    else form.marker + form.root[3:]
                )
            else:
                form.root = (
                    form.root
                    if request.subject in ("S1_Singular", "S1_Plural")
                    and form.marker == "u"
                    or form.marker
                    else form.root[2:]
                )
        elif form.marker and request.subject in "S3_Singular" and (request.obj in "O2_Plural"):
            form.root = form.marker + form.root[3:]
        elif form.marker:
            form.root = (
                "c" + form.marker + form.root[3:]
                if (request.applicative and request.causative or request.causative)
                and request.subject in ("S2_Singular", "S3_Singular", "S2_Plural", "S3_Plural")
                and (request.obj in ("O3_Singular", "O3_Plural"))
                and form.root.startswith(("icu", "ucu", "ocu"))
                else form.root[2:]
            )
        else:
            form.root = (
                form.root[1:]
                if request.subject in ("S1_Singular", "S1_Plural")
                or request.obj in ("O1_Singular", "O1_Plural", "O2_Singular", "O2_Plural")
                else form.root
            )
            form.preverb = (
                "ce"
                if request.subject in ("S1_Singular", "S1_Plural")
                or request.obj in ("O1_Singular", "O1_Plural", "O2_Singular", "O2_Plural")
                else ""
            )
    elif form.marker and request.obj in ["O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural"]:
        form.root = form.root
    else:
        form.root = form.root
    form.first_letter = get_first_letter(form.root)
    if form.root.startswith(("ca", "ic", "uc", "oc")):
        if request.infinitive == "cebgaru" and form.marker:
            form.root = form.root[:3] + "b" + form.root[3:]
        if (
            request.subject in ["S1_Singular", "S1_Plural"]
            and form.marker
            or (
                request.obj
                in [
                    ["O2_Singular", "O3_Singular", "O3_PluralO2_Plural", "O1_Singular", "O1_Plural"]
                ]
                and form.marker
            )
        ):
            if form.marker:
                form.root = form.root[2:]
            else:
                form.root = form.root[1:]
        elif request.subject in ["S1_Singular", "S1_Plural"] or (
            request.subject in ["S3_Singular", "S3_Plural"]
            and request.obj in ["O2_Singular", "O2_Plural"]
        ):
            form.root = (
                form.root[2:]
                if request.obj in ["O2_Plural", "O2_Singular"] and form.marker
                else form.root[1:]
            )
            form.preverb = "ce"
        elif request.obj in ["O1_Singular", "O1_Plural", "O2_Plural"]:
            form.root = form.root[2:] if form.marker else form.root[1:]
            form.preverb = "ce"
        else:
            form.root = form.root
            form.preverb = ""
    if request.infinitive in "ceyonu" and (not form.marker):
        form.root = (
            "i" + form.root[2:]
            if request.obj in ("O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural")
            else form.root[1:]
        )
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
        form.prefix = ""
    else:
        form.prefix = (
            form.preverb[:1] if form.root.startswith(("a", "e", "i", "o", "u")) else form.preverb
        )
    if form.root.startswith(("ic", "uc", "oc")):
        form.root = form.root[1:]


def _preverb_oxo(form: Morphology) -> None:
    """Apply the oxo preverb branch."""
    request = form.request
    if request.infinitive in ("oxoǯonu", "oxoşkvinu"):
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
        form.prefix = form.preverb + form.adjusted_prefix
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


def _preverb_oǩo(form: Morphology) -> None:
    """Apply the oǩo preverb branch."""
    request = form.request
    if request.infinitive in "oǩobğu":
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


def _preverb_mo(form: Morphology) -> None:
    """Apply the mo preverb branch."""
    request = form.request
    if form.root.startswith(("mu", "imu", "umu", "omu")):
        if form.root.startswith(("mu", "imu", "umu", "omu")):
            if not form.marker:
                form.root = (
                    "i" + form.root[2:]
                    if request.obj in ("O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural")
                    else form.root[1:]
                )
            if form.marker:
                form.root = (
                    form.marker + form.root[3:]
                    if request.obj in ("O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural")
                    else form.marker + form.root[3:]
                )
        else:
            if form.marker:
                form.root = (
                    form.marker + form.root[1:]
                    if request.obj in ("O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural")
                    else form.marker + form.root[2:]
                )
            if not form.marker:
                form.root = (
                    form.root[1:]
                    if request.obj in ("O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural")
                    else form.root[1:]
                )
            else:
                form.root = (
                    form.marker + form.root[3:]
                    if request.obj in ("O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural")
                    else form.root[2:]
                )
        form.preverb = (
            "m"
            if request.subject in ("S2_Singular", "S3_Singular", "S2_Plural", "S3_Plural")
            and request.obj in ("O3_Singular", "O3_Plural")
            else "m"
            if request.subject in ("S2_Singular", "S2_Plural") and (not request.obj)
            else form.preverb
        )
    form.first_letter = get_first_letter(form.root)
    if request.obj in ["O2_Singular", "O2_Plural"] and request.subject not in [
        "S2_Singular",
        "S2_Plural",
    ]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.preverb = (
            "m" if form.adjusted_prefix.startswith(("a", "e", "i", "o", "u")) else form.preverb
        )
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"] and request.subject not in [
        "S1_Singular",
        "S1_Plural",
    ]:
        form.prefix = "mom"
    else:
        form.prefix = ""
    if request.infinitive.startswith("mo") and (
        not form.original_root.startswith(("mo", "mu"))
        or (
            form.original_root.startswith("mu")
            and request.subject in ("S3_Singular", "S3_Plural")
            and (request.obj is None)
        )
    ):
        form.preverb = form.preverb[:1]


def _preverb_me(form: Morphology) -> None:
    """Apply the me preverb branch."""
    request = form.request
    if request.infinitive in request.no_verbs:
        if form.root.startswith(("nu", "inu", "unu", "onu")):
            if not form.marker:
                form.root = (
                    "i" + form.root[2:]
                    if request.obj in ("O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural")
                    else form.root[1:]
                )
            if form.marker:
                form.root = (
                    form.marker + form.root[3:]
                    if request.obj in ("O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural")
                    else form.marker + form.root[3:]
                )
        else:
            if form.marker:
                form.root = (
                    form.marker + form.root[1:]
                    if request.obj in ("O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural")
                    else form.marker + form.root[2:]
                )
            if not form.marker:
                form.root = (
                    form.root[1:]
                    if request.obj in ("O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural")
                    else form.root[1:]
                )
            else:
                form.root = (
                    form.marker + form.root[3:]
                    if request.obj in ("O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural")
                    else form.marker + form.root[2:]
                )
    form.first_letter = get_first_letter(form.root)
    if request.obj in ["O2_Singular", "O2_Plural"] and request.subject not in [
        "S2_Singular",
        "S2_Plural",
    ]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.preverb = "n" if form.root.startswith(("a", "e", "i", "o", "u")) else form.preverb
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.adjusted_prefix = adjust_prefix("v", form.first_letter, form.phonetic_rules_v)
        form.prefix = form.preverb + form.adjusted_prefix
    elif request.obj in ["O1_Singular", "O1_Plural"] and request.subject not in [
        "S1_Singular",
        "S1_Plural",
    ]:
        form.prefix = "mem" if request.infinitive in request.no_verbs else "mom"
    else:
        form.prefix = "me"
    if (
        is_vowel(form.root[0])
        and form.prefix.endswith(("a", "i", "u", "o", "e"))
        and (not form.adjusted_prefix)
    ):
        form.preverb = "n"
    elif form.prefix == "mom":
        form.preverb = "mo"
    else:
        form.preverb = "me"


def _preverb_ge(form: Morphology) -> None:
    """Apply the ge preverb branch."""
    request = form.request
    if request.infinitive == "gemgaru":
        if form.marker:
            form.root = form.marker + form.root[3:]
        elif request.subject in ("S1_Singular", "S1_Plural") or request.obj in (
            "O2_Singular",
            "O2_Plural",
            "O1_Singular",
            "O1_Plural",
        ):
            form.root = form.root[2:]
        else:
            form.preverb = ""
    if request.infinitive in request.gyo_verbs:
        if (
            request.subject in ["S1_Singular", "S1_Plural"]
            and form.marker
            or (
                request.obj in ["O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural"]
                and form.marker
            )
        ):
            if form.root.startswith(("igyu", "ugyu", "ogyu")):
                form.root = form.marker + form.root[4:]
            else:
                form.root = (
                    "u" + form.root[2:]
                    if request.subject in ("S1_Singular", "S1_Plural") and form.marker == "u"
                    else form.root[2:]
                )
        elif (
            request.subject in ("S2_Singular", "S2_Plural", "S3_Singular", "S3_Plural")
            and form.marker
        ):
            if form.root.startswith(("igyu", "ugyu", "ogyu")):
                form.root = (
                    "y" + form.marker + form.root[4:]
                    if request.applicative or (request.applicative and request.causative)
                    else "gy" + form.marker + form.root[4:]
                )
            else:
                form.root = (
                    "yu" + form.root[2:]
                    if request.applicative or (request.applicative and request.causative)
                    else "gy" + form.root[2:]
                )
        else:
            form.root = (
                form.root[2:]
                if request.subject in ("S1_Singular", "S1_Plural")
                or request.obj in ("O2_Singular", "O2_Plural", "O1_Singular", "O1_Plural")
                else form.root[1:]
            )
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
