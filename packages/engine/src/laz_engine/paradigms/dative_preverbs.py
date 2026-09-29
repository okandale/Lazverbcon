"""Shared dative preverb rules. Only identical source branches are shared."""

from ..rules.phonology import adjust_prefix
from .state import Morphology


def _preverb_me(form: Morphology) -> None:
    """Apply the me preverb branch."""
    request = form.request
    if form.root.startswith("na") and request.subject not in ("S3_Singular",):
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


def _preverb_go(form: Morphology) -> None:
    """Apply the go preverb branch."""
    request = form.request
    if request.subject in ("S3_Singular", "S3_Plural") and (not request.obj):
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
        form.prefix = form.preverb + "g"
    else:
        form.prefix = form.preverb[:-1]


def _preverb_do(form: Morphology) -> None:
    """Apply the do preverb branch."""
    request = form.request
    if request.subject in ("S3_Singular", "S3_Plural") and (not request.obj):
        form.preverb = ""
    else:
        form.root = form.root[2:] if request.region in ("PZ", "AŞ", "HO") else form.root[1:]
    if request.subject in ("S3_Singular", "S3_Plural"):
        if request.obj in ("O1_Singular", "O1_Plural"):
            form.adjusted_prefix = "v" if request.region in ("PZ", "AŞ", "HO") else "b"
            form.prefix = form.preverb + form.adjusted_prefix
        else:
            form.prefix = "d" if request.region in "FA" else "dv"
    elif request.subject in ["S1_Singular", "S1_Plural"]:
        form.prefix = form.preverb + "m"
    elif request.subject in ["S2_Singular", "S2_Plural"]:
        form.adjusted_prefix = adjust_prefix("g", form.first_letter, form.phonetic_rules_g)
        form.prefix = form.preverb + form.adjusted_prefix
    else:
        form.prefix = form.preverb[:-1]
