from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import requests
import random
from .Blueprint import dungeons_and_dragons
from sqlalchemy.orm import joinedload
from sqlalchemy import create_engine, text
from .database import database as db
from .models.D_D_game import game_data
from .models.D_D_player import player_data
import click
from .cli import create_all, drop_all, populate

# from .cli import create_all, drop_all, populate  # Importing commands

def app(testing=False):
    # Initialise the Flask app
    app = Flask(__name__, template_folder="templates", static_folder="static")

    if testing:
        app.config.update(
            {
                "TESTING": True,
                "SECRET_KEY": "testing_key",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
                "DND_API_KEY": os.getenv("DND_API_KEY"),
            }
        )
        db.init_app(app)
        app.register_blueprint(dungeons_and_dragons)

    return app

app = app()

# Configuring database
app.config["SQLALCHEMY_DATABASE_URI"] = ( "postgresql://avr24:f61Q%T421>i@db.doc.ic.ac.uk/avr24" ) # psql URL
app.config["DND_API_KEY"] = os.getenv("DND_API_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialising database
db.init_app(app)
app.register_blueprint(dungeons_and_dragons)

with app.app_context():
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)
    app.cli.add_command(populate)

    # Debugging statement echoing that CLI commands registered
    click.echo("Registered CLI commands successfully.")

"""


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


@app.route('/process_new_game', methods=["GET", "POST"])
def process_new_game():
    data = request.get_json()
    game_name = data.get('gameName')
    player_list = data.get('playerList')
    
    player_list = [ int(player_id) for player_id in player_list ]
    
    game_id = 0
    while True:
        current_db = db.session.get( game_data, game_id )
        if current_db == None: break
        game_id += 1
    
    db.session.add(
        game_data(
            game_id,
            game_name,
            player_list
        )
    )
    
    db.session.commit()
    
    return jsonify(game_id= game_id)


@app.route('/STARTGAME', methods=["GET", "POST"])
def startGame():
    # get the game from the request
    game_id_input = request.args.get("game_id")

    # get the game from the database
    passed_game = db.get_or_404( game_data, game_id_input )

    # get the players of that game from the database
    passed_players = [ db.get_or_404( player_data, player_id ) for player_id in passed_game.player_id ]

    # here get the monsters
    challenge_rating_input = request.args.get("challenge_index")

    if challenge_rating_input == None:
        challenge_rating_input = 0

    url = f'https://www.dnd5eapi.co/api/monsters?challenge_rating={challenge_rating_input}'
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
    players = []
    
    id = 0
    current_player = db.session.get( player_data, id )
    while ( current_player ) != None:
        players.append(current_player)
        id+=1
        current_player = db.session.get( player_data, id )
    
    return render_template(
        "create_new_game.html",
        players=players
    )

@app.route('/player_creation', methods=["GET", "POST"])
def create_player():

    # go to api and get all information that is needed

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
    passed_games = [] 
    
    i = 0
    while True:
        current_db = db.session.get( game_data, i )
        if current_db == None: break
        passed_games.append(current_db)
        i += 1
    
    passed_players = [ [ db.get_or_404( player_data, player_id ) for player_id in passed_game.player_id ] for passed_game in passed_games ]
    
    passed_json = []
    
    for i in range(len(passed_games)):
        passed_json.append(
            {
                "game": passed_games[i],
                "players": passed_players[i]
            }
        )
    
    return render_template("games_index.html", json_input=passed_json)

# Every character needs:
    # name
    # race
    # class
    # background
    # attribute scores for the 6 attributes
    # attribute modifiers

def get_race_modifier(skill, race):
    url = f"https://www.dnd5eapi.co/api/races/{race}"

    response = requests.get(url)
    if response.status_code == 200:
        specific_race_data = response.json()

    bonuses = specific_race_data.get("ability_bonuses", [])

    for bonus in bonuses:
        ability = bonus["ability_score"]["name"] # STR
        if (ability == skill):
            return bonus["bonus"]
    # if no modifier for that race and skill, return 0 
    return 0
 
def determine_ability_modifier(skill, ability_score, race):
    race_modifier = get_race_modifier(skill, race)
    return round((ability_score + race_modifier) - 10) // 2

def roll_ability_scores():
    scores = []
    for i in range(6):
        rolls = sorted([random.randint(1, 6) for j in range(4)], reverse=True)
        scores.append(sum(rolls[1:])) # Drop the lowest roll and keep the rest
    return scores

def calculate_hp(race_name, class_name, constitution_score):
    constitution_modifier = determine_ability_modifier("CON", constitution_score, race_name)

    # Fetch the hit die and constitution modifier from the API
    url = f"https://www.dnd5eapi.co/api/classes/{class_name}"
    response = requests.get(url)
    if response.status_code == 200:
        response_specifc_class = response.json()
    else: 
        raise ValueError("Failed to fetch class data.")

    hit_die = response_specifc_class['hit_die']
    return hit_die + constitution_modifier

    
@app.route("/save_player", methods=["GET", "POST"])
def save_character():
    data = request.get_json()
    # get basic information from the character creation form
    input_character_name = data.get("characterName")
    input_character_race = data.get("race")
    input_character_class = data.get("class")
    input_character_background = data.get("background")
    input_character_alignment = data.get("alignment")

    # get ability scores for the character
    input_character_strength = int( data.get("ability1") )
    input_character_dexterity = int( data.get("ability2") )
    input_character_constitution = int( data.get("ability3") )
    input_character_intelligence = int( data.get("ability4") )
    input_character_wisdom = int( data.get("ability5") )
    input_character_charisma = int( data.get("ability6") )

    # calculate ability modifiers
    strength_modifier = determine_ability_modifier("STR", input_character_strength, input_character_race)
    dexterity_modifier = determine_ability_modifier("DEX", input_character_dexterity, input_character_race)
    constitution_modifier = determine_ability_modifier("CON", input_character_constitution, input_character_race)
    intelligence_modifier = determine_ability_modifier("INT", input_character_intelligence, input_character_race)
    wisdom_modifier = determine_ability_modifier("WIS", input_character_wisdom, input_character_race)
    charisma_modifier = determine_ability_modifier("CHA", input_character_charisma, input_character_race)
    
    modifiers = [ strength_modifier, dexterity_modifier, constitution_modifier, intelligence_modifier, wisdom_modifier, charisma_modifier]

    max_hp = calculate_hp(input_character_race, input_character_class, input_character_constitution)
    
    player_id = 0
    while True:
        current_db = db.session.get( player_data, player_id )
        if current_db == None: break
        player_id += 1

    new_character = player_data(
        id=player_id,
        name=input_character_name,
        race=input_character_race,
        class_name=input_character_class,
        alignement=input_character_alignment,
        abilities=[ input_character_strength,
                    input_character_dexterity,
                    input_character_constitution,
                    input_character_intelligence,
                    input_character_wisdom,
                    input_character_charisma
        ],
        skill="",
        current_health=max_hp,
        max_health=max_hp,
        #ability_modifiers = modifiers
    )

    db.session.add(new_character)
    db.session.commit()

    return jsonify(hello=0) #render_template("character.html", character=new_character)

    if __name__ == "__main__":
        app.run(debug=True)

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
