import math

from flask import abort, Blueprint, jsonify, request

from .db import get_db

verbs = Blueprint("verbs", __name__)


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
        (sql_pattern,)
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
        pattern = f'%{pattern}%'
    else:
        pattern = '%%'
    
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
        (pattern, pattern, pattern, start,)
    )
    rows = cursor.fetchall()
    page_count = math.ceil(count / 20)
    
    return jsonify({
        "count": count,
        "results": [dict(row) for row in rows],
        "page": page,
        "pages": page_count
    })

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
        (verb_id, verb_type)
    )
    rows = cursor.fetchall()
    if rows:
        results = [dict(row) for row in rows]
        infinitive_form = results[0]["infinitive_form"]
        return jsonify({
            "verb_id": verb_id,
            "infinitive_form": infinitive_form,
            "results": results
        })
    else:
        abort(400)