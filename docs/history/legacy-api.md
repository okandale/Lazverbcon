> Historical record. Deployment commands, counts and editorial policies below
> describe the earlier migration. Use the [current guides](../README.md).

# Old API inventory

Audited on 2026-10-01 from the original Flask `app.py`, `verbs.py` and `admin.py`,
now preserved in [Git history](../legacy-archive.md).
The old API includes public lookup functions as well as administration. Public
features already exist in the new app, but the new API has its own request/response
format and entry IDs. That distinction is API compatibility, not missing UI behaviour.

## Public functions

| Old endpoint | Purpose | New equivalent |
| --- | --- | --- |
| `GET /ping` | Service health | `GET /api/v1/health` |
| `GET /api/conjugate` | Main database-backed conjugation lookup | `POST /api/v1/conjugations` |
| `GET /api/reverse` | Find infinitives and analyses from a conjugated spelling | `GET /api/v1/reverse` |
| `GET /api/reverse/suggestions` | Suggestions while typing a conjugated form | `GET /api/v1/reverse/suggestions` |
| `GET /api/verbs/search` | Search infinitive spellings for the old v2 explorer | `GET /api/v1/verbs?q=...` |
| `GET /api/verbs/list` | Paginated verb directory with translations | `GET /api/v1/verbs` |
| `GET /api/verbs/get/{id}/{type}` | Entry and regional principal parts for v2 | `GET /api/v1/verbs/{entry_id}` |
| `POST /api/verbs/conjugate` | Runtime conjugation through the old v2 class implementation | `POST /api/v1/conjugations`, using the verified engine/catalog |

No old-format adapters are required. On 2026-10-01 the owner confirmed that
the only API users are the owner and author, both aware of the migration. They
will use the new contract. The new website does not call the old endpoints. A fully static public website would replace its
current `/api/v1` calls with data-file lookups; that work is not implemented yet.

### Old page IDs

`/v2/verb/{id}/{type}` belonged to the SQLite schema with `verb.infinitive_form`
and `region_verb` records. The latest maintainer dump instead has dialect-specific
`verb` records and `verb_form` rows. The dump's reviewed mapping ledger is valid
for its source IDs; it does not establish that a historical v2 URL used those IDs.
On 2026-10-01 the owner confirmed that old bookmark compatibility is unnecessary.
Keep the existing recovery page; no further ID mapping or redirect work is required.

## Administration and deployment: intentionally not copied

| Old endpoint | Purpose | Decision |
| --- | --- | --- |
| `POST /api/admin/auth` | Admin password login and token issuance | Retired with the old admin |
| `POST /api/admin/refresh` | Refresh authentication token | Retired with the old admin |
| `GET /api/admin/me` | Check the logged-in admin identity | Retired with the old admin |
| `POST /api/admin/add-verb` | Insert directly into the old SQLite verb tables | Do not migrate; user confirmed on 2026-10-01 |
| `POST /update` | GitHub-triggered update of the running server | Retired; use a build/test/publish workflow |

No complete edit/delete API was found in these Flask blueprints. A future editor
should change source lexical definitions, preview generated forms, run validation,
then publish a versioned release. It should not patch the generated catalog.

Feedback is separate from these endpoints. It submits directly to the original
Google Apps Script deployment; see [feedback delivery](../feedback.md).
