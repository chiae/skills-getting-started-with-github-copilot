from src.app import activities


def test_unregistration_success_removes_participant(client):
    # Arrange
    activity_name = "Programming Class"
    existing_email = activities[activity_name]["participants"][0]

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {existing_email} from {activity_name}"
    assert existing_email not in activities[activity_name]["participants"]


def test_unregistration_rejects_missing_activity(client):
    # Arrange
    missing_activity = "Robotics Club"

    # Act
    response = client.delete(
        f"/activities/{missing_activity}/participants", params={"email": "student@mergington.edu"}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregistration_rejects_non_member(client):
    # Arrange
    activity_name = "Gym Class"
    absent_email = "not.registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": absent_email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
