# Conjugation migration: detailed appendix

Start with the [short review](conjugation-behaviour-review.md). This appendix keeps
the exact conditions, complete tables and audit evidence.

Audit date: 2 October 2026. Application code reviewed: `84615c6`.

## Purpose and comparison baseline

This document inventories the behaviour changes identified in the conjugation
migration: generated spellings, available constructions, lexical identity,
grammatical labels and displayed pronouns. It also identifies inherited behaviour
that could otherwise look like a new rule. No linguistic decisions were changed
while preparing this audit.

There are two different old baselines:

1. The original notebook-derived Python functions, data loader and generation
   wrapper/service at commit `0b3c9cd` (immediately before the remake).
2. The database-backed public endpoint and the later authoritative
   `lazverbcon2.dump`, which includes manual edits absent from those functions.

The retained `migration/reference/engine.py` is a dispatcher written during the
migration. Passing tests against it does **not**, by itself, prove that every
detail of the old public endpoint was preserved. This audit also examined the
original loader, wrapper, service and database query code in Git history.

The list concerns the supplied source and dump. It cannot establish undocumented
behaviour of a different production checkout. Website styling, translations,
pagination and deployment are outside this linguistic review.

### What is verified, and what is not

- All **580,129 canonical requests**, representing **582,147 dump rows**, match
  the current engine for complete **spelling/frame sets and accepted/rejected
  status**. There are no missing or additional forms for those mapped requests.
- This comparison does **not** check displayed pronouns, meaning text, old numeric
  IDs or old HTTP selection defaults. The pronoun audit below found a real gap.
- The generated catalog contains **820,151 forms for requests absent from the
  mapped dump**. These are predictions, not forms linguistically validated by
  database agreement.
- The general rules are not claimed to describe every valid construction in Laz.
  “Unsupported” below means the software currently declines to generate it.

Dialect abbreviations: **AS/AŞ** = Art̆aşeni/Ardeşen; **PZ** = Pazar;
**FA** = Fındıklı–Arhavi; **HO** = Hopa. Class codes are the source project's
**IVD**, **TVE** and **TVM**, displayed as Dative, Ergative and Nominative.

## A. New or corrected form-generating behaviour

### A1. Hopa dative past progressive: retain `r` before the ending

**Before:** the original function omitted `r` in the affected forms.

**Now:** in the dative progressive function, insert `r` before the ending if:

- the dialect is HO;
- there is no explicit object;
- the prepared root ends in `en`;
- the subject is 1sg, 2sg, 1pl, 2pl or 3pl;
- the infinitive is not exactly `oqvapu`.

Examples:

| Infinitive / request | Original function | Current form |
| --- | --- | --- |
| `dodginu`, HO, past progressive, 1sg, no object | `domadginet̆u` | `domadginert̆u` |
| `oncğore oqvapu`, same features | `oncğore maqvet̆u` | `oncğore maqvert̆u` |

`oqvapu` itself keeps `maqvet̆u`. Third-person singular and explicit-object
requests are outside this correction. The exclusion is a new lexical exception.

The changed forms in the current lexicon belong to these **17 infinitives**:
`dodginu`, `doǯonu`, `gonç̌elu`, `goşinu`, `guris meç̌valu`, `ǩai oǯonu`,
`memgvapu`, `oçit̆inu`, `oçindu`, `oç̌u`, `omç̌u`, `omşkironu`,
`oncğore oqvapu`, `oqominu`, `oşkurinu`, `ožiru`, `oǯǩunu`.

The check is a root-pattern condition, not a whitelist of those infinitives.
Future verbs meeting it would also receive the change. It also runs whenever
dispatch selects the progressive function; the existing past-as-progressive
dispatch is retained, although the current audit found changed requests here
only under past progressive.

**Evidence:** 85 directly attested corrected forms: 80 initially mapped rows plus
5 dative `ožiru` rows. Including the old optional-preverb boolean gives 170
changed requests in the current enumerated input space.

**Review:** Is this a productive rule with `oqvapu` as an exception, or should its
application be restricted to approved lexical entries?

### A2. Applicative `eç̌opu` future: recognise `e-` and reposition agreement

**Before:** the affected agreement consonant occurred before `e`.

