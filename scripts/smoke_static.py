"""Check the actual host's routing after deploying a static release."""

import argparse
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import urlopen

from laz_api.website import PUBLIC_PAGES


def check(base_url):
    base_url = base_url.rstrip("/")
    checked = 0
    for route in sorted(PUBLIC_PAGES):
        path = f"/{route}"
        for suffix in ("", "/") if route else ("",):
            with urlopen(f"{base_url}{path}{suffix}?lang=en", timeout=30) as response:
                destination = urlsplit(response.url)
                assert response.status == 200, (path, response.status)
                assert (destination.path.rstrip("/") or "/") == path, (
                    f"{path}{suffix} redirected to {destination.path}"
                )
                assert destination.query == "lang=en", f"Query lost for {path}"
                assert 'id="root"' in response.read().decode(), f"Missing app shell at {path}"
                checked += 1
    for path in ("/missing-page", "/assets/missing.js", "/data/missing.json", "/api/v1/verbs"):
        try:
            with urlopen(base_url + path, timeout=30) as response:
                raise AssertionError(f"Expected 404 at {path}; got {response.status}")
        except HTTPError as error:
            assert error.code == 404, (path, error.code)
    print(f"Passed: {checked} page URLs retain their routes and queries; missing URLs return 404.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Public deployment or a local Cloudflare Pages emulator")
    check(parser.parse_args().url)
