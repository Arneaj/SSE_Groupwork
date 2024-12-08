''''''''''

import pytest
from ..app import *
import requests
import json
from unittest.mock import Mock

# Mock Flask client for testing
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test the character creation page
def test_character_creation_page(client):
    """
    Test that the character creation page loads properly with the expected fields.
    """
    response = client.get('/player_creation')
    assert response.status_code == 200, "Expected status code 200"
    assert b'Choose race' in response.data, "Expected 'Choose race' to be in the page content"
    assert b'Choose a class' in response.data, "Expected 'Choose a class' to be in the page content"

# Test ability modifier calculation
def test_calculate_ability_modifier():
    """
    Test the calculation of ability modifiers based on ability score and race.
    """
    assert determine_ability_modifier(skill="stealth", ability_score=2, race="human") == -4
    assert determine_ability_modifier(skill="acrobatics", ability_score=7, race="elf") == -2
    assert determine_ability_modifier(skill="persuasion", ability_score=15, race="dwarf") == 2
    assert determine_ability_modifier(skill="intimidation", ability_score=20, race="orc") == 5

# Mock function to simulate requests.get for the DnD API
def mock_get(url):
    """
    Mock the API response for specific class data.
    """
    if url == "https://www.dnd5eapi.co/api/classes/fighter":
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'hit_die': 10}
        return mock_response
    else:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status = lambda: (_ for _ in ()).throw(
            requests.exceptions.HTTPError(f"HTTP error {mock_response.status_code}")
        )
        return mock_response

# Test for valid player creation
@pytest.mark.parametrize("test_input, expected", [
    ({
        'characterName': 'TestPlayer',
        'race': 'Elf',
        'class': 'fighter',
        'ability1': 8,
        'ability2': 10,
        'ability3': 12,
        'ability4': 13,
        'ability5': 14,
        'ability6': 15,
        'alignment': 'Lawful Good'
    }, 200)
])
def test_create_player_valid(monkeypatch, client, test_input, expected):
    """
    Test the creation of a valid player character.
    """
    monkeypatch.setattr(requests, "get", mock_get)
    response = client.post('/save_player',
                           data=json.dumps(test_input),
                           content_type='application/json')
    assert response.status_code == expected, f"Expected status code {expected}, got {response.status_code}"

# Test for invalid player creation (empty name)
def test_create_player_invalid_name(monkeypatch, client):
    """
    Test the creation of a player character with an empty name.
    """
    monkeypatch.setattr(requests, "get", mock_get)
    response = client.post('/save_player',
                           data=json.dumps({
                               'characterName': '', # Empty name
                               'race': 'Elf',
                               'class': 'fighter',
                               'ability1': 8,
                               'ability2': 10,
                               'ability3': 12,
                               'ability4': 13,
                               'ability5': 14,
                               'ability6': 15,
                               'alignment': 'Lawful Good'
                           }),
                           content_type='application/json')
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

# Test creating a player with missing race
def test_create_player_missing_race(monkeypatch, client):
    """
    Test the creation of a player character with a missing race.
    """
    # Mock the response from the DnD API (for races)
    mock_response = Mock()
    mock_response.status_code = 404  # Assuming the API returns a 404 error for missing races
    monkeypatch.setattr(requests, "get", lambda url: mock_response)
    
    response = client.post('/save_player',
                           data=json.dumps({
                               'characterName': 'TestPlayer',
                               'race': '',  # Missing race
                               'class': 'fighter',
                               'ability1': 8,
                               'ability2': 10,
                               'ability3': 12,
                               'ability4': 13,
                               'ability5': 14,
                               'ability6': 15,
                               'alignment': 'Lawful Good'
                           }),
                           content_type='application/json')
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

# Test creating a player with missing class
def test_create_player_missing_class(monkeypatch, client):
    """
    Test the creation of a player character with a missing class.
    """
    # Mock the response from the DnD API (for classes)
    mock_response = Mock()
    mock_response.status_code = 404  # Assuming the API returns a 404 error for missing classes
    monkeypatch.setattr(requests, "get", lambda url: mock_response)
    
    response = client.post('/save_player',
                           data=json.dumps({
                               'characterName': 'TestPlayer',
                               'race': 'Elf',
                               'class': '',  # Missing class
                               'ability1': 8,
                               'ability2': 10,
                               'ability3': 12,
                               'ability4': 13,
                               'ability5': 14,
                               'ability6': 15,
                               'alignment': 'Lawful Good'
                           }),
                           content_type='application/json')
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"