**Now:** when the infinitive is `eç̌opu` and applicative is selected, recognise
`e-` before marker processing, then select agreement as follows:

- second-person object with a non-second-person subject: `eg-`;
- first-person object with a non-first-person subject: `em-`;
- otherwise first-person subject: `e-` followed by the existing phonologically
  adjusted first-person agreement consonant;
- otherwise: `y-`.

The existing marker, stem and ending rules still follow their normal sequence.
For example, FA future 1sg subject / 1sg object, applicative, no causative changes
from `bieç̌opare` to `ebiç̌opare`; the corresponding AS example changes from
`vieç̌opare` to `eviç̌opare`.

This is a verb-specific rule, not a general change to every `e-` verb. Its code
does not restrict causative type: it applies with no causative, simple causative
or double causative, subject to normal validation. It also has no explicit
dialect whitelist; the current entry supplies AS, PZ and FA.

**Evidence:** 192 corrected dump forms. Another **96 applicative + simple
causative** requests extend the existing equivalence in the source functions;
these are expressly not direct dump evidence. Including both settings of the
old optional-preverb boolean gives 576 changed requests.

The inherited general future-preverb table contains `ele`, resulting from
adjacent `el` and `e` string literals. Splitting it broadly changed 1,068 otherwise
matching dump rows in the earlier investigation, so that change was discarded.

**Review:** Confirm the agreement pattern, its extension with simple causative,
and the intended dialect/construction limits.

### A3. `oxenu` past: singular first-person subject / second-person object

**Before:** `(do)p̌i`.

**Now:** `(do)ǩi` for AS, PZ and FA, with subject 1sg, object 2sg, no applicative,
and either no causative or simple causative. The existing outer branch excludes
double causative.

This is a new explicit lexical/person exception. It does not extend to `oxvenu`,
HO, other person/number combinations or applicative forms. Plural `(do)p̌it`
behaviour is retained.

**Evidence:** all six corresponding dump forms; 12 changed requests when both
old optional-preverb boolean settings are counted.

**Review:** Confirm the narrow scope. No general productive rule has been inferred.

### A4. Explicit optional-prefix selection and attachment

The old rule interface had an optional-preverb boolean whose effect differed
between functions. The old database already stored explicit `ko`/`do`, but its
forward query selected only rows with no explicit prefix.

The remake adds a separate choice: **none, `ko`, or `do`**.

- Generate the base form first, then attach the selected prefix.
- Both prefixes lose `o` before an initial `a`, `e`, `i`, `o` or `u`.
- If the form starts with a parenthesised copy of the selected prefix, remove
  that notation before attachment: selecting `do` resolves leading `(do)`.
- Attach to the beginning of the complete output string, including compounds
  and negative particles. The dump's `komot giğur` convention is preserved.
- Availability is recorded per lexical entry and dialect, then used for **all
  otherwise supported base constructions**, rather than only the exact requests
  in which the prefix appeared in the dump. Potential and perfect can therefore
  have explicit prefixes where this metadata permits them.
- The old boolean remains a distinct option. It cannot be combined with explicit
  prefix selection, and it keeps its earlier restrictions.

There are **42 entry/dialect/prefix combinations** across 17 entries. Each has at
least one actual form in the dump; none is supported solely by an `N/A` row.

| Entry | Explicit prefix | Dialects |
| --- | --- | --- |
| `goşinu`, IVD and TVE separately | `ko` | FA, HO |
| `oç̌aru`, TVE | `do` | PZ, FA, HO |
| `oçkinu`, IVD | `ko` | FA, HO |
| `oçodinu`, TVE and TVM separately | `ko` | AS, PZ, FA |
| `olva`, TVM | `ko` | AS, PZ |
| `onç̌aru`, TVE | `do` | AS |
| `oşǩunu`, IVD | `ko` | AS, PZ |
| `oxenu`, TVE | `do` | AS, PZ, FA |
| `oxoǯonu`, TVE | `ko` | AS, PZ, FA, HO |
| `oxtimu`, TVM | `ko` | FA, HO |
| `oxvenu`, TVE | `do` | HO |
| `ren`, TVM | `ko` | AS, PZ, FA, HO |
| `uğun`, IVD | `ko` | AS, PZ, FA, HO |
| `uqoun`, IVD | `ko` | HO |
| `uyonun`, IVD | `ko` | AS, PZ, FA |

