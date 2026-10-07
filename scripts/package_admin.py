"""Run on Windows to produce the standalone admin directory bundle."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    if sys.platform != "win32":
        raise SystemExit("Build Windows packages on Windows (see the Windows Admin workflow).")
    if not (ROOT / "artifacts/admin-public/index.html").is_file():
        raise SystemExit("Run scripts/build_admin_preview.py first")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--clean",
            "--onedir",
            "--name",
            "Lazuri Admin",
            # Editable installs use import hooks that PyInstaller cannot analyze.
            "--paths",
            str(ROOT / "apps/admin/src"),
            "--paths",
            str(ROOT / "apps/api/src"),
            "--paths",
            str(ROOT / "packages/engine/src"),
            "--collect-submodules",
            "laz_engine.paradigms",
            "--collect-data",
            "laz_engine",
            "--collect-data",
            "laz_admin",
            "--copy-metadata",
            "lazverbcon",
            "--add-data",
            f"{ROOT / 'tests/fixtures/maintainer-release.jsonl.gz'};seed",
            "--add-data",
            f"{ROOT / 'artifacts/admin-public'};public-preview",
            str(ROOT / "scripts/run_admin.py"),
        ],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()
