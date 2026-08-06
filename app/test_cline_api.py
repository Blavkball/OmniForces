from fastapi.testclient import TestClient
from app.main import app
from app.security import verify_api_key


def test_cline_orchestrate_endpoint():
    app.dependency_overrides[verify_api_key] = lambda: True
    client = TestClient(app)

    response = client.post(
        "/cline/orchestrate",
        json={
            "task_description": "Coordinate release planning",
            "team": ["Forge", "QA Engineer"],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "Coordinate release planning" in body["plan"]
    assert body["team"] == ["Forge", "QA Engineer"]

    app.dependency_overrides.clear()
