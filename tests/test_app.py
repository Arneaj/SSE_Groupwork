import pytest
import requests
from unittest.mock import patch
import app

# Test the Race API integration
@patch('app.requests.get')
def test_race_api(mock_get):
    """
    Test that the race API correctly fetches race data and returns expected values.
    """
    # Setup mock response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "results": [{"name": "Elf"}, {"name": "Dwarf"}]
    }
    
    # Make API call
    response = requests.get("https://www.dnd5eapi.co/api/races")
    
    # Assertions to check for correct status code and content
    assert response.status_code == 200, "Expected status code 200"
    assert "Elf" in response.json()["results"][0]["name"], "Expected 'Elf' in first race"
    assert "Dwarf" in response.json()["results"][1]["name"], "Expected 'Dwarf' in second race"


# Test the Class API integration
@patch('app.requests.get')
def test_class_api(mock_get):
    """
    Test that the class API correctly fetches class data and returns expected values.
    """
    # Setup mock response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "results": [{"name": "Warrior"}, {"name": "Mage"}]
    }
    
    # Make API call
    response = requests.get("https://www.dnd5eapi.co/api/classes")
    
    # Assertions to check for correct status code and content
    assert response.status_code == 200, "Expected status code 200"
    assert "Warrior" in response.json()["results"][0]["name"], "Expected 'Warrior' in first class"
    assert "Mage" in response.json()["results"][1]["name"], "Expected 'Mage' in second class"


# Test invalid response (non-200 status code)
@patch('app.requests.get')
def test_api_invalid_status_code(mock_get):
    """
    Test the API response when an invalid status code is returned (e.g., 404).
    """
    # Setup mock response with 404 status code
    mock_get.return_value.status_code = 404
    
    # Make API call
    response = requests.get("https://www.dnd5eapi.co/api/races")
    
    # Assertions for invalid response handling
    assert response.status_code == 404, "Expected status code 404 for invalid API endpoint"


# Test API with no data (empty response)
@patch('app.requests.get')
def test_api_empty_response(mock_get):
    """
    Test the API when it returns an empty response.
    """
    # Setup mock response with empty data
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"results": []}
    
    # Make API call
    response = requests.get("https://www.dnd5eapi.co/api/races")
    
    # Assertions for empty data
    assert response.status_code == 200, "Expected status code 200"
    assert len(response.json()["results"]) == 0, "Expected no results in the API response"


# Test API with malformed JSON (e.g., missing expected fields)
@patch('app.requests.get')
def test_api_malformed_json(mock_get):
    """
    Test the API when it returns malformed JSON.
    """
    # Setup mock response with malformed JSON
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"unexpected_field": "unexpected_value"}
    
    # Make API call
    response = requests.get("https://www.dnd5eapi.co/api/races")
    
    # Assertions to check for status code and key error
    assert response.status_code == 200, "Expected status code 200"
    with pytest.raises(KeyError):
        # Ensure that expected fields are missing and cause a KeyError
        response.json()["results"]


# Test API handling of network errors (requests exceptions)
@patch('app.requests.get')
def test_api_network_error(mock_get):
    """
    Test handling of network errors, such as a timeout or connection error.
    """
    # Simulate a network exception
    mock_get.side_effect = requests.exceptions.RequestException("Network error")
    
    # Make API call and check for exception
    with pytest.raises(requests.exceptions.RequestException):
        requests.get("https://www.dnd5eapi.co/api/races")


# Test API with incorrect URL (404 Not Found)
@patch('app.requests.get')
def test_api_invalid_url(mock_get):
    """
    Test the API with an invalid URL that should return a 404 error.
    """
    # Setup mock response for a non-existent URL (404)
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {"detail": "Not Found"}
    
    # Make API call to invalid URL
    response = requests.get("https://www.dnd5eapi.co/api/nonexistent")
    
    # Assertions for 404 error
    assert response.status_code == 404, "Expected 404 for invalid URL"
    assert "Not Found" in response.json().get("detail", ""), "Expected 'Not Found' message in the response"