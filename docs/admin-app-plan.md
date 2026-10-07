# Local admin app: implementation plan

Proposed on 2 October 2026. Implementation is now in `apps/admin`; see the
[current user guide and deployment checks](admin-app.md). This document records
the original plan. The delivered UI uses bundled JavaScript/CSS rather than a
second React build. Imports use explicit documented columns rather than a mapping
wizard. Proposal adjustments use reject-and-replace. Windows package execution
passed in CI on 7 October 2026. Interactive Windows use and a live GitHub/Pages
publication still need verification on their target systems.

## Recommended setup

- Keep one repository, with separate public and admin interfaces.
- Keep the existing Python engine and use FastAPI for the local admin service.
- Build the admin interface in React/TypeScript, matching the existing frontend.
- Package the program, Python dependencies and built web assets for Windows.
- Distribute a versioned ZIP containing `Lazuri Admin.exe` and its supporting
  files. Double-clicking the executable starts a localhost-only service and opens
  the browser. Provide a visible stop control and prevent duplicate instances.
- End users should not need Python, Node, Docker, Git or an always-running server
  to edit and export a project. Source commands remain available for development.
- Build and test the Windows package on a Windows CI runner. Local macOS tests
  cannot establish that the packaged executable works on Windows.

Use PyInstaller's directory bundle initially. A native desktop shell and a single
self-extracting executable add packaging work without improving the editing flow.

## Data and application updates

Store the master SQLite database, history, backups and preferences outside the
installation, under the user's local application-data directory. Support explicit
project backup/export and restoration onto another computer.

Updating the app means downloading the next release and replacing its program
folder. On opening a project, check its schema version, back it up before any
required migration, and refuse unsupported newer schemas. An app update must
never regenerate or replace approved forms. Database restoration is separate
from reinstalling an older executable.

Start with manual versioned downloads; add an update notification later. Do not
make development-branch updates or network availability a startup requirement.

## Editing and approval

The master database becomes authoritative for approved linguistic content.

1. Seed it from the latest maintainer dump, including its pronoun table and
   original record provenance. Preserve the reviewed mapping ledger. Label forms
   found only in the wider generated catalog as unreviewed predictions.
2. Add/edit verbs, dialect assignments, principal parts and conjugation analyses.
3. Generate proposals for selected verbs or constructions. Import documented
   JSON/CSV formats with a preview and explicit field mapping; reject malformed
   input without partially applying it. Replacing a whole project is a separate
   backup/restore action, not an ordinary conjugation import.
4. Compare proposals with approved data, including alternative spellings,
   grammatical features, frames and pronouns. The author can accept, edit or
   reject them. Generator disagreement is visible but does not veto an approved
   exception within the supported feature schema.
5. Log additions, edits, removals, approvals and reversals in the same transaction
   as the change. Record actor name, time, previous/new values, source or reason,
   and import/generation batch. Undo creates a new history event.
6. Long generation/import/export jobs show progress and can be cancelled safely.

An actor name in a local application is attribution, not verified authentication.
Loopback binding, session protection and origin/host checks should prevent other
websites from using the local editing API.

## Publishing

- Publishing takes a consistent snapshot of approved records and builds the
  static files and search indexes from that snapshot.
- Draft edits stay out of the release. Record the project revision, application
  version, checksums and included changes so a release can be traced or restored.
- Replace the exporter's rule-derived eligibility checks with availability based
  on approved data. A manually approved form must work in forward lookup, reverse
  lookup, suggestions and the options UI even if the generator rejects it.
- Package prebuilt public-site assets with the publisher, or build them in CI;
  the author's Windows computer should not need Node to publish.
- Keep the existing GitHub-to-Cloudflare Pages connection. Change its build to
  consume a pinned approved export instead of running a full conjugation rebuild.
  A versioned GitHub release asset plus a checksum-pinned release manifest is the
  proposed delivery mechanism. Verify the complete deployment path before adding
  a one-click publishing action. Public assets contain no admin history or secrets.
- Editing works offline; GitHub upload and website deployment require internet.
  Publication credentials are supplied by the user, never included in the app.

## Sharing between the owner and author

First version: one designated master editor at a time. Either person can run the
app; a project backup carries the database and history for a deliberate handover.
The app creates consistent SQLite backups rather than asking users to copy an
open database file. This is not automatic synchronisation.

If simultaneous independent editing becomes necessary, add exchangeable change
bundles with base revisions and conflict review. Do not silently merge diverged
database copies or use a live SQLite file in a shared synchronisation folder.

## Implementation order and completion checks

1. **Master data and history:** schema, dump import, provenance, drafts/approval,
   backups and undo. Verify baseline spelling/frame/status parity and pronouns.
2. **Working editor:** search, inspect, edit and generate a selected verb; staged
   JSON/CSV import; review differences and history. Verify approved corrections
   survive repeated generation, restart and backup restoration.
3. **Approved-data export:** support editorial entries and exceptions, omit
   drafts, preview the public site and compare its results with the snapshot.
4. **Windows distribution:** build the packaged launcher and assets in Windows CI;
   test startup, persistence, Unicode paths, long jobs and a schema upgrade on a
   machine without a development environment. User verifies a first Windows build.
5. **Publishing integration:** transfer and pin approved releases through GitHub,
   update the Pages build, then verify deployment and rollback on the test domain.

Keep the existing public deployment working while these pieces are developed.
Outstanding linguistic decisions remain in the migration checklist; implementation
must not silently resolve them by treating generated predictions as approved.
