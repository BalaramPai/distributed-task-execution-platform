from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == True
    assert response.json()["message"] == "Server is Up and Running"

def test_create_task():

    payload = {
        "title": "Pytest Task",
        "description": "Testing create",
        "duration": 60,
        "location": "Bangalore",
        "dueDate": "2026-12-31"
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 200
    assert response.json()["status"] == True
    assert response.json()["data"]["id"] is not None
    assert response.json()["data"]["title"] == payload["title"]
    
    
def test_get_task():

    payload = {
        "title": "Get Task",
        "description": "Testing get",
        "duration": 60,
        "location": "Bangalore",
        "dueDate": "2026-12-31"
    }

    create_response = client.post("/tasks", json=payload)

    task_id = create_response.json()["data"]["id"]

    response = client.get(f"/task/{task_id}")

    assert response.status_code == 200
    assert response.json()["status"] == True
    assert response.json()["data"]["id"] == task_id
    
    
def test_update_task():

    payload = {
        "title": "Old Title",
        "description": "Old Desc",
        "duration": 60,
        "location": "Bangalore",
        "dueDate": "2026-12-31"
    }

    create_response = client.post("/tasks", json=payload)

    task_id = create_response.json()["data"]["id"]

    update_payload = {
        "title": "New Title"
    }

    response = client.put(
        f"/task/{task_id}",
        json=update_payload
    )

    assert response.status_code == 200
    assert response.json()["status"] == True
    

def test_update_status():

    payload = {
        "title": "Status Task",
        "description": "Testing status",
        "duration": 60,
        "location": "Bangalore",
        "dueDate": "2026-12-31"
    }

    create_response = client.post("/tasks", json=payload)

    task_id = create_response.json()["data"]["id"]

    response = client.patch(
        f"/task/{task_id}/status",
        json={"status": "COMPLETED"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == True
    
    
def test_delete_task():

    payload = {
        "title": "Delete Task",
        "description": "Testing delete",
        "duration": 60,
        "location": "Bangalore",
        "dueDate": "2026-12-31"
    }

    create_response = client.post("/tasks", json=payload)

    task_id = create_response.json()["data"]["id"]

    response = client.delete(f"/task/{task_id}")

    assert response.status_code == 200
    assert response.json()["status"] == True
    
    
def test_invalid_title():

    payload = {
        "title": "ab",
        "description": "Testing",
        "duration": 60,
        "location": "Bangalore",
        "dueDate": "2026-12-31"
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422
    
    
def test_invalid_duration():

    payload = {
        "title": "Valid Title",
        "description": "Testing",
        "duration": -10,
        "location": "Bangalore",
        "dueDate": "2026-12-31"
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422
    
    
def test_invalid_status():

    payload = {
        "title": "Status Task",
        "description": "Testing",
        "duration": 60,
        "location": "Bangalore",
        "dueDate": "2026-12-31"
    }

    create_response = client.post("/tasks", json=payload)

    task_id = create_response.json()["data"]["id"]

    response = client.patch(
        f"/task/{task_id}/status",
        json={"status": "HELLO"}
    )

    assert response.status_code == 422
    
    
def test_task_not_found():
    response = client.get("/task/999999")

    assert response.status_code == 200
    assert response.json()["status"] == False