from fastapi.testclient import TestClient

from app.main import app, create_app


def test_create_app_returns_a_fastapi_application() -> None:
    created = create_app()

    assert created.title == "Employer Account Portal API"


def test_app_starts_and_serves_openapi_schema() -> None:
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Employer Account Portal API"
