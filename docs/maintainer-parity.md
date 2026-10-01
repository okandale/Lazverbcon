# Full parity with lazverbcon2.dump

All **582,147 source rows** pass against both the pure engine and a freshly
built SQLite catalog. The comparison uses **580,129 canonical grammatical
requests**, accounting for duplicate source rows without dropping their IDs.

| Result | Source rows |
| --- | ---: |
| Exact conjugation and grammatical-frame matches | 483,471 |
| Invalid combinations rejected by both implementations | 98,676 |
| Missing, different, unsupported or unmapped source forms | **0** |

For every attested request, the verifier compares the **complete set** of
spellings and frames. It detects unexpected extra forms as well as missing ones.
The separate raw-dump audit also reports no extra outputs for shared requests.
Subject, object number, dialect, tense, mood, derivation, markers and explicit
optional prefix are retained in the request.

## What changed

- Added `optional_prefix` with `none`, `ko` and `do` choices to the domain model,
  API, shared links and website. The old `optional_preverb` boolean remains for
  existing links and cannot be combined with an explicit prefix.
- Added one prefix-attachment rule: both prefixes lose `o` before a vowel;
  explicit selection resolves leading `(do)` notation. Attachment preserves the
  dump's convention around negative particles.
- Kept the prior corrections to Hopa progressive endings, applicative `eç̌opu`
  future and the specific `oxenu` past agreement pattern. Their limited lexical
  exceptions are described in [the first report](rule-corrections-2026-10-01.md).
- Added the attested Hopa `meǩorums` principal part from legacy verb 1357.
- Recorded **797 legacy record/class mappings** for the 751 old verb records.
  Ordinary constructions use their stored frame to resolve mixed-class records;
  potential, passive and perfect retain their construction-specific frame.
- Resolved equivalent `oçindu` duplicates using matching meanings/principal
  parts and the entry with complete dialect coverage. The Hopa `oǯǩunu` ergative
  forms map to the existing `uǯǩunaps` paradigm: all 762 previously differing
  forms agree with it. Meanings alone were insufficient for that mixed record.

No additional table of per-conjugation exceptions was necessary. The runtime
uses morphology rules, lexical principal parts and prefix-availability metadata.
It does not read the uploaded dump or the expected-output fixture.

## Scope

This establishes consistency with **every request in the dump**, including all
manual corrections represented there. It does not establish that every possible
Laz conjugation is linguistically correct.

The full generator still covers more combinations than the dump. The rebuilt
catalog contains **1,303,622 forms** over **1,298,134 requests**, with 820,151
forms for requests absent from the mapped dump. Those additional requests are
not validated by this source. Consequently, reverse lookup can still show
additional analyses for the same spelling. The databases are not identical in
coverage, numeric IDs or record layout.

No dump spelling was excluded as erroneous. One convention is flagged for later
linguistic review: row **568322** stores `komot giğur`, placing `ko` before the
negative particle. The implementation preserves it exactly. Mixed-class labels
are reconciled in the mapping ledger without discarding their conjugations.

## Evidence and build protection

- `migration/maintainer-mappings.json`: legacy IDs, canonical entries and reasons.
- `packages/engine/src/laz_engine/data/maintainer.json`: source fingerprint and
  attested prefixes per entry/dialect; contains no conjugation outputs.
- `tests/fixtures/maintainer-release.jsonl.gz`: all expected spelling/frame sets
  and source row IDs, exported from the original archive independently of the
  engine. It is used only for verification and excluded from the runtime image.
- `scripts/import_maintainer.py`: checks the archive fingerprint, exports selected
  COPY data without executing SQL, resolves identities and checks the rules.
  It refuses to publish metadata when any rule differences remain; it does not
  automatically insert output overrides to hide them.
- `scripts/verify_maintainer_release.py`: compares every request using either
  `conjugate()` or SQLite, including API validation. A regression test deliberately
  inserts an extra spelling and confirms the verifier fails.
- Docker builds the database from the rules and runs both the historical-fixture
  checks and the complete maintainer verification before creating the runtime image.

The upload and raw SQL exports remain ignored by Git and excluded from Docker
builds. The compressed, selected conjugation evidence is versioned so CI and
hosting builds can verify all rows without the private upload or PostgreSQL.

## Reproduce

From the repository root, with the Python environment installed:

```bash
# Verify the rules directly.
.venv/bin/python scripts/verify_maintainer_release.py

# Generate a new immutable SQLite release, then check it.
.venv/bin/lazcon build --output artifacts/next.sqlite
.venv/bin/python scripts/verify_release.py artifacts/next.sqlite
.venv/bin/python scripts/verify_maintainer_release.py artifacts/next.sqlite
```

To recapture the evidence from the original upload, with `pg_restore` installed:

```bash
.venv/bin/python scripts/import_maintainer.py lewis-upload/lazverbcon2.dump \
  --pg-restore /opt/homebrew/opt/libpq/bin/pg_restore
```

Use the appropriate `pg_restore` path on other systems. Hosting builds require
neither PostgreSQL nor the original upload.

To independently compare the raw archive with a release and preserve every audit
row, choose a new output directory:

```bash
.venv/bin/python scripts/compare_legacy_database.py \
  lewis-upload/lazverbcon2.dump artifacts/next.sqlite \
  --output artifacts/legacy-audit/next \
  --pg-restore /opt/homebrew/opt/libpq/bin/pg_restore
```

The audit's initial verb-level mapping counts may still show ambiguous records;
its reviewed form-level mapping resolves those identities before comparing rows.
The definitive `old_row_status` contains only `exact` and `both_reject`.

## Verified release

- Source SHA-256: `54964059bff2c7dbd5ae465235ce649f1a49491299116ccbf51757d0a280c35d`.
- Catalog: `artifacts/maintainer-full.sqlite`, schema **2**.
- Catalog SHA-256: `cefdf873b41174a874782d91f247442b4c1b1157c9adbcf44283c11d8064eb8a`.
- Engine revision: `8072fb36defbef45514e148bdad0e7c2a4cde9e44890d79ffdd5411333ff38e5`.
- Lexicon revision: `dacdcf7e3e63e37a60aa5e19597ea6bd15d893c55b16ce273ef9de2e06e578c1`.
- Engine report: `artifacts/maintainer-engine-verification.json`, **0 mismatches**.
- SQLite report: `artifacts/maintainer-database-verification.json`, **0 mismatches**.
- Independent raw-dump audit: `artifacts/legacy-audit/full-parity/`.
- Historical/correction release checks: **6,019 passing cases**.
- Python tests: **6,666 passed**. Frontend tests: **25 passed**. Production web
  build passed. The full database build reported no generation errors.

This is a database schema change; rebuild rather than reuse a schema 1 file.
The original prototype and first corrected catalog remain available for historical
comparisons. The remote server and existing local preview have not been restarted.
Docker execution itself was not available locally; its build inputs and the same
release-verification scripts were checked here.
