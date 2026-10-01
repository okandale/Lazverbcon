# Retired application and recovery

The old application was removed from the active `codex/remake` tree on 2026-10-01.
It remains in Git history at commit:

`b2f0f8b57e51702da215dc48dc7b78587c139c2d`

[Browse the original application at that commit](https://github.com/okandale/Lazverbcon/tree/b2f0f8b57e51702da215dc48dc7b78587c139c2d/laz_verb_conjugator).

## Removed from the active tree

- `laz_verb_conjugator/`: original Flask app, both older frontend/conjugator paths,
  admin database editor, notebooks, old dependency manifests, obsolete assets and
  bundled development database/dump.
- `lazverbcon.sql`: the earlier SQL export, superseded by the maintainer's upload.
- `scripts/import_legacy.py` and `scripts/capture_reference.py`: one-time tools
  requiring the original checkout. They are recoverable with that source.
- `et --hard HEAD~1`: an unrelated tracked terminal-output file.

No Git history was rewritten. This is branch cleanup, not a merge or deployment.
The owner's `lewis-upload/` directory and generated `artifacts/` remain untouched
and Git ignored. Earlier uncommitted feedback/page changes are also retained.

## Kept as regression evidence

- `migration/reference/`: the frozen Python rules and dispatcher used by tests.
  These are not an application, installed package or runtime dependency.
- `migration/reference-checksums.json`: hashes of every retained reference Python
  file. The original function AST comparison passed before removing the old app;
  the replacement test detects missing, altered or additional reference files.
- Historical and maintainer fixtures under `tests/fixtures/`, including the
  complete 582,147-row dump evidence.
- `migration/maintainer-mappings.json`, extraction records and source provenance.
- Keyboard illustrations already copied into `apps/web/public/images/keyboard/`.
- The original unfinished phrase prompts, now in `apps/web/src/site/phrases.ts`.

## Recover the old source without changing the working branch

Inspect a file directly:

```bash
git show b2f0f8b57e51702da215dc48dc7b78587c139c2d:laz_verb_conjugator/frontend/src/components/FeedbackForm.jsx
```

Or extract the application and original migration scripts to a separate directory:

```bash
mkdir -p /tmp/lazverbcon-legacy
git archive b2f0f8b57e51702da215dc48dc7b78587c139c2d \
  laz_verb_conjugator lazverbcon.sql scripts/import_legacy.py \
  scripts/capture_reference.py packages/engine/src/laz_engine/data \
  | tar -x -C /tmp/lazverbcon-legacy
```

The old scripts require their historical environment and directory layout. Use
that separate copy for investigation; do not run the importer against the current
lexicon or regenerate expected fixtures to make a failing rule pass.

## Migration status

The owner confirmed [feedback delivery](feedback.md) works on 2026-10-01. Old bookmarks and API contracts are intentionally
retired by owner decision. Future static hosting, authoring tools and translation
completion are separate work; see the [checklist](migration-backlog.md).

## Cleanup verification

After removal, all 6,666 Python tests and 40 frontend tests passed. The frontend
production build, Python lint/format checks and API schema comparison passed.
A fresh full catalog generated 1,303,622 forms with no generation errors, passed
all 6,019 historical/correction checks, and matched all 582,147 maintainer source
rows across 580,129 canonical requests with zero mismatches. Engine and lexicon
revision hashes are unchanged from the previously verified release.

Local evidence is Git ignored:

- `artifacts/cleanup-python-tests.txt`
- `artifacts/cleanup-build.json`
- `artifacts/cleanup-reference-verification.json`
- `artifacts/cleanup-maintainer-verification.json`
- `artifacts/cleanup-2026-10-01.sqlite`
