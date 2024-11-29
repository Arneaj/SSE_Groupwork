from flask import Flask, render_template, request, jsonify
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

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/STARTGAME')
def startGame():
	return render_template("main.html")


@app.route('/game_creation')
def create_game():
    return render_template("create_new_game.html")

@app.route('/player_creation')
def create_player():
    return render_template('create_new_player.html')


Games = [
	dict(
		{
      "name": "Game1",
      "players": ["Molly, Callum, Charlotte, Arnie"]
     	}
  	),
	dict(
		{
      "name": "Game2",
      "players": ["Molly, Callum, Charlotte, Arnie"]
        }
	)
]

@app.route('/games_index', methods=["POST", "GET"])
def games_index():
    games = Games ### REQUEST FROM DATABASE!
    
    return render_template("games_index.html", games=games)

