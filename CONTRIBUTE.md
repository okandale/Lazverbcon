# Contributing

Start with the [development setup](README.md#development-without-docker).
Use the repository-root Python virtual environment and `apps/web` for the React
website. The old application is preserved in [Git history](docs/legacy-archive.md);
`migration/reference/` contains only frozen test evidence.

## Where to make changes

- Conjugation rules and lexical definitions: `packages/engine/src/laz_engine/`.
  Follow [the rule guide](docs/rules.md). Update source data/rules, never a generated
  database. The maintainer dump is the authoritative regression target.
- Public pages and bilingual content: `apps/web/src/site/`.
- Conjugator and reverse lookup: `apps/web/src/features/` and `apps/web/src/App.tsx`.
- API and SQLite publisher: `apps/api/src/laz_api/`.
- Unfinished phrase translations: `draftGuides` in `apps/web/src/site/phrases.ts`.
  Each dialect has independent data; replace `laz: null` as translations become
  available. Preserve remaining placeholders and do not substitute Hopa forms.

## Check changes

Run the relevant tests and build commands in [Tests and checks](README.md#tests-and-checks).
For rule or lexical changes, also generate a fresh catalog and run the exhaustive
[maintainer verification](docs/maintainer-parity.md#reproduce). Do not rewrite the
expected-output fixtures to hide a discrepancy.

Uploaded files belong in Git-ignored `lewis-upload/`; generated catalogs and audit
reports belong in Git-ignored `artifacts/`. Keep source provenance and useful
regression evidence. Do not commit credentials or personal feedback submissions.

See [the migration checklist](docs/migration-backlog.md) for remaining work,
[feedback delivery](docs/feedback.md) for the integration and verification details, and
[the old API inventory](docs/legacy-api.md) for retired endpoints.
