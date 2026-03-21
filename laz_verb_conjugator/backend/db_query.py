import os
import unicodedata
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set.")

engine = create_engine(DATABASE_URL, future=True)

# Canonical tokens
TOKEN_K = "{KCARON}"
TOKEN_P = "{PCARON}"
TOKEN_T = "{TBREVE}"
TOKEN_C = "{CCARON}"
TOKEN_Z = "{ZCARON}"
TOKEN_J = "{JCARON}"
TOKEN_X = "{XLIKE}"
TOKEN_ZH = "{EZH}"

STRICT_NORMALIZATION_RULES = [
    # already-canonical spellings -> token
    ("ǩ", TOKEN_K),
    ("p̌", TOKEN_P),
    ("t̆", TOKEN_T),
    ("ç̌", TOKEN_C),
    ("ž", TOKEN_Z),
    ("ǯ", TOKEN_J),
    ("ʒ", TOKEN_ZH),
    ("x", TOKEN_X),

    # elder / alternative spellings -> token
    ("3'", TOKEN_J),
    ("ts", TOKEN_ZH),
    ("tz", TOKEN_J),
    ("dz", TOKEN_Z),
    ("z'", TOKEN_Z),
    ("k'", TOKEN_K),
    ("p'", TOKEN_P),
    ("t'", TOKEN_T),
    ("ç'", TOKEN_C),

    ("h", TOKEN_X),
    ("ğ", TOKEN_X),
    ("c", TOKEN_ZH),
    ("3", TOKEN_ZH),
    ("z", TOKEN_Z),
]

BROAD_NORMALIZATION_RULES = [
    ("k", TOKEN_K),
    ("ç", TOKEN_C),
    # Uncomment later only if you truly want these broader fallbacks:
    # ("p", TOKEN_P),
    # ("t", TOKEN_T),
]

TOKEN_TO_CANONICAL = {
    TOKEN_K: "ǩ",
    TOKEN_P: "p̌",
    TOKEN_T: "t̆",
    TOKEN_C: "ç̌",
    TOKEN_Z: "ž",
    TOKEN_J: "ǯ",
    TOKEN_X: "x",
    TOKEN_ZH: "ʒ",
}


def _apply_rules(text: str, rules) -> str:
    if not text:
        return ""

    t = unicodedata.normalize("NFC", text.strip().lower())
    for src, target in rules:
        t = t.replace(src, target)
    return t


def _finalize_tokens(text: str) -> str:
    t = text
    for token, canonical in TOKEN_TO_CANONICAL.items():
        t = t.replace(token, canonical)
    return unicodedata.normalize("NFC", t)


def _normalize_reverse_input_strict(text: str) -> str:
    t = _apply_rules(text, STRICT_NORMALIZATION_RULES)
    return _finalize_tokens(t)


def _normalize_reverse_input_broad(text: str) -> str:
    t = _apply_rules(text, STRICT_NORMALIZATION_RULES)
    t = _apply_rules(t, BROAD_NORMALIZATION_RULES)
    return _finalize_tokens(t)


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
            row.get("verb_group_code"),
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


def _candidate_prefixes_for_query(query: str, broad: bool = False):
    if not query:
        return ["%"]

    q = query.strip().lower()

    # Tier 2: strict alternate spellings
    if q.startswith("k'") or q.startswith("ǩ"):
        prefixes = ["k%", "ǩ%"]
    elif q.startswith("p'") or q.startswith("p̌"):
        prefixes = ["p%", "p̌%"]
    elif q.startswith("t'") or q.startswith("t̆"):
        prefixes = ["t%", "t̆%"]
    elif q.startswith("ts") or q.startswith("c") or q.startswith("3") or q.startswith("ʒ"):
        prefixes = ["ts%", "c%", "3%", "ʒ%"]
    elif q.startswith("tz") or q.startswith("3'") or q.startswith("ǯ"):
        prefixes = ["tz%", "3'%", "ǯ%"]
    elif q.startswith("dz") or q.startswith("z") or q.startswith("z'") or q.startswith("ž"):
        prefixes = ["dz%", "z%", "z'%", "ž%"]
    elif q.startswith("ç'") or q.startswith("ç̌"):
        prefixes = ["ç'%", "ç̌%"]
    else:
        first = q[:1]
        groups = {
            "x": ["x", "h", "ğ"],
            "h": ["x", "h", "ğ"],
            "ğ": ["x", "h", "ğ"],
            "c": ["c", "ʒ", "3"],
            "3": ["c", "ʒ", "3"],
            "ʒ": ["c", "ʒ", "3"],
            "z": ["z", "ž"],
            "ž": ["z", "ž"],
        }
        prefixes = [f"{ch}%" for ch in groups.get(first, [first])]

    # Tier 3: broad plain-letter equivalence
    if broad:
        extra = []
        first = q[:1]

        broad_groups = {
            "k": ["k", "ǩ"],
            "ǩ": ["k", "ǩ"],
            "ç": ["ç", "ç̌"],
            "ç̌": ["ç", "ç̌"],
            # Uncomment later only if truly needed:
            # "p": ["p", "p̌"],
            # "p̌": ["p", "p̌"],
            # "t": ["t", "t̆"],
            # "t̆": ["t", "t̆"],
        }

        if first in broad_groups:
            extra.extend([f"{ch}%" for ch in broad_groups[first]])

        prefixes = list(dict.fromkeys(prefixes + extra))

    return prefixes


