# Local admin app

The admin app keeps one authoritative SQLite project on the editor's computer.
The public website continues to run from static files on Cloudflare Pages.
Editing, generating and reviewing work offline. Publishing needs internet access.

## Windows: download and run

After this code is pushed to `codex/static-export`, the **Windows Admin** GitHub
Actions workflow builds and tests a Windows package. In the repository's
**Actions → Windows Admin**, open the successful run and download the
**Lazuri-Admin-Windows** artifact. Extract the entire ZIP into a program folder.

Double-click **Lazuri Admin.exe**. It opens the editor in your browser. Keep the
program window open while editing; **Stop app** closes the local service and its
website preview. Python, Docker, Node and Git are not needed on that computer.
The executable is unsigned; distributing a signed installer is future work.

The project lives in `%LOCALAPPDATA%\LazuriAdmin`, separately from the program.
To update the app, stop it and extract the newer package into a new program
folder. Open the new executable. It uses the same project without regenerating
its contents. Unsupported database versions are refused without modifying them.
There is no automatic updater or multi-user synchronization.

**Build status:** the source workflow is included; a Windows build and packaged
smoke test must succeed before distributing an EXE. macOS source tests do not
establish that the Windows executable works.

## Start a project

1. Enter your name for the change history.
2. Choose **Import maintainer baseline** on Overview. This is available only in
   an empty project. Alternatively, restore an existing admin backup.
3. In **Settings**, save your editor name and an additional backup folder if wanted.

The bundled baseline comes from the reconciled `lazverbcon2.dump` fixture and
its original pronoun table: 327 verbs, 580,129 grammatical requests and 483,471
form records. The 98,676 rejected source rows are retained as unsupported requests.
Original row IDs are retained as provenance. Generated combinations absent from
the source are **not** automatically approved. This produces fewer public analyses
than the previous full generated catalog, deliberately.

The pronoun snapshot is `apps/admin/src/laz_admin/data/pronouns.json`, extracted
from the dump's 144 pronoun rows. It fixes display data for approved exports;
the Python rule modules retain their existing pronouns for proposals, so differences
remain visible for review. The private dump is not bundled or uploaded.

## Edit, generate and review

- **Verbs:** search an infinitive or meaning, open a verb, and edit its metadata,
  principal parts or dialects. Use grammatical filters to narrow the form list. Metadata changes take effect immediately in the
  master and are logged; a new export/publication is still required for the site.
- **Add conjugation / Edit:** set the grammatical analysis, spelling alternatives,
  frame and displayed pronouns. Save creates a proposal. To change an existing
  analysis, add its replacement and propose removal of the old request.
- **Generate proposals:** runs the Python engine for that verb. It never replaces
  approved forms. Identical linguistic results are skipped even when provenance
  differs. Generator limitations still apply to generation, while manual forms
  can use any combination within the supported feature schema.
- **Review:** compare approved and proposed values, then approve or reject selected
  proposals. Selection covers the displayed page (100 requests). Stale proposals
  cannot be approved after their entry or approved forms have changed; reject them
  and create a fresh proposal. To adjust a proposal, reject it and create the revised
  form from the verb page.
- **History:** every approved edit and rejection records the editor, time and
  reason. Form history also includes its proposer and import/generation batch.
  Undo writes another event and refuses to overwrite subsequent edits.

Manual edits change the master database, **not** Python rules. A recurring
correction can later be incorporated into the engine and reviewed as proposals.
Editor names are local attribution, not authenticated identities.

### Import files

Import previews the file before creating proposals. Existing verb IDs must be
used. A malformed file is rejected without partially staging it. Use UTF-8,
at most 20 MiB and 10,000 grammatical requests per file.

CSV uses these columns; repeated entry/feature combinations are alternatives
for one request. Include the entire intended set, because approval replaces that
request's alternatives. Blank `object` means no object; booleans are `true`/`false`.
Unspecified grammatical fields take the same defaults as the conjugator.

```csv
entry_id,dialect,subject,object,tense,mood,derivation,applicative,causative,optional_preverb,optional_prefix,spelling,frame,subject_pronoun,object_pronoun,rule
```

JSON also supports unsupported results and removal (`value: null`). Example
shape only; substitute a real entry ID and linguistically verified content:

```json
[
  {
    "entry_id": "verb-0001",
    "features": {"dialect": "AS", "subject": "1sg"},
    "value": {
      "status": "ok",
      "forms": [{"spelling": "example", "frame": "Nominative", "subject_pronoun": "ma", "object_pronoun": ""}],
      "source": "Author review"
    }
  }
]
```

## Backups and handing over editing

The app creates a consistent daily SQLite backup before writes, retaining the
latest 14 daily backups. **Back up now** creates a retained manual backup.
Before-import, before-restore and after-publish backups are also retained.
Choose OneDrive, another synchronized folder or external storage as an additional
destination for completed backups. The working SQLite file stays local.