**Review:** Does prefix availability need narrower tense, mood, person, marker
or compound restrictions? Confirm attachment before negative particles.

### A5. Potential optative is now explicitly dispatched and enumerated

The original potential function contains an optative ending table. The remake
selects it explicitly and exposes potential optative for TVE/TVM entries that
pass validation. It uses all six subjects, available dialects, no object and no
markers. The request stores `present` as its canonical tense; the potential
function receives `optative` as its construction selector.

This added **4,290 forms** at the original coverage expansion. It does not invent
new endings, but makes the original table systematically accessible. The old
service's generic mood argument did not explicitly select this table.

**Review:** Should every eligible lexical entry support it, or are lexical
restrictions required? Source-code agreement does not establish productivity.

### A6. Hopa `meǩoru`: added principal part

Added **`meǩorums` for HO** to the TVE entry `verb-0086`, using dump record 1357.
That entry now has HO conjugations generated from this principal part. Other
principal parts were retained. No other principal-part addition was made in the
maintainer correction commit.

**Review:** The dump-backed outputs match. Confirm whether the wider generated
HO paradigm has lexical exceptions or construction restrictions.

## B. Lexical identity and source-data handling

### B1. Separate entries replace selection by infinitive alone

The old loaders assigned dictionary entries by infinitive, allowing a later
same-spelling row to overwrite an earlier row. The old database endpoint also
fetched one matching verb ID for an infinitive/dialect without an ordering or
explicit sense/class selection.

The remake preserves all **327 source rows** with separate entry IDs, meanings,
classes and principal parts. A request selects an entry. It does not implicitly
combine every sense or class sharing the same infinitive.

Repeated spellings in the source are: `dobalu`, `dotanu`, `goşinu`, `meǩoru`,
`memgvapu`, `monžinu`, `moşvacu`, `oçaminu`, `oçindu`, `oçodinu`, `oç̌u`,
`ogibu`, `oǩiru`, `oǩriu`, `op̌lanu`, `oqvapu`, `ordu`, `oropu`, `ostibu`,
`ot̆ǩoçu`, `ovapu`, `oxarsuvu`, `oyapu`, `ožiru`, `oǯǩunu`, `oǯunu`, `oʒxunu`.

This can change which meaning, principal part and class a user sees even when
the spelling of a conjugation is identical. Preserving source rows is not a
linguistic claim that every repeated row deserves a separate dictionary entry.

### B2. Principal parts stay paired with their own dialect fields

The old loader separately collected nonempty principal parts and nonempty region
fields, then zipped those lists. The remake preserves each original form/region
column pair and generates only from principal parts assigned to the requested
dialect. A missing dialect is not guessed or treated as “all dialects.”

The current unpaired item is `osinapu` alternative **`isinapay`**, with no dialect.
It remains in the source as an unresolved item and is not independently used for
generation. The old zip also omitted this unpaired trailing alternative; retaining
it visibly is a data-handling improvement, not a newly suppressed attested form.

**Review:** Assign its dialect(s), or confirm that it should remain unused.

### B3. Lexical prefix groups are scoped to the selected entry

Classification into `co/cu`, `gyo/gyu` and `no/nu/n` groups uses the principal
parts of the selected entry. Same-spelling entries no longer share global
membership accidentally. Classification still considers all that entry's
principal parts, rather than being recomputed from only the current dialect.

One additional implementation difference: the old TVM loader checked `co` and
`gyo`, whereas the remake uses `co/cu` and `gyo/gyu` for every class. The current
lexicon has **no TVM entry whose group membership changes because of this**.
It could affect a future TVM entry with `cu-` or `gyu-` principal parts.

**Review:** Confirm whether those extended TVM group tests are intended.

### B4. Rule selection is per entry and construction

The old service checked module membership by infinitive, sometimes giving a
different class priority for a shared spelling. The remake dispatches according
to the selected entry:

| Construction | Current selection |
| --- | --- |
| IVD affirmative imperative | Present optative |
| TVE affirmative imperative | Past |
| TVM affirmative imperative | Past |
| Negative imperative | Present, plus the inherited negative-particle treatment |
| IVD/TVE optative | Present function with optative mood |
| TVM optative | TVM optative construction |
| Potential optative | Potential optative ending table |

