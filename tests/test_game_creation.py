import pytest
import app

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
        'gameName': 'Test Game'
    })
    # Assert that the response status is 200 (success) or 302 if it redirects after creation
    assert response.status_code == 200  # or 302 if redirected
    # Check if the page contains 'Start game' which should appear after a successful creation
    assert b'Start game' in response.data

# Test adding a character to the game
def test_add_character_to_game(client):
    # First, create the game
    client.post('/game_creation', data={
        'gameName': 'Test Game'
    })
    
    # Now, add a character to the game (this assumes the game creation page leads to a 'start game' route)
    response = client.post('/STARTGAME?gameName=Test Game', data={
        'character': 'TestPlayer'
    })
    # Assert that the response status is 200
    assert response.status_code == 200
    # Check if the page contains the current list of characters in the game
    assert b'Current List of Characters in Game' in response.data
    # Verify if the player has been added by checking for their name (or some expected text)
    assert b'TestPlayer' in response.data

# Test that the game creation page handles missing data gracefully (e.g., empty game name)
def test_game_creation_with_missing_data(client):
    # Send a POST request with missing game name
    response = client.post('/game_creation', data={})
    # Assert the page responds with a 400 or some error message
    assert response.status_code == 400
    # Check that an error message is displayed (replace with your actual error message)
    assert b'Game name is required' in response.data

# Test the game start page (e.g., loading the game after creation)
def test_start_game_page(client):
    # Create a new game first
    client.post('/game_creation', data={'gameName': 'Test Game'})

    # Now test the start game page
    response = client.get('/STARTGAME?gameName=Test Game')
    # Assert that the page loads correctly
    assert response.status_code == 200
    # Check if the page displays the name of the game
    assert b'Test Game' in response.data
    # Check if it displays an option to start the game
    assert b'Start' in response.data

    # Add a character to the game
    client.post('/STARTGAME?gameName=Test Game', data={'character': 'TestPlayer'})

    # Now test the start game page again
    response = client.get('/STARTGAME?gameName=Test Game')
    # Assert that the page loads correctly
    assert response.status_code == 200
    # Check if the page displays the name of the game
    assert b'Test Game' in response.data
    # Check if it displays an option to start the game
    assert b'Start' in response.data

    # Start the game
    response = client.post('/STARTGAME?gameName=Test Game', data={'start': 'Start'})
    # Assert that the game starts successfully
    assert response.status_code == 200
    # Check if the page displays the name of the game
    assert b'Test Game' in response.data
    # Check if it displays an option to start the game
    assert b'Start' in response.data
