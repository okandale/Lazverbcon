"""Check a running release through HTTP, using only the Python standard library."""

import argparse
import json
import re
import time
from urllib.error import URLError
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs="?", default="http://127.0.0.1:8080")
    args = parser.parse_args()
    base = args.url.rstrip("/")

    def fetch(path, payload=None):
        request = Request(
            base + path,
            data=json.dumps(payload).encode() if payload is not None else None,
            headers={"Content-Type": "application/json"} if payload is not None else {},
        )
        with urlopen(request, timeout=3) as response:
            return response.read().decode()

    for attempt in range(30):
        try:
            health = json.loads(fetch("/api/v1/health"))
            break
        except (URLError, TimeoutError):
            if attempt == 29:
                raise
            time.sleep(1)
    assert health["status"] == "ok" and health["source"] == "database", health
    assert health["catalog"]["profile"] == "full", health
    html = fetch("/")
    assert '<div id="root">' in html, "Website shell missing"
    for page in (
        "/conjugator",
        "/verbs",
        "/keyboard/mac",
        "/resources/phrase-guide/hopa",
        "/feedback",
    ):
        assert '<div id="root">' in fetch(page), f"Direct page load failed: {page}"
    assets = re.findall(r'(?:src|href)="(/assets/[^\"]+)"', html)
    assert assets, "Built website assets missing"
    for asset in assets:
        assert fetch(asset), f"Empty asset: {asset}"
    request = {"entry_id": "verb-0232", "dialects": ["AS"], "subject": "1sg"}
    forward = json.loads(fetch("/api/v1/conjugations", request))
    assert len(forward["cells"]) == 1, forward
    cell = forward["cells"][0]
    assert cell["status"] == "ok", cell
    assert any(form["spelling"] == "visinapam" for form in cell["forms"]), cell
    reverse = json.loads(fetch("/api/v1/reverse?q=visinapam"))
    assert any(match["entry"]["id"] == request["entry_id"] for match in reverse["matches"]), reverse
    print("Release smoke check passed: full catalog, website assets, forward and reverse lookup.")


if __name__ == "__main__":
    main()