The class-specific imperative derivations themselves were already in the old
service. The change is reliable selection for the chosen entry, including
homographs, and explicit potential-optative dispatch.

Potential and perfect retain the Dative frame; passive retains Nominative.
Ordinary forms retain the selected entry's frame. The old service could collect
multiple modules and label combined results using the last module encountered;
the new engine assigns the frame with each result.

### B5. Mixed legacy database records are mapped by their stored form frames

An old verb record can contain forms belonging to different classes. For ordinary
constructions, migration uses each form's stored frame to select the corresponding
lexical entry. For potential/passive/perfect, it respects their construction frame
and resolves the underlying eligible lexical entry separately.

There are **797 record/class mappings for 751 old verb records**. In 53 mappings,
the selected lexical class differs from the old record's class header. This does
not rewrite the stored form's grammatical frame. Appendix A lists those mappings.

Two specific identity decisions also matter:

- **`oçindu`:** equivalent old records 269/270/271 map to `verb-0142`, which has
  the same meanings/principal parts in their shared dialects and also covers HO.
  The separate source entry is still retained.
- **Hopa `oǯǩunu`:** the TVE part of old record 617 maps to `verb-0309`, the
  `uǯǩunaps` paradigm. It differs from the other candidate in 762 forms and agrees
  with the dump throughout. This is an explicit one-record mapping exception in
  the importer, although not a runtime spelling override.

**Review:** Confirm the sense/class assignments. For example, a stored form may
now be shown under the selected spreadsheet entry's meaning rather than the old
mixed record's single meaning. Spelling/frame parity does not verify translation
or sense equivalence. The complete ID ledger is `migration/maintainer-mappings.json`.

## C. Accepted combinations and request semantics

These are part of observable conjugator behaviour. Some enforce existing
restrictions earlier; others limit options that individual old functions accepted,
ignored or handled inconsistently. They should not all be described as new
linguistic prohibitions.

| Item | Current behaviour and difference from the old paths |
| --- | --- |
| **C1. Mood/tense combinations** | Every non-indicative mood uses `present` as its canonical request tense. Other tense/mood pairs are rejected instead of letting the old service forward flags to functions that might ignore them. The underlying imperative can still use past, as shown in B4. |
| **C2. Conflicting moods** | One mood is selected. Old independent booleans could be supplied together and service precedence selected one. That ambiguity is removed. |
| **C3. Causative selection** | One value: none, simple or double. Old `simple_causative` maps to simple; old `causative` maps to double. The old wrapper already rejected both flags together; the new model makes that combination unrepresentable. This is not a new rule equating or merging the two causatives. |
| **C4. No object versus third-person singular** | The old database endpoint's blank object filter selected both NULL and O3SG. The remake's “no object” means NULL only; third-person singular is a separate choice. “All objects” covers the six explicit persons, with no-object separate. This can change displayed rows without changing their spellings. |
| **C5. Imperative subjects** | Only second-person singular/plural. The old service already imposed this restriction. The remake applies it centrally and declines other subjects instead of depending on extraction/filtering later. |
| **C6. Same-person subject/object pairs** | First- or second-person subject/object pairs with the same person are rejected, except TVE applicatives when the subject and object also have the same number. Cross-number same-person pairs remain rejected. This centralises original rejection branches; it does not add a new reflexive rule. Rejected pairs are no longer stored/searchable as `N/A` forms or empty successful requests. |
| **C7. IVD markers** | IVD entries reject applicative, simple causative and double causative. The old wrapper applied its marker restriction by infinitive membership and could behave differently for a spelling also present in another class. It is now enforced per entry. |
| **C8. IVD optative/affirmative-imperative objects** | Explicit objects are rejected. The original IVD present function already raised an exception for optative objects; the remake gives a structured unavailable result before generation. This restriction does not apply to IVD negative imperatives simply because they are negative imperatives: they use present indicative plus negation. |
| **C9. TVM objects and markers** | Explicit objects and all markers are rejected. This adopts a restricted public interface despite the old TVM function containing object/marker branches. Those branches were not turned into new public support. Homograph membership no longer changes this per-entry restriction. |
| **C10. Potential** | TVE/TVM only; indicative simple tenses plus the explicitly enabled optative; no explicit object, applicative or causative. Potential imperatives are unsupported. Some old function parameters/branches were more permissive or unused; that does not constitute implemented public support in the remake. |
| **C11. Passive** | TVE/TVM only; indicative simple tenses, no explicit object or applicative; supports either no causative or double causative. Simple causative, optative and imperatives are unsupported. The old passive function has object branches and accepts a simple-causative parameter, so this is a restriction of the published interface, not a claim that the language lacks those forms. |
| **C12. Present perfect** | TVE/TVM only, no explicit object or markers, indicative only. Object/marker rejection comes from the original perfect function. Non-indicative/perfect combinations are now rejected explicitly. |
| **C13. Marker-required verbs and perfect** | Ordinary `gexvamu`, `cexvamu`, `otebriǩu`, `oteşekkyuru` still require an applicative or causative marker. However, the new validator handles perfect before that lexical restriction, allowing unmarked perfect. The old generation wrapper checked marker-required verbs before its perfect branch and blocked this request when no aspect was selected. This is an additional interface difference requiring review. |
| **C14. Marker/object requirement** | Ordinary TVE marked forms require an explicit object. This retains the old wrapper requirement for ordinary forms. Passive double causative is handled as a separate derived construction, without an explicit object; it does not inherit the ordinary TVE check. |
| **C15. Old optional-preverb boolean** | Retained for ordinary constructions and passive. Rejected for potential and perfect, whose original functions accepted the parameter but did not implement that option. Explicit `ko`/`do` is the separate mechanism in A4. |
| **C16. Explicit-prefix restrictions** | Selected prefix must be present in the entry/dialect metadata. It cannot be combined with the old optional-preverb boolean. These validations accompany the new explicit option. |
| **C17. Dialect availability** | A dialect must have a paired principal part for the selected entry. Missing dialect data produces an unavailable result; membership in a same-spelling entry cannot supply it. |
| **C18. Named lexical restrictions** | `guri mentxu` remains potential-only. `coxons`, `cozun`, `gyožin` retain their ordinary no-object restrictions. These were in the old wrapper/validator; they were not added as new lexical exceptions. |

