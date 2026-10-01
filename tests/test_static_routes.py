"""Regression coverage for Pages canonicalizing index.html rewrites to home."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.build_static import write_page_routes  # noqa: E402


@pytest.mark.parametrize(
    "route",
    [
        "conjugator",
        "verbs",
        "about",
        "events",
        "feedback",
        "resources",
        "keyboard",
        "keyboard/windows",
        "keyboard/mac",
        "keyboard/android",
        "keyboard/iphone",
        "keyboard/computer",
        "keyboard/phone",
        "resources/phrase-guide",
        "resources/phrase-guide/hopa",
        "resources/phrase-guide/pazar",
        "resources/phrase-guide/ardesen",
        "resources/phrase-guide/findikli-arhavi",
    ],
)
def test_public_pages_have_native_clean_url_assets(tmp_path, route):
    shell = b'<html><div id="root"></div><script src="/assets/app.js"></script></html>'
    (tmp_path / "index.html").write_bytes(shell)
    write_page_routes(tmp_path)
    # Pages serves /path.html at /path. It must not need a rewrite to index.html,
    # which Cloudflare canonicalizes to / and loses the route.
    assert (tmp_path / f"{route}.html").read_bytes() == shell
    assert (tmp_path / "404.html").read_bytes() == shell
    assert "index.html" not in (tmp_path / "_redirects").read_text()
    assert not (tmp_path / "missing-page.html").exists()
    assert not (tmp_path / "data/missing.json").exists()
