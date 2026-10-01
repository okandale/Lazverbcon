"""Build a self-contained Cloudflare Pages directory without an API server."""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from laz_api.static_export import export_catalog
from laz_api.website import PUBLIC_PAGES

ROOT = Path(__file__).resolve().parents[1]


def write_page_routes(site):
    """Use Pages' native clean-URL files instead of rewriting to index.html.

    Pages canonicalizes /index.html to /. A 200 rewrite to that filename can
    therefore send the browser back to the home page and lose its route.
    /conjugator.html is served at /conjugator without changing the requested page.
    """
    shell = (site / "index.html").read_bytes()
    for route in sorted(PUBLIC_PAGES):
        if route:
            page = site / f"{route}.html"
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_bytes(shell)
    # Keep real 404s for missing pages, data and assets, instead of SPA fallback.
    (site / "404.html").write_bytes(shell)
    (site / "_redirects").write_text("/v2/verbs /verbs 301\n")


def build(database, output, data=None):
    output = output.resolve()
    marker = ".laz-static-build"
    if output.exists() and not (output / marker).is_file():
        raise ValueError(f"Refusing to replace a directory not created by this builder: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="pages-build-", dir=output.parent) as work:
        work = Path(work)
        if data is None:
            data = work / "export"
            print("Exporting the verified catalog…", flush=True)
            print(json.dumps(export_catalog(database, data), indent=2), flush=True)
        manifest = json.loads((data / "manifest.json").read_text())
        if manifest["schema_version"] != 1 or manifest["catalog"]["coverage"] != "full":
            raise ValueError("Public builds require a complete, supported static release")
        for filename, expected in manifest["files"].items():
            content = (data / filename).read_bytes()
            if hashlib.sha256(content).hexdigest() != expected["sha256"]:
                raise ValueError(f"Static data integrity check failed: {filename}")
        site = work / "site"
        env = dict(os.environ, VITE_STATIC_DATA=f"/data/{manifest['release']}")
        subprocess.run(["pnpm", "exec", "tsc", "-b"], cwd=ROOT / "apps/web", env=env, check=True)
        subprocess.run(
            ["pnpm", "exec", "vite", "build", "--outDir", str(site)],
            cwd=ROOT / "apps/web",
            env=env,
            check=True,
        )
        shutil.copytree(data, site / "data" / manifest["release"])
        write_page_routes(site)
        (site / "_headers").write_text(
            "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
            "/data/*\n  Cache-Control: public, max-age=31536000, immutable\n"
            "/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n"
        )
        files = [p for p in site.rglob("*") if p.is_file()]
        if len(files) > 20000 or any(p.stat().st_size > 25 * 1024 * 1024 for p in files):
            raise ValueError("Site exceeds Cloudflare Pages upload limits")
        report = {
            "release": manifest["release"],
            "files": len(files),
            "bytes": sum(p.stat().st_size for p in files),
        }
        (site / marker).write_text(json.dumps(report, indent=2) + "\n")
        # Keep the previous build until its replacement is complete.
        backup = work / "previous"
        if output.exists():
            output.rename(backup)
        try:
            site.rename(output)
        except BaseException:
            if backup.exists():
                backup.rename(output)
            raise
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--database", type=Path)
    source.add_argument("--data", type=Path, help="Reuse an existing, unchanged export")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/pages")
    args = parser.parse_args()
    print(json.dumps(build(args.database, args.output, args.data), indent=2))
