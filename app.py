from flask import Flask, render_template, request, jsonify
import requests
from sqlalchemy import create_engine, text
#from dotenv import load_dotenv
import os

app = Flask(__name__)

"""
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@app.route('/test-db', methods=['GET'])
def test_db():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return jsonify({"status": "success", "result": [dict(row) for row in result]})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
"""

Games = [
	{
        "name": "Game1",
        "players": ["Molly","Callum","Charlotte","Arnie"] # Still need to link the players from the database once created
    },

	{
        "name": "Game2",
        "players": ["Molly","Callum","Charlotte"]
    }
]

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/STARTGAME', methods=["GET", "POST"])
def startGame():
    game_name_input = "Game1"  # request.form.get("gameName")
    game = Games[0]  # here should be API request to get the actual game we want from the game_name !
    #data = request.get_json()
    #player_list = data['list']
    
    return render_template("main.html", game=game)


@app.route('/game_creation')
def create_game():
    return render_template(
        "create_new_game.html")

@app.route('/player_creation')
def create_player():
    # got to api and get all information that is needed

    # get races
    url = "https://www.dnd5eapi.co/api/races"
    response = requests.get(url)
    if response.status_code == 200:
        races_response = response.json()

    races = races_response["results"]

    # get classes
    url = "https://www.dnd5eapi.co/api/classes"
    response = requests.get(url)
    if response.status_code == 200:
        classes_response = response.json()

    classes = classes_response["results"]

    url = "https://www.dnd5eapi.co/api/backgrounds"
    response = requests.get(url)
    if response.status_code == 200:
        backgrounds_response = response.json()

    backgrounds = backgrounds_response["results"]

    return render_template(
        'create_new_character.html',
        races=races,
        classes=classes,
        backgrounds=backgrounds,
    )


@app.route('/games_index', methods=["GET", "POST"])
def games_index():
    return render_template("games_index.html", games=Games)