**Review priorities:** C4, C9–C11, C13 and C15 affect what users can select or
which analyses appear. Confirm intended availability using concrete forms,
rather than treating the software's unsupported status as a linguistic judgment.

## D. Displayed pronouns: a newly identified migration gap

The remake preserved the original **notebook** pronoun tables. The old public
database endpoint read pronouns from the dump's **`pronoun` table**. Those sources
are not identical.

This audit compared 480 rule/dialect/person display positions, excluding object
positions for TVM, potential, passive and perfect because the current interface
does not expose them. **61 positions differ**, grouped into the 20 rows below.
These are table positions, not a count of affected conjugations.

`S` means subject, `O` object; SG/PL mean singular/plural. “All IVD tenses” means
present, past, future and past progressive. Actual dispatch determines the table:
for example, an IVD affirmative imperative uses the IVD present table.

| Dialect | Person | Dump / old DB display | Current notebook-derived display | Rule families |
| --- | --- | --- | --- | --- |
| AS | O1PL | şǩu | çku | All IVD tenses; TVE past progressive |
| AS | O2PL | t̆ǩva | tkva | All IVD tenses; TVE past progressive |
| PZ | O1PL | şǩu | çku | All IVD tenses; TVE past progressive |
| PZ | O2PL | t̆ǩva | tkva | All IVD tenses; TVE past progressive |
| HO | O1PL | çkin | çku | All IVD tenses; TVE past progressive |
| HO | O2PL | tkvan | tkva | All IVD tenses; TVE past progressive |
| HO | S3SG | (h)emus | hemus | IVD past progressive |
| HO | O3SG | (h)em | hem | IVD past progressive |
| PZ | O3SG | him | himus | All four TVE tenses |
| PZ | O3PL | hini | hinis | TVE present, past, future |
| FA | O3SG | heya | heyas | All four TVE tenses |
| FA | O3PL | hentepe | hentepes | All four TVE tenses |
| HO | O3SG | (h)em | (h)emus | All four TVE tenses |
| HO | O3PL | entepe | entepes | TVE present, past, future |
| AS | O3PL | hini | hentepes | TVE past progressive |
| PZ | O3PL | hini | hentepes | TVE past progressive |
| HO | S3PL | entepek | entepe | TVE past progressive |
| HO | O3PL | entepe | hentepes | TVE past progressive |
| AS | S3SG | him | himus | Potential and present perfect |
| AS | S3PL | hini | hinis | Potential |

