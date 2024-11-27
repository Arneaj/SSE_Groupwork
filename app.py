from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")


@app.route('/STARTGAME')
def startGame():
	return render_template("main.html")


@app.route('/game_creation')
def create_game():
    return render_template("create_new_game.html")

@app.route('/games_index')
def games_index():
    return render_template("games_index.html")
