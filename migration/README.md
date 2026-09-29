# Reference engine and migration coverage

This document covers the engine. For website pages, integrations and remaining
work, use the [website migration checklist](../docs/migration-backlog.md).

The new public engine is `laz_engine.engine.conjugate(Entry, Features)`. Its input
models, lexical identity, validation, construction dispatch and output handling
are independent of Flask, the old database and the original request service.

## Rule migration completed

The twelve active implementations live in `packages/engine/src/laz_engine/paradigms/`.
Each processes a single principal part through explicit stages. Shared preverb
handlers, phonology, vowel markers, suffix tables and pronouns are separated into
focused modules. `docs/rules.md` explains their order and editing workflow.

The application no longer imports a legacy rule adapter. Original rule bodies
are retained in `migration/reference/rules/` strictly as test evidence, together
with the previous dispatcher and validation. They are excluded from the installed
Python package and Docker image. AST tests still ensure this reference matches
the source modules, while output tests compare the refactored implementation to it.

All **1,511,672 requests** in the first SQLite release match the refactored engine,
including statuses, complete variant sets, pronouns and grammatical codes. The
new release adds **4,290 potential optative forms**, for **1,278,826 form records**.
There are **1,273,322 stored requests**: impossible person pairs are now rejected
by common validation before generation, rather than stored as empty requests.

## What is supported

- All 327 lexical records, with stable entry IDs, class and meaning preserved.
- All available dialects for each entry (AS/AŞ, PZ, FA, HO).
- Present, past, future and past progressive in all three base classes.
- Optative, imperative and negative imperative, with class-specific dispatch.
- TVE applicative, simple causative, double causative and their combinations.
- TVE/TVM present perfect, potential and passive; passive double causative.
- Potential optative, using the original module’s explicit optative ending table.
- Optional preverbs where the original functions implement that parameter.
- All six subjects, all six explicit objects and no object, subject to restrictions.

This is coverage of the **supported reference interface**, not a claim that every
grammatical construction in Laz has been implemented. Non-indicative moods have
one canonical request tense (`present`); dispatch chooses the underlying rule.
Passive optatives and imperatives, potential imperatives, potential markers,
passive simple causative and optional preverbs in potential/perfect remain
explicitly unavailable. They need reviewed linguistic examples because the
source has no usable rule for them or accepts a flag without applying it.
TVM object/marker branches conflict with the original service’s TVM-only object
restriction, so that interface remains restricted pending reviewed examples.

The potential module does contain a complete optative ending table. It is now
selected explicitly and checked for every non-dative lexical entry, dialect and
subject against the original function. Its canonical request tense is `present`,
consistent with the other non-indicative moods.

## Explicit changes to data handling

- Source rows are never deduplicated by infinitive or spelling/dialect pair.
- Principal parts remain paired with their source dialects.
- `osinapu` (verb-0232) has an alternative `isinapay` with no dialect field. The
  orphan principal part is retained and reported, but not assigned to a dialect.
  Rules may independently generate the same spelling from a valid principal part.
- Each call uses a context for one entry and dialect. The old loader's accidental
  overwriting of same-spelling entries cannot choose another entry's principal part.
- Subject/object codes are carried directly; display pronouns never determine IDs.
- Legacy `N/A` forms become structured unsupported results, never searchable forms.
- Dative optatives and their imperatives reject explicit objects during validation,
  matching the exception already present in `ivd_present.conjugate_present`.
- IVD imperative uses present optative; TVE imperative uses past. This is selected
  per entry, so homographs in different classes do not steal one another's dispatch.
- The past-as-progressive exceptions in the original wrapper are preserved.

Source hashes are recorded in `packages/engine/src/laz_engine/data/provenance.json`.
The generated database records engine and lexicon hashes and its coverage profile.

## Regression evidence

`tests/fixtures/reference.json` contains 4,836 outputs captured by executing the
original modules, independently of the new engine. It covers all twelve modules,
all four dialect codes, subjects, representative objects/markers, moods, compounds,
Unicode spelling and optional preverbs. `scripts/capture_reference.py` recreates
it using an environment that can import the old modules (including pandas).

Do not regenerate the fixture file to silence a regression. Inspect differences
and record any intentional linguistic change with concrete examples first.

Additional tests cover unchanged rule ASTs, lexical identity, concurrent calls,
API validation, database publication failures, Unicode search, reverse round trips,
and read-only serving. A complete generation run additionally exercises every
enumerated combination and refuses publication on unexpected failures.

The historical PostgreSQL dump remains secondary evidence. It is not imported
into the new serving database. A complete row-by-row reconciliation of that export
has not been performed; its collapsed lexical identities and export losses must
be resolved before treating differences as linguistic defects.