The earlier full-dump verifier checks spelling, frame and status, so it did not
detect these pronoun differences. Consequently, “full database consistency” was
too broad a description. No new pronoun spellings were invented, but choosing the
notebook tables instead of the edited database changes public output.

**Resolution needed:** align with the authoritative dump unless the author
identifies a particular dump error. This audit records the discrepancy without
changing the runtime tables.

Person/number identity is now carried in explicit codes, independently of these
display strings. No inference of person from an ambiguous pronoun is required.

## E. Catalogue and result behaviour

1. **Broader enumeration:** the generator systematically enumerates the accepted
   combinations of dialect, subject, object, tense, mood, derivation, applicative,
   causative and prefix. The old editorial database contains a selected set of
   stored requests. The remake therefore returns analyses absent from the dump,
   including different analyses sharing an identical spelling. Identical spelling
   does not establish that every proposed analysis is valid.
2. **Variant preservation:** every distinct spelling from the selected entry's
   eligible principal parts is retained. Duplicate identical results within that
   request are collapsed; different entries, frames or grammatical requests remain
   separate. A source dictionary overwrite no longer removes another entry's forms.
3. **Invalid forms:** original `N/A` text becomes a structured unavailable result
   and is excluded from search. Unexpected empty, mixed-valid/invalid or failed
   rule outputs raise an error instead of silently becoming a missing form.
4. **Reverse presentation:** identical spellings can be grouped across dialects
   and optional settings while retaining the underlying requests. Different
   person/number, markers, frames and lexical entries remain distinct. Fewer cards
   do not mean the underlying grammatical analyses were merged or deleted.
5. **Authoritative source workflow:** the current build reconstructs SQLite from
   the rules and lexical data, then exports it. Direct edits to a generated file
   do not survive a rebuild. The author's former workflow added generated forms
   and kept later editorial corrections in the master database. Adopting that
   workflow requires a reviewed-data/editor/publishing change; it is not yet
   implemented merely because static export exists.
6. **Static serving:** browser lookup reads exported forms and validation data.
   It does not run a separately ported morphology engine. This hosting change
   introduces no intended new conjugation rules.

## F. Inherited behaviour that was deliberately retained

- Existing irregular stems and verb-specific branches throughout the original
  functions, including preverb exceptions, remain unless superseded by A1–A3.
- Past uses the progressive function for the IVD entries `uğun`, `oçkinu`,
  `uyonun`, `uqoun`, `unon`, as in the old wrapper.
- Negative particles remain `mo` in AS/HO and `mot` in PZ/FA. The inherited TVM
  treatment prefixes the whole phrase; the IVD/TVE treatment inserts the particle
  before the last word. Explicit `ko`/`do` attachment then follows A4.
- The future `ele` table issue and potential `ceçamu` comparison-instead-of-
  assignment branch remain unchanged pending evidence.
- The spelling routines keep their original operation order. Sharing identical
  handlers and splitting functions into stages were intended to preserve output,
  not establish broader linguistic equivalence between different paradigms.
- There is no runtime lookup table of individual corrected conjugations. There
  are explicit lexical exceptions in code, lexical principal parts, prefix
  availability metadata and the one-record importer mapping described above.

## G. Evidence and review priorities

Checks performed for this audit:

- Compared the 44 retained original Python functions with their pre-migration
  source ASTs, ignoring only injected data context and removed debug printing:
  **no unexpected differences**.
- Ran engine, rule-migration and maintainer-correction tests: **6,643 passed**.
- Examined every currently enumerated request in the three directly corrected
  branch scopes, excluding the separate explicit-prefix feature: **2,388 checked;
  758 changed** (170 Hopa progressive, 576 `eç̌opu` future, 12 `oxenu` past).
  Of those 758 concrete requests, **283** have direct dump row IDs; the remainder
  include legacy boolean variants and inferred extensions. This is not a count
  of all migration changes or all extra generated forms.
