"""Explicit construction dispatch into the preserved reference rule bodies."""

from dataclasses import dataclass
from functools import lru_cache
from importlib import import_module

from laz_engine.models import (
    Causative,
    Derivation,
    Dialect,
    EngineFailure,
    Entry,
    Features,
    Form,
    Mood,
    Result,
    Tense,
    VerbClass,
)
from .validation import unavailable, validate

PAST_AS_PROGRESSIVE = frozenset({"uğun", "oçkinu", "uyonun", "uqoun", "unon"})


@dataclass(frozen=True)
class RuleContext:
    verbs: dict
    regions: dict
    co_verbs: tuple[str, ...]
    gyo_verbs: tuple[str, ...]
    no_verbs: tuple[str, ...]


@lru_cache(maxsize=2048)
def context_for(entry: Entry, dialect: Dialect) -> RuleContext:
    parts = tuple(
        (v.form, dialect.legacy) for v in entry.variants if v.form and dialect in v.dialects
    )
    # Match the loader's prefix classification, but keep each entry independent.
    words = [w for v in entry.variants for w in v.form.split()]

    def matching(prefixes):
        return (entry.infinitive,) if any(w.startswith(prefixes) for w in words) else ()

    return RuleContext(
        verbs={entry.infinitive: parts},
        regions={entry.infinitive: (dialect.legacy,)},
        co_verbs=matching(("co", "cu")),
        gyo_verbs=matching(("gyo", "gyu")),
        no_verbs=matching(("no", "nu", "n")),
    )


def select_rule(entry: Entry, f: Features) -> tuple[str, str, dict, str]:
    """Return module, function, construction arguments, and resulting frame."""
    tense = {Tense.PAST_PROGRESSIVE: "pastpro"}.get(f.tense, f.tense.value)
    if f.derivation != Derivation.NONE:
        kind = f.derivation.value
        return (
            f"tvm_tve_{kind}",
            f"conjugate_{kind}_form",
            {"tense": tense},
            "Dative" if f.derivation == Derivation.POTENTIAL else "Nominative",
        )
    if f.tense == Tense.PRESENT_PERFECT:
        return "tvm_tve_presentperf", "conjugate_present_perfect_form", {}, "Dative"
    if entry.verb_class == VerbClass.NOMINATIVE:
        tense = "past progressive" if f.tense == Tense.PAST_PROGRESSIVE else tense
        if f.mood == Mood.OPTATIVE:
            tense = "optative"
        elif f.mood == Mood.IMPERATIVE:
            tense = "past"
        return "tvm_tense", "conjugate_verb", {"tense": tense}, "Nominative"
    prefix = "ivd" if entry.verb_class == VerbClass.DATIVE else "tve"
    extra = {}
    if f.mood == Mood.IMPERATIVE:
        tense = "present" if prefix == "ivd" else "past"
        if prefix == "ivd":
            extra["mood"] = "optative"
    elif f.mood == Mood.OPTATIVE:
        extra["mood"] = "optative"
    elif f.tense == Tense.PAST and prefix == "ivd" and entry.infinitive in PAST_AS_PROGRESSIVE:
        tense = "pastpro"
    function = "conjugate_past_progressive" if tense == "pastpro" else f"conjugate_{tense}"
    return f"{prefix}_{tense}", function, extra, "Dative" if prefix == "ivd" else "Ergative"


@lru_cache(maxsize=12)
def rule_module(name: str):
    return import_module(f"migration.reference.rules.{name}")


def conjugate(entry: Entry, features: Features) -> Result:
    problem = validate(entry, features)
    if problem:
        return problem
    module_name, function_name, construction, frame = select_rule(entry, features)
    module = rule_module(module_name)
    subject = features.subject.legacy("S")
    obj = features.object.legacy("O") if features.object else None
    try:
        raw = getattr(module, function_name)(
            entry.infinitive,
            subject=subject,
            obj=obj,
            applicative=features.applicative,
            causative=features.causative == Causative.DOUBLE,
            simple_causative=features.causative == Causative.SIMPLE,
            use_optional_preverb=features.optional_preverb,
            context=context_for(entry, features.dialect),
            **construction,
        )
        rows = raw.get(features.dialect.legacy, [])
        if features.mood == Mood.NEGATIVE_IMPERATIVE:
            # The service historically prepends TVM negatives to the whole phrase.
            if entry.verb_class == VerbClass.NOMINATIVE:
                prefix = "mo" if features.dialect in (Dialect.HO, Dialect.AS) else "mot"
                rows = [(s, o, f"{prefix} {form}") for s, o, form in rows]
            else:
                rows = module.extract_neg_imperatives({features.dialect.legacy: rows}, [subject])[
                    features.dialect.legacy
                ]
        if not rows:
            raise EngineFailure(f"{module_name} returned no forms for {entry.id}.")
        if all("N/A" in form for _, _, form in rows):
            return unavailable(
                "person_combination", "The reference rejects this subject/object combination."
            )
        pronouns = module.get_personal_pronouns(features.dialect.legacy, module_name)
        forms = set()
        for s, o, spelling in rows:
            if (
                s != subject
                or o != obj
                or not spelling
                or "N/A" in spelling
                or "not found" in spelling
            ):
                raise EngineFailure(
                    f"Unexpected rule output in {module_name}: {(s, o, spelling)!r}"
                )
            forms.add(
                Form(
                    spelling=spelling,
                    frame=frame,
                    subject=features.subject,
                    object=features.object,
                    subject_pronoun=pronouns.get(subject, subject),
                    object_pronoun=pronouns.get(obj, "") if obj else "",
                    rule=module_name,
                )
            )
        return Result("ok", tuple(sorted(forms)))
    except EngineFailure:
        raise
    except Exception as exc:
        raise EngineFailure(f"{entry.id}/{module_name}: {type(exc).__name__}: {exc}") from exc
