# conjugation.py
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Optional, Dict, Tuple

from validators import ConjugationValidator
from services.conjugation import ConjugationService


SIMPLIFIED_TENSE_MAPPING = {
    "present": ["ivd_present", "tve_present", ("tvm_tense", "present")],
    "past": ["ivd_past", "tve_past", ("tvm_tense", "past")],
    "future": ["ivd_future", "tve_future", ("tvm_tense", "future")],
    "pastpro": ["ivd_pastpro", "tve_pastpro", ("tvm_tense", "past progressive")],
    "presentperf": ["tvm_tve_presentperf"],
}

SIMPLIFIED_ASPECT_MAPPING = {
    "potential": ["tvm_tve_potential"],
    "passive": ["tvm_tve_passive"],
}

SPECIAL_IVD_PAST_AS_PASTPRO = {"uğun", "oçkinu", "uyonun", "uqoun", "unon"}
SPECIAL_REQUIRES_MARKER = {"gexvamu", "cexvamu", "otebriǩu", "oteşekkyuru"}


@dataclass
class ConjugationMeta:
    # normalized inputs actually used
    infinitive: str
    tense: Optional[str]
    aspect: Optional[str]
    obj: Optional[str]

    subject: str
    optative: bool
    imperative: bool
    neg_imperative: bool

    applicative: bool
    causative: bool
    simple_causative: bool

    # derived flags
    has_markers: bool
    exists_in_ivd: bool
    exists_in_tve: bool
    exists_in_tvm: bool
    exists_in_tvm_tve: bool

    # what happened / what we decided
    selected: Dict[str, Any]


def check_verb_existence(infinitive: str, tense_modules: Dict[str, Any]) -> Tuple[bool, bool, bool, bool]:
    """Copied from app.py, moved here."""
    infinitive = infinitive.lower().strip()

    # IVD
    exists_in_ivd = False
    for module_name in ["ivd_present", "ivd_past", "ivd_pastpro", "ivd_future"]:
        mod = tense_modules.get(module_name)
        if mod and hasattr(mod, "verbs"):
            verbs = {v.lower().strip() for v in mod.verbs}
            if infinitive in verbs:
                exists_in_ivd = True
                break

    # TVE
    exists_in_tve = False
    for module_name in ["tve_present", "tve_past", "tve_pastpro", "tve_future"]:
        mod = tense_modules.get(module_name)
        if mod and hasattr(mod, "verbs"):
            verbs = {v.lower().strip() for v in mod.verbs}
            if infinitive in verbs:
                exists_in_tve = True
                break

    # TVM
    exists_in_tvm = False
    tvm_mod = tense_modules.get("tvm_tense")
    if tvm_mod and hasattr(tvm_mod, "verbs"):
        verbs = {v.lower().strip() for v in tvm_mod.verbs}
        if infinitive in verbs:
            exists_in_tvm = True

    # TVM/TVE special modules
    exists_in_tvm_tve = False
    for module_name in ["tvm_tve_presentperf", "tvm_tve_potential", "tvm_tve_passive"]:
        mod = tense_modules.get(module_name)
        if mod and hasattr(mod, "verbs"):
            verbs = {v.lower().strip() for v in mod.verbs}
            if infinitive in verbs:
                exists_in_tvm_tve = True
                break

    return exists_in_ivd, exists_in_tve, exists_in_tvm, exists_in_tvm_tve


def _request_params(
    *,
    infinitive: str,
    tense: Optional[str],
    aspect: Optional[str],
    obj: Optional[str],
    subject: str,
    optative: bool,
    imperative: bool,
    neg_imperative: bool,
    applicative: bool,
    causative: bool,
    simple_causative: bool,
) -> Dict[str, Any]:
    """
    Canonical request dict that matches what your ConjugationValidator expects
    (string booleans, etc.).
    """
    return {
        "infinitive": infinitive,
        "tense": tense,
        "aspect": aspect,
        "obj": obj,
        "subject": subject,
        "optative": str(optative).lower(),
        "imperative": str(imperative).lower(),
        "neg_imperative": str(neg_imperative).lower(),
        "applicative": str(applicative).lower(),
        "causative": str(causative).lower(),
        "simple_causative": str(simple_causative).lower(),
    }


