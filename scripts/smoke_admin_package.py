"""Exercise the real bundled executable without installing Python on its PATH."""

import argparse
import json
import os
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("executable", type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="Lazuri Unicode ç-") as temp:
        log = Path(temp) / "launcher.log"
        with log.open("w") as output:
            child = subprocess.Popen(
                [str(args.executable.resolve()), "--data-dir", temp, "--no-browser"],
                stdout=output,
                stderr=output,
                env={**os.environ, "PYTHONPATH": ""},
            )
        try:
            match = None
            for _ in range(120):
                match = re.search(
                    r"(http://127.0.0.1:\d+)/#session=(\S+)",
                    log.read_text(encoding="utf-8", errors="replace"),
                )
                if match:
                    break
                if child.poll() is not None:
                    raise RuntimeError(log.read_text(encoding="utf-8", errors="replace"))
                time.sleep(0.25)
            if not match:
                raise RuntimeError("Packaged launcher did not start")
            root, token = match.groups()
            headers = {"X-Laz-Session": token, "Content-Type": "application/json"}

            def api(path, body=None):
                with urllib.request.urlopen(
                    urllib.request.Request(
                        root + "/api/" + path,
                        data=json.dumps(body).encode() if body is not None else None,
                        headers=headers,
                    ),
                    timeout=30,
                ) as response:
                    return json.load(response)

            for attempt in range(60):
                try:
                    status = api("status")
                    break
                except urllib.error.URLError:
                    if attempt == 59:
                        raise
                    time.sleep(0.25)
            assert (
                status["seed_available"] and status["preview_available"] and status["entries"] == 0
            )
            assert status["credential_storage_available"]
            # A dummy token tests the actual Windows vault, never a real GitHub account.
            credential_repo = "lazuri-admin-test/package-smoke"
            assert api(
                "github-credential",
                {"repository": credential_repo, "token": "ghp_PackageSmoke_NotARealToken"},
            ) == {"saved": True}
            assert api("github-credential?repository=" + credential_repo)["saved"]
            with urllib.request.urlopen(root, timeout=15) as response:
                assert b"Lazuri Admin" in response.read()
            api(
                "entry",
                {
                    "actor": "Package test",
                    "entry": {
                        "id": "smoke",
                        "infinitive": "doguru",
                        "english": "to die",
                        "turkish": "ölmek",
                        "verb_class": "TVM",
                        "source_row": 0,
                        "variants": [{"form": "gurun", "dialects": ["AS"]}],
                    },
                },
            )
            api("generate", {"actor": "Package test", "entry_id": "smoke", "profile": "core"})
            for _ in range(120):
                job = api("job")
                if job["state"] != "running":
                    break
                time.sleep(0.25)
            assert job["state"] == "complete", job
            proposals = api("proposals")["proposals"]
            assert proposals
            api("review", {"actor": "Package test", "ids": [proposals[0]["id"]], "approve": True})
            assert api("status")["records"] == 1
            api("export", {"actor": "Package test"})
            for _ in range(120):
                job = api("job")
                if job["state"] != "running":
                    break
                time.sleep(0.25)
            assert job["state"] == "complete", job
            api("preview", {"filename": job["result"]["filename"]})
            for _ in range(120):
                job = api("job")
                if job["state"] != "running":
                    break
                time.sleep(0.25)
            assert job["state"] == "complete", job
            with urllib.request.urlopen(job["result"]["preview_url"], timeout=15) as response:
                assert response.status == 200
            with urllib.request.urlopen(
                urllib.request.Request(root + "/api/backup", data=b"{}", headers=headers),
                timeout=15,
            ) as response:
                assert Path(json.load(response)["path"]).is_file()
            with urllib.request.urlopen(
                urllib.request.Request(root + "/api/shutdown", data=b"{}", headers=headers),
                timeout=15,
            ):
                pass
            child.wait(timeout=15)
            assert child.returncode == 0
            # Reopening the same project must preserve approved edits and history.
            with log.open("w") as output:
                child = subprocess.Popen(
                    [str(args.executable.resolve()), "--data-dir", temp, "--no-browser"],
                    stdout=output,
                    stderr=output,
                    env={**os.environ, "PYTHONPATH": ""},
                )
            for attempt in range(120):
                match = re.search(
                    r"(http://127.0.0.1:\d+)/#session=(\S+)",
                    log.read_text(encoding="utf-8", errors="replace"),
                )
                if match:
                    root, fresh_token = match.groups()
                    assert fresh_token != token
                    headers["X-Laz-Session"] = fresh_token
                    try:
                        status = api("status")
                        break
                    except urllib.error.URLError:
                        pass
                if child.poll() is not None or attempt == 119:
                    raise RuntimeError("Packaged app did not reopen its project")
                time.sleep(0.25)
            assert status["records"] == 1 and status["entries"] == 1
            assert any(event["entity"] == "record" for event in api("history"))
            assert api("github-credential?repository=" + credential_repo)["saved"]
            with urllib.request.urlopen(
                urllib.request.Request(
                    root + "/api/github-credential",
                    method="DELETE",
                    data=json.dumps({"repository": credential_repo}).encode(),
                    headers=headers,
                ),
                timeout=15,
            ) as response:
                assert json.load(response) == {"saved": False}
            assert not api("github-credential?repository=" + credential_repo)["saved"]
            api("shutdown", {})
            child.wait(timeout=15)
            assert child.returncode == 0
        finally:
            if child.poll() is None:
                child.terminate()
                child.wait(timeout=15)


if __name__ == "__main__":
    main()
