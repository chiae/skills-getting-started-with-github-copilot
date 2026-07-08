def test_root_redirects_to_static(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == expected_location


def test_get_activities_returns_expected_structure(client):
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert payload
    for details in payload.values():
        assert required_fields.issubset(details.keys())
        assert isinstance(details["participants"], list)
        assert isinstance(details["max_participants"], int)
