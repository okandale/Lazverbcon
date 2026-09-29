"""One typed API for local engine preview and published SQLite releases."""

import logging
import os
from dataclasses import asdict
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from laz_engine.engine import conjugate
from laz_engine.lexicon import entries_by_id, load_entries, search_entries
from laz_engine.models import (
    Causative,
    Derivation,
    Dialect,
    EngineFailure,
    Entry,
    Features,
    Form,
    Mood,
    Person,
    PrincipalPart,
    Tense,
    VerbClass,
)
from laz_engine.validation import validate
from pydantic import BaseModel, ConfigDict, Field

from .catalog import Catalog, engine_revision, lexicon_revision
from .website import WebsiteFiles

logger = logging.getLogger(__name__)


class ConjugationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    entry_id: str = Field(min_length=1, max_length=80)
    dialects: list[Dialect] = Field(
        default_factory=lambda: list(Dialect), min_length=1, max_length=4
    )
    subject: Person | Literal["all"] = "all"
    object: Person | Literal["all"] | None = None
    tense: Tense = Tense.PRESENT
    mood: Mood = Mood.INDICATIVE
    derivation: Derivation = Derivation.NONE
    applicative: bool = False
    causative: Causative = Causative.NONE
    optional_preverb: bool = False


class Cell(BaseModel):
    features: Features
    status: Literal["ok", "unsupported", "not_generated", "error"]
    forms: list[Form] = Field(default_factory=list)
    reason: str | None = None
    message: str | None = None


class ConjugationResponse(BaseModel):
    entry: Entry
    source: Literal["engine", "database"]
    cells: list[Cell]


class VerbPage(BaseModel):
    entries: list[Entry]
    total: int


class Match(BaseModel):
    entry: Entry
    features: Features
    form: Form


class ReverseResponse(BaseModel):
    match_type: Literal["exact", "alternate", "broad", "none"]
    total: int
    matches: list[Match]


class Option(BaseModel):
    value: str | bool | None
    enabled: bool
    reason: str | None
    reason_code: str | None = None


class OptionsResponse(BaseModel):
    dialects: list[Dialect]
    options: dict[str, list[Option]]


class SuggestionsResponse(BaseModel):
    suggestions: list[str]


def entry_from_record(record: dict) -> Entry:
    return Entry(
        **{
            **record,
            "verb_class": VerbClass(record["verb_class"]),
            "issues": tuple(record["issues"]),
            "variants": tuple(
                PrincipalPart(v["form"], tuple(Dialect(d) for d in v["dialects"]))
                for v in record["variants"]
            ),
        }
    )


