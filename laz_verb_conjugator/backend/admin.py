from flask import abort, Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from .db import get_db

from typing import List

admin = Blueprint("admin", __name__)

VALID_REGIONS = {"FA", "AS", "HO", "PZ"}


@admin.route("/auth", methods=["POST"])
def auth():
    """Authenticate the user."""
    username = request.json.get("username")
    password = request.json.get("password")

    if username is None or password is None:
        abort(400)

    if username == "admin" and password == "password":
        # Okay.
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token})
    else:
        abort(401)  # Not okay.


@admin.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@admin.route("/me")
@jwt_required()
def me():
    """A simple, protected route to detect whether we are authenticated."""
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@admin.route("/add-verb", methods=["POST"])
@jwt_required()
def add_verb():
    verb_infinitive: str = request.json.get("verb_infinitive")
    regions: List[str] = request.json.get("regions")
    verb_type: str = request.json.get("verb_type")
    third_person_form: str = request.json.get("third_person_form")
    turkish_infinitive: str = request.json.get("turkish_infinitive")
    english_translation: str = request.json.get("english_translation")

    if (
        verb_infinitive is None
        or regions is None
        or verb_type is None
        or third_person_form is None
        or turkish_infinitive is None
        or english_translation is None
    ):
        abort(400)
    db = get_db()
    cursor = db.cursor()
    region_placeholders = ", ".join("?" for _ in regions)

    # First: does the infinitive exist?
    cursor.execute(
        "SELECT verb_id FROM verb WHERE infinitive_form = ?",
        (verb_infinitive,),
    )
    row = cursor.fetchone()
    if row is None:
        # The infinitive does not exist. Insert it and get its ID.
        cursor.execute(
            "INSERT INTO verb(infinitive_form) VALUES(?)", (verb_infinitive,)
        )
        verb_id = cursor.lastrowid
    else:
        verb_id = row[0]

    # verb_id is defined.
    cursor.execute(
        f"""
        SELECT V.infinitive_form, RV.region_code
        FROM
            verb V,
            region_verb RV
        WHERE
            V.verb_id = ? AND
            V.infinitive_form = ? AND
            RV.region_code IN ({region_placeholders}) AND
            V.verb_id = RV.verb_id
        """,
        (verb_id, verb_infinitive, *regions),
    )
    rows = cursor.fetchall()
    # Should be no row.
    if rows:
        # Fetch the existing regions for the error message.
        db.close()
        abort(400)

    # Otherwise, no region set for the infinitive. Insert the rows!
    for region in regions:
        if region not in VALID_REGIONS:
            db.close()
            abort(400)

        # Insert.
        cursor.execute(
            """
            INSERT INTO region_verb(
                region_code,
                verb_id,
                verb_type,
                verb_root,
                english_translation,
                turkish_verb
            ) VALUES(?, ?, ?, ?, ?, ?)
            """,
            (
                region,
                verb_id,
                verb_type.upper(),
                third_person_form,
                english_translation,
                turkish_infinitive,
            ),
        )
    db.commit()
    db.close()
    return jsonify({"verb_id": verb_id})