**Restore** replaces the whole project, including entries, proposals, history,
preferences and publication state. The app validates the backup and saves the
current project first. A backup made by this app is required; the raw PostgreSQL
dump and old generated catalog are different formats.

For handover: back up after the last publication, send that backup privately,
stop editing on the old machine, and restore it on the new machine. The recipient
should change the editor name and backup folder. Keep one master editor at a time.
GitHub's public static export cannot recover proposals or editorial history.

## Export and preview

In **Publish**, choose **Export approved snapshot**. Each export has a project ID,
revision, content identifier and SHA-256 checksum. Pending proposals and history
are omitted. **Preview website** starts a separate localhost website using that
snapshot. It works offline and closes with the admin app.

The export is a ZIP of JSON shards and search indexes. Availability in the public
conjugator comes from approved forms, allowing manually approved exceptions and
new verbs even when the generator cannot produce them. No SQLite file reaches
the public deployment.

## Connect GitHub and Cloudflare once

The connected Pages repository is currently **lewisccz/Lazverbcon**, branch
**codex/static-export**. Get this application code into that fork first. Pushing
only to `okandale/Lazverbcon` does not update the fork or its website.

1. In Pages build settings, retain **Framework: None**, an empty root directory,
   and output directory **artifacts/pages**. Replace the generating build command
   with:

   ```bash
   python -m venv .venv && .venv/bin/pip install -r requirements.lock && .venv/bin/pip install --no-deps . && pnpm --dir apps/web install --frozen-lockfile && .venv/bin/python scripts/build_published.py
   ```

2. Keep `PYTHON_VERSION=3.14`, `NODE_VERSION=24`, `PNPM_VERSION=11.25.0` and
   `SKIP_DEPENDENCY_INSTALL=1`. Keep existing feedback configuration unchanged.
3. In the admin's Settings, save repository `lewisccz/Lazverbcon` and branch
   `codex/static-export`. Use a GitHub fine-grained token authorized for that
   public repository, with **Contents: read and write**. Enter it in Publish;
   it is used for that operation and is never saved to settings or the database.
4. Export, preview, confirm the destination and click **Publish to GitHub**.
5. Check the Cloudflare deployment result, then test the conjugator and reverse
   lookup on the test domain. A successful upload is not proof of deployment.

Publishing uploads the approved ZIP as a GitHub Release asset and commits the
small pointer **published/catalog.json** to the chosen branch. The pointer contains
the asset URL and checksum. That commit triggers Pages. The build downloads and
verifies the exact export and builds the public UI; it never regenerates forms.

Before the first publication, the new build command fails clearly because no
pointer exists; the previously deployed site stays available. Publish the first
export to trigger the complete build. Don't keep the old generating command:
that would deploy generator output instead of approved edits.

Publication checks the previous remote release and GitHub file SHA before updating
the pointer. An out-of-date restored database cannot overwrite a newer publication.
If the upload succeeded but local bookkeeping was interrupted, republishing the
same export verifies the remote checksum and recovers the local publication state.
Other conflicts require the current master backup. A failed pointer update can
leave an unused GitHub Release, but does not change the deployed site's pointer.
To roll the public site back, publish an earlier export from the current master
project; this records a publication event without rolling back the working database.

The first live publication and Windows package run remain deployment checks;
automated tests use a fake GitHub service and do not send credentials or alter Pages.

## Run from source

From the repository root, after installing Python dependencies and the editable
package (`python -m pip install -r requirements.lock` and `python -m pip install --no-deps -e .`):

```bash
pnpm --dir apps/web install --frozen-lockfile
python scripts/build_admin_preview.py
lazadmin
```

Activate your virtual environment first. On macOS/Linux, `.venv/bin/lazadmin`
also works directly. `--data-dir artifacts/admin-prototype` selects a separate
development project, and `--no-browser` prints the authenticated launch URL.
On macOS the default data folder is `~/Library/Application Support/LazuriAdmin`;
on Linux it is `$XDG_DATA_HOME/lazuri-admin` or `~/.local/share/lazuri-admin`.

Development checks:

```bash
python -m pytest -q tests/test_admin.py
python scripts/verify_admin_baseline.py artifacts/admin-prototype
python scripts/admin_static_test_cases.py artifacts/admin-static-test
LAZ_ADMIN_STATIC_TEST_DIR=../../artifacts/admin-static-test pnpm --dir apps/web exec vitest run src/api/editorial.integration.test.mjs
```

Baseline verification expects a freshly imported project, before linguistic edits.
It compares every request's status, spellings, frames and pronouns. The browser
integration checks a new verb and a generator-disallowed exception across forward
lookup, options, reverse lookup and suggestions, and verifies draft exclusion.

The modules are separated by purpose: `store.py` owns transactions and history;
`publish.py` owns approved snapshots and GitHub; `archive.py` verifies release ZIPs;
`preview.py` serves previews; `app.py` exposes the protected loopback API;
`launcher.py` owns persistent paths, instance locking and process lifetime.
The admin UI is plain JavaScript/CSS and is bundled with the Python package.
