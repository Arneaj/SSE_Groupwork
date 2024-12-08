import pytest
from ..app import *
import re

@pytest.fixture
def client():
    # This fixture sets up a test client for making requests to your app
    with app.test_client() as client:
        yield client

# Test game creation page loads correctly
def test_game_creation_page(client):
    response = client.get('/game_creation')
    # Assert that the page loads successfully (status code 200)
    assert response.status_code == 200
    # Check if the page contains the text 'Create New Game'
    assert b'Create New Game' in response.data

# Test creating a new game
def test_create_new_game(client):
    # Sending a POST request to create a new game
    response = client.post('/game_creation', data={
        'gameName': 'TestGame'
    })
    # Assert that the response status is 200 (success) or 302 if it redirects after creation
    assert response.status_code == 200  # or 302 if redirected
    # Check if the page contains 'Start game' which should appear after a successful creation
    assert b'Start your new game!' in response.data

"""
# Test adding a character to the game
def test_add_character_to_game(client):
    # First, create the game
    response_create_game = client.post('/game_creation', data={
        'gameName': 'TestGame'
    })
    # Assert that the game creation was successful
    assert response_create_game.status_code == 200
    
    print(response_create_game.data)
    
    # Check if the page contains the specific header or text confirming the game name
    assert b'<h1>' in response_create_game.data and b'TestGame' in response_create_game.data
"""
