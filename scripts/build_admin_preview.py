"""Build the public UI once for offline previews inside the packaged admin."""

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    subprocess.run(
        [shutil.which("pnpm") or "pnpm", "exec", "tsc", "-b"], cwd=ROOT / "apps/web", check=True
    )
    subprocess.run(
        [
            shutil.which("pnpm") or "pnpm",
            "exec",
            "vite",
            "build",
            "--outDir",
            str(ROOT / "artifacts/admin-public"),
        ],
        cwd=ROOT / "apps/web",
        check=True,
        env={**os.environ, "VITE_STATIC_DATA": "/data/current"},
    )
