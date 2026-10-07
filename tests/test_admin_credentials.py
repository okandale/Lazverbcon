"""Saved-token isolation, publication, failure handling and native Windows round trip."""

import sys
import time
import uuid
from dataclasses import asdict

import pytest
from fastapi.testclient import TestClient
from laz_admin import app as admin_app
from laz_admin.credentials import WindowsCredentials, credential_target, validate_token
from laz_admin.store import Store


class MemoryCredentials:
    available = True

    def __init__(self):
        self.values = {}

    def get(self, target):
        return self.values.get(target)

    def save(self, target, token):
        self.values[target] = token

    def delete(self, target):
        self.values.pop(target, None)


@pytest.fixture
def editing_project(tmp_path, verb):
    store = Store(tmp_path / "project")
    store.save_entry(asdict(verb("doguru")), "Author", "Existing verb")
    return store


def client(store, credentials):
    instance = TestClient(
        admin_app.create_app(store, token="session", credentials=credentials),
        base_url="http://127.0.0.1",
    )
    instance.headers["X-Laz-Session"] = "session"
    return instance


def test_saved_tokens_survive_reopen_and_never_enter_project_backups(editing_project):
    credentials = MemoryCredentials()
    secret = "ghp_TestSecretForCredentialIsolation"
    with client(editing_project, credentials) as browser:
        assert browser.post(
            "/api/github-credential", json={"repository": "Owner/Repo", "token": secret}
        ).json() == {"saved": True}
        assert browser.get(
            "/api/github-credential", params={"repository": "owner/repo"}
        ).json() == {"available": True, "saved": True}
        assert (
            browser.get("/api/github-credential", params={"repository": "other/repo"}).json()[
                "saved"
            ]
            is False
        )
        assert secret not in browser.get("/api/status").text
        assert secret not in browser.get("/api/history").text
        assert browser.post("/api/backup", json={}).status_code == 200
    reopened = Store(editing_project.directory)
    with client(reopened, credentials) as browser:
        assert (
            browser.get("/api/github-credential", params={"repository": "owner/repo"}).json()[
                "saved"
            ]
            is True
        )
        assert browser.request(
            "DELETE", "/api/github-credential", json={"repository": "owner/repo"}
        ).json() == {"saved": False}
        assert (
            browser.get("/api/github-credential", params={"repository": "owner/repo"}).json()[
                "saved"
            ]
            is False
        )
    for path in editing_project.directory.rglob("*"):
        if path.is_file():
            assert secret.encode() not in path.read_bytes(), path


def test_same_repository_in_a_different_project_does_not_use_saved_token(editing_project, tmp_path):
    credentials = MemoryCredentials()
    target = credential_target(editing_project.status()["project"], "owner/repo")
    credentials.save(target, "ghp_ProjectScopedSecret")
    other = Store(tmp_path / "another")
    with client(other, credentials) as browser:
        assert not browser.get(
            "/api/github-credential", params={"repository": "owner/repo"}
        ).json()["saved"]


def test_publish_reads_saved_token_only_on_server_and_accepts_manual_override(
    editing_project, monkeypatch
):
    credentials = MemoryCredentials()
    credentials.save(
        credential_target(editing_project.status()["project"], "owner/repo"), "ghp_SavedSecret"
    )
    used = []

    def fake_publish(store, filename, actor, token, repository, branch):
        used.append(token)
        return {"release": "test-release"}

    monkeypatch.setattr(admin_app, "publish", fake_publish)
    with client(editing_project, credentials) as browser:
        for supplied, expected in [("", "ghp_SavedSecret"), ("ghp_Override", "ghp_Override")]:
            response = browser.post(
                "/api/publish",
                json={
                    "filename": "test.zip",
                    "actor": "Author",
                    "token": supplied,
                    "repository": "owner/repo",
                    "branch": "main",
                },
            )
            assert response.status_code == 200
            deadline = time.monotonic() + 3
            while browser.get("/api/job").json()["state"] == "running":
                assert time.monotonic() < deadline
                time.sleep(0.01)
            assert used[-1] == expected
            assert expected not in browser.get("/api/job").text
        assert (
            credentials.get(credential_target(editing_project.status()["project"], "owner/repo"))
            == "ghp_SavedSecret"
        )  # A one-off override does not silently replace the saved token.
        response = browser.post("/api/publish", json={"repository": "different/repo", "token": ""})
        assert response.status_code == 400


def test_credential_routes_require_local_authenticated_session(editing_project):
    credentials = MemoryCredentials()
    with client(editing_project, credentials) as browser:
        browser.headers.pop("X-Laz-Session")
        assert browser.get("/api/github-credential").status_code == 403
        assert browser.post("/api/github-credential", json={}).status_code == 403
        assert browser.request("DELETE", "/api/github-credential", json={}).status_code == 403
        browser.headers["X-Laz-Session"] = "session"
        assert (
            browser.post(
                "/api/github-credential", headers={"Origin": "https://other.test"}, json={}
            ).status_code
            == 403
        )
        assert (
            browser.get("/api/github-credential", headers={"Host": "other.test"}).status_code == 403
        )


def test_storage_failure_has_no_plaintext_fallback(editing_project):
    class FailedCredentials(MemoryCredentials):
        def save(self, target, token):
            raise ValueError("Windows Credential Manager failed (code 5)")

    credentials = FailedCredentials()
    with client(editing_project, credentials) as browser:
        response = browser.post(
            "/api/github-credential",
            json={"repository": "owner/repo", "token": "ghp_DoNotPersistOrEchoThis"},
        )
        assert response.status_code == 400
        assert "ghp_DoNotPersistOrEchoThis" not in response.text
        assert not credentials.values
        assert not editing_project.settings()


@pytest.mark.parametrize("token", ["", None, "ghp_secret\nAuthorization: invalid", "ghp_秘密"])
def test_invalid_tokens_are_rejected_without_echoing_them(token):
    with pytest.raises(ValueError) as error:
        validate_token(token)
    assert "ghp_" not in str(error.value)


@pytest.mark.skipif(sys.platform != "win32", reason="Native Credential Manager needs Windows")
def test_native_windows_credential_round_trip():
    credentials = WindowsCredentials()
    target = credential_target(str(uuid.uuid4()), "lazuri-admin-test/credential-test")
    secret = "ghp_DummyWindowsRoundTrip_NotARealToken"
    try:
        assert credentials.get(target) is None
        credentials.save(target, secret)
        assert WindowsCredentials().get(target) == secret
        credentials.save(target, "ghp_ReplacementDummy")
        assert credentials.get(target) == "ghp_ReplacementDummy"
    finally:
        credentials.delete(target)
    assert credentials.get(target) is None
    credentials.delete(target)  # Forget is idempotent.
