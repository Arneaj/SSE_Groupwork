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


# Test API with incorrect URL (404 Not Found)
def test_api_invalid_url():
    """
    Test the API with an invalid URL that should return a 404 error.
    """
    
    # Make API call to invalid URL
    response = requests.get("https://www.dnd5eapi.co/api/nonexistent")
    
    # Assertions for 404 error
    assert response.status_code == 404, "Expected 404 for invalid URL"