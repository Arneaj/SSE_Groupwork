import pytest
from ..app import *
from unittest.mock import patch

# Fixture to provide a test client for making requests to the app
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test the player creation page
def test_character_creation_page(client):
    """
    Test that the character creation page loads properly with the expected fields.
    """
    response = client.get('/player_creation')
    assert response.status_code == 200, "Expected status code 200"
    assert b'Choose race' in response.data, "Expected 'Choose race' to be in the page content"
    assert b'Choose a class' in response.data, "Expected 'Choose a class' to be in the page content"


# Test creating a player with valid data
@patch('SSE_Groupwork.app.requests.get')
def test_create_player_valid(mock_get, client):
    """
    Test that the player creation works when valid data is provided.
    """
    # Mock the response from the external API (for races)
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"results": [{"name": "Elf"}, {"name": "Dwarf"}]}  # Mock species data

    # Send POST request to save player data
    response = client.post('/save_player', data={
        'name': 'TestPlayer',
        'race': 'Elf',
        'class': 'Warrior',
    })
    
    # Assert successful response (adjust based on actual behavior in your app)
    assert response.status_code == 200, "Expected status code 200"
    assert b'Character saved' in response.data, "Expected 'Character saved' message in the response"


# Test creating a player with invalid data (empty name)
@patch('SSE_Groupwork.app.requests.get')
def test_create_player_invalid_name(mock_get, client):
    """
    Test that the player creation fails when no character name is provided.
    """
    # Mock the response from the external API (for races)
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"results": [{"name": "Elf"}]}  # Mock species data

    # Send POST request with missing name
    response = client.post('/save_player', data={
        'name': '',
        'race': 'Elf',
        'class': 'Warrior',
    })
    
    # Assert that there is a validation error for missing name
    assert response.status_code == 400, "Expected status code 400 for bad request"
    assert b'Name cannot be empty' in response.data, "Expected 'Name cannot be empty' error message"


# Test creating a player with missing race
@patch('SSE_Groupwork.app.requests.get')
def test_create_player_missing_race(mock_get, client):
    """
    Test that the player creation fails when no race is selected.
    """
    # Mock the response from the external API (for races)
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"results": [{"name": "Elf"}]}  # Mock species data

    # Send POST request with missing race
    response = client.post('/save_player', data={
        'name': 'TestPlayer',
        'race': '',
        'class': 'Warrior',
    })
    
    # Assert that there is a validation error for missing race
    assert response.status_code == 400, "Expected status code 400 for bad request"
    assert b'Race cannot be empty' in response.data, "Expected 'Race cannot be empty' error message"


# Test creating a player with missing class
@patch('SSE_Groupwork.app.requests.get')
def test_create_player_missing_class(mock_get, client):
    """
    Test that the player creation fails when no class is selected.
    """
    # Mock the response from the external API (for races)
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"results": [{"name": "Elf"}]}  # Mock species data

    # Send POST request with missing class
    response = client.post('/save_player', data={
        'name': 'TestPlayer',
        'race': 'Elf',
        'class': '',
    })
    
    # Assert that there is a validation error for missing class
    assert response.status_code == 400, "Expected status code 400 for bad request"
    assert b'Class cannot be empty' in response.data, "Expected 'Class cannot be empty' error message"


# Test creating a player with invalid class
@patch('SSE_Groupwork.app.requests.get')
def test_create_player_invalid_class(mock_get, client):
    """
    Test that the player creation fails when an invalid class is provided.
    """
    # Mock the response from the external API (for races)
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"results": [{"name": "Elf"}]}  # Mock species data

    # Send POST request with invalid class
    response = client.post('/save_player', data={
        'name': 'TestPlayer',
        'race': 'Elf',
        'class': 'InvalidClass',  # Invalid class
    })
    
    # Assert that there is a validation error for invalid class
    assert response.status_code == 400, "Expected status code 400 for bad request"
    assert b'Invalid class' in response.data, "Expected 'Invalid class' error message"


# Test creating a player when the race API returns an empty list
@patch('SSE_Groupwork.app.requests.get')
def test_create_player_empty_race_list(mock_get, client):
    """
    Test that the player creation fails when the race API returns no available races.
    """
    # Mock the response from the external API (for races) with empty list
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"results": []}  # No races available

    # Send POST request with valid data
    response = client.post('/save_player', data={
        'name': 'TestPlayer',
        'race': 'Elf',
        'class': 'Warrior',
    })
    
    # Assert that there is an error due to no races being available
    assert response.status_code == 500, "Expected status code 500 for internal server error"
    assert b'No races available' in response.data, "Expected 'No races available' error message"


# Test creating a player when the class API returns an empty list
@patch('SSE_Groupwork.app.requests.get')
def test_create_player_empty_class_list(mock_get, client):
    """
    Test that the player creation fails when the class API returns no available classes.
    """
    # Mock the response from the external API (for races)
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"results": [{"name": "Elf"}]}  # Mock species data

    # Mock the response from the class API with empty list
    with patch('app.requests.get') as mock_get_classes:
        mock_get_classes.return_value.status_code = 200
        mock_get_classes.return_value.json.return_value = {"results": []}  # No classes available

        # Send POST request with valid data
        response = client.post('/save_player', data={
            'name': 'TestPlayer',
            'race': 'Elf',
            'class': 'Warrior',
        })
        
        # Assert that there is an error due to no classes being available
        assert response.status_code == 500, "Expected status code 500 for internal server error"
        assert b'No classes available' in response.data, "Expected 'No classes available' error message"