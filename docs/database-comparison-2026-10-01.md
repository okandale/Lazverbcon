# Old database comparison — 1 October 2026

This is the initial baseline. All dump-row differences listed below have since
been resolved; see [the final verification report](maintainer-parity.md).

## Inputs and scope

**Authority confirmed by the project owner on 2026-10-01:** this dump is the
latest corrected database, including manual edits. Its conjugations take
precedence over the notebooks and frozen engine. The results below describe the
initial comparison, before implementing those corrections. Apparent dump errors
must be reported for review rather than silently excluded. See the
[rule update policy](rules.md#authoritative-conjugation-target).

The uploaded `lewis-upload/lazverbcon2.dump` is a PostgreSQL **custom archive**,
not SQLite. Its archive metadata says PostgreSQL/pg_dump 15.19, created
2026-10-01 02:23:44 BST. This establishes the format of this export, not when the
maintainer changed database software. The remake continues to use SQLite.

- Upload SHA-256: `54964059bff2c7dbd5ae465235ce649f1a49491299116ccbf51757d0a280c35d`.
- Old database: **751** dialect-specific verb records and **582,147** stored form rows.
- Remake: **327** lexical entries and **1,278,826** forms in `artifacts/prototype.sqlite`.
- Remake SQLite SHA-256: `882152653d2c259aa8f25626905a577330c2ed44a82fb605a7cffeb12b89f118`.
- Engine revision: `eaabacc0fd7489bc20dc2337b3d58d68832dd8b42f65841262bb11f47821041e`.

All old form rows and all new form rows were compared. This is a database-output
comparison, not a fresh exhaustive engine run or proof of linguistic correctness.
Unmapped rows are explicitly accounted for rather than silently discarded.

## Old-row results

Each old row belongs to exactly one category below.

| Result | Rows |
| --- | ---: |
| Same grammatical request, spelling and frame | 456,979 |
| Both reject the combination; old database stores an N/A message | 98,568 |
| Different spelling for a mapped request | 14,782 |
| Actual old form uses a combination rejected by current validation | 11,130 |
| Same spelling, different grammatical frame | 108 |
| Ambiguous lexical entry | 492 |
| No matching lexical entry/class/dialect | 88 |
| **Total** | **582,147** |

The old database contains **98,676 N/A rows** overall. The remaining 108 are among
the ambiguously mapped rows and have not been counted as confirmed equivalent
rejections. Such rows must not be presented as missing conjugations.

### Mapping quality

- 648 old verbs match class, dialect, infinitive, both meanings and principal part.
- 99 have a unique class/dialect/infinitive match but different lexical metadata.
- 3 are ambiguous `oçindu` records: candidate entries `verb-0128` and `verb-0142`.
- 1 is Hopa `meǩoru` under the ergative class, for which that lexical combination
  is absent from the current source. Its 88 rows remain unmapped.

Dialect IDs and verb IDs are never equated between databases. Unchanged request
features include subject, object number, tense, mood, derivation and markers.
Explicit old `ko`/`do` prefixes are provisionally compared with the remake's
boolean optional-preverb setting and retained in the original row data. This is
an information-losing feature mapping, identified as a review item below.

## What needs investigation

### 1. Old lexical identities were collapsed

**12,675** non-exact rows have an exact spelling-and-frame match for the same
features under another entry with the same infinitive:

| Original category | Rows matching another lexical entry |
| --- | ---: |
| Spelling difference | 3,051 |
| Unsupported request | 9,132 |
| Frame difference | 108 |
| Ambiguous entry | 384 |

These are diagnostic candidates, not automatic remappings. The preserved old
import notebook deduplicates verbs by `(dialect_id, infinitive)` and later joins
forms on that same pair, losing class identity. This could explain conflicting
class/meaning associations for `dobalu`, `dotanu`, `goşinu`, `memgvapu` and other
homographs. It does not establish that the manually corrected dump is wrong or
justify dropping its forms. Preserve those outputs while reconciling identities;
report concrete contradictions to the owner. See DATA-01/02 in the checklist.

### 2. Explicit optional prefixes

After setting aside alternative lexical-entry matches:

- **11,448 spelling differences** use an explicit old optional prefix:
  **6,464 `do`**, **4,984 `ko`**.
- **1,998 unsupported old forms** also have optional prefixes:
  **240 `do`**, **1,758 `ko`**. Some combine this with a class/marker mismatch;
  the prefix alone is not necessarily the cause of rejection.

Examples (old → remake):

| Verb / request | Old | Remake |
| --- | --- | --- |
| `oxoǯonu`, Pazar, present, I → you singular, `ko` | `koxogoǯonam` | `oxogoǯonam` |
| `oç̌aru`, Fındıklı/Arhavi, present, I → you singular, `do` | `doǩç̌arum` | `meǩç̌arum` |
| `olva`, Ardeşen, present, I, `ko` | `kovulur` | `mevulur` |
| `oşǩunu`, Ardeşen, present, third singular → I, `ko` | `kovuşǩur` | `kovşǩur` |

The remake's boolean option cannot distinguish a requested `ko` from `do`.
A proper implementation needs an explicit feature and rules for where each
prefix attaches, plus reference cases from this dump. Blindly prepending text
would not address vowel and consonant changes.

### 3. Non-prefix spelling differences

After setting aside alternative entry matches, **283** non-prefix rows differ:

- **192**: `eç̌opu`, AS/PZ/FA future (64 per dialect); e.g. old `ebiç̌opare` versus
  new `bieç̌opare`. Review preverb/agreement ordering.
- **80**: Hopa dative past-progressive forms; e.g. `dodginu`, first singular:
  old `domadginert̆u` versus new `domadginet̆u`. Review retention of `r`.
- **5**: `ožiru` Hopa past progressive; e.g. old `mažirert̆u` versus
  new `bžiropt̆i`. Reconcile the lexical class before changing endings.
- **6**: `oxenu` AS/PZ/FA past; e.g. I → you singular: old `(do)ǩi` versus
  new `(do)p̌i`. Review person-conditioned agreement.

All 283 requests were individually re-run through the current engine and the
frozen reference engine: those two implementations agree on all 283. Thus these
are differences from the newly supplied database, not demonstrated regressions
introduced by the rule refactor. Under the owner's confirmed policy, the dump's
outputs are the correction targets; the frozen reference is historical evidence.

These rule cases are now implemented; see the subsequent
[correction report](rule-corrections-2026-10-01.md). Counts in this document remain
the original baseline, before those changes.

## New-only results

**821,847** new rows have no exact mapped old counterpart:

- 11,663 have a mapped old request but a different output (spelling/frame).
- 810,184 have no mapped old request.

Broader generation, optional settings that do not change the spelling, and old
identity collapse all contribute. These counts are coverage differences, not a
claim that 821,847 new conjugations are wrong. The other **456,979** new forms
match old rows exactly.

## Reproduce and inspect

The comparison script is `scripts/compare_legacy_database.py`. It reads selected
COPY sections exported by [PostgreSQL's pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html)
and never executes dumped SQL. Neither source database is changed. `libpq`
provides the required client utility; no PostgreSQL server is needed.

From the repository root, use a **new output directory** on each run:

```bash
.venv/bin/python scripts/compare_legacy_database.py \
  lewis-upload/lazverbcon2.dump artifacts/prototype.sqlite \
  --output artifacts/legacy-audit/new-run \
  --pg-restore /opt/homebrew/opt/libpq/bin/pg_restore
```

The completed audit is in `artifacts/legacy-audit/verified/`:

- `summary.json`: counts, provenance and representative mismatches.
- `audit.sqlite`: all 582,147 old rows, their statuses, mapping candidates,
  original metadata, and all 821,847 unmatched new forms.
- `source.sql`: selected exported lexical/form tables.
- `rule-investigation.json`: the additional 283-case current/frozen-rule check.

Useful SQL queries against `audit.sqlite`:

```sql
SELECT status, count(*) FROM old_rows GROUP BY status;
SELECT id, entry_id, features, spelling, reason, alternative_entries
FROM old_rows WHERE status = 'spelling_difference';
SELECT * FROM verb_mapping WHERE quality <> 'exact_metadata';
SELECT status, count(*) FROM new_only GROUP BY status;
```

Uploads and complete reports are ignored by Git and excluded from Docker builds.
Only the reusable script, its tests and this summary belong in the repository.
Five audit tests pass, covering COPY escapes/NULLs, malformed input, marker
mapping, ambiguous homographs, complete row accounting and unchanged inputs.
No conjugation rules or lexical data were changed during this audit.