def _fetch_reverse_candidates(conn, prefixes):
    if not prefixes:
        return []

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
            vf.optional_prefix,
            vc.code AS verb_group_code,
            vc.english_name AS verb_group_english,
            vc.turkish_name AS verb_group_turkish
        FROM verb_form vf
        JOIN verb v
          ON vf.verb_id = v.verb_id
        JOIN dialect d
          ON v.dialect_id = d.dialect_id
        JOIN verb_category vc
          ON v.verb_category_id = vc.verb_category_id
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

    return conn.execute(candidate_sql, candidate_params).mappings().all()


def reverse_lookup(spelling: str):
    spelling = (spelling or "").strip()
    strict_normalized_spelling = _normalize_reverse_input_strict(spelling)
    broad_normalized_spelling = _normalize_reverse_input_broad(spelling)

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
            vf.optional_prefix,
            vc.code AS verb_group_code,
            vc.english_name AS verb_group_english,
            vc.turkish_name AS verb_group_turkish
        FROM verb_form vf
        JOIN verb v
          ON vf.verb_id = v.verb_id
        JOIN dialect d
          ON v.dialect_id = d.dialect_id
        JOIN verb_category vc
          ON v.verb_category_id = vc.verb_category_id
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
        # Tier 1: exact
        exact_rows = conn.execute(
            exact_sql,
            {"spelling": spelling}
        ).mappings().all()

        if exact_rows:
            results = [dict(row) for row in exact_rows]
            for row in results:
                row["match_type"] = "exact"
                row["matched_query"] = spelling
                row["normalized_query"] = strict_normalized_spelling
            return results

        # Tier 2: strict alternate-spelling fallback
        strict_prefixes = _candidate_prefixes_for_query(spelling, broad=False)
        strict_candidate_rows = _fetch_reverse_candidates(conn, strict_prefixes)

        strict_matches = []
        for row in strict_candidate_rows:
            row_dict = dict(row)
            candidate_spelling = row_dict.get("conjugated_form", "")
            normalized_candidate = _normalize_reverse_input_strict(candidate_spelling)

            if normalized_candidate == strict_normalized_spelling:
                row_dict["match_type"] = "normalized_strict"
                row_dict["matched_query"] = spelling
                row_dict["normalized_query"] = strict_normalized_spelling
                strict_matches.append(row_dict)

        strict_matches = _dedupe_reverse_rows(strict_matches)
        if strict_matches:
            return strict_matches

        # Tier 3: broad plain-letter fallback
        broad_prefixes = _candidate_prefixes_for_query(spelling, broad=True)
        broad_candidate_rows = _fetch_reverse_candidates(conn, broad_prefixes)

    broad_matches = []
    for row in broad_candidate_rows:
        row_dict = dict(row)
        candidate_spelling = row_dict.get("conjugated_form", "")
        normalized_candidate = _normalize_reverse_input_broad(candidate_spelling)

        if normalized_candidate == broad_normalized_spelling:
            row_dict["match_type"] = "normalized_broad"
            row_dict["matched_query"] = spelling
            row_dict["normalized_query"] = broad_normalized_spelling
            broad_matches.append(row_dict)

    broad_matches = _dedupe_reverse_rows(broad_matches)
    return broad_matches


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