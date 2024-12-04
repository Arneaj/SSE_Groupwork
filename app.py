from flask import Flask, render_template, request, jsonify
import requests
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import click
from .game_database import db
from .player import Player
from .game import Game
from .models.D_D_game import game_data
from .models.D_D_player import player_data

# from .cli import create_all, drop_all, populate  # Importing commands


app = Flask(__name__, template_folder="templates", static_folder="static")


load_dotenv() # Loading the environment variables

# Configuring database
app.config["SQLALCHEMY_DATABASE_URI"] = ( "postgresql://avr24:f61Q%T421>i@db.doc.ic.ac.uk/avr24" ) # psql URL
app.config["DND_API_KEY"] = os.getenv("DND_API_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialising database
db.init_app(app)

# Registering blueprints - come back to later! If others don't want we dont have to do this
# app.register_blueprint(blueprints.collection)

"""
# Adding commands to access and modify the database
with app.app_context():
    app.cli.add_command(create_all)
    app.cli.add_command(populate)
    app.cli.add_command(drop_all)
    
    # Debugging statement echoing that CLI commands registered
    click.echo("Registered CLI commands successfully.")


@app.route("/player_data")
def collection():
    players = db.Player.query.all() 
    return render_template("main.html", players=players) # Check whether this is correct - not duplicationg
"""

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

Players = [
    {
        "name": "Arnie",
        "max_HP": 120,
        "current_HP": 100,
        "ability": [ 0,0,0,0,0,0 ]
    },
    {
        "name": "Charlotte",
        "max_HP": 120,
        "current_HP": 120,
        "ability": [ 0,0,0,0,0,0 ]
    },
    {
        "name": "Molly",
        "max_HP": 120,
        "current_HP": 110,
        "ability": [ 0,0,0,0,0,0 ]
    },
    {
        "name": "Callum",
        "max_HP": 1000,
        "current_HP": 205,
        "ability": [ 0,0,0,0,0,0 ]
    }
]
"""

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/STARTGAME', methods=["GET", "POST"])
def startGame():
    # get the game from the request
    game_name_input = request.args.get("gameName")
    
    # get the game from the database
    passed_game = db.get_or_404( game_data, 0 )
            
    # get the players of that game from the database
    passed_players = [ db.get_or_404( player_data, player_id ) for player_id in passed_game.player_id ] 
    
    # here should be API request to get the actual game we want
    # from the game_name !
    
    # here get the monsters
    challenge_rating_input = request.args.get("challenge_index")
    
    if challenge_rating_input == None:
        challenge_rating_input = 0
    
    url = f'https://www.dnd5eapi.co/api/monsters?challenge_rating=\
        {challenge_rating_input}'
    response = requests.get(url)
    if response.status_code == 200:
        monsters_response = response.json()

    monsters = monsters_response["results"]

    return render_template(
        "main.html", 
        game=passed_game, 
        players=passed_players,
        monsters=monsters,
        )


@app.route('/game_creation', methods=["GET", "POST"])
def create_game():
    return render_template(
        "create_new_game.html")

@app.route('/player_creation')
def create_player():
    # got to api and get all information that is needed

    # get races - Note we called them species in database and app
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

    url = "https://www.dnd5eapi.co/api/alignments"
    response = requests.get(url)
    if response.status_code == 200:
        alignments_response = response.json()

    alignments = alignments_response["results"]

    return render_template(
        'create_new_character.html',
        races=races,
        classes=classes,
        backgrounds=backgrounds,
        alignments=alignments,
    )


@app.route('/games_index', methods=["GET", "POST"])
def games_index():
    passed_games = [ db.get_or_404( game_data, i ) for i in range(2) ] 
    return render_template("games_index.html", games=passed_games)


# Every character needs:
    # name
    # race
    # class
    # background
    # attribute scores for the 6 attributes
    # attribute modifiers

def determine_ability_modifier(ability_score, race):
    url = f"https://www.dnd5eapi.co/api/races/{race}"
    response = requests.get(url)
    if response.status_code == 200:
        response_specifc_race = response.json()

    race_modifier = 0

    #race_modifier = response_specifc_race[ability]["bonus"] # strength

    modifier = (ability_score + race_modifier) - 10
    modifier = modifier / 2
    return round(modifier)

def calculate_hp(class_name, constitution):
    url = f"https://www.dnd5eapi.co/api/classes/{class_name}"
    response = requests.get(url)
    if response.status_code == 200:
        response_specifc_class = response.json()

    hit_die = response_specifc_class['hit_die']
    return hit_die + constitution

    
@app.route("/save_player", methods=["GET", "POST"])
def save_character():
    # get basic information from the character creation form
    input_character_name = request.form.get("characterName")
    input_character_race = request.form.get("race")
    input_character_class = request.form.get("class")
    input_character_background = request.form.get("background")

    # get ability scores for the character
    input_character_strength = request.form.get("ability1")
    input_character_dexterity = request.form.get("ability2")
    input_character_constitution = request.form.get("ability3")
    input_character_intelligence = request.form.get("ability4")
    input_character_wisdom = request.form.get("ability5")
    input_character_charisma = request.form.get("ability6")

    # calculate ability modifiers
    strength_modifier = determine_ability_modifier(input_character_strength, input_character_race)
    dexterity_modifier = determine_ability_modifier(input_character_dexterity, input_character_race)
    constitution_modifier = determine_ability_modifier(input_character_constitution, input_character_race)
    intelligence_modifier = determine_ability_modifier(input_character_intelligence, input_character_race)
    wisdom_modifier = determine_ability_modifier(input_character_wisdom, input_character_race)
    charisma_modifier = determine_ability_modifier(input_character_charisma, input_character_race)

    max_hp = calculate_hp()

    # determine proficiency modifier - if there is time

    # render_template("character.html",
    #     name=input_character_name,
    #     race=input_character_race,
    #     charClass=input_character_class,
    #     background=input_character_background,
    #     strength=input_character_strength,
    #     dexterity=input_character_dexterity,
    #     constitution=input_character_constitution,
    #     intelligence=input_character_intelligence,
    #     wisdom=input_character_wisdom,
    #     charisma=input_character_charisma,
    #     strength_modifier=strength_modifier,
    #     dexterity_modifier=dexterity_modifier,
    #     constitution_modifier=constitution_modifier,
    #     intelligence_modifier=intelligence_modifier,
    #     wisdom_modifier=wisdom_modifier,
    #     charisma_modifier=charisma_modifier,
    #     )