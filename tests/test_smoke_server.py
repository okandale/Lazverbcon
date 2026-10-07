"""Startup resets are retried without hiding persistent server failures."""

import importlib.util
from pathlib import Path
from unittest.mock import Mock

import pytest

spec = importlib.util.spec_from_file_location(
    "smoke_server", Path(__file__).parents[1] / "scripts/smoke_server.py"
)
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)


def test_wait_for_health_retries_startup_connection_reset(monkeypatch):
    monkeypatch.setattr(smoke.time, "sleep", lambda _: None)
    fetch = Mock(side_effect=[ConnectionResetError("Starting"), '{"status":"ok"}'])
    assert smoke.wait_for_health(fetch) == {"status": "ok"}
    assert fetch.call_count == 2


def test_wait_for_health_reports_persistent_connection_failure(monkeypatch):
    monkeypatch.setattr(smoke.time, "sleep", lambda _: None)
    fetch = Mock(side_effect=ConnectionResetError("Unavailable"))
    with pytest.raises(ConnectionResetError, match="Unavailable"):
        smoke.wait_for_health(fetch)
    assert fetch.call_count == 30