def _meta(
    *,
    infinitive: str,
    tense: Optional[str],
    aspect: Optional[str],
    obj: Optional[str],
    subject: str,
    optative: bool,
    imperative: bool,
    neg_imperative: bool,
    applicative: bool,
    causative: bool,
    simple_causative: bool,
    has_markers: bool,
    exists_in_ivd: bool,
    exists_in_tve: bool,
    exists_in_tvm: bool,
    exists_in_tvm_tve: bool,
    selected: Dict[str, Any],
) -> Dict[str, Any]:
    return asdict(
        ConjugationMeta(
            infinitive=infinitive,
            tense=tense,
            aspect=aspect,
            obj=obj,
            subject=subject,
            optative=optative,
            imperative=imperative,
            neg_imperative=neg_imperative,
            applicative=applicative,
            causative=causative,
            simple_causative=simple_causative,
            has_markers=has_markers,
            exists_in_ivd=exists_in_ivd,
            exists_in_tve=exists_in_tve,
            exists_in_tvm=exists_in_tvm,
            exists_in_tvm_tve=exists_in_tvm_tve,
            selected=selected,
        )
    )


def conjugate_verb(
    *,
    tense_modules: Dict[str, Any],
    infinitive: str,
    tense: Optional[str] = None,
    aspect: Optional[str] = None,
    obj: Optional[str] = None,
    subject: str = "all",
    optative: bool = False,
    imperative: bool = False,
    neg_imperative: bool = False,
    applicative: bool = False,
    causative: bool = False,
    simple_causative: bool = False,
) -> Dict[str, Any]:
    """
    Pure function: takes explicit params, returns JSON-able dict.
    Returns:
      {"result": <conjugations or {"error": "..."}>, "meta": {...}}
    """

    infinitive_n = (infinitive or "").strip().lower()
    tense_n = tense or None
    aspect_n = aspect or None

    # normalize obj
    if obj in ("", "None"):
        obj = None

    has_markers = any([applicative, causative, simple_causative])

    # conflicting marker rule
    if causative and simple_causative:
        return {
            "result": {"error": "Select only one causative type at a time."},
            "meta": _meta(
                infinitive=infinitive_n, tense=tense_n, aspect=aspect_n, obj=obj,
                subject=subject, optative=optative, imperative=imperative, neg_imperative=neg_imperative,
                applicative=applicative, causative=causative, simple_causative=simple_causative,
                has_markers=True,
                exists_in_ivd=False, exists_in_tve=False, exists_in_tvm=False, exists_in_tvm_tve=False,
                selected={"reason": "conflicting_causatives"},
            ),
        }

    if not infinitive_n:
        return {
            "result": {"error": "Infinitive is required"},
            "meta": _meta(
                infinitive=infinitive_n, tense=tense_n, aspect=aspect_n, obj=obj,
                subject=subject, optative=optative, imperative=imperative, neg_imperative=neg_imperative,
                applicative=applicative, causative=causative, simple_causative=simple_causative,
                has_markers=has_markers,
                exists_in_ivd=False, exists_in_tve=False, exists_in_tvm=False, exists_in_tvm_tve=False,
                selected={"reason": "missing_infinitive"},
            ),
        }

    # special-case: "guri mentxu"
    if infinitive_n == "guri mentxu" and aspect_n != "potential":
        return {
            "result": {"error": "This verb only exists in potential form. You need to select the potential form under 'Aspect'"},
            "meta": _meta(
                infinitive=infinitive_n, tense=tense_n, aspect=aspect_n, obj=obj,
                subject=subject, optative=optative, imperative=imperative, neg_imperative=neg_imperative,
                applicative=applicative, causative=causative, simple_causative=simple_causative,
                has_markers=has_markers,
                exists_in_ivd=False, exists_in_tve=False, exists_in_tvm=False, exists_in_tvm_tve=False,
                selected={"reason": "guri_mentxu_requires_potential"},
            ),
        }

    # existence flags
    exists_in_ivd, exists_in_tve, exists_in_tvm, exists_in_tvm_tve = check_verb_existence(infinitive_n, tense_modules)

    # requires marker verbs
    if infinitive_n in SPECIAL_REQUIRES_MARKER and aspect_n is None and not has_markers:
        return {
            "result": {"error": "This verb requires a marker (applicative, causative or double causative)/bu fiile uygulamalı, oldurgan veya ettirgen belirteci gerekiyor."},
            "meta": _meta(
                infinitive=infinitive_n, tense=tense_n, aspect=aspect_n, obj=obj,
                subject=subject, optative=optative, imperative=imperative, neg_imperative=neg_imperative,
                applicative=applicative, causative=causative, simple_causative=simple_causative,
                has_markers=has_markers,
                exists_in_ivd=exists_in_ivd, exists_in_tve=exists_in_tve, exists_in_tvm=exists_in_tvm, exists_in_tvm_tve=exists_in_tvm_tve,
                selected={"reason": "marker_required"},
            ),
        }

    # TVE marker requires object
    if exists_in_tve and has_markers and not obj:
        err = (
            "Applicative requires an object to be specified. / Uygulamalı belirteç bir nesnenin belirtilmesini gerektirir."
            if applicative
            else "Causative requires an object to be specified. / Ettirgen belirteç bir nesnenin belirtilmesini gerektirir"
        )
        return {
            "result": {"error": err},
            "meta": _meta(
                infinitive=infinitive_n, tense=tense_n, aspect=aspect_n, obj=obj,
                subject=subject, optative=optative, imperative=imperative, neg_imperative=neg_imperative,
                applicative=applicative, causative=causative, simple_causative=simple_causative,
                has_markers=has_markers,
                exists_in_ivd=exists_in_ivd, exists_in_tve=exists_in_tve, exists_in_tvm=exists_in_tvm, exists_in_tvm_tve=exists_in_tvm_tve,
                selected={"reason": "marker_requires_obj"},
            ),
        }

    # ---- Aspect path (potential / passive) ----
    aspect_error = None
    if aspect_n and aspect_n in SIMPLIFIED_ASPECT_MAPPING and exists_in_tvm_tve:
        aspect_validator = ConjugationValidator(tense_modules, {}, SIMPLIFIED_ASPECT_MAPPING)
        aspect_service = ConjugationService(tense_modules, {}, SIMPLIFIED_ASPECT_MAPPING)

        req = _request_params(
            infinitive=infinitive_n, tense=tense_n, aspect=aspect_n, obj=obj,
            subject=subject, optative=optative, imperative=imperative, neg_imperative=neg_imperative,
            applicative=applicative, causative=causative, simple_causative=simple_causative,
        )
        params, aspect_error = aspect_validator.validate_request(req)
        if not aspect_error:
            out = aspect_service.conjugate(params)
            if out:
                return {
                    "result": out,
                    "meta": _meta(
                        infinitive=infinitive_n, tense=tense_n, aspect=aspect_n, obj=obj,
                        subject=subject, optative=optative, imperative=imperative, neg_imperative=neg_imperative,
                        applicative=applicative, causative=causative, simple_causative=simple_causative,
                        has_markers=has_markers,
                        exists_in_ivd=exists_in_ivd, exists_in_tve=exists_in_tve, exists_in_tvm=exists_in_tvm, exists_in_tvm_tve=exists_in_tvm_tve,
                        selected={
                            "path": "aspect",
                            "aspect_module": SIMPLIFIED_ASPECT_MAPPING[aspect_n],
                        },
                    ),
                }

    # marker restriction: IVD-only verbs cannot take markers
    if exists_in_ivd and not (exists_in_tve or exists_in_tvm_tve) and has_markers:
        return {
            "result": {"error": "This verb belongs to a verb group that cannot take additional markers"},
            "meta": _meta(
                infinitive=infinitive_n, tense=tense_n, aspect=aspect_n, obj=obj,
                subject=subject, optative=optative, imperative=imperative, neg_imperative=neg_imperative,
                applicative=applicative, causative=causative, simple_causative=simple_causative,
                has_markers=has_markers,
                exists_in_ivd=exists_in_ivd, exists_in_tve=exists_in_tve, exists_in_tvm=exists_in_tvm, exists_in_tvm_tve=exists_in_tvm_tve,
                selected={"reason": "ivd_marker_forbidden"},
            ),
        }

    # ---- Present perfect special handling ----
    presentperf_error = None
    if tense_n == "presentperf":
        validator = ConjugationValidator(tense_modules, {"presentperf": ["tvm_tve_presentperf"]}, {})
        service = ConjugationService(tense_modules, {"presentperf": ["tvm_tve_presentperf"]}, {})

        req = _request_params(
            infinitive=infinitive_n, tense=tense_n, aspect=aspect_n, obj=obj,
            subject=subject, optative=optative, imperative=imperative, neg_imperative=neg_imperative,
            applicative=applicative, causative=causative, simple_causative=simple_causative,
        )
        params, presentperf_error = validator.validate_request(req)
        if not presentperf_error:
            out = service.conjugate(params)
            if out:
                return {
                    "result": out,
                    "meta": _meta(
                        infinitive=infinitive_n, tense=tense_n, aspect=aspect_n, obj=obj,
                        subject=subject, optative=optative, imperative=imperative, neg_imperative=neg_imperative,
                        applicative=applicative, causative=causative, simple_causative=simple_causative,
                        has_markers=has_markers,
                        exists_in_ivd=exists_in_ivd, exists_in_tve=exists_in_tve, exists_in_tvm=exists_in_tvm, exists_in_tvm_tve=exists_in_tvm_tve,
                        selected={
                            "path": "presentperf",
                            "modules": ["tvm_tve_presentperf"],
                        },
                    ),
                }

    # ---- Regular tense path ----
    ivd_mapping: Dict[str, Any] = {}
    tve_mapping: Dict[str, Any] = {}
    tvm_mapping: Dict[str, Any] = {}

    for tense_key, modules in SIMPLIFIED_TENSE_MAPPING.items():
        if not isinstance(modules, list):
            continue

        ivd_modules_for_tense = [m for m in modules if isinstance(m, str) and m.startswith("ivd_")]
        tve_modules_for_tense = [m for m in modules if isinstance(m, str) and m.startswith("tve_")]
        tvm_modules_for_tense = [m for m in modules if isinstance(m, tuple) or (isinstance(m, str) and m.startswith("tvm_"))]

        if ivd_modules_for_tense and exists_in_ivd and not has_markers:
            if tense_key == "past" and infinitive_n in SPECIAL_IVD_PAST_AS_PASTPRO:
                ivd_mapping[tense_key] = ["ivd_pastpro"]
            else:
                ivd_mapping[tense_key] = ivd_modules_for_tense

        if tve_modules_for_tense and exists_in_tve:
            tve_mapping[tense_key] = tve_modules_for_tense

        if tvm_modules_for_tense and exists_in_tvm:
            tvm_mapping[tense_key] = tvm_modules_for_tense

    req = _request_params(
        infinitive=infinitive_n, tense=tense_n, aspect=aspect_n, obj=obj,
        subject=subject, optative=optative, imperative=imperative, neg_imperative=neg_imperative,
        applicative=applicative, causative=causative, simple_causative=simple_causative,
    )

    results: Dict[str, Any] = {}

    ivd_error = None
    tve_error = None
    tvm_error = None

    if exists_in_ivd and not has_markers:
        ivd_validator = ConjugationValidator(tense_modules, ivd_mapping, {})
        ivd_service = ConjugationService(tense_modules, ivd_mapping, {})
        ivd_params, ivd_error = ivd_validator.validate_request(req)
        if not ivd_error:
            ivd_out = ivd_service.conjugate(ivd_params)
            if ivd_out:
                results.update(ivd_out)

    if exists_in_tve:
        tve_validator = ConjugationValidator(tense_modules, tve_mapping, {})
        tve_service = ConjugationService(tense_modules, tve_mapping, {})
        tve_params, tve_error = tve_validator.validate_request(req)
        if not tve_error:
            tve_out = tve_service.conjugate(tve_params)
            if tve_out:
                for region in tve_out:
                    results.setdefault(region, {}).update(tve_out[region])

    if exists_in_tvm:
        tvm_validator = ConjugationValidator(tense_modules, tvm_mapping, {})
        tvm_service = ConjugationService(tense_modules, tvm_mapping, {})
        tvm_params, tvm_error = tvm_validator.validate_request(req)
        if not tvm_error:
            tvm_out = tvm_service.conjugate(tvm_params)
            if tvm_out:
                for region in tvm_out:
                    results.setdefault(region, {}).update(tvm_out[region])

    if results:
        return {
            "result": results,
            "meta": _meta(
                infinitive=infinitive_n, tense=tense_n, aspect=aspect_n, obj=obj,
                subject=subject, optative=optative, imperative=imperative, neg_imperative=neg_imperative,
                applicative=applicative, causative=causative, simple_causative=simple_causative,
                has_markers=has_markers,
                exists_in_ivd=exists_in_ivd, exists_in_tve=exists_in_tve, exists_in_tvm=exists_in_tvm, exists_in_tvm_tve=exists_in_tvm_tve,
                selected={
                    "path": "tense",
                    "ivd_mapping": ivd_mapping,
                    "tve_mapping": tve_mapping,
                    "tvm_mapping": tvm_mapping,
                },
            ),
        }

    # ---- Final: distinguish truly-not-found vs no-output ----
    if not (exists_in_ivd or exists_in_tve or exists_in_tvm or exists_in_tvm_tve):
        return {
            "result": {"error": f"Infinitive {infinitive_n} not found in any module."},
            "meta": _meta(
                infinitive=infinitive_n, tense=tense_n, aspect=aspect_n, obj=obj,
                subject=subject, optative=optative, imperative=imperative, neg_imperative=neg_imperative,
                applicative=applicative, causative=causative, simple_causative=simple_causative,
                has_markers=has_markers,
                exists_in_ivd=exists_in_ivd, exists_in_tve=exists_in_tve, exists_in_tvm=exists_in_tvm, exists_in_tvm_tve=exists_in_tvm_tve,
                selected={"reason": "not_found"},
            ),
        }

    # Verb exists somewhere but nothing came out -> surface validator errors
    return {
        "result": {"error": "Verb exists in module lists, but no conjugation output was produced (likely missing/invalid parameters)."},
        "meta": _meta(
            infinitive=infinitive_n, tense=tense_n, aspect=aspect_n, obj=obj,
            subject=subject, optative=optative, imperative=imperative, neg_imperative=neg_imperative,
            applicative=applicative, causative=causative, simple_causative=simple_causative,
            has_markers=has_markers,
            exists_in_ivd=exists_in_ivd, exists_in_tve=exists_in_tve, exists_in_tvm=exists_in_tvm, exists_in_tvm_tve=exists_in_tvm_tve,
            selected={
                "reason": "no_output",
                "validator_errors": {
                    "aspect_error": aspect_error,
                    "presentperf_error": presentperf_error,
                    "ivd_error": ivd_error,
                    "tve_error": tve_error,
                    "tvm_error": tvm_error,
                },
                "mappings": {
                    "ivd_mapping": ivd_mapping,
                    "tve_mapping": tve_mapping,
                    "tvm_mapping": tvm_mapping,
                },
            },
        ),
    }