- Rechecked explicit-prefix evidence: **42** entry/dialect/prefix combinations,
  all with non-`N/A` dump forms.
- Independently extracted the dump's pronoun table for the comparison in D.
- The full 580,129-request engine parity verifier was rerun earlier on the same
  unchanged code on 2 October 2026: **zero spelling/frame/status mismatches**.

The concrete 758 before/after requests, their available dump row IDs, and all 61
pronoun differences are saved locally in
`artifacts/conjugation-behaviour-review-2026-10-02.json` (Git ignored).

For the author, the most useful decisions are:

1. Confirm or limit the productivity of A1, A2, A4 and A5.
2. Confirm A3's narrow exception and A6's lexical addition.
3. Review availability and selection semantics in C, especially C4 and C9–C15.
4. Resolve the pronoun-source discrepancy in D.
5. Confirm the mixed-record mappings in B5 and Appendix A.
6. Decide whether forms absent from the dump should remain unpublished drafts
   until approved. The current public catalogue does not make that distinction.

Source references: `packages/engine/src/laz_engine/{engine,validation,enumeration}.py`,
`paradigms/{dative_progressive,ergative_future,ergative_past}.py`,
`rules/{optional_prefixes,pronouns}.py`, `data/{entries,maintainer}.json`,
`scripts/import_maintainer.py`, `migration/maintainer-mappings.json`, and the old
`backend/{dataloader,conjugation,validators,db_query}.py` and
`backend/services/conjugation.py` in Git history.

## Appendix A. Mappings whose selected class differs from the old record header

These entries preserve the stored form's frame. They do not reclassify every form
in the old record. “Dialect:ID” gives the old record ID for checking against the
dump. The entire mapping ledger includes the unchanged assignments too.

| Infinitive | Old record class | Selected entry class | Entry | Dialect:old ID |
| --- | --- | --- | --- | --- |
| dobalu | TVE | TVM | verb-0020 | PZ:36, AS:37, FA:38 |
| dobalu | TVM | TVE | verb-0019 | HO:39 |
| dotanu | TVE | TVM | verb-0037 | PZ:79, AS:80, FA:81 |
| dotanu | TVM | TVE | verb-0036 | HO:82 |
| goşinu | IVD | TVE | verb-0071 | FA:145, HO:1348 |
| goşinu | TVE | IVD | verb-0070 | AS:146, PZ:147 |
| memgvapu | IVD | TVE | verb-0091 | PZ:186, AS:187, HO:188, FA:1320 |
| meǩoru | TVE | TVM | verb-0087 | PZ:179, AS:180, FA:181, HO:1357 |
| monžinu | TVE | TVM | verb-0104 | PZ:215, AS:216, FA:217 |
| monžinu | TVM | TVE | verb-0103 | HO:218 |
| moşvacu | TVM | TVE | verb-0108 | HO:512 |
| ogibu | TVE | TVM | verb-0150 | HO:306 |
| op̌lanu | TVM | TVE | verb-0215 | PZ:445, AS:446, FA:447, HO:1371 |
| oqvapu | IVD | TVM | verb-0225 | HO:460 |
| ordu | TVE | TVM | verb-0228 | FA:462, AS:463, PZ:464 |
| ordu | TVM | TVE | verb-0227 | HO:465 |
| ot̆ǩoçu | TVM | TVE | verb-0264 | FA:536 |
| ovapu | IVD | TVM | verb-0271 | FA:547 |
| oyapu | IVD | TVM | verb-0294 | PZ:592 |
| oyapu | TVM | IVD | verb-0293 | AS:593 |
| oçaminu | TVE | TVM | verb-0120 | HO:257 |
| oçaminu | TVM | TVE | verb-0121 | FA:256 |
| oçodinu | TVE | TVM | verb-0138 | PZ:283, AS:284, FA:285 |
| oçodinu | TVM | TVE | verb-0137 | HO:286 |
| oç̌u | IVD | TVE | verb-0144 | PZ:296, AS:297, FA:298, HO:299 |
| ožiru | TVE | IVD | verb-0299 | HO:602 |
| oǯunu | IVD | TVE | verb-0313 | PZ:623, AS:624 |
| oǯǩunu | IVD | TVE | verb-0309 | HO:617 |
