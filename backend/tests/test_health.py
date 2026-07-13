"""Tests for the health endpoint and app wiring (Issue #4)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_ok() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["version"] == "0.0.1"
    assert "env" in body


def test_openapi_available() -> None:
    assert client.get("/openapi.json").status_code == 200
