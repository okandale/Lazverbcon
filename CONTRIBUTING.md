# Contributing

Start with [local development](docs/local-development.md) for cloning and live
localhost previews. The public website, local admin and Python generator have
separate responsibilities; see [architecture](docs/architecture.md).

## Make changes in the right place

- Public UI and content: `apps/web/src/`.
- Admin UI and editing workflow: `apps/admin/src/laz_admin/`.
- Linguistic rules and generator lexical inputs: `packages/engine/src/laz_engine/`.
- Shared contracts and static export: `apps/api/src/laz_api/`.
- Approved conjugations: review edits and proposals in the admin.

Changing the rules does not replace the approved database. Follow the
[rule guide](docs/rules.md); preserve source evidence and record reviewed changes.
Do not rewrite expected fixtures to hide discrepancies.

Unfinished phrase translations live in `draftGuides` in
`apps/web/src/site/phrases.ts`. Fill supplied translations independently and keep
remaining placeholders. Do not substitute forms from another dialect.

Run the relevant checks in [the README](README.md#development-checks). Keep uploads
in ignored `lewis-upload/` and generated files in ignored `artifacts/`. Never commit
working databases, backups, credentials or personal feedback submissions.

See [remaining work](docs/migration-backlog.md) before starting a new feature.
The old application and migration reports are [historical evidence](docs/history/README.md).
