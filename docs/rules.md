# Working on conjugation rules

The [website migration checklist](migration-backlog.md) tracks missing pages,
integrations and the language/data decisions alongside this engine guide.

## Authoritative conjugation target

On 2026-10-01 the project owner confirmed that `lewis-upload/lazverbcon2.dump`
is the latest, authoritative database. It includes manual corrections absent
from the original notebooks and frozen engine. When they disagree, target the
dump's conjugations. Agreement with the frozen engine does not justify keeping
a conflicting output.

Implement corrections in the rules and versioned lexical data, then regenerate
SQLite. Use explicit, narrowly scoped lexical exceptions where necessary to
preserve manual corrections; do not patch the generated database or require the
ignored upload at runtime. Generalize a rule only as far as the evidence supports.

For each correction, retain the dump row IDs, grammatical inputs and expected
outputs in regression evidence. Keep the frozen reference unchanged and record
intentional departures separately. Reconcile legacy identities so every dump
row is accounted for, including N/A rows as structured unsupported results.
Different prefixes, meanings, dialects and grammatical analyses must remain
distinguishable.

Completion requires reproducing the dump's conjugations for every resolved
request after a clean rebuild, with no unexplained differences or unmapped rows.
Report apparent dump errors or contradictory records to the owner with concrete
examples before excluding or changing them. A suspected import problem is not
permission to discard a stored correction. Additional requests absent from the
dump remain separately validated; absence alone does not mean they are invalid.

See the [initial exhaustive comparison](database-comparison-2026-10-01.md) and
[completed dump verification](maintainer-parity.md).

## Runtime flow

`laz_engine.engine.conjugate(entry, features)` accepts one entry, dialect, subject,
object and construction. It validates the request, selects a paradigm, applies
that paradigm independently to each applicable principal part, and returns all
distinct forms with their grammatical codes. It does not read SQLite or import
the migration reference.

Each paradigm's `conjugate` function lists its execution order. For example,
ergative present runs:

1. Prepare the stem and recognize its preverb.
2. Choose and apply vowel markers and lexical exceptions.
3. Apply preverb-specific agreement and sound changes.
4. Adjust the stem for the selected construction.
5. Select the subject/object ending.
6. Join the prefix, final stem and ending; reattach the compound word.

The orders differ between classes and constructions. Do not reorder stages or
merge similar-looking rules without comparing their outputs.

## Where to edit

| Change | Location under `packages/engine/src/laz_engine/` |
| --- | --- |
| Supported combinations and validation reasons | `validation.py` |
| Class, tense and mood dispatch | `engine.py` |
| Dative, ergative, nominative and derived constructions | `paradigms/` |
| Shared, identical preverb branches | `paradigms/dative_preverbs.py`, `paradigms/ergative_preverbs.py` |
| Compound handling and phonetic changes | `rules/phonology.py` |
| Ordered preverb recognition | `rules/preverbs.py` |
| Explicit `ko`/`do` attachment | `rules/optional_prefixes.py` |
| Attested prefix availability per entry/dialect | `data/maintainer.json` |
| Vowel markers | `rules/markers.py` |
| Endings independent of the stem | `rules/endings.py` |
| Dialect pronouns used for display | `rules/pronouns.py` |
| Lexical principal parts and meanings | `data/entries.json` |
| Combinations included in SQLite | `enumeration.py` |

`RuleRequest` is immutable. `Morphology` contains the changing stem, prefix,
suffix and related intermediate values for one principal part. Every call creates
fresh local state. Intermediate fields have no fallback values: missing a
preparation stage raises an error instead of silently producing a partial form.

Thirteen identical preverb handlers replaced 42 copied branches. Related but
different branches remain with their own tense. Large tables use the order
1sg, 2sg, 3sg, 1pl, 2pl, 3pl. Display pronouns never determine person IDs.

## Verification

Every Docker build now runs `scripts/verify_maintainer_release.py` against the
fresh SQLite catalog. The compressed test fixture contains expected spelling/frame
sets and source row IDs for every dump request. It is never loaded by the runtime
engine. The same verifier without a database argument checks the pure engine.
It fails on missing forms, extra forms for an attested request, wrong frames,
rejected valid requests or accepted N/A combinations.

```bash
python scripts/verify_maintainer_release.py
lazcon build --output artifacts/next.sqlite
python scripts/verify_maintainer_release.py artifacts/next.sqlite
```

The former boolean `optional_preverb` remains for old shared links. New requests
use `optional_prefix` (`none`, `ko`, `do`); the two settings cannot be combined.
Explicit prefixes use the base form independently of the old boolean rule.

`tests/fixtures/maintainer-corrections.json` records corrected dump spellings,
row IDs and neighboring unchanged cases. It takes precedence over the frozen
engine for those exact requests. Its 96 inferred applicative/simple-causative
cases are explicitly labeled and preserve the existing equivalence; they are
not presented as rows stored in the dump. Both pytest and the Docker release
check verify these cases. See [the correction report](rule-corrections-2026-10-01.md)
for the rule scope and remaining differences.

Run `pytest -q` for the fixed reference fixtures, cross-entry comparisons,
potential optative coverage and API/catalog tests. The frozen implementation in
`migration/reference/` is comparison evidence only. Do not edit it to make a new
output pass. `migration/rule-extraction.json` maps active paradigms to their
original modules and extracted stages.

For a change that should preserve existing behavior, compare the whole earlier
release before publishing:

```bash
python scripts/compare_engine_release.py artifacts/release.sqlite --report artifacts/comparison.json
lazcon build --output artifacts/next.sqlite
python scripts/verify_release.py artifacts/next.sqlite
```

The completed refactor matched all 1,511,672 requests in the previous release,
including unsupported results, spelling variants, grammatical analyses and
pronouns. The added potential optative is tested independently against the source
ending table across every applicable entry/dialect/subject, adding 4,290 forms.

## Decisions that need linguistic evidence

The application rejects combinations for which the source does not define a
usable calculation: passive optative/imperative, potential imperative, potential
markers, passive simple causative, and optional preverbs in potential/perfect.
TVM object/marker branches also conflict with the old service restriction.
To add one, obtain reviewed input/output examples, define its rule and case frame,
then update validation, enumeration and tests together. The API and UI already
have the relevant feature fields.

Some suspicious source behavior was preserved deliberately. For example, the
ergative future preverb table contains `ele` where the source joined adjacent
`'el' 'e'` string literals, and the potential `ceçamu` branch compares rather than
assigns a replacement stem. Correcting either could change forms; neither has
been silently treated as a linguistic correction. The orphan `osinapu` principal
part still needs a dialect assignment.

## Current local artifacts

- `artifacts/release.sqlite`: the previous implementation, retained for comparison.
- `artifacts/prototype.sqlite`: the current generated database.
- `artifacts/rule-comparison-final.json`: full comparison report, zero differences.
- `artifacts/prototype.report.json`: build counts and unresolved lexical data issues.

Artifacts are Git-ignored. Docker builds its own matching database from source.
