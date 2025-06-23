import math
from typing import List, Tuple

from flask import Blueprint, abort, jsonify, request

from .conjugator.builder import ConjugatorBuilder
from .conjugator.common import Aspect, Mood, Person, Region, Tense
from .conjugator.errors import ConjugatorError
from .conjugator.verbs import DativeVerb, ErgativeVerb, NominativeVerb, Verb
from .db import get_db

verbs = Blueprint("verbs", __name__)

REGIONS = {
    "AS": Region.ARDESEN,
    "HO": Region.HOPA,
    "FA": Region.FINDIKLI_ARHAVI,
    "PZ": Region.PAZAR,
}

TENSES = {
    "present": Tense.PRESENT,
    "past": Tense.PAST,
    "future": Tense.FUTURE,
    "present_perfect": Tense.PRESENT_PREFECT,
    "past_progressive": Tense.PAST_PROGRESSIVE,
}

ASPECTS = {"potential": Aspect.POTENTIAL, "passive": Aspect.PASSIVE}

VERB_TYPES = {
    "nominative": NominativeVerb,
    "ergative": ErgativeVerb,
    "dative": DativeVerb,
}

SUBJECTS = {
    "first_singular": [Person.FIRST_SINGULAR],
    "second_singular": [Person.SECOND_SINGULAR],
    "third_singular": [Person.THIRD_SINGULAR],
    "first_plural": [Person.FIRST_PLURAL],
    "second_plural": [Person.SECOND_PLURAL],
    "third_plural": [Person.THIRD_PLURAL],
    "all": Person,
}

OBJECTS = {
    "": None,
    "first_singular": Person.FIRST_SINGULAR,
    "second_singular": Person.SECOND_SINGULAR,
    "third_singular": Person.THIRD_SINGULAR,
    "first_plural": Person.FIRST_PLURAL,
    "second_plural": Person.SECOND_PLURAL,
    "third_plural": Person.THIRD_PLURAL,
}


def _build_verb_with_region(
    region, verb_type, infinitive_form, verb_root
) -> Tuple[Region, Verb]:
    return region, VERB_TYPES[verb_type](
        infinitive=infinitive_form, present_third=verb_root
    )


@verbs.route("/search", methods=["GET"])
def search_verb():
    db = get_db()
    pattern = request.args.get("pattern")
    if pattern is None:
        abort(400)
    cursor = db.cursor()

    sql_pattern = f"%{pattern}%"

    cursor.execute(
        "SELECT DISTINCT infinitive_form FROM verb WHERE infinitive_form LIKE ?",
        (sql_pattern,),
    )
    rows = cursor.fetchall()
    results = [dict(row) for row in rows]
    return jsonify(results)


@verbs.route("/list", methods=["GET"])
def list_verbs():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(DISTINCT infinitive_form) as count FROM verb")
    row = cursor.fetchone()
    count = row[0]

    page = request.args.get("page")
    if page is None:
        start = 0
    else:
        start = (int(page) - 1) * 20

    pattern = request.args.get("pattern")
    if pattern is not None:
        pattern = f"%{pattern}%"
    else:
        pattern = "%%"

    # Pick the next 20 results.
    cursor.execute(
        "SELECT DISTINCT V.verb_id, V.infinitive_form, RV.verb_root, "
        "RV.english_translation, RV.turkish_verb, "
        "LOWER(RV.verb_type) as verb_type FROM verb V, region_verb RV "
        "WHERE "
        "(V.infinitive_form LIKE ? "
        "OR RV.english_translation LIKE ?"
        "OR RV.turkish_verb LIKE ?) "
        "AND V.verb_id = RV.verb_id LIMIT ?, 20",
        (
            pattern,
            pattern,
            pattern,
            start,
        ),
    )
    rows = cursor.fetchall()
    page_count = math.ceil(count / 20)

    return jsonify(
        {
            "count": count,
            "results": [dict(row) for row in rows],
            "page": page,
            "pages": page_count,
        }
    )


@verbs.route("/get/<int:verb_id>/<string:verb_type>")
def get_verb(verb_id, verb_type):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT V.verb_id AS verb_id,
        V.infinitive_form AS infinitive_form,
        R.name as region_name,
        RV.region_code AS region_code,
        RV.verb_type AS verb_type,
        RV.verb_root AS verb_root,
        RV.english_translation AS english_translation,
        RV.turkish_verb As turkish_verb
        FROM
            verb V,
            region_verb RV,
            REGION R
        WHERE
            V.verb_id = ? AND
            LOWER(RV.verb_type) = ? AND
            V.verb_id = RV.verb_id AND
            RV.region_code = R.code
        """,
        (verb_id, verb_type),
    )
    rows = cursor.fetchall()
    if rows:
        results = [dict(row) for row in rows]
        infinitive_form = results[0]["infinitive_form"]
        return jsonify(
            {
                "verb_id": verb_id,
                "infinitive_form": infinitive_form,
                "results": results,
            }
        )
    else:
        abort(400)


@verbs.route("/conjugate", methods=["POST"])
def conjugate():
    verb_id: int = request.json.get("verb_id")
    verb_type: str = request.json.get("verb_type")
    regions: List[str] = request.json.get("regions")
    tense: str = request.json.get("tense")
    aspect: str = request.json.get("aspect")
    subject: str = request.json.get("subject")
    object_: str = request.json.get("object")
    moods: int = request.json.get("moods")

    if (
        verb_id is None
        or verb_type is None
        or tense is None
        or moods is None
        or subject is None
    ):
        abort(400)

    verb_type = verb_type.lower()

    db = get_db()
    cursor = db.cursor()
    region_placeholders = ", ".join("?" for _ in regions)
    cursor.execute(
        f"""
        SELECT
            V.infinitive_form AS infinitive_form,
            RV.verb_root AS verb_root,
            RV.verb_type as verb_type,
            RV.region_code as region_code
        FROM
            verb V, region_verb RV
        WHERE
            RV.region_code IN ({region_placeholders}) AND
            V.verb_id = ? AND
            LOWER(RV.verb_type) = ? AND
            V.verb_id = RV.verb_id
        """,
        (*regions, verb_id, verb_type.lower()),
    )
    rows = cursor.fetchall()
    if not rows:
        abort(404)
    results = [dict(row) for row in rows]

    verbs_and_regions = [
        _build_verb_with_region(
            region=REGIONS[result["region_code"]],
            verb_type=verb_type,
            infinitive_form=result["infinitive_form"],
            verb_root=result["verb_root"],
        )
        for result in results
    ]
    if tense not in TENSES:
        abort(400)
    else:
        tense = TENSES[tense]

    results = dict()

    for region, verb in verbs_and_regions:
        conjugations = list()
        builder = ConjugatorBuilder()
        if aspect is not None:
            builder.set_aspect(ASPECTS[aspect])

        try:
            conjugator = (
                builder.set_tense(tense)
                .set_region(region)
                .set_object(OBJECTS[object_])
                .add_mood(Mood(moods))
                .build()
            )
        except ConjugatorError as e:
            return jsonify({"error": str(e)}), 400
        else:
            for current_subject in SUBJECTS[subject]:
                try:
                    conjugator.update_subject(current_subject)
                except ConjugatorError as e:
                    conjugations.append("N/A")
                else:
                    conjugations.append(conjugator.conjugate(verb))
            results[region.name] = conjugations

    return jsonify({"conjugations": results})
