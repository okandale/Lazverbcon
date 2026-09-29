from fastapi.testclient import TestClient
from laz_api.app import create_app
from laz_api.website import PUBLIC_PAGES


def test_public_routes_and_missing_assets(tmp_path, monkeypatch):
    (tmp_path / "index.html").write_text('<html><div id="root"></div></html>')
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets" / "main.js").write_text("// built bundle")
    monkeypatch.setenv("LAZ_WEB_DIST", str(tmp_path))
    with TestClient(create_app()) as client:
        for route in PUBLIC_PAGES:
            response = client.get(f"/{route}?lang=tr")
            assert response.status_code == 200, route
            assert 'id="root"' in response.text
        assert client.get("/keyboard/mac/").status_code == 200
        assert client.get("/assets/main.js").text == "// built bundle"
        for path in ("/assets/missing.js", "/images/missing.jpg", "/api/typo", "/api/v1/typo"):
            response = client.get(path)
            assert response.status_code == 404
            assert 'id="root"' not in response.text
        response = client.get("/unknown-page")
        assert response.status_code == 404 and 'id="root"' in response.text
        old = client.get("/v2/verbs?lang=tr&q=osinapu", follow_redirects=False)
        assert old.status_code == 308
        assert old.headers["location"] == "/verbs?lang=tr&q=osinapu"
        assert client.get("/v2/verb/1/TVE").status_code == 410
        assert client.head("/resources/phrase-guide/hopa").status_code == 200
        assert client.post("/resources").status_code == 405
