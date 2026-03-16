import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set.")

engine = create_engine(DATABASE_URL, future=True)


def get_verb_id(infinitive: str, dialect_id: int) -> int | None:
    sql = text("""
        SELECT verb_id
        FROM verb
        WHERE infinitive = :infinitive
          AND dialect_id = :dialect_id
    """)
    with engine.connect() as conn:
        row = conn.execute(sql, {
            "infinitive": infinitive,
            "dialect_id": dialect_id
        }).fetchone()
    return row[0] if row else None


def get_conjugation_rows(
    verb_id: int,
    tense: str,
    frame: str,
    mood: str,
    derivation: str,
    is_applicative: bool,
    is_causative: bool,
    is_double_causative: bool,
    subject_filter: str = "all",
    object_filter: str = "",
):
    conditions = [
        "vf.verb_id = :verb_id",
        "vf.tense = :tense",
        "vf.frame = :frame",
        "vf.mood = :mood",
        "vf.derivation = :derivation",
        "vf.is_applicative = :is_applicative",
        "vf.is_causative = :is_causative",
        "vf.is_double_causative = :is_double_causative",
    ]

    params = {
        "verb_id": verb_id,
        "tense": tense,
        "frame": frame,
        "mood": mood,
        "derivation": derivation,
        "is_applicative": is_applicative,
        "is_causative": is_causative,
        "is_double_causative": is_double_causative,
    }

    if subject_filter and subject_filter != "all":
        conditions.append("vf.subject = CAST(:subject_filter AS person)")
        params["subject_filter"] = subject_filter

    if object_filter == "":
        conditions.append("(vf.object IS NULL OR vf.object = 'O3SG')")
    elif object_filter and object_filter != "all":
        conditions.append("vf.object = CAST(:object_filter AS person)")
        params["object_filter"] = object_filter
    # if object_filter == "all": no object filter

    sql = text(f"""
        SELECT
            COALESCE(ps.form, vf.subject::text) AS subject,
            COALESCE(po.form, vf.object::text) AS object,
            vf.subject AS subject_code,
            vf.object AS object_code,
            vf.spelling,
            vf.frame,
            vf.optional_prefix
        FROM verb_form vf
        JOIN verb v
          ON vf.verb_id = v.verb_id
        LEFT JOIN pronoun ps
          ON ps.dialect_id = v.dialect_id
         AND ps.code = vf.subject
         AND ps.frame = vf.frame
        LEFT JOIN pronoun po
          ON po.dialect_id = v.dialect_id
         AND po.code = vf.object
         AND po.frame = vf.frame
        WHERE {" AND ".join(conditions)}
        ORDER BY vf.subject, vf.object
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql, params).mappings().all()

    return [dict(row) for row in rows]


def reverse_lookup(spelling: str):
    sql = text("""
        SELECT
            vf.spelling AS conjugated_form,
            v.infinitive,
            d.laz_name AS dialect,
            v.meaning_english,
            v.meaning_turkish,
            vf.tense,
            vf.mood,
            vf.frame,
            COALESCE(ps.form, vf.subject::text) AS subject,
            COALESCE(po.form, vf.object::text) AS object,
            vf.subject AS subject_code,
            vf.object AS object_code,
            vf.derivation,
            vf.is_applicative,
            vf.is_causative,
            vf.is_double_causative,
            vf.optional_prefix
        FROM verb_form vf
        JOIN verb v
          ON vf.verb_id = v.verb_id
        JOIN dialect d
          ON v.dialect_id = d.dialect_id
        LEFT JOIN pronoun ps
          ON ps.dialect_id = v.dialect_id
         AND ps.code = vf.subject
         AND ps.frame = vf.frame
        LEFT JOIN pronoun po
          ON po.dialect_id = v.dialect_id
         AND po.code = vf.object
         AND po.frame = vf.frame
        WHERE LOWER(vf.spelling) = LOWER(:spelling)
        ORDER BY d.dialect_id, v.infinitive
    """)
    with engine.connect() as conn:
        rows = conn.execute(sql, {
            "spelling": spelling
        }).mappings().all()
    return [dict(row) for row in rows]

def reverse_suggestions(query: str, limit: int = 8):
    sql = text("""
        SELECT DISTINCT
            vf.spelling
        FROM verb_form vf
        WHERE LOWER(vf.spelling) LIKE LOWER(:query)
        ORDER BY vf.spelling
        LIMIT :limit
    """)
    with engine.connect() as conn:
        rows = conn.execute(sql, {
            "query": f"{query}%",
            "limit": limit
        }).mappings().all()
    return [dict(row) for row in rows]