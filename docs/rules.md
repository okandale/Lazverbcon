# Working on conjugation rules

## Authoritative conjugation target

The local admin master holds approved data. Its initial conjugations and pronouns
come from the owner-supplied `lazverbcon2.dump`, including manual corrections.
The Python generator proposes answers; it does not determine whether an approved
manual exception may be stored or published.

Change the rules when evidence supports a reusable correction. Keep narrow lexical
exceptions where needed, with concrete examples and source row IDs. Apply changes
to the master through reviewed proposals, rather than rebuilding it. Differences
from approved data need linguistic review; they are not automatic database errors.

The author's [behaviour review](conjugation-behaviour-review.md) records changes
made during migration. Apparent source errors should be reported with examples
before changing or excluding their answers. Requests absent from the dump need
separate review. See the [open decisions](migration-backlog.md).

## Runtime flow

`laz_engine.engine.conjugate(entry, features)` handles one entry, dialect, subject,
object and construction. It validates the input, selects a paradigm and applies
its ordered stages independently to each principal part. It returns distinct
forms or a structured unsupported result. It does not read the admin database.

For example, ergative present prepares the stem, applies markers and agreement,
adjusts the construction, selects an ending and joins the form. The order differs
between paradigms; do not merge similar branches without comparing outputs.

## Where to edit

Locations below are under `packages/engine/src/laz_engine/`:

| Change                                             | Location                                                         |
| -------------------------------------------------- | ---------------------------------------------------------------- |
| Supported combinations                             | `validation.py`                                                  |
| Class, tense and mood dispatch                     | `engine.py`                                                      |
| Ordered morphology stages                          | `paradigms/`                                                     |
| Shared preverb branches                            | `paradigms/dative_preverbs.py`, `paradigms/ergative_preverbs.py` |
| Phonology, markers, endings and generator pronouns | `rules/`                                                         |
| Explicit `ko`/`do` attachment                      | `rules/optional_prefixes.py`                                     |
| Attested prefix availability                       | `data/maintainer.json`                                           |
| Generator principal parts and meanings             | `data/entries.json`                                              |
| Enumeration used by generation                     | `enumeration.py`                                                 |

`RuleRequest` is immutable; `Morphology` contains intermediate state for one
principal part. Each call uses fresh state. Display pronouns never determine
subject/object IDs. Approved imports use the separate dump pronoun snapshot;
generator pronouns are still subject to the review listed in the checklist.

Editing the generator lexicon does not edit an existing admin entry. Change its
metadata in the admin too when appropriate, then generate and review proposals.

## Verification

In the Python environment:

```bash
python -m pytest -q
python scripts/verify_maintainer_release.py
```

The second command compares rule outputs against every attested spelling/frame
request in the original dump fixture. It does not prove linguistic validity beyond
that source or compare later admin edits. The compressed fixture is also the
admin's initial import source; it is not read by `conjugate`.

To verify a freshly imported, unedited admin project including displayed pronouns:

```bash
python scripts/verify_admin_baseline.py artifacts/admin-dev
```

That check expects the original snapshot. It should not be used to reject intentional
approved corrections. A whole-master comparison against rules has no admin button
yet; see the checklist.

`migration/reference/` is frozen comparison evidence. Do not change it or rewrite
expected fixtures just to hide a regression. Add reviewed expectations for an
intentional linguistic change. `migration/rule-extraction.json` records where the
stages came from.

Generated-catalog builders and comparison scripts remain for regression work.
Their disposable databases are separate from the admin master and publication.
Historical measurements and the original migration audit are in
[history](history/README.md).
