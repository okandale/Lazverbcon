import ast
import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path

import pytest
from laz_engine.engine import conjugate
from laz_engine.lexicon import entries_by_id, load_entries
from laz_engine.models import Causative, Derivation, Dialect, Features, Mood, Person, Tense

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "tests/fixtures/reference.json").read_text())


def features_from_dict(data):
    return Features(
        **{
            **data,
            "dialect": Dialect(data["dialect"]),
            "subject": Person(data["subject"]),
            "object": Person(data["object"]) if data["object"] else None,
            "tense": Tense(data["tense"]),
            "mood": Mood(data["mood"]),
            "derivation": Derivation(data["derivation"]),
            "causative": Causative(data["causative"]),
        }
    )


@pytest.mark.parametrize("case", FIXTURE["cases"])
def test_matches_original_forms(case):
    result = conjugate(entries_by_id()[case["entry_id"]], features_from_dict(case["features"]))
    expected = case["expected"]
    if expected and all("N/A" in form for form in expected):
        assert result.status == "unsupported"
    else:
        assert result.status == "ok", result
        assert sorted(f.spelling for f in result.forms) == expected


def test_source_entries_and_unpaired_variant_preserved(verb):
    assert len(load_entries()) == 327
    duplicates = [e for e in load_entries() if e.infinitive == "oǩiru"]
    assert len(duplicates) > 1
    assert len({e.id for e in duplicates}) == len(duplicates)
    entry = verb("osinapu")
    assert any(v.form == "isinapay" and not v.dialects for v in entry.variants)
    assert entry.issues


def test_subject_object_codes_survive_pronoun_ambiguity(verb):
    f = Features(Dialect.HO, Person.FIRST_PLURAL, Person.THIRD_SINGULAR)
    result = conjugate(verb("uğun", "IVD"), f)
    assert result.status == "ok"
    assert all(form.subject == f.subject and form.object == f.object for form in result.forms)


def test_invalid_and_unimplemented_are_not_forms(verb):
    entry = verb("osinapu")
    result = conjugate(entry, Features(Dialect.AS, Person.FIRST_SINGULAR, Person.FIRST_SINGULAR))
    assert result.status == "unsupported" and not result.forms
    result = conjugate(entry, Features(Dialect.AS, Person.FIRST_SINGULAR, mood=Mood.IMPERATIVE))
    assert result.reason == "imperative_subject"
    result = conjugate(
        verb("oropu", "IVD"),
        Features(Dialect.AS, Person.SECOND_SINGULAR, Person.THIRD_SINGULAR, mood=Mood.IMPERATIVE),
    )
    assert result.reason == "dative_optative_object"


def test_concurrent_calls_do_not_change_each_others_lexicon(verb):
    entries = [verb("oropu"), verb("osinapu"), verb("oropu", "IVD"), verb("oskidu", "TVM")]
    f = Features(Dialect.AS, Person.FIRST_SINGULAR)
    expected = [conjugate(e, f) for e in entries]
    with ThreadPoolExecutor(8) as pool:
        actual = list(pool.map(lambda e: conjugate(e, f), entries * 20))
    assert actual == expected * 20


def test_past_substitution_and_distinct_imperatives(verb):
    f = Features(Dialect.AS, Person.SECOND_SINGULAR, mood=Mood.IMPERATIVE)
    assert conjugate(verb("oropu", "IVD"), f).forms[0].rule == "ivd_present"
    assert conjugate(verb("oropu"), replace(f, dialect=Dialect.FA)).forms[0].rule == "tve_past"
    f = replace(f, mood=Mood.INDICATIVE, tense=Tense.PAST)
    assert conjugate(verb("uğun", "IVD"), f).forms[0].rule == "ivd_pastpro"


class StripPrints(ast.NodeTransformer):
    def visit_Expr(self, node):
        if (
            isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "print"
        ):
            return None
        return self.generic_visit(node)


def test_extracted_rule_bodies_are_unchanged():
    """Independent AST check: no accidental linguistic edits during extraction."""
    for original in (ROOT / "laz_verb_conjugator/backend/notebooks").glob("*.py"):
        if original.name == "__init__.py":
            continue
        source = {
            n.name: n
            for n in ast.parse(original.read_text()).body
            if isinstance(n, ast.FunctionDef)
        }
        extracted = ast.parse((ROOT / "migration/reference/rules" / original.name).read_text())
        for fn in (n for n in extracted.body if isinstance(n, ast.FunctionDef)):
            old = StripPrints().visit(source[fn.name])
            if fn.name.startswith("conjugate_"):
                fn.args.kwonlyargs = []
                fn.args.kw_defaults = []
                while (
                    fn.body
                    and isinstance(fn.body[0], ast.Assign)
                    and isinstance(fn.body[0].value, ast.Attribute)
                    and isinstance(fn.body[0].value.value, ast.Name)
                    and fn.body[0].value.value.id == "context"
                ):
                    fn.body.pop(0)
            assert ast.dump(fn) == ast.dump(old), f"Rule body changed: {original.name}/{fn.name}"
