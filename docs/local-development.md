# Local development

The public website and admin are separate apps. Run only the one you are changing.
Local development does not publish anything to GitHub or Cloudflare.

## Clone the current version

Install Git and Node.js 24. Then run:

```bash
git clone --branch codex/static-export https://github.com/okandale/Lazverbcon.git
cd Lazverbcon
npm install --global pnpm@11.25.0
pnpm --dir apps/web install --frozen-lockfile
```

Use your fork's URL if contributing through a fork. `codex/static-export` currently
contains the remake; the repository's default branch may contain the old app.

## Public website: preview approved data

This runs the same static data client used on Cloudflare, with automatic reload
when you save React, CSS or page content. Python and the admin do not need to run.

1. Get an approved export ZIP from the editor. In the admin, use **Publish → Export
   approved snapshot → Download ZIP**. This is the public data ZIP, rather than a
   SQLite project backup.
2. Extract its contents into `apps/web/public/data/preview/`. The file
   `apps/web/public/data/preview/manifest.json` must exist directly in that folder.
3. Create `apps/web/.env.local` containing:

   ```dotenv
   VITE_STATIC_DATA=/data/preview
   ```

4. From the repository root, run:

   ```bash
   pnpm --dir apps/web dev
   ```

5. Open **http://127.0.0.1:5173**. If that port is occupied, use the URL printed
   by Vite.

Edit `apps/web/src/` and save. The browser updates automatically. To preview newer
approved data, replace the extracted export and refresh the browser. Neither the
export folder nor `.env.local` is committed to Git.

Stop the server with **Ctrl+C**. Restart it after changing `.env.local`.

## Python setup: admin or rule development

Install Python 3.14. From the repository root, create and activate a virtual
environment.

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, use Command Prompt and
`.venv\Scripts\activate.bat`; no execution-policy change is required.

In the activated environment:

```bash
python -m pip install -r requirements.lock
python -m pip install --no-deps -e .
```

## Admin: run from source

After both the Node and Python setup above:

```bash
python scripts/build_admin_preview.py
python scripts/run_admin.py --data-dir artifacts/admin-dev
```

The launcher opens an authenticated localhost URL in your browser. Enter your
name, then choose **Import original database** on Overview to load the data
extracted from `lazverbcon2.dump`. A full project backup can instead be restored
through **Backups**.

`artifacts/admin-dev` is a separate development database. The packaged Windows
app's normal project stays in `%LOCALAPPDATA%\LazuriAdmin`. Do not use your editing
master for code experiments.

The admin interface lives in `apps/admin/src/laz_admin/assets/`. Refresh after
saving its JavaScript/CSS/HTML. Stop and restart the launcher after Python changes.
Use **Stop app** or Ctrl+C to stop it. Rebuild the public preview assets with
`python scripts/build_admin_preview.py` after changing the public frontend.

See [the admin guide](admin-app.md) for reviewing proposals, backups and publishing.

## Rules and API: preview generated answers

This mode helps develop the generator without altering approved admin data.
Remove `VITE_STATIC_DATA` from `apps/web/.env.local` before starting it.

In an activated Python terminal at the repository root:

```bash
lazcon serve
```

In another terminal at the repository root:

```bash
pnpm --dir apps/web dev
```

Open **http://127.0.0.1:5173**; API docs are at **http://127.0.0.1:8000/docs**.
Vite forwards `/api` to the local Python service. Frontend saves reload
automatically; restart `lazcon serve` after changing Python code.

Forward conjugation uses rules directly. Reverse lookup needs a catalog, so use
the approved-data preview above when testing the complete public interface.
Rule changes do not change the approved SQLite master; the admin generates
proposals for review.

## Checks before contributing

From the repository root, in the Python environment:

```bash
python -m pytest -q
pnpm --dir apps/web test
pnpm --dir apps/web build
```

The main code locations are:

| Area                    | Folder                            |
| ----------------------- | --------------------------------- |
| Public website          | `apps/web/src/`                   |
| Local admin             | `apps/admin/src/laz_admin/`       |
| Conjugation rules       | `packages/engine/src/laz_engine/` |
| API and static exporter | `apps/api/src/laz_api/`           |

Keep databases, backups, exports and credentials out of commits. Opening a local
preview never publishes the website; publication is a separate admin action.
