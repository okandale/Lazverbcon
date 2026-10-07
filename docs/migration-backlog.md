# Remaining work

Updated 7 October 2026. The engine, public pages and local admin are implemented.
Feedback delivery was confirmed by the owner on 1 October. The Windows executable
[build and automated package tests passed](https://github.com/okandale/Lazverbcon/actions/runs/37603514294).
Original unfinished phrase prompts and translation placeholders are preserved.

The active workflow is **local admin → approved export → Cloudflare Pages**.
The Docker deployment and its CI job are retired. Old API contracts and exact
bookmark compatibility were deliberately retired by the owner.

## Deployment checks

- [ ] Test launch, editing, approval, backup and restore on the intended Windows
      computer. CI covers the packaged launcher, generation, approval, export,
      preview, backup and reopening saved data.
- [ ] Bring the current code into the Pages-connected fork and switch its build
      to `scripts/build_published.py`.
- [ ] Publish the first approved admin export and verify the test domain: direct
      routes, forward/reverse lookups, suggestions and dump-derived pronouns.
- [ ] Run `scripts/smoke_static.py` against that deployment. Confirm the page-route
      fix prevents redirects back to home.
- [ ] Confirm feedback receipt from the Pages origin. Its original destination
      remains unchanged.

See [admin publishing](admin-app.md#connect-github-and-cloudflare-once).

## Linguistic decisions

Preserve existing outputs until the author provides reviewed examples or decisions.

- **LANG-01:** Passive optative/imperative and potential imperative.
- **LANG-02:** Potential markers and passive simple causative outside attested requests.
- **LANG-03:** TVM object/marker behavior versus the original service restriction.
- **LANG-04:** Dialect assignment for `osinapu` principal part `isinapay`.
- **LANG-05:** Inherited future `ele` preverb data and the potential `ceçamu` branch.
- **LANG-10:** Decisions on the [complete behaviour inventory](conjugation-behaviour-review.md).
- **DATA-04:** Review generated combinations absent from the original dump before
  approving them. Generator coverage is not linguistic approval.
- **DATA-05:** Confirm the preserved negative-particle prefix convention such as
  `komot giğur`; it has not been silently changed.
- **DATA-06:** Decide whether to change the generator's displayed pronouns. The
  admin baseline and approved exports already use the dump's pronouns and passed
  full import comparison. Live publication remains to be verified above.

The dated reports and original checklist remain in [history](history/README.md).

## Later improvements

These are not missing migration pages or requirements for the current workflow:

- A read-only whole-database comparison against rule outputs, with a downloadable
  mismatch report and recorded correction context; no button exists yet.
- A one-step latest-data preview; current preview uses an explicit export snapshot.
- Signed Windows distribution and update notifications.
- Import mapping tools and multi-editor synchronization, if needed later.
- Complete the Laz translations in `draftGuides` in
  `apps/web/src/site/phrases.ts` when the author supplies them. Keep all remaining
  prompts and placeholders.
- Native mobile clients remain deferred.
