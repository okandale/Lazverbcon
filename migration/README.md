# Frozen linguistic reference

This folder contains regression evidence, not another runnable application.
The active rules are in `packages/engine/src/laz_engine/`.

- `reference/`: the original rules, dispatcher and validation used by tests.
- `reference-checksums.json`: pins the unchanged reference Python files.
- `rule-extraction.json`: maps the refactored stages to their original modules.
- `maintainer-mappings.json`: legacy verb identities and mapping reasons.

Do not modify the reference or regenerate expected fixtures just to silence a
failure. The owner-supplied `lazverbcon2.dump` supersedes conflicting historical
answers; record reviewed departures with source rows and examples.

`tests/fixtures/reference.json` contains original-rule expectations.
`tests/fixtures/maintainer-release.jsonl.gz` contains extracted dump requests and
conjugations. The latter is both comparison evidence and the admin's initial
import source. The engine computes proposals from rules and does not load it.

The reference is excluded from installed application packages. Keeping it enables
independent regression checks without retaining two entire applications.

See [rule development](../docs/rules.md), [open decisions](../docs/migration-backlog.md),
and [historical migration reports](../docs/history/README.md). The original app is
recoverable from [Git history](../docs/legacy-archive.md).
