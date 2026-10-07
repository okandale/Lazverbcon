> Historical record. Deployment commands, counts and editorial policies below
> describe the earlier migration. Use the [current guides](../README.md).

# Maintainer database corrections — first rule update

Historical first-batch report. The remaining dump differences described here
are now resolved in the [complete parity report](maintainer-parity.md).

The source is `lewis-upload/lazverbcon2.dump`, SHA-256
`54964059bff2c7dbd5ae465235ce649f1a49491299116ccbf51757d0a280c35d`.
Expected spellings come from its stored forms, including manual corrections.
No changes are made directly to the generated SQLite file.

## Implemented

| Construction | Implementation | Directly mapped dump rows corrected |
| --- | --- | ---: |
| Hopa dative past progressive | Retain `r` for -en stems without an object, for the five attested subjects. Preserve `oqvapu` without `r`. | 80 |
| Applicative `eç̌opu` future | Recognize `e-` before applying markers; place the agreement consonant after it, or use `y-` when no consonant intervenes. Covers AS, PZ and FA. | 192 |
| `oxenu` past, singular I → you | Use `(do)ǩi` in AS/PZ/FA, with no causative or simple causative. | 6 |
| **Total** | | **278** |

The Hopa rule also generates all five corrected `ožiru` spellings using the
existing dative entry (`verb-0299`). Their dump record combines dative and
ergative rows. The rule is corrected, but legacy mapping still needs to select
the appropriate entry per grammatical analysis; these five are not counted as
resolved rows under the initial audit's verb-level mapping.

## Why some rules stay specific

The future preverb table inherited an adjacent-string typo (`el` + `e` became
`ele`). Simply splitting that string changes **1,068 previously matching dump
rows**, including non-applicative `eç̌opu` and other verbs. That attempted general
change was discarded. The implemented correction is a compact agreement rule
for applicative `eç̌opu`, rather than a table of its 192 spellings.

The dump changes singular I → you for `oxenu` but retains `(do)p̌it` for plural
combinations. This is an explicit lexical/person exception. It has not been
extended to `oxvenu` or unattested dialects.

The Hopa ending generalizes across the attested -en verbs. `oqvapu` is an explicit
exception because the dump retains `maqvet̆u`, whereas compound `oncğore oqvapu`
has `oncğore maqvert̆u`. Third-person singular is absent from the corrected
no-object rows, so this update leaves that subject unchanged.

These are limits on generalization, not declarations that the dump is wrong.
No authoritative outputs were discarded as errors.

## Regression evidence

`tests/fixtures/maintainer-corrections.json` contains 1,188 cases:

- 283 corrected spellings from identified dump rows, including the five dative
  `ožiru` cases with their mapping documented.
- 809 neighboring, unchanged dump forms to protect dialects, objects and markers.
- 96 explicitly labeled extensions preserving the existing equivalence between
  applicative alone and applicative with simple causative for `eç̌opu`.

The frozen reference and its original fixtures remain unchanged. Cross-entry
tests allow only recorded corrected spellings for exact requests, and still
compare frames, pronouns, status and other metadata with the frozen reference.
Docker's release verification also reads the corrected fixtures.

A comparison with the previous catalog inspected all 5,724 stored requests in
the edited entry/paradigm scope. There are 758 changed outputs, including optional
flag variants and the 96 simple-causative extensions; all changes are spelling
changes, with no changes to form counts or grammatical metadata. This count is
larger than 278 because the remake enumerates requests absent from the dump.
The full delta is in ignored `artifacts/rule-corrections-delta.json`.

## Fresh build and exhaustive comparison

- All **6,662 Python tests pass**; lint and formatting checks pass.
- A fresh full build produced **1,278,826 forms**, with no generation errors.
- All **6,019 release checks pass**, including the maintainer fixtures.
- Forward and reverse API lookup of corrected `ebiç̌opare` passes against SQLite.
- The repeated exhaustive audit accounts for all **582,147 dump rows** and every
  new form. **279** previously different rows now match exactly, including the
  278 targeted rows and `goşinu` row 575832 (`kogvaşinert̆es`). **No previously
  exact match was lost.** The five dative `ožiru` rows now have exact alternatives
  under the separate dative entry and still await legacy mapping reconciliation.

| Dump row status | Before | After |
| --- | ---: | ---: |
| Exact match | 456,979 | 457,258 |
| Both reject | 98,568 | 98,568 |
| Spelling difference | 14,782 | 14,503 |
| Unsupported actual form | 11,130 | 11,130 |
| Frame difference | 108 | 108 |
| Ambiguous entry | 492 | 492 |
| Unmapped entry | 88 | 88 |

The verified catalog is `artifacts/maintainer-stage1.sqlite`, engine revision
`884f9c57b1aa1b48fa921080d3cb41312f352d7c7fb1da05a368e3adf1f79731`.
Its SHA-256 is `2c29c99683d9c9000ef03b853c5480aa4af67722509c624f9854372485e0ece9`.
Full audit evidence is in ignored `artifacts/legacy-audit/stage1/`; build and
verification reports are `artifacts/maintainer-stage1-build.json` and
`artifacts/maintainer-stage1-verification.json`. The original prototype catalog
is retained for comparisons. Docker generates the corrected catalog on rebuild;
the existing local preview and remote deployment have not been restarted.

## Still outstanding

- Explicit `ko` and `do` selection and attachment (LANG-06).
- Actual dump forms currently rejected by validation.
- Legacy records combining different classes/meanings; ambiguous `oçindu` and
  missing Hopa `meǩoru` (DATA-01/02/03).
- Full parity must account for every dump row, not merely pass these fixtures.

The [migration checklist](migration-audit.md) tracks this remaining work.
