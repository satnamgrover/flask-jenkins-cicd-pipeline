import pytest
from app.main import app, tasks


@pytest.fixture
def client():
    app.config["TESTING"] = True
    tasks.clear()
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_get_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Write CI/CD pipeline"})
    assert response.status_code == 201
    body = response.get_json()
    assert body["title"] == "Write CI/CD pipeline"
    assert body["done"] is False
    assert "id" in body


def test_create_task_missing_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_get_single_task(client):
    create_response = client.post("/tasks", json={"title": "Deploy to prod"})
    task_id = create_response.get_json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Deploy to prod"


def test_get_nonexistent_task(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_complete_task(client):
    create_response = client.post("/tasks", json={"title": "Test the pipeline"})
    task_id = create_response.get_json()["id"]

    response = client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.get_json()["done"] is True


def test_delete_task(client):
    create_response = client.post("/tasks", json={"title": "Temporary task"})
    task_id = create_response.get_json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404