def create_app(database: Path | None = None) -> FastAPI:
    database = database or (Path(os.environ["LAZ_DATABASE"]) if os.getenv("LAZ_DATABASE") else None)
    catalog = Catalog(database) if database else None
    revision = engine_revision()
    if catalog and catalog.manifest["engine_revision"] != revision:
        raise ValueError("Database and engine revisions differ; deploy the matching release.")
    app = FastAPI(title="Lazverbcon", version="1.0.0")

    def get_entry(entry_id: str) -> Entry:
        if catalog:
            record = catalog.entry(entry_id)
            entry = entry_from_record(record) if record else None
        else:
            entry = entries_by_id().get(entry_id)
        if entry is None:
            raise HTTPException(404, "Unknown verb entry")
        return entry

    @app.get("/api/v1/health", operation_id="health")
    def health():
        return {
            "status": "ok",
            "source": "database" if catalog else "engine",
            "engine_revision": revision,
            "lexicon_revision": catalog.manifest["lexicon_revision"]
            if catalog
            else lexicon_revision(),
            "catalog": catalog.manifest if catalog else None,
            "entry_count": catalog.manifest["entry_count"] if catalog else len(load_entries()),
        }

    @app.get("/api/v1/verbs", response_model=VerbPage, operation_id="search_verbs")
    def verbs(
        q: str = Query("", max_length=200),
        limit: int = Query(30, ge=1, le=100),
        offset: int = Query(0, ge=0),
    ):
        if catalog:
            rows, total = catalog.entries(q, limit, offset)
            return {"entries": rows, "total": total}
        matches = search_entries(q)
        return {"entries": matches[offset : offset + limit], "total": len(matches)}

    @app.get("/api/v1/verbs/{entry_id}", response_model=Entry, operation_id="get_verb")
    def verb(entry_id: str):
        return get_entry(entry_id)

    @app.post("/api/v1/conjugations", response_model=ConjugationResponse, operation_id="conjugate")
    def conjugations(request: ConjugationRequest):
        entry = get_entry(request.entry_id)
        subjects = list(Person) if request.subject == "all" else [request.subject]
        objects = list(Person) if request.object == "all" else [request.object]
        cells = []
        for dialect in dict.fromkeys(request.dialects):
            for subject in subjects:
                for obj in objects:
                    features = Features(
                        dialect,
                        subject,
                        obj,
                        request.tense,
                        request.mood,
                        request.derivation,
                        request.applicative,
                        request.causative,
                        request.optional_preverb,
                    )
                    restriction = validate(entry, features)
                    try:
                        result = (
                            asdict(restriction)
                            if restriction
                            else (
                                catalog.lookup(entry.id, features)
                                if catalog
                                else asdict(conjugate(entry, features))
                            )
                        )
                    except EngineFailure:
                        logger.exception("Conjugation failed for %s: %s", entry.id, features)
                        result = {
                            "status": "error",
                            "forms": [],
                            "reason": "engine_failure",
                            "message": "The reference rule failed for this combination; it needs review.",
                        }
                    cells.append({"features": features, **result})
        return {"entry": entry, "source": "database" if catalog else "engine", "cells": cells}

    @app.post(
        "/api/v1/conjugation-options",
        response_model=OptionsResponse,
        operation_id="conjugation_options",
    )
    def options(request: ConjugationRequest):
        """Option metadata uses the same validation as generation and requests."""
        entry = get_entry(request.entry_id)
        dialect = next((d for d in request.dialects if d in entry.dialects), entry.dialects[0])
        fields = {
            "tense": list(Tense),
            "mood": list(Mood),
            "derivation": list(Derivation),
            "subject": ["all", *Person],
            "object": [None, "all", *Person],
            "applicative": [False, True],
            "causative": list(Causative),
            "optional_preverb": [False, True],
        }
        result = {}
        for field, values in fields.items():
            choices = []
            for value in values:
                candidate = request.model_copy(update={field: value})
                subjects = list(Person) if candidate.subject == "all" else [candidate.subject]
                objects = list(Person) if candidate.object == "all" else [candidate.object]
                # An aggregate choice is available when at least one of its
                # concrete forms is supported. A representative person can lie.
                problems = [
                    validate(
                        entry,
                        Features(
                            dialect,
                            subject,
                            obj,
                            candidate.tense,
                            candidate.mood,
                            candidate.derivation,
                            candidate.applicative,
                            candidate.causative,
                            candidate.optional_preverb,
                        ),
                    )
                    for subject in subjects
                    for obj in objects
                ]
                problem = None if None in problems else problems[0]
                choices.append(
                    {
                        "value": value,
                        "enabled": problem is None,
                        "reason": problem.message if problem else None,
                        "reason_code": problem.reason if problem else None,
                    }
                )
            result[field] = choices
        return {"dialects": entry.dialects, "options": result}

    @app.get("/api/v1/reverse", response_model=ReverseResponse, operation_id="reverse_lookup")
    def reverse(
        q: str = Query(min_length=1, max_length=200),
        limit: int = Query(50, ge=1, le=100),
        offset: int = Query(0, ge=0),
    ):
        if not catalog:
            raise HTTPException(
                503, "Reverse lookup needs a generated SQLite catalog. Run lazcon build first."
            )
        return catalog.reverse(q, limit, offset)

    @app.get(
        "/api/v1/reverse/suggestions",
        response_model=SuggestionsResponse,
        operation_id="reverse_suggestions",
    )
    def suggestions(q: str = Query("", max_length=200)):
        return {"suggestions": catalog.suggestions(q) if catalog else []}

    web = Path(os.environ["LAZ_WEB_DIST"]) if os.getenv("LAZ_WEB_DIST") else None
    if web:
        app.mount("/", WebsiteFiles(directory=web, html=True), name="website")
    return app
