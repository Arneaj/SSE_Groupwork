import pytest
from ..app import test_client


@pytest.fixture
def client():
    # This fixture sets up a test client for making requests to your app
    with test_client() as client:
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
    # Assert that the response status is 200 (success)
    # or 302 if it redirects after creation
    assert response.status_code == 200  # or 302 if redirected
    # Check if the page contains 'Start game'
    # which should appear after a successful creation
    assert b'Start your new game!' in response.data
