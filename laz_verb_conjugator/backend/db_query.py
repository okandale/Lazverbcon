import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set.")

engine = create_engine(DATABASE_URL, future=True)


# Order matters:
# - longer/multi-character patterns first
# - more specific apostrophe forms before shorter forms
NORMALIZATION_RULES = [
    # multi-character elder/alternative spellings
    ("3'", "ǯ"),
    ("ts", "ʒ"),
    ("tz", "ǯ"),
    ("dz", "ž"),
    ("z'", "ž"),
    ("k'", "ǩ"),
    ("p'", "p̌"),
    ("t'", "t̆"),
    ("ç'", "ç̌"),

    # optional direct canonicalizations
    ("t̆", "t̆"),
    ("p̌", "p̌"),
    ("ǩ", "ǩ"),
    ("ʒ", "ʒ"),
    ("ǯ", "ǯ"),
    ("ž", "ž"),
    ("ç̌", "ç̌"),

    # single-character substitutions
    ("h", "x"),
    ("ğ", "x"),
    ("c", "ʒ"),
    ("3", "ʒ"),
    ("ç", "ç̌"),
    ("z", "ž"),
]


def _normalize_reverse_input(text: str) -> str:
    if not text:
        return ""

    t = text.strip().lower()

    for src, target in NORMALIZATION_RULES:
        t = t.replace(src, target)

    return t


def _dedupe_reverse_rows(rows):
    seen = set()
    deduped = []

    for row in rows:
        key = (
            row.get("conjugated_form"),
            row.get("infinitive"),
            row.get("dialect"),
            row.get("tense"),
            row.get("mood"),
            row.get("frame"),
            row.get("subject_code"),
            row.get("object_code"),
            row.get("derivation"),
            bool(row.get("is_applicative")),
            bool(row.get("is_causative")),
            bool(row.get("is_double_causative")),
            row.get("optional_prefix"),
        )

        if key in seen:
            continue

        seen.add(key)
        deduped.append(row)

    return deduped


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
        "vf.optional_prefix IS NULL",
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

def _candidate_prefixes_for_query(query: str):
    if not query:
        return ["%"]

    q = query.strip().lower()

    # Check multi-character starts first
    if q.startswith("k'") or q.startswith("ǩ"):
        return ["k%", "ǩ%"]

    if q.startswith("p'") or q.startswith("p̌"):
        return ["p%", "p̌%"]

    if q.startswith("t'") or q.startswith("t̆"):
        return ["t%", "t̆%"]

    if q.startswith("ts") or q.startswith("c") or q.startswith("3") or q.startswith("ʒ"):
        return ["ts%", "c%", "3%", "ʒ%"]

    if q.startswith("tz") or q.startswith("3'") or q.startswith("ǯ"):
        return ["tz%", "3'%", "ǯ%"]

    if q.startswith("dz") or q.startswith("z") or q.startswith("z'") or q.startswith("ž"):
        return ["dz%", "z%", "z'%", "ž%"]

    if q.startswith("ç'") or q.startswith("ç̌"):
        return ["ç'%", "ç̌%"]

    first = q[:1]

    groups = {
        "x": ["x", "h", "ğ"],
        "h": ["x", "h", "ğ"],
        "ğ": ["x", "h", "ğ"],
        "k": ["k", "ǩ"],
        "ǩ": ["k", "ǩ"],
        "p": ["p", "p̌"],
        "p̌": ["p", "p̌"],
        "t": ["t", "t̆"],
        "t̆": ["t", "t̆"],
        "c": ["c", "ʒ", "3"],
        "3": ["c", "ʒ", "3"],
        "ʒ": ["c", "ʒ", "3"],
        "z": ["z", "ž"],
        "ž": ["z", "ž"],
    }

    return [f"{ch}%" for ch in groups.get(first, [first])]

def reverse_lookup(spelling: str):
    spelling = (spelling or "").strip()
    normalized_spelling = _normalize_reverse_input(spelling)

    exact_sql = text("""
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

    # Fetch candidate pool for Python-side normalized matching.
    # Starting conservative: candidates with same first letter OR first normalized letter.
    prefixes = _candidate_prefixes_for_query(spelling)

    candidate_conditions = []
    candidate_params = {}

    for i, prefix in enumerate(prefixes):
        key = f"prefix{i}"
        candidate_conditions.append(f"LOWER(vf.spelling) LIKE LOWER(:{key})")
        candidate_params[key] = prefix

    candidate_sql = text(f"""
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
        WHERE {" OR ".join(candidate_conditions)}
        ORDER BY d.dialect_id, v.infinitive
    """)

    with engine.connect() as conn:
        exact_rows = conn.execute(
            exact_sql,
            {"spelling": spelling}
        ).mappings().all()

        if exact_rows:
            results = [dict(row) for row in exact_rows]
            for row in results:
                row["match_type"] = "exact"
                row["matched_query"] = spelling
                row["normalized_query"] = normalized_spelling
            return results

        # Use first raw character as a first-pass filter.
        # If you notice missed matches, widen this later.
        candidate_rows = conn.execute(
            candidate_sql,
            candidate_params
        ).mappings().all()

    normalized_matches = []

    for row in candidate_rows:
        row_dict = dict(row)
        candidate_spelling = row_dict.get("conjugated_form", "")
        normalized_candidate = _normalize_reverse_input(candidate_spelling)

        if normalized_candidate == normalized_spelling:
            row_dict["match_type"] = "normalized"
            row_dict["matched_query"] = spelling
            row_dict["normalized_query"] = normalized_spelling
            normalized_matches.append(row_dict)

    normalized_matches = _dedupe_reverse_rows(normalized_matches)
    return normalized_matches


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