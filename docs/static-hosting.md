# Cloudflare Pages

The public website serves approved static data. No hosted Python server or
SQLite service is required.

## Set up once

Follow [Connect GitHub and Cloudflare](admin-app.md#connect-github-and-cloudflare-once)
for the exact build command, environment variables and admin settings.

The Pages project must use the repository and branch that the admin publishes to.
The current test project uses `lewisccz/Lazverbcon`, branch `codex/static-export`;
pushing the upstream repository alone does not update that fork.

Pages reads `published/catalog.json`, downloads the referenced export, verifies
its checksum, and builds `artifacts/pages`. The first publication must create that
pointer. There is no fallback that generates or replaces approved conjugations.

## Normal publication

1. Approve the intended changes in the admin.
2. **Publish → Export approved snapshot → Preview website**.
3. Confirm the repository and publish the export to GitHub.
4. Check the resulting Pages deployment and test the public website.

Code changes to the connected branch rebuild the frontend using the same pinned
approved data. Database changes require a new approved export and publication.
Pending proposals and change history stay private.

## Local development

Use [local development](local-development.md#public-website-preview-approved-data)
for a frontend preview with automatic reload. The admin's **Preview website**
uses a fixed approved snapshot and works offline.

## Verify a deployment

In an activated Python environment:

```bash
python scripts/smoke_static.py https://YOUR-TEST-DOMAIN
```

This checks direct page loads, query preservation and missing-page/asset/data
404 responses. Also test forward lookup, reverse lookup, suggestions and feedback
receipt from the Pages domain. The [checklist](migration-backlog.md) records
pending live verification; a successful upload alone does not prove it works.
