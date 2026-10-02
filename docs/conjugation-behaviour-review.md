# Conjugation changes for review

We compared the remake with your original code and latest database. **Every
request in the database matches for conjugated spellings, grammatical frames
and accepted/rejected status.** However:

- The generator produces **820,151 additional forms** for combinations absent
  from your database. These still need linguistic approval.
- The displayed pronouns differ in some cases, as explained below.

Here are the changes and decisions to review. The [detailed appendix](conjugation-behaviour-details.md)
keeps the full conditions, examples, affected verbs and mappings.

## 1. Changes to generated forms

| Change | What we implemented | What needs confirmation |
| --- | --- | --- |
| **Hopa dative past progressive** | Keep `r` for `-en` stems without an object, except third-person singular and `oqvapu`. Example: `domadginet̆u` → `domadginert̆u`. | Is this productive, or should it apply only to specific verbs? |
| **Applicative `eç̌opu` future** | Agreement follows `e-`, with `y-` where no agreement consonant intervenes. Example: `bieç̌opare` → `ebiç̌opare`. Applies with no, simple or double causative. | Confirm the pattern, especially the **96 simple-causative combinations not attested in the database**. |
| **`oxenu` past** | Singular “I → you” changes `(do)p̌i` → `(do)ǩi` in AS/PZ/FA, without applicative and with no or simple causative. Other combinations stay unchanged. | Confirm this narrow exception. |
| **Explicit `ko` / `do`** | Added separate prefix choices. Both lose `o` before a vowel. A prefix attested for an entry/dialect becomes available across its supported constructions. It attaches before the complete phrase, including negative particles. | Should availability be restricted by construction? Is attachment such as `komot giğur` intended? |
| **Potential optative** | Enabled the ending table already present in your code across eligible TVE/TVM entries. | Are there verbs that should be excluded? |
| **Hopa `meǩoru`** | Added the database's principal part `meǩorums` and generate its paradigm. | Are there restrictions or irregular forms beyond the database examples? |

The `oqvapu` exclusion, `eç̌opu` rule and `oxenu` correction are explicit lexical
exceptions. We did not eliminate exceptions or force everything into general rules.

## 2. Which combinations users can request

The remake enforces these limits consistently. Some were already enforced by the
old website; some old functions accepted options that were ignored or handled
inconsistently. **“Unsupported” describes the software, not what is possible in Laz.**

| Construction | Current limits |
| --- | --- |
| **IVD** | No applicative or causative. No explicit object for optative or affirmative imperative. |
| **TVM** | No explicit object or markers, despite branches for these in the original function. |
| **Potential** | TVE/TVM only; indicative or optative; no explicit object or markers. No imperative. |
| **Passive** | TVE/TVM only; indicative; no explicit object or applicative. Double causative is supported; simple causative is not. |
| **Perfect** | TVE/TVM only; indicative; no explicit object or markers. |
| **Imperatives** | Second-person subjects only, as before. |
| **Ordinary marked TVE forms** | Require an explicit object. |

Other selection changes:

- **No object is separate from third-person singular.** The old database's blank
  object selection returned both; the remake returns only no-object forms.
- **One mood and one causative type at a time.** Non-indicative moods use
  `present` as their stored request tense; the engine still uses the appropriate
  underlying construction, such as past for TVE imperatives.
- **Same-person combinations** retain the original restrictions, now checked
  before generation. TVE applicatives allow matching person/number; cross-number
  first-/second-person pairs remain rejected.
- **Unmarked perfect** is now allowed for `gexvamu`, `cexvamu`, `otebriǩu` and
  `oteşekkyuru`. The old generation wrapper blocked it. **Please review this.**
- **The old optional-preverb checkbox** remains separate from explicit `ko`/`do`.
  It is unavailable for potential/perfect and cannot be combined with explicit
  prefix selection.

## 3. Entries, dialects and grammatical labels

- Same-spelling entries keep separate meanings, classes and principal parts.
  Earlier code could overwrite one entry or choose the first matching record.
- A principal part is used only for its assigned dialects. The unassigned
  `osinapu` alternative **`isinapay`** is retained but needs a dialect assignment.
- Rule selection follows the selected entry's class. This prevents another
  same-spelling entry from determining its imperative or grammatical frame.
- Mixed database records are mapped using each form's frame. Two specific
  decisions need confirmation: equivalent **`oçindu`** records use the entry with
  complete dialect coverage; Hopa **`oǯǩunu`** ergative forms use the `uǯǩunaps`
  paradigm. All affected database spellings match.
- Prefix-group classification is now per entry. TVM also recognises `cu-` and
  `gyu-` alongside `co-` and `gyo-`; this affects no current entry but could affect
  future additions.

The [complete mapping table](conjugation-behaviour-details.md#appendix-a-mappings-whose-selected-class-differs-from-the-old-record-header)
shows every assignment that differs from an old record's class header.

## 4. Pronouns: an outstanding migration issue

The remake kept the **notebook pronouns**, while the old website used the
**database pronouns**. They differ in **61 table positions**, including case forms
and dialect spellings. For example, PZ third-person singular objects in TVE
constructions display `himus` in the remake versus `him` in the database.

These differences were missed by the spelling/frame comparison. We should use
the database values unless you identify a specific error. The
[full pronoun table](conjugation-behaviour-details.md#d-displayed-pronouns-a-newly-identified-migration-gap)
lists every difference.

## 5. Other behaviour

- Distinct variants are retained; identical duplicates within one request are
  collapsed. Different grammatical analyses remain separate, even if spelled alike.
- Invalid `N/A` results are excluded from search. Unexpected generation failures
  are reported as errors.
- Reverse lookup can return more analyses because we generate more combinations.
  Grouping results does not remove their underlying analyses.
- Rebuilding currently replaces the generated database. Your former workflow
  preserved manual edits. A local master database with reviewed additions would
  require changing this publishing workflow.

Existing irregular stems, named restrictions such as potential-only `guri mentxu`,
class-specific imperative formation, negative particles and the five inherited
past-as-progressive substitutions were retained. The suspicious future `ele`
table entry and potential `ceçamu` branch were also left unchanged.

**Requested feedback:** which extensions are productive, which need lexical
restrictions, and which request limits should change? The appendix contains the
exact cases if needed. No rules were changed while preparing this review.
