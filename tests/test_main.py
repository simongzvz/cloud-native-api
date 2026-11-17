from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_task_validation():
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 400


def test_create_task_success():
    response = client.post("/tasks", json={"title": "Deploy CI/CD Pipeline"})
    assert response.status_code == 201
    assert response.json()["title"] == "Deploy CI/CD Pipeline"
