# Lazverbcon

A Laz conjugator with a static public website and a separate local admin.

## Start here

- **Edit conjugations:** [Admin setup and Windows downloads](docs/admin-app.md).
- **Change the code:** [Clone and run locally](docs/local-development.md).
- **Publish the website:** [Cloudflare Pages setup](docs/static-hosting.md).
- **Return after a break:** [Architecture](docs/architecture.md) and [remaining work](docs/migration-backlog.md).

## How it works

1. The admin stores approved verbs and conjugations in a local SQLite master.
2. First-run import loads the data extracted from the supplied `lazverbcon2.dump`.
3. Manual changes, imports and rule generation create proposals for review.
   Verb metadata edits take effect immediately and are logged.
4. Approval changes the master. Backups include proposals and change history.
5. Export creates public JSON files containing approved data. Publishing uploads
   that export to GitHub and updates a pinned pointer for Cloudflare Pages.
6. The public website loads those files as needed. It needs no hosted backend.

Changing Python rules does not overwrite approved conjugations. The generator
remains available for adding verbs, proposing changes and regression tests.

## Code layout

| Folder                            | Purpose                                                              |
| --------------------------------- | -------------------------------------------------------------------- |
| `apps/web/src/`                   | Public React/TypeScript website                                      |
| `apps/admin/src/laz_admin/`       | Local editor, SQLite master, history, backups and publishing         |
| `apps/api/src/laz_api/`           | Shared API contracts, catalog/export utilities and developer preview |
| `packages/engine/src/laz_engine/` | Python conjugation rules and lexical inputs                          |
| `scripts/`                        | Build, package, import and verification tools                        |
| `tests/`                          | App tests and source-derived expected outputs                        |
| `migration/`                      | Frozen linguistic reference and mapping evidence, used by tests      |

The API package is still used by the admin exporter, type generation and tests.
It is not a public hosting requirement. The original application is in Git history.
[Historical evidence](docs/history/README.md) is separate from current instructions.

## Development checks

After [local setup](docs/local-development.md):

```bash
python -m pytest -q
ruff check packages/engine/src/laz_engine apps/api/src apps/admin/src scripts tests
ruff format --check packages/engine/src/laz_engine apps/api/src apps/admin/src scripts tests
pnpm --dir apps/web test
pnpm --dir apps/web build
pnpm --dir apps/web format:check
```

CI checks the Python code, API contract, website and static exporter. Windows CI
also packages and exercises the actual admin executable. Test catalogs are
throwaway comparison inputs; CI does not publish them or edit the admin master.

Keep uploads in ignored `lewis-upload/` and generated files in ignored `artifacts/`.
Never commit the working database, backups or credentials.

See [contributing](CONTRIBUTING.md), [rule development](docs/rules.md), and
[all current guides](docs/README.md).
