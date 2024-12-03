import pytest
import requests
from unittest.mock import patch

# Test species API
@patch('SSE_Groupwork.app.requests.get')
def test_race_api(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "results": [{"name": "Elf"}, {"name": "Dwarf"}]
    }
    
    response = requests.get("https://www.dnd5eapi.co/api/races")
    assert response.status_code == 200
    assert "Elf" in response.json()["results"][0]["name"]
    assert "Dwarf" in response.json()["results"][1]["name"]

# Test class API
@patch('SSE_Groupwork.app.requests.get')
def test_class_api(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "results": [{"name": "Warrior"}, {"name": "Mage"}]
    }
    
    response = requests.get("https://www.dnd5eapi.co/api/classes")
    assert response.status_code == 200
    assert "Warrior" in response.json()["results"][0]["name"]
    assert "Mage" in response.json()["results"][1]["name"]
