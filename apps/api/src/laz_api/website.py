"""Serve public page URLs without turning missing API/assets into HTML successes."""

import re
from pathlib import Path

from starlette.exceptions import HTTPException
from starlette.responses import FileResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

PUBLIC_PAGES = {
    "",
    "conjugator",
    "verbs",
    "events",
    "resources",
    "about",
    "feedback",
    "keyboard",
    *(
        f"keyboard/{platform}"
        for platform in ("windows", "mac", "android", "iphone", "computer", "phone")
    ),
    "resources/phrase-guide",
    *(
        f"resources/phrase-guide/{dialect}"
        for dialect in ("pazar", "ardesen", "findikli-arhavi", "hopa")
    ),
}


class WebsiteFiles(StaticFiles):
    async def get_response(self, path, scope):
        route = path.strip("/")
        if scope["method"] not in ("GET", "HEAD"):
            return await super().get_response(path, scope)
        if route == "v2/verbs":
            query = scope.get("query_string", b"").decode("latin-1")
            return RedirectResponse("/verbs" + (f"?{query}" if query else ""), status_code=308)
        if route in PUBLIC_PAGES:
            return self.page()
        if re.fullmatch(r"v2/verb/[^/]+/[^/]+", route):
            # The old numeric IDs cannot safely be matched to a new lexical identity.
            return self.page(410)
        try:
            return await super().get_response(path, scope)
        except HTTPException as exc:
            if exc.status_code != 404:
                raise
            # Never disguise an API typo or missing static asset as a page response.
            if route.split("/")[0] in {"api", "assets", "images"} or Path(route).suffix:
                raise
            return self.page(404)

    def page(self, status_code=200):
        return FileResponse(
            Path(self.directory) / "index.html",
            status_code=status_code,
            headers={"Cache-Control": "no-cache"},
        )
