# Lazverbcon

A mobile-friendly Laz verb explorer, an independent Python conjugation engine,
and a reproducible SQLite publisher. The original application remains under
`laz_verb_conjugator/` as a migration reference.

## Quick start: Docker

With Docker and [Docker Compose](https://docs.docker.com/reference/compose-file/services/)
installed and running, run this from the repository root:

```bash
docker compose up --build -d
```

Open **http://localhost:8080**. Docker builds the website, installs Python,
generates the full SQLite database, checks the historical reference cases and
every conjugation/rejection in the maintainer's dump, and packages
everything into one image. No local Python, Node or database setup is required.
The first build downloads dependencies and generates about 452 MiB of data, so
allow several minutes. Later builds reuse cached steps when their inputs have
not changed. Starting an existing image does not regenerate the database.

```bash
docker compose logs -f   # View server logs; Ctrl-C leaves the server running
docker compose down      # Stop the app
docker compose up -d     # Start the existing image again
```

After changing the code or lexical data, run `docker compose up --build -d` again.
For another local port, use `LAZ_PORT=8081 docker compose up -d`.
The database is bundled in the image; there is no database container or volume
to configure. The default port binding is accessible only on this computer.

For LAN access, add the server's actual LAN IP to a `.env` file in the repository
root, then recreate the container (no image rebuild is needed):

```dotenv
LAZ_BIND_ADDRESS=192.168.1.50
```

```bash
docker compose up -d --wait
```

Open `http://192.168.1.50:8080` from another device on the same network, replacing
the example IP with your server's address. If a firewall is enabled on the VM,
allow TCP port 8080 from your LAN.

Without Compose, the equivalent commands are:

```bash
docker build -t lazverbcon:local .
docker run --rm -p 127.0.0.1:8080:8000 lazverbcon:local
```

This builds a local image; no prebuilt image has been published to a registry.
The image build, reference verification, container startup and health endpoint
passed on a Debian VM on 2026-09-29 after correcting release-directory
permissions. The server reported all 327 entries and 1,278,826 forms in the full
SQLite catalog. The build checks application setup as the runtime user. CI also
includes a complete image build and HTTP smoke check. Docker is unavailable in
the implementation workspace.

## Migration status

The latest maintainer dump, `lazverbcon2.dump`, is the authoritative conjugation
target. Every one of its 582,147 rows is covered by the release checks, including
98,676 rejection rows. Explicit `ko`/`do` prefixes, corrected grammar and lexical
mappings are implemented. See the [complete verification report](docs/maintainer-parity.md).
This verifies all attested requests; the generator also supports combinations
absent from the dump, which do not acquire linguistic validation from this check.

This update uses SQLite schema 2. Rebuild the image/database; existing schema 1
files are retained as historical evidence and cannot serve the new prefix field.

Reverse lookup groups equivalent spellings across dialects and unchanged
optional-preverb settings. Counts and pagination refer to groups. Each result's
“Dialects and options” section retains the individual settings; the main action
opens matching dialects together. Different lexical entries, object numbers and
markers remain separate. The API returns those original requests in `variants`
alongside representative `features` and `form` fields. Existing SQLite releases
work without a database schema migration.

**The core engine and public learning pages are migrated.** The page-by-page
[migration checklist](docs/migration-backlog.md) tracks completed work and the
remaining translations, data decisions, integrations and deferred administration.

The core conjugator is running in the new architecture. All 327 lexical entries
and all twelve reference rule modules are included, with forward lookup, reverse
lookup, dialect comparison and an English/Turkish website.

All twelve rule modules now run through named stages in `paradigms/`, with shared
phonology, markers, endings and pronoun tables in `rules/`. Thirteen identical
preverb handlers are shared across tenses. Each principal part uses fresh local
state. The application does not import the original rule modules; a frozen copy
under `migration/reference/` is used only by regression tests.

The learning home, searchable verb directory, resources, workshops, about page,
all six keyboard guides and Hopa phrase guide are implemented in English/Turkish.
Feedback prepares an email draft with the selected form or page; automatic delivery
from the website is not configured. Other phrase dialects explicitly show that
translations are unavailable. Admin editing and native mobile support remain deferred. Some combinations with unclear
or inconsistent support in the original code are explicitly unavailable; see the
exact list in [migration/README.md](migration/README.md). The old SQL export has
not been fully reconciled with the newly generated forms.

## How it works

1. **Lexicon:** versioned JSON holds each verb's meaning, class, principal parts
   and dialects. Same-spelling entries keep separate identities.
2. **Engine:** pure Python applies the linguistic rules to one verb and one
   grammatical combination. It can run independently of the website or database.
3. **Build:** the publisher enumerates supported combinations and stores their
   outputs and grammatical analyses in SQLite. Unexpected failures stop publication.
4. **Website:** React sends selections to FastAPI. FastAPI reads the published
   SQLite file for both forward conjugation and reverse lookup. The same API can
   support a future mobile client.

Changing a rule or lexical entry means building a new image and database release.

## Development without Docker

Use Python 3.14, Node.js 24 and pnpm 11.25.0. Run these commands from the repository root.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.lock
pip install --no-deps -e .
```

### Engine preview

```bash
lazcon serve
```

In another terminal:

```bash
cd apps/web
pnpm install --frozen-lockfile
pnpm dev
```

Open **http://localhost:5173**. Vite proxies `/api` to the Python API at
`http://127.0.0.1:8000`. The API documentation is at **http://127.0.0.1:8000/docs**.
Forward conjugation runs directly through the engine. Reverse lookup becomes
available after a database is generated.

### Generate and serve SQLite

```bash
lazcon build --output artifacts/release.sqlite
python scripts/verify_release.py artifacts/release.sqlite
lazcon serve --database artifacts/release.sqlite
```

Stop the preview API before starting this server on the same port. In database
mode, **both forward conjugation and reverse lookup use the generated database**.
There is no silent fallback to runtime generation for missing database rows.

The full build currently produces **1,278,826 forms** from 327 lexical entries,
covering the supported feature matrix in [migration/README.md](migration/README.md).
The resulting SQLite file is approximately 452 MiB. Generated files live in the
Git-ignored `artifacts/` directory. Generation takes several minutes, depending
on the machine, and records progress on stderr.

For a quick present-tense build or a small subset:

```bash
lazcon build --profile core --output artifacts/present.sqlite
lazcon build --verb osinapu --verb oskidu --output artifacts/sample.sqlite
```

These databases declare partial coverage; absent combinations return
`not_generated`, not empty success. Existing release filenames cannot be
overwritten. Publish updates to a new filename, then restart the API with that
release. Use the matching engine code: the server checks the engine revision.

### Serve the built website from Python

```bash
cd apps/web
pnpm build
cd ../..
LAZ_WEB_DIST="$PWD/apps/web/dist" lazcon serve --database artifacts/release.sqlite
```

Now **http://127.0.0.1:8000** opens the learning-center home. The conjugator is at
**http://127.0.0.1:8000/conjugator**. The server serves public page URLs and the API together. No external
database service is needed. `.env.example` documents the optional environment
variables; export them in the shell rather than placing secrets in source files.

## Architecture

```text
packages/engine/src/laz_engine/
  models.py        Typed entries, grammatical features and results
  lexicon.py       Versioned lexical data, with stable record IDs
  validation.py    Shared restrictions and supported feature combinations
  engine.py        Explicit class/construction dispatch and form results
  enumeration.py   Finite enumeration for database generation
  orthography.py   Search equivalences, separate from linguistic spelling
  paradigms/       Ordered stem, marker, preverb, agreement and ending stages
  rules/           Shared phonology, preverbs, markers, pronouns and endings
  data/            Lexical entries and source provenance
apps/api/src/laz_api/
  app.py           FastAPI routes and generated OpenAPI contract
  catalog.py       SQLite generation, publication and read-only queries
  cli.py           Development and release commands
apps/web/src/
  api/             Generated API types, client and shared-link validation
  features/        Lexicon, conjugation results and reverse lookup
  site/            Public pages, bilingual content, navigation and phrase data
  App.tsx          Conjugator selection state, controls and results
  i18n.ts          English/Turkish interface text
scripts/           Reference import, capture and release verification
```

The engine has no framework or database dependency. Its public function handles
one concrete grammatical combination. The application expands selections such
as all subjects. It distinguishes accepted forms, unsupported combinations and
unexpected failures.

All 1,511,672 requests in the previous release were compared with the refactored
engine, including complete form sets and grammatical analyses, with zero differences.
Potential optatives add 4,290 form records, checked against the original ending
table for every applicable entry, dialect and subject. See the [rule guide](docs/rules.md),
[architecture](docs/architecture.md) and [migration notes](migration/README.md).

## Tests and checks

```bash
pytest -q
ruff check packages/engine/src/laz_engine apps/api/src scripts tests
ruff format --check packages/engine/src/laz_engine apps/api/src scripts tests
cd apps/web
pnpm test
pnpm build
pnpm format:check
```

4,836 fixtures were captured by running the original twelve rule modules,
independently of the new engine. Further tests cover input validation, separate
same-spelling entries, concurrent calls, failed publication, read-only database
access, Unicode matching and reverse-result navigation. Tests also compare every
entry with the frozen rules across tenses, people, moods, markers and dialects.

To compare a future refactor with an earlier database release:

```bash
python scripts/compare_engine_release.py artifacts/release.sqlite --report artifacts/comparison.json
```

After changing API models, regenerate the frontend contract:

```bash
lazcon openapi
cd apps/web
pnpm generate:api
```

GitHub Actions checks Python tests, the API schema, frontend types, UI tests and
the complete Docker build. The container job starts the image and checks its
health endpoint, website, forward conjugation and reverse lookup.

## Editing data and rules

Edit `packages/engine/src/laz_engine/data/entries.json` for lexical changes.
Keep existing IDs stable and assign a new ID to each new entry. Homographs and
different verb classes remain separate records. Each principal part carries its
own dialect list. Run the tests and build a new database release after changes.

`scripts/import_legacy.py` is a one-time/reproducibility import. Rerunning it
replaces the imported lexicon and reference snapshot from the old source; it is
not the normal editing workflow. Do not regenerate reference fixtures merely to
make a changed rule pass tests.

## Known review items

- One source variant, `osinapu` → `isinapay`, has no dialect assignment. It is
  retained and reported, but its applicability is not guessed.
- The published coverage is all supported reference combinations, not a claim
  that every construction in Laz has been implemented or linguistically reviewed.
- The old PostgreSQL dump has not undergone a complete row-by-row reconciliation.
- Admin editing, the broader learning portal, user accounts and native/offline
  mobile clients are outside this first release.
