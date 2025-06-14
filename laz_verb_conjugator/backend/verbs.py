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
        "SELECT DISTINCT V.infinitive_form, RV.verb_root, "
        "RV.english_translation, RV.turkish_verb FROM verb V, region_verb RV "
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