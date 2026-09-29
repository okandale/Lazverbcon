# Website migration checklist

Last audited: 2026-09-29, against the checked-in original frontend/backend and
the public pages at [lazuri.org](https://lazuri.org/).

**The supported conjugation engine and public learning pages are migrated.**
Remaining work is translations, reviewed linguistic/data decisions, exact legacy
ID compatibility, optional automatic feedback delivery, admin and hosting. This
file tracks the completed pages and remaining work. Keep it updated as work
lands; completing an engine test does not complete a website item.

Status meanings: **Done** = implemented and checked; **Partial** = some behavior
exists but the original page or workflow is missing; **Missing** = not migrated;
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
| WEB-13 | `/resources/phrase-guide/pazar`, `/ardesen`, `/findikli-arhavi` under the same phrase-guide prefix | Needs evidence | All three routes now have correct dialect names, an explicit unavailable-content message, a Hopa link and contact details. Remaining: reviewed Pazar/Ardeşen/Fındıklı–Arhavi phrases. The live originals contained placeholder translations; none were invented. |
| WEB-14 | Conjugator feedback form | Partial | Feedback page prepares an email draft to `info@lazuri.org` with form, correction, explanation and optional conjugation/phrase context. User opens their mail app or copies the message; the UI never claims it sent anything. Tests confirm no network submission. Remaining only if desired: automatic delivery from the website, requiring a chosen receiving service and delivery test. Old JSONP integration was removed. |
| WEB-15 | Contact, support and acknowledgements | Done | Restored contact, support and acknowledgements. Corrected the Institute acknowledgement to `lazenstitu.com`; partner/support destinations retained from the old site. |
| WEB-16 | English/Turkish language choice | Done | All new public pages support English/Turkish, with local preference storage and explicit language query links. Shared links override the stored preference. Language persistence and Turkish mobile navigation checked. |
| WEB-17 | `/v2/verbs`, `/v2/verb/:verbID/:verbType` | Partial | `/v2/verbs` permanently redirects to `/verbs`, preserving query parameters. Old `/v2/verb/:id/:class` links return a recovery page (HTTP 410) pointing to search. Remaining: a verified mapping of historical production IDs to current entries; a local numeric ID is not reliable proof of the production identity. The duplicate conjugator stays retired. |

## Administration and hosting

| ID | Feature | Status | Remaining work and completion check |
| --- | --- | --- | --- |
| OPS-01 | `/admin`, `/admin/panel`, `/admin/logout`, `/admin/manage-verbs`, `/admin/add-verb` | Deferred | User requested deciding on editing tools after the core works. Old source includes login, protected browsing and add-verb submission; complete edit/delete behavior has not been established. Define the desired editing workflow first. Changes should update versioned lexical data, validate it, rebuild and publish SQLite. No live admin login or writes were attempted. |
| OPS-02 | Old public URLs and bookmarks | Done | Public routes load directly and on refresh. Unknown pages show a recovery page with HTTP 404; missing API/assets remain 404 rather than receiving an HTML success. Old detail links have deliberate 410 handling. Tests cover all public routes, query-preserving redirect, missing files and method handling. |
| OPS-03 | Old API paths and response formats | Deferred | New typed API is implemented, but it is not a compatibility layer for every old Flask route. Inventory external consumers before retiring old endpoints; add adapters only where needed. Internal new frontend already uses the new contract. |
| OPS-04 | Old `/update` deployment webhook | Deferred | Not migrated. Current approach builds a reproducible image/database release. Choose the hosting provider and deployment trigger when hosting starts; no need to restore server-side source updates automatically. |
| OPS-05 | Docker deployment verification | Deferred | Dockerfile, Compose and CI checks are written. Local engine, SQLite, API and web builds passed; Docker has not been run here. User explicitly deferred running Docker until hosting. Before launch, build the image, run the smoke check and verify HTTPS/domain routing, restart and release rollback. |
| OPS-06 | Native mobile client | Deferred | Website is the current target. A future client can use the same API. No app implementation is required for website parity. |

## Engine and data decisions

See [the rule guide](rules.md) and [migration evidence](../migration/README.md)
for exact implementation details and tests. These are unresolved language/data
questions, separate from the missing public pages.

- [ ] **LANG-01:** Define passive optative/imperative and potential imperative
  with reviewed input/output examples; these currently return unsupported.
- [ ] **LANG-02:** Resolve potential markers, passive simple causative, and
  optional preverbs in potential/perfect. Source flags lack usable rules.
- [ ] **LANG-03:** Resolve TVM object/marker branches versus the original
  service restriction before changing accepted combinations.
- [ ] **LANG-04:** Assign a supported dialect to the orphan `osinapu` principal
  part `isinapay`, or explicitly mark it unusable with provenance.
- [ ] **LANG-05:** Review suspicious inherited behavior, including future
  `ele` preverb data and the potential `ceçamu` comparison/assignment branch.
  Preserve current outputs until reviewed examples justify a correction.
- [ ] **DATA-01:** Reconcile the historical SQL export with the new lexicon and
  generated forms, accounting for collapsed lexical identities and export losses.
  This has not been done row by row; a mismatch alone is not proof of a rule error.

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
  current catalog contains 1,278,826 form records. This proves migration parity
  with that baseline, not completeness of all Laz grammar or the website.

## Remaining implementation order

1. Obtain reviewed phrases for WEB-13; extend the existing phrase data/components.
2. Decide whether automatic feedback delivery is needed (WEB-14). Email drafts
   work now without a service or credentials.
3. Obtain a trustworthy production ID/entry mapping for WEB-17 and inventory
   external API consumers before adding any compatibility adapters (OPS-03).
4. Resolve LANG/DATA items as examples and reviewed decisions become available.
5. Define admin editing (OPS-01) and the hosting workflow (OPS-04/05) when requested.

No ordinary public page is left blocked by the engine. Do not mark translations,
linguistic corrections or external message delivery complete without evidence.

## Implementation and verification

- Page components, bilingual content and shared navigation: `apps/web/src/site/`.
- Content source notes and deliberate editorial changes: [content sources](content-sources.md).
- Server route handling: `apps/api/src/laz_api/website.py`.
- Frontend journey tests cover language persistence, phrase category/history,
  unavailable dialects, feedback draft/context and directory identity/pagination.
- Backend route tests cover direct loads, redirects, real missing-page status,
  missing assets/API paths, HEAD and unsupported methods.
- Existing conjugator journeys pass with the new navigation. Engine rules and
  the generated SQLite catalog were not changed for this page migration.
- Browser checks cover desktop home, phrase refresh, language navigation and
  mobile home, keyboard guide, directory, conjugator and feedback entry point.

## Evidence and audit limits

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
