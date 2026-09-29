"""Finite, documented coverage of the reference engine's supported interface."""

from itertools import product

from .models import Causative, Derivation, Entry, Features, Mood, Person, Tense, VerbClass
from .validation import validate


def iter_features(entry: Entry, profile: str = "full"):
    if profile not in {"core", "full"}:
        raise ValueError("Profile must be core or full")
    tenses = (Tense.PRESENT,) if profile == "core" else tuple(Tense)
    constructions = [(t, Mood.INDICATIVE, Derivation.NONE) for t in tenses]
    if profile == "full":
        constructions += [(Tense.PRESENT, m, Derivation.NONE) for m in Mood if m != Mood.INDICATIVE]
        constructions += [
            (t, Mood.INDICATIVE, d)
            for t, d in product(Tense, Derivation)
            if t != Tense.PRESENT_PERFECT and d != Derivation.NONE
        ]
        constructions.append((Tense.PRESENT, Mood.OPTATIVE, Derivation.POTENTIAL))
    for tense, mood, derivation in constructions:
        subjects = (
            tuple(p for p in Person if p.value[0] == "2")
            if mood in (Mood.IMPERATIVE, Mood.NEGATIVE_IMPERATIVE)
            else tuple(Person)
        )
        ordinary = derivation == Derivation.NONE and tense != Tense.PRESENT_PERFECT
        objects = (
            (None, *Person)
            if profile == "full" and ordinary and entry.verb_class != VerbClass.NOMINATIVE
            else (None,)
        )
        markers = [(False, Causative.NONE)]
        if profile == "full" and ordinary and entry.verb_class == VerbClass.ERGATIVE:
            markers = list(product((False, True), Causative))
        elif profile == "full" and derivation == Derivation.PASSIVE:
            markers.append((False, Causative.DOUBLE))
        optional = (
            (False, True)
            if profile == "full" and (ordinary or derivation == Derivation.PASSIVE)
            else (False,)
        )
        for dialect, subject, obj, (applicative, causative), preverb in product(
            entry.dialects, subjects, objects, markers, optional
        ):
            features = Features(
                dialect, subject, obj, tense, mood, derivation, applicative, causative, preverb
            )
            if validate(entry, features) is None:
                yield features
