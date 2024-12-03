import pytest
import requests
from unittest.mock import patch
from ..app import *

# Test the Race API integration
def test_race_api():
    """
    Test that the race API correctly fetches race data and returns expected values.
    """
    
    # Make API call
    response = requests.get("https://www.dnd5eapi.co/api/races")
    
    # Assertions to check for correct status code and content
    assert response.status_code == 200, "Expected status code 200"
    assert "Dragonborn" in response.json()["results"][0]["name"], "Expected 'Dragonborn' in first race"
    assert "Dwarf" in response.json()["results"][1]["name"], "Expected 'Dwarf' in second race"


# Test the Class API integration
def test_class_api():
    """
    Test that the class API correctly fetches class data and returns expected values.
    """
    
    # Make API call
    response = requests.get("https://www.dnd5eapi.co/api/classes")
    
    # Assertions to check for correct status code and content
    assert response.status_code == 200, "Expected status code 200"
    assert "Barbarian" in response.json()["results"][0]["name"], "Expected 'Barbarian' in first class"
    assert "Bard" in response.json()["results"][1]["name"], "Expected 'Bard' in second class"


# Test invalid response (non-200 status code)
def test_api_invalid_status_code():
    """
    Test the API response when an invalid status code is returned (e.g., 404).
    """
    
    # Make API call
    response = requests.get("https://www.dnd5eapi.co/api/class")
    
    # Assertions for invalid response handling
    assert response.status_code == 404, "Expected status code 404 for invalid API endpoint"


# Test API with no data (empty response)
def test_api_empty_response():
    """
    Test the API when it returns an empty response.
    """
    
    # Make API call
    response = requests.get("https://www.dnd5eapi.co/api/monsters?challenge_rating=-1")
    
    # Assertions for empty data
    assert response.status_code == 200, "Expected status code 200"
    assert len(response.json()["results"]) == 0, "Expected no results in the API response"


# Test API with malformed JSON (e.g., missing expected fields)
def test_api_malformed_json():
    """
    Test the API when it returns malformed JSON.
    """
    
    # Make API call
    response = requests.get("https://www.dnd5eapi.co/api/races")
    
    # Assertions to check for status code and key error
    assert response.status_code == 200, "Expected status code 200"
    with pytest.raises(KeyError):
        # Ensure that expected fields are missing and cause a KeyError
        response.json()["results"]


# Test API handling of network errors (requests exceptions)
def test_api_network_error():
    """
    Test handling of network errors, such as a timeout or connection error.
    """
    
    # Make API call and check for exception
    with pytest.raises(requests.exceptions.RequestException):
        requests.get("https://www.dnd5eapi.co/api/races")


# Test API with incorrect URL (404 Not Found)
def test_api_invalid_url():
    """
    Test the API with an invalid URL that should return a 404 error.
    """
    
    # Make API call to invalid URL
    response = requests.get("https://www.dnd5eapi.co/api/nonexistent")
    
    # Assertions for 404 error
    assert response.status_code == 404, "Expected 404 for invalid URL"
    assert "Not Found" in response.json().get("detail", ""), "Expected 'Not Found' message in the response"