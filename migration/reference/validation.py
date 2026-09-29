"""Supported feature combinations, including restrictions from the old service.

Unsupported means outside the verified reference interface, not a claim that a
construction cannot exist in Laz. See migration/README.md for coverage decisions.
"""

from laz_engine.models import Causative, Derivation, Entry, Features, Mood, Result, Tense, VerbClass

MARKER_REQUIRED = frozenset({"gexvamu", "cexvamu", "otebriǩu", "oteşekkyuru"})
NO_OBJECT = frozenset({"coxons", "cozun", "gyožin"})


def unavailable(code: str, message: str) -> Result:
    return Result(status="unsupported", reason=code, message=message)


def validate(entry: Entry, f: Features) -> Result | None:
    markers = f.applicative or f.causative != Causative.NONE
    if f.dialect not in entry.dialects:
        return unavailable(
            "dialect_unavailable", "This entry has no principal part in this dialect."
        )
    if entry.infinitive == "guri mentxu" and f.derivation != Derivation.POTENTIAL:
        return unavailable("potential_required", "This entry is available in the potential form.")
    if f.mood != Mood.INDICATIVE and f.tense != Tense.PRESENT:
        return unavailable("mood_tense", "Select present as the canonical tense for this mood.")
    if f.mood in (Mood.IMPERATIVE, Mood.NEGATIVE_IMPERATIVE) and f.subject.value[0] != "2":
        return unavailable("imperative_subject", "Imperatives require a second-person subject.")
    if f.derivation != Derivation.NONE:
        if entry.verb_class == VerbClass.DATIVE:
            return unavailable(
                "derivation_class", "The reference has no derivation for this class."
            )
        if f.tense == Tense.PRESENT_PERFECT or f.mood != Mood.INDICATIVE:
            return unavailable(
                "derivation_construction", "This derivation supports indicative simple tenses."
            )
        if f.object is not None or f.applicative:
            return unavailable(
                "derivation_object", "Derived forms use no explicit object or applicative."
            )
        if f.causative != Causative.NONE and not (
            f.derivation == Derivation.PASSIVE and f.causative == Causative.DOUBLE
        ):
            return unavailable(
                "derivation_marker", "This marker is not implemented for this derivation."
            )
        if f.optional_preverb and f.derivation == Derivation.POTENTIAL:
            return unavailable(
                "optional_preverb_unsupported", "The potential rule does not implement this option."
            )
        return None
    if f.tense == Tense.PRESENT_PERFECT:
        if entry.verb_class == VerbClass.DATIVE or markers or f.object is not None:
            return unavailable(
                "perfect_features", "Perfect supports TVE/TVM without objects or markers."
            )
        if f.optional_preverb:
            return unavailable(
                "optional_preverb_unsupported", "The perfect rule does not implement this option."
            )
        return None
    if entry.infinitive in MARKER_REQUIRED and not markers:
        return unavailable(
            "marker_required", "This entry requires an applicative or causative marker."
        )
    if entry.verb_class == VerbClass.NOMINATIVE and (f.object is not None or markers):
        return unavailable(
            "nominative_object", "The reference nominative interface takes no object or markers."
        )
    if entry.verb_class == VerbClass.DATIVE and markers:
        return unavailable(
            "dative_marker", "The reference dative interface takes no additional markers."
        )
    if (
        entry.verb_class == VerbClass.DATIVE
        and f.object is not None
        and f.mood in (Mood.OPTATIVE, Mood.IMPERATIVE)
    ):
        return unavailable(
            "dative_optative_object",
            "Dative optatives and their imperatives take no explicit object.",
        )
    if entry.infinitive in NO_OBJECT and f.object is not None:
        return unavailable("object_forbidden", "This entry cannot take an object.")
    if markers and f.object is None:
        return unavailable(
            "marker_object", "Select an object for an applicative or causative form."
        )
    return None
