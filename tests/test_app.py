import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Setze die Aktivitäten-Datenbank vor jedem Test zurück
    for name, data in activities.items():
        data["participants"] = []
        if name == "Chess Club":
            data["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
        elif name == "Programming Class":
            data["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
        elif name == "Gym Class":
            data["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
        elif name == "Basketball Team":
            data["participants"] = ["liam@mergington.edu", "noah@mergington.edu"]
        elif name == "Swimming Club":
            data["participants"] = ["ava@mergington.edu", "mia@mergington.edu"]


def test_get_activities():
    # Arrange: TestClient ist initialisiert
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()
    assert "Programming Class" in response.json()


def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]


def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_success():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_not_registered():
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"


def test_unregister_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
