"""Capture independent fixtures by executing the ORIGINAL modules.

Run with the old environment (pandas is imported by its passive module).
This script never imports laz_engine. Regenerating fixtures is a review action.
"""

import contextlib
import hashlib
import importlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "laz_verb_conjugator"))
SUBJECTS = [f"S{p}_{n}" for n in ("Singular", "Plural") for p in (1, 2, 3)]
ENTRIES = json.loads((ROOT / "packages/engine/src/laz_engine/data/entries.json").read_text())
WORDS = {"osinapu", "oropu", "oskidu", "uğun", "ot̆axu", "avara doskudu", "oç̌ǩomu"}


def capture():
    cases = []
    for entry in ENTRIES:
        if entry["infinitive"] not in WORDS:
            continue
        category = entry["verb_class"]
        scenarios = []
        for tense, legacy_tense, function in (
            ("present", "present", "conjugate_present"),
            ("past", "past", "conjugate_past"),
            ("future", "future", "conjugate_future"),
            ("past_progressive", "pastpro", "conjugate_past_progressive"),
        ):
            if category == "TVM":
                name, function = "tvm_tense", "conjugate_verb"
                extra = {"tense": "past progressive" if legacy_tense == "pastpro" else legacy_tense}
            else:
                if category == "IVD" and tense == "past" and entry["infinitive"] == "uğun":
                    legacy_tense, function = "pastpro", "conjugate_past_progressive"
                name, extra = f"{category.lower()}_{legacy_tense}", {}
            scenarios.append((name, function, extra, tense, "indicative", "none"))
        for mood in ("optative", "imperative", "negative_imperative"):
            if category == "TVM":
                name, fn = "tvm_tense", "conjugate_verb"
                extra = {
                    "tense": {
                        "optative": "optative",
                        "imperative": "past",
                        "negative_imperative": "present",
                    }[mood]
                }
            else:
                past = category == "TVE" and mood == "imperative"
                name, fn = (
                    f"{category.lower()}_{'past' if past else 'present'}",
                    f"conjugate_{'past' if past else 'present'}",
                )
                extra = (
                    {"mood": "optative"}
                    if mood == "optative" or (category == "IVD" and mood == "imperative")
                    else {}
                )
            scenarios.append((name, fn, extra, "present", mood, "none"))
        if category != "IVD":
            scenarios.append(
                (
                    "tvm_tve_presentperf",
                    "conjugate_present_perfect_form",
                    {},
                    "present_perfect",
                    "indicative",
                    "none",
                )
            )
            for derivation in ("potential", "passive"):
                for tense in ("present", "past", "future", "past_progressive"):
                    scenarios.append(
                        (
                            f"tvm_tve_{derivation}",
                            f"conjugate_{derivation}_form",
                            {"tense": "pastpro" if tense == "past_progressive" else tense},
                            tense,
                            "indicative",
                            derivation,
                        )
                    )
        for module_name, function_name, extra, tense, mood, derivation in scenarios:
            module = importlib.import_module(f"backend.notebooks.{module_name}")
            variants = [(None, False, "none", False)]
            ordinary = derivation == "none" and tense != "present_perfect"
            if ordinary:
                variants.append((None, False, "none", True))
            if category == "TVE" and ordinary:
                variants.extend(
                    ("O3_Singular", app, cause, False)
                    for app in (False, True)
                    for cause in ("none", "simple", "double")
                )
            elif category == "IVD" and mood == "indicative":
                variants.append(("O3_Singular", False, "none", False))
            if derivation == "passive":
                variants.append((None, False, "double", True))
            for subject in SUBJECTS:
                if "imperative" in mood and not subject.startswith("S2"):
                    continue
                for obj, applicative, causative, optional in variants:
                    kwargs = {
                        "subject": subject,
                        "obj": obj,
                        "applicative": applicative,
                        "causative": causative == "double",
                        "simple_causative": causative == "simple",
                        "use_optional_preverb": optional,
                        **extra,
                    }
                    with contextlib.redirect_stdout(io.StringIO()):
                        raw = getattr(module, function_name)(entry["infinitive"], **kwargs)
                    if mood == "negative_imperative":
                        if category == "TVM":
                            raw = {
                                region: [
                                    (s, o, f"{'mo' if region in ('HO', 'AŞ') else 'mot'} {form}")
                                    for s, o, form in rows
                                ]
                                for region, rows in raw.items()
                            }
                        else:
                            raw = module.extract_neg_imperatives(raw, [subject])
                    for dialect, forms in raw.items():
                        features = {
                            "dialect": "AS" if dialect == "AŞ" else dialect,
                            "subject": subject[1] + ("sg" if "Singular" in subject else "pl"),
                            "object": obj[1] + ("sg" if "Singular" in obj else "pl")
                            if obj
                            else None,
                            "tense": tense,
                            "mood": mood,
                            "derivation": derivation,
                            "applicative": applicative,
                            "causative": causative,
                            "optional_preverb": optional,
                        }
                        cases.append(
                            {
                                "entry_id": entry["id"],
                                "features": features,
                                "expected": sorted({form for _, _, form in forms}),
                                "module": module_name,
                            }
                        )
    path = ROOT / "tests/fixtures/reference.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    original = ROOT / "laz_verb_conjugator/backend/data/verb_data.json"
    path.write_text(
        json.dumps(
            {
                "source": "original modules at 0b3c9cd",
                "lexicon_sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
                "cases": cases,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    print(
        f"Captured {len(cases)} original-engine cases across {len({c['module'] for c in cases})} modules."
    )


if __name__ == "__main__":
    capture()
