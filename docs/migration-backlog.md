# Website migration checklist

Last updated: 2026-10-02. Original frontend/backend audited locally; unfinished
phrase pages rechecked on [lazuri.org](https://lazuri.org/) on 2026-10-01.

**The supported conjugation engine and public learning pages are migrated.**
The 2026-10-02 audit identified a remaining displayed-pronoun migration gap
(DATA-06); the earlier dump comparison covered spelling/frame sets and status,
not every displayed field. See the [full behaviour review](conjugation-behaviour-review.md).
The owner confirmed feedback delivery works on 2026-10-01. Remaining work concerns
reviewed linguistic/data decisions, future admin tooling and hosting. Old bookmarks and old API contracts
are intentionally retired by owner decision on 2026-10-01.
Unfinished translations are authoring work, not a migration blocker; their original
placeholders are preserved. This
file tracks the completed pages and remaining work. Keep it updated as work
lands; completing an engine test does not complete a website item.

Status meanings: **Done** = implemented and checked; **Retired** = intentionally not carried over; **Partial** = some behavior
exists but the original page or workflow is missing; **Missing** = not migrated; **Implemented** = code complete, external verification pending;
**Deferred** = deliberately postponed; **Needs evidence** = source behavior or
content must be resolved before completing it.

## Public pages and workflows

| ID | Original route / feature | Status | Remaining work and completion check |
| --- | --- | --- | --- |
| WEB-01 | `/` learning-center home | Done | Restored learning-center home, mobile navigation, support and contact links. English/Turkish choice persists across pages. Checked in the production build at desktop and 390px mobile width. |
| WEB-02 | `/conjugator` | Done | Conjugator is at `/conjugator` with directory and contextual feedback links. Earlier root `?selection=` and `?reverse=` shared links still open the explorer. Direct loading and mobile directory-to-form flow checked. |
| WEB-03 | `/verbs` | Done | Standalone `/verbs` has search, pagination, all three language columns and per-entry links. Tests verify homographs retain separate identities and searching resets pagination. |
| WEB-04 | `/events` | Done | Restored workshops page with the current live no-events state and contact link. Outdated class prices/schedule/signup form were omitted. Update this content when a real event is scheduled. |
| WEB-05 | `/resources` | Done | Restored resource directory, dictionaries, Minecraft project and video, contact and phrase guide. Official Institute/dictionary/GitHub pages were reachable during research; availability of every third-party destination could not be confirmed (see content source notes). |
| WEB-06 | `/keyboard` | Done | Restored keyboard index and links to all six guides, in English and Turkish. |
| WEB-07 | `/keyboard/windows`, `/keyboard/mac` | Done | Rewritten Windows/Mac setup guides with official downloads/help and selected original screenshots. Kept durable setup steps; no dependency on an old Google document. Screenshots are labeled as original-version examples. Physical-device installation was not tested. |
| WEB-08 | `/keyboard/android`, `/keyboard/iphone` | Done | Rewritten Android/iPhone setup guides with store and official help links, original illustrations and bilingual instructions. Removed nonfunctional `#` video links. Device installation remains a manual check, not a migration blocker. |
| WEB-09 | `/keyboard/computer`, `/keyboard/phone` | Done | Desktop/phone usage guides include layout images, special characters, input switching, suggestions and emoji guidance. Removed the claim that one shortcut works identically on every OS/version. |
| WEB-10 | `/about` | Done | About page rewritten around the project, dialects, contributions and acknowledgements. No broken component imports carried over. |
| WEB-11 | `/resources/phrase-guide` | Done | Restored phrase index and all four dialect URLs, preserving QR destinations. Each dialect has its correct heading; unavailable translations are clearly identified. |
| WEB-12 | `/resources/phrase-guide/hopa` | Done | Transcribed all 24 Hopa phrases and 12 vocabulary rows into `apps/web/src/site/phrases.ts`. Four categories, bilingual meanings, expandable vocabulary, copy buttons and persistent category links implemented. Laz spelling preserved; only obvious English/Turkish typos corrected. |
| WEB-13 | `/resources/phrase-guide/pazar`, `/ardesen`, `/findikli-arhavi` under the same phrase-guide prefix | Done | Restored each live page’s Market, Pharmacy and Restaurant tabs with the original English prompt and `...` translation placeholder. Correct dialect headings and explicit pending labels; independent editable data in `draftGuides`. Completing translations is future authoring work, not migration. |
| WEB-14 | Conjugator feedback form | Done | Sends the original three fields to the same Google Apps Script deployment; context is included in the explanation. Isolated JSONP frame, 20-second timeout, callback validation, duplicate-submit protection, cleanup, retained text and email/copy fallback. Local success/failure tests pass. The owner confirmed live feedback works on 2026-10-01. See [feedback delivery](feedback.md). |
| WEB-15 | Contact, support and acknowledgements | Done | Restored contact, support and acknowledgements. Corrected the Institute acknowledgement to `lazenstitu.com`; partner/support destinations retained from the old site. |
| WEB-16 | English/Turkish language choice | Done | All new public pages support English/Turkish, with local preference storage and explicit language query links. Shared links override the stored preference. Language persistence and Turkish mobile navigation checked. |
| WEB-17 | `/v2/verbs`, `/v2/verb/:verbID/:verbType` | Retired | Owner confirmed on 2026-10-01 that preserving old bookmarks is unnecessary. Keep the existing directory redirect and detail recovery page; no historical ID mapping or exact redirects are required. |

### Reverse result grouping — implemented

**WEB-18 (Done):** Reverse lookup groups matching dialects and optional-preverb
settings with identical spellings before counting and pagination. Each card keeps
its lexical entry, spelling, frame, rule and grammatical features distinct;
third-person singular/plural objects and different markers are not collapsed.
All original requests remain in the API's `variants` list and the card's
“Dialects and options” details. The main Open action selects all grouped dialects
that support its representative optional-preverb setting; individual settings
can also be opened from the details. Reset clears input, results and shared query.

Historical verification on 2026-09-29: checked with five backend regression tests and frontend tests for grouped dialect
selection, opening an individual optional-preverb variant, and resetting search.
All 14 focused backend tests and 21 frontend tests pass, as do the production
build and the local full-catalog HTTP smoke check. Browser verification confirmed
three `doviba` cards and opening the nominative group with AS/PZ/HO selected.
Deployment status must be checked against the current release; these counts describe the September baseline.

Investigation on 2026-09-29: `doviba` has 18 underlying exact rows in the full catalog:

- `verb-0020`, TVM, “to flow, to leak”: 3 dialects (AS/PZ/HO) × 2 optional-preverb
  settings = 6 rows. Present optative, first-person singular, no object/markers.
- `verb-0019`, TVE, “to pour”: the same 3 dialects × 2 optional-preverb settings ×
  2 marker combinations = 12 rows. Present optative, first-person singular subject
  and object, applicative, with either no causative or simple causative.

All 18 rows were re-evaluated against both the current engine and frozen reference
and reproduced `doviba`. Ignoring dialect and the unchanged optional-preverb
setting leaves 3 feature groups, not 18. This establishes software behavior, not
linguistic validity. The historical SQL export has only 3 exact rows, grouped into
2 cards by the old frontend; its lexical assignments also differ (see DATA-02).

### Form lookup suggestions

The reverse-search suggestions endpoint was migrated, but the initial frontend
used a native HTML datalist, which did not provide the old site's visible
dropdown consistently. Replaced it with an explicit suggestion list on
2026-09-29. It appears after two characters, supports pointer selection, arrow
keys, Enter and Escape, and hides stale results while the input changes.
Selecting a suggestion fills the input; submitting searches for its analyses.
The dropdown shows spellings; infinitives and dialects appear in search results.
Five regression tests cover selection, keyboard use, stale prefixes, focus and reset.
The production build and all 21 frontend tests passed. Browser verification
against the full SQLite catalog confirmed `dovigur` suggestions and a successful
lookup of the selected `doviguram` form.

## Administration and hosting

| ID | Feature | Status | Remaining work and completion check |
| --- | --- | --- | --- |
| OPS-01 | Old admin login and direct database editor | Retired | User confirmed on 2026-10-01: do not copy direct database editing endpoints. Future admin tools should edit versioned source definitions, preview, generate, verify and publish. This is new authoring functionality, not unfinished old-admin migration. |
| OPS-02 | Old public URLs and bookmarks | Done | Public routes load directly and on refresh. Unknown pages show a recovery page with HTTP 404; missing API/assets remain 404 rather than receiving an HTML success. Old detail links have deliberate 410 handling. Tests cover all public routes, query-preserving redirect, missing files and method handling. |
| OPS-03 | Old API paths and response formats | Retired | Owner confirmed on 2026-10-01 that the only API users are the owner and author, both aware of the migration. Use the new contract; no old-format adapters are required. Public equivalents are documented in the [endpoint inventory](legacy-api.md). |
| OPS-04 | Old `/update` deployment webhook | Retired | Use a build/test/publish workflow. No server-side source-update hook will be copied. Static Cloudflare publishing is being considered; its exporter/browser lookups are not implemented yet. |
| OPS-05 | Docker deployment verification | In progress | Image build, reference verification, container startup and HTTP health check passed on the Debian VM on 2026-09-29 after correcting release-directory traversal permissions. The server reported the full catalog: 327 entries, 1,278,826 forms and no generation errors. The build now verifies application setup as the runtime user. Before launch, run the full HTTP smoke check and verify HTTPS/domain routing, restart and release rollback. |
| OPS-06 | Native mobile client | Deferred | Website is the current target. A future client can use the same API. No app implementation is required for website parity. |

## Engine and data decisions

**Source of truth (owner confirmed 2026-10-01):** `lewis-upload/lazverbcon2.dump`
contains the latest conjugations and manual corrections. Implement its outputs
in rules/source data and regenerate SQLite; notebooks and frozen-rule parity
cannot override it. Report apparent dump errors before making exceptions. See
the [acceptance and correction policy](rules.md#authoritative-conjugation-target).

See [the rule guide](rules.md) and [migration evidence](../migration/README.md)
for exact implementation details and tests. These are unresolved language/data
questions and the displayed-pronoun gap below, separate from missing public
pages. Every request actually present in `lazverbcon2.dump` now passes the spelling/frame/status engine
and rebuilt-SQLite checks; see [the final report](maintainer-parity.md).

- [ ] **LANG-01:** Define passive optative/imperative and potential imperative
  with reviewed input/output examples; these currently return unsupported.
- [ ] **LANG-02:** Resolve potential markers and passive simple causative outside
  the attested dump requests. Explicit optional prefixes in potential/perfect
  are implemented and verified; the old boolean option keeps its old restrictions.
- [ ] **LANG-03:** Resolve TVM object/marker branches versus the original
  service restriction before changing accepted combinations.
- [ ] **LANG-04:** Assign a supported dialect to the orphan `osinapu` principal
  part `isinapay`, or explicitly mark it unusable with provenance.
- [ ] **LANG-05:** Review suspicious inherited behavior, including future
  `ele` preverb data and the potential `ceçamu` comparison/assignment branch.
  Preserve current outputs until reviewed examples justify a correction.
- [x] **DATA-01:** All 582,147 dump rows reconciled and verified: 483,471 exact
  conjugation/frame matches and 98,676 equivalent rejections. Zero spelling,
  frame, support or row-mapping differences remain. Both the pure engine and
  a fresh SQLite build pass all 580,129 canonical requests. Docker checks them
  on every build. [Evidence and scope](maintainer-parity.md).
- [x] **DATA-02 (dump mapping):** Mixed-class legacy records, including `dobalu`,
  are mapped by each form's frame for ordinary constructions and by construction
  for derived forms. Nominative `doviba` rows retain their spelling and grammatical
  features under the existing nominative entry. The ledger records all legacy
  IDs; no dump conjugation was discarded. Additional analyses generated for
  combinations absent from the dump are not validated by dump parity (DATA-04).

### Cases identified by the 2026-10-01 database audit

- [x] **LANG-06:** Explicit `ko`/`do` selection, vowel contraction, optional
  notation and particle attachment implemented in the engine, API and UI.
  Availability comes from attested entry/dialect pairs. Old boolean links remain
  supported separately. All explicit-prefix dump requests pass full verification.
- [x] **LANG-07 (rules):** Hopa dative past-progressive -en stems retain `r`
  for the five attested subjects without an object; `oqvapu` keeps its attested
  shorter ending. All 80 directly mapped dump rows now match. The same rule
  reproduces the 5 `ožiru` spellings under its existing dative entry; DATA-01
  resolves their attachment to the old mixed-class record.
- [x] **LANG-08:** All 192 applicative `eç̌opu` future corrections implemented
  (64 each in AS/PZ/FA). Agreement follows `e-`, with `y-` before the vowel marker
  when no agreement consonant intervenes. Kept this specific to the attested
  construction: changing the general future preverb table breaks other dump forms.
- [x] **LANG-09:** All 6 `oxenu` past corrections implemented (AS/PZ/FA,
  no causative or simple causative). Singular I → you uses `(do)ǩi`.
  Other person combinations retain the dump's existing outputs.
- [x] **DATA-03:** The `oçindu` duplicates have identical meanings and principal
  parts in the overlapping dialects; map to `verb-0142`, which also covers Hopa.
  Added Hopa `meǩorums` to `meǩoru` from dump record 1357. All 580 affected rows
  pass; the original distinct source IDs remain in the mapping evidence.
- [ ] **DATA-04 (outside dump coverage):** Review extra generated combinations
  separately before claiming linguistic validation beyond the dump. The full
  catalog has 820,151 forms for requests absent from the mapped dump. There are
  no extra or missing outputs for any request that the dump does contain.
- [ ] **DATA-05 (source convention review):** The dump writes `komot giğur`
  (e.g. row 568322), placing the optional prefix before the negative particle.
  This exact convention is preserved. Linguistic confirmation can be sought
  later; no source spelling was silently changed or excluded.
- [ ] **DATA-06 (displayed pronouns):** The original notebook pronoun tables
  retained by the remake differ from the authoritative dump's `pronoun` table
  in 61 of 480 compared rule/dialect/person display positions. The old database
  endpoint used the dump table. Align display data with the dump unless a
  specific source error is identified, add independent pronoun verification,
  and regenerate/publish affected output. No runtime fix was made during the
  audit. All differences are listed in [section D of the behaviour review](conjugation-behaviour-details.md#d-displayed-pronouns-a-newly-identified-migration-gap).
- [ ] **LANG-10 (full behavioural review):** Obtain the author's decisions on
  the [behaviour inventory](conjugation-behaviour-review.md), including productive
  extensions, explicit-prefix scope, potential optative, unmarked perfect for
  marker-required verbs, TVM/derived-construction restrictions and lexical
  identity mappings. Record decisions per item; do not treat the extra 820,151
  forms as linguistically approved solely because the source code generates them.

The initial audit supplied authoritative correction examples. The first rule
update is documented in [the correction report](rule-corrections-2026-10-01.md).
The subsequent [complete verification](maintainer-parity.md) resolves the prefix,
support and lexical-mapping differences. Open items concern coverage and source
review, plus displayed pronouns that the earlier parity check did not include.

## Already implemented

- [x] Independent typed Python engine; all twelve active rule modules refactored
  into stages and shared rules, with frozen source retained for regression tests.
- [x] All 327 lexical records and available dialects in the migrated source data.
- [x] Supported tense/mood/marker combinations and explicit unsupported reasons.
- [x] Potential optative, checked against the original ending table.
- [x] Reproducible SQLite generation with forward and reverse lookup.
- [x] Searchable lexicon, dialect comparison, character insertion, copied forms,
  English/Turkish explorer, shared selection/reverse links and reverse-to-form flow.
- [x] Full comparison of 1,511,672 previous requests with zero differences;
  that historical catalog contained 1,278,826 form records. The current schema 2
  release contains 1,303,622 forms across 1,298,134 requests; all dump requests pass.
  This does not establish linguistic validity outside dump coverage.

## Repository cleanup — completed 2026-10-01

Removed the old application, obsolete SQL/dump/development database, one-time
import/capture scripts and stray terminal-output file from the active branch.
Retained frozen regression rules, fixtures, mapping/provenance records, current
assets and unfinished phrase placeholders. The extraction AST check passed before
removal; a checksum test now protects the complete reference snapshot.
[Recovery instructions](legacy-archive.md) identify the exact Git commit.
Uploads and generated databases are untouched. No merge or deployment was made.

## Remaining work

1. Resolve LANG/DATA items only as reviewed examples and decisions become available.
2. Implement and benchmark a static data exporter/browser lookup layer if proceeding
   with Cloudflare hosting; keep the working API deployment until replacement is verified.
3. Design future admin editing around source data and the generator. Old direct
   database writes and the `/update` webhook are intentionally retired.

### Authoring work outside migration

The missing Laz translations on Pazar, Ardeşen and Fındıklı–Arhavi pages remain
unfinished, matching the original website. Their three categories and prompts
are preserved in `draftGuides` in `apps/web/src/site/phrases.ts`. The author can
replace each `laz: null` independently; no Hopa forms are substituted. These are
content tasks, not blockers to retiring the old application.

### Documentation corrections on 2026-10-01

Updated current release counts, explicit-prefix support, feedback behaviour and
contributor setup. Older parity reports remain historical evidence. These stale
documentation statements did not indicate additional missing conjugation rules.
See [the current parity report](maintainer-parity.md) for the verified scope.

## Implementation and verification

- Page components, bilingual content and shared navigation: `apps/web/src/site/`.
- Content source notes and deliberate editorial changes: [content sources](content-sources.md).
- Server route handling: `apps/api/src/laz_api/website.py`.
- Frontend journey tests cover language persistence, phrase category/history,
  unfinished dialect placeholders, feedback submission/fallback/context and directory identity/pagination.
- Backend route tests cover direct loads, redirects, real missing-page status,
  missing assets/API paths, HEAD and unsupported methods.
- Existing conjugator journeys pass with the new navigation. Engine rules and
  the generated SQLite catalog were not changed for this page migration.
- Browser checks cover desktop home, phrase refresh, language navigation and
  mobile home, keyboard guide, directory, conjugator and feedback entry point.

## Evidence and audit limits

Original source paths below are historical; see [Git recovery](legacy-archive.md).

- Local route inventory: `laz_verb_conjugator/frontend/src/App.jsx`.
- Local page sources: `laz_verb_conjugator/frontend/src/components/`, including
  `constants.js`, `FeedbackForm.jsx`, `v2/` and `admin/`.
- Local API sources: `laz_verb_conjugator/backend/app.py`, `verbs.py`, `admin.py`.
- Live pages inspected: [home](https://lazuri.org/),
  [conjugator](https://lazuri.org/conjugator), [verbs](https://lazuri.org/verbs),
  [events](https://lazuri.org/events), [resources](https://lazuri.org/resources),
  [keyboard index](https://lazuri.org/keyboard),
  [phrase index](https://lazuri.org/resources/phrase-guide) and its four dialect
  links. Keyboard detail content was inspected in the repo, not fully checked on
  each live platform page. External service delivery and protected admin behavior
  were not tested. This is a public page/source audit, not a production data audit.
- The live phrase pages and revised events text show that the checkout does not
  contain all current site content. Consult both sources during the remaining work.

## Static publishing (1 October 2026)

- [x] Export every catalog request and form into bounded static files.
- [x] Browser forward/reverse lookup, suggestions, option validation and lexical search.
- [x] Preserve content pages, shared URLs, language selection and feedback delivery code.
- [x] Verify every maintainer fixture request and every exported search reference.
- [x] Add reproducible Pages build, cache/route configuration and CI verification.
- [x] Deploy the separate Pages test project through the user's GitHub fork.
- [ ] Redeploy the route-file fix and run `scripts/smoke_static.py` against the public URL.
  The first deployment generated/uploaded the full release, but the index.html
  rewrites redirected public page URLs to home. Native page files replace those
  rewrites; all 18 non-home routes have local regression coverage.
- [ ] Confirm feedback receipt from the Pages origin (existing destination unchanged).

The remaining items are deployment verification. See [static hosting](static-hosting.md)
for commands, output sizes and the browser/API parity checks. The existing API and
Docker build remain available; they are not required by the static public site.
