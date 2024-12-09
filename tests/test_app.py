import requests


# Test the Race API integration
def test_race_api():
    """
    Test that the race API correctly fetches race data
    and returns expected values.
    """

    # Make API call
    response = requests.get("https://www.dnd5eapi.co/api/races")

    # Assertions to check for correct status code and content
    assert response.status_code == 200, "Expected status code 200"
    error_msg = "Expected 'Dragonborn' in first race"
    assert "Dragonborn" in response.json()["results"][0]["name"], error_msg
    error_msg = "Expected 'Dwarf' in second race"
    assert "Dwarf" in response.json()["results"][1]["name"], error_msg


# Test the Class API integration
def test_class_api():
    """
    Test that the class API correctly fetches class data
    and returns expected values.
    """

    # Make API call
    response = requests.get("https://www.dnd5eapi.co/api/classes")

    # Assertions to check for correct status code and content
    assert response.status_code == 200, "Expected status code 200"
    error_msg = "Expected 'Barbarian' in first class"
    assert "Barbarian" in response.json()["results"][0]["name"], error_msg
    error_msg = "Expected 'Bard' in second class"
    assert "Bard" in response.json()["results"][1]["name"], error_msg


# Test API with no data (empty response)
def test_api_empty_response():
    """
    Test the API when it returns an empty response.
    """

    # Make API call
    response = requests.get(
        "https://www.dnd5eapi.co/api/monsters?challenge_rating=-1"
        )

    # Assertions for empty data
    assert response.status_code == 200, "Expected status code 200"
    error_msg = "Expected no results in the API response"
    assert len(response.json()["results"]) == 0, error_msg


# Test API with incorrect URL (404 Not Found)
def test_api_invalid_url():
    """
    Test the API with an invalid URL that should return a 404 error.
    """

    # Make API call to invalid URL
    response = requests.get("https://www.dnd5eapi.co/api/nonexistent")

    # Assertions for 404 error
    assert response.status_code == 404, "Expected 404 for invalid URL"
