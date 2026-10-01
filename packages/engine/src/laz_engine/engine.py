"""Pure conjugation: validate, select a paradigm, and return explicit form variants."""

from dataclasses import replace
from functools import lru_cache
from importlib import import_module

from .models import (
    Causative,
    Derivation,
    Dialect,
    EngineFailure,
    Entry,
    Features,
    Form,
    Mood,
    OptionalPrefix,
    Result,
    Tense,
    VerbClass,
)
from .paradigms.state import RuleRequest
from .rules.optional_prefixes import attach
from .rules.phonology import get_first_word, process_compound_verb
from .rules.pronouns import get_personal_pronouns
from .validation import unavailable, validate, validate_base

PAST_AS_PROGRESSIVE = frozenset({"uğun", "oçkinu", "uyonun", "uqoun", "unon"})
PARADIGMS = {
    "ivd_present": "dative_present",
    "ivd_past": "dative_past",
    "ivd_future": "dative_future",
    "ivd_pastpro": "dative_progressive",
    "tve_present": "ergative_present",
    "tve_past": "ergative_past",
    "tve_future": "ergative_future",
    "tve_pastpro": "ergative_progressive",
    "tvm_tense": "nominative",
    "tvm_tve_potential": "potential",
    "tvm_tve_passive": "passive",
    "tvm_tve_presentperf": "perfect",
}


def select_rule(entry: Entry, f: Features) -> tuple[str, str, str | None, str]:
    """Return provenance code, underlying tense/mood, and resulting case frame."""
    tense = {Tense.PAST_PROGRESSIVE: "pastpro"}.get(f.tense, f.tense.value)
    mood = "optative" if f.mood == Mood.OPTATIVE else None
    if f.derivation != Derivation.NONE:
        if f.mood == Mood.OPTATIVE:
            tense = "optative"
        return (
            f"tvm_tve_{f.derivation.value}",
            tense,
            mood,
            "Dative" if f.derivation == Derivation.POTENTIAL else "Nominative",
        )
    if f.tense == Tense.PRESENT_PERFECT:
        return "tvm_tve_presentperf", tense, mood, "Dative"
    if entry.verb_class == VerbClass.NOMINATIVE:
        tense = "past progressive" if f.tense == Tense.PAST_PROGRESSIVE else tense
        if f.mood == Mood.OPTATIVE:
            tense = "optative"
        elif f.mood == Mood.IMPERATIVE:
            tense = "past"
        return "tvm_tense", tense, mood, "Nominative"
    prefix = "ivd" if entry.verb_class == VerbClass.DATIVE else "tve"
    if f.mood == Mood.IMPERATIVE:
        tense = "present" if prefix == "ivd" else "past"
        if prefix == "ivd":
            mood = "optative"
    elif f.tense == Tense.PAST and prefix == "ivd" and entry.infinitive in PAST_AS_PROGRESSIVE:
        tense = "pastpro"
    return f"{prefix}_{tense}", tense, mood, "Dative" if prefix == "ivd" else "Ergative"


@lru_cache(maxsize=12)
def rule_module(code: str):
    return import_module(f"laz_engine.paradigms.{PARADIGMS[code]}")


@lru_cache(maxsize=512)
def lexical_groups(entry: Entry) -> tuple[tuple[str, ...], ...]:
    """Classify all principal parts without mixing same-spelling lexical entries."""
    words = [word for part in entry.variants for word in part.form.split()]
    return tuple(
        (entry.infinitive,) if any(w.startswith(prefixes) for w in words) else ()
        for prefixes in (("co", "cu"), ("gyo", "gyu"), ("no", "nu", "n"))
    )


def negative_imperative(spelling: str, entry: Entry, dialect: Dialect) -> str:
    prefix = "mo" if dialect in (Dialect.HO, Dialect.AS) else "mot"
    if entry.verb_class == VerbClass.NOMINATIVE:
        return f"{prefix} {spelling}"
    words = spelling.split()
    return " ".join([*words[:-1], prefix, words[-1]])


def conjugate(entry: Entry, features: Features) -> Result:
    problem = validate(entry, features)
    if problem:
        return problem
    return conjugate_regular(entry, features)


def conjugate_regular(entry: Entry, features: Features) -> Result:
    """General rules only; used to audit whether an exception is still needed."""
    if features.optional_prefix != OptionalPrefix.NONE:
        base = conjugate_regular(entry, replace(features, optional_prefix=OptionalPrefix.NONE))
        return replace(
            base,
            forms=tuple(
                sorted(
                    replace(form, spelling=attach(form.spelling, features.optional_prefix))
                    for form in base.forms
                )
            ),
        )
    problem = validate_base(entry, features)
    if problem:
        return problem
    code, tense, mood, frame = select_rule(entry, features)
    co, gyo, no = lexical_groups(entry)
    request = RuleRequest(
        infinitive=entry.infinitive,
        main_infinitive=process_compound_verb(entry.infinitive),
        first_word_infinitive=get_first_word(entry.infinitive),
        region=features.dialect.legacy,
        subject=features.subject.legacy("S"),
        obj=features.object.legacy("O") if features.object else None,
        tense=tense,
        mood=mood,
        applicative=features.applicative,
        causative=features.causative == Causative.DOUBLE,
        simple_causative=features.causative == Causative.SIMPLE,
        use_optional_preverb=features.optional_preverb,
        co_verbs=co,
        gyo_verbs=gyo,
        no_verbs=no,
    )
    # Derived constructions start from the infinitive; base classes use principal parts.
    parts = (
        (entry.infinitive,)
        if features.derivation != Derivation.NONE or features.tense == Tense.PRESENT_PERFECT
        else tuple(p.form for p in entry.variants if p.form and features.dialect in p.dialects)
    )
    try:
        rule = rule_module(code).conjugate
        spellings = {rule(request, part) for part in parts}
        if spellings and all("N/A" in spelling for spelling in spellings):
            return unavailable(
                "person_combination", "The reference rejects this subject/object combination."
            )
        if not spellings or any(not s or "N/A" in s or "not found" in s for s in spellings):
            raise EngineFailure(f"Unexpected output in {code}: {spellings!r}")
        pronouns = get_personal_pronouns(request.region, code)
        forms = tuple(
            sorted(
                Form(
                    spelling=negative_imperative(s, entry, features.dialect)
                    if features.mood == Mood.NEGATIVE_IMPERATIVE
                    else s,
                    frame=frame,
                    subject=features.subject,
                    object=features.object,
                    subject_pronoun=pronouns[request.subject],
                    object_pronoun=pronouns[request.obj] if request.obj else "",
                    rule=code,
                )
                for s in spellings
            )
        )
        return Result("ok", forms)
    except EngineFailure:
        raise
    except Exception as exc:
        raise EngineFailure(f"{entry.id}/{code}: {type(exc).__name__}: {exc}") from exc
