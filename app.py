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
from sqlalchemy.exc import IntegrityError
import click
from .cli import create_all, drop_all, populate

# MAY NEED TO IMPLEMENT DROP_ALL IN HERE so we can have nice stuff saved in our tables for the demo
# from .cli import create_all, drop_all, populate  # Importing commands - commented out as we didn't want to create/drop things every time at one point


def app(testing=False):
    # Initialise the Flask app
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # For testing the app
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
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://avr24:f61Q%T421>i@db.doc.ic.ac.uk/avr24"  # psql URL - using Arni's personal database
)
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


# Adding behaviours for different app routes
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")  # Takes user to landing page


@app.route("/process_new_game", methods=["GET", "POST"])
def process_new_game():
    data = request.get_json()  # Gets the json object
    game_name = data.get("gameName")  # Different games
    player_list = data.get("playerList")  # Different players

    player_list = [int(player_id) for player_id in player_list]

    game_id = 0
    while True:
        current_db = db.session.get(game_data, game_id)
        if current_db == None:
            break
        game_id += 1

    db.session.add(game_data(game_id, game_name, player_list))

    db.session.commit()

    return jsonify(game_id=game_id)


# The start game page
@app.route("/STARTGAME", methods=["GET", "POST"])
def startGame():
    # Get the game from the request - game_id is separate to the player id (primary key)
    game_id_input = request.args.get("game_id")

    # Get the game from the database
    passed_game = db.get_or_404(game_data, game_id_input)

    # Get the players of that game from the database
    passed_players = [
        db.get_or_404(player_data, player_id) for player_id in passed_game.player_id
    ]

    # Gets the monsters
    challenge_rating_input = request.args.get(
        "challenge_index"
    )  # Challenge rating input required for fetching appropriate monsters

    if challenge_rating_input == None:
        challenge_rating_input = 0

    # Gets different monsters depending on player's challenge rating input
    url = f"https://www.dnd5eapi.co/api/monsters?challenge_rating={challenge_rating_input}"
    response = requests.get(url)
    if response.status_code == 200:
        monsters_response = response.json()

    monsters = monsters_response["results"]

    return render_template(  # Takes user to the main page - containing info on game, players, abilities, monsters, dice
        "main.html",
        game=passed_game,
        players=passed_players,
        monsters=monsters,
    )


# Functionality for the new game page
@app.route("/game_creation", methods=["GET", "POST"])
def create_game():
    players = (
        db.session.query(player_data).order_by(player_data.id).all()
    )  # Fetch all players

    # If no game name was provided, render the game creation form (consider returning a 400 response)
    return render_template("create_new_game.html", players=players)


# The create player page
@app.route("/player_creation", methods=["GET", "POST"])
def create_player():

    # go to api and get all information that is needed - STILL RELEVANT?

    # Get races - Note: we called them "species" in database and app
    url = "https://www.dnd5eapi.co/api/races"
    response = requests.get(url)  # Gets the races from the api
    if response.status_code == 200:
        races_response = response.json()

    races = races_response["results"]  # Returns the races from the json

    # Gets DnD classes
    url = "https://www.dnd5eapi.co/api/classes"
    response = requests.get(url)
    if response.status_code == 200:
        classes_response = response.json()

    classes = classes_response["results"]  # Returns the classes from the json

    # Gets DnD backgrounds
    url = "https://www.dnd5eapi.co/api/backgrounds"
    response = requests.get(url)
    if response.status_code == 200:
        backgrounds_response = response.json()

    backgrounds = backgrounds_response["results"]

    # Gets alignments
    url = "https://www.dnd5eapi.co/api/alignments"
    response = requests.get(url)
    if response.status_code == 200:
        alignments_response = response.json()

    alignments = alignments_response["results"]

    return render_template(  # Renders the create new character page
        "create_new_character.html",
        races=races,
        classes=classes,
        backgrounds=backgrounds,
        alignments=alignments,
    )


@app.route("/games_index", methods=["GET", "POST"])
def games_index():
    passed_games = db.session.query(game_data).order_by(game_data.game_id).all()

    """
    i = 0
    while True:
        current_db = db.session.get( game_data, i )
        if current_db == None: 
            break
        passed_games.append(current_db)
        i += 1
    """

    passed_players = [
        [
            db.session.get(player_data, player_id)
            for player_id in passed_game.player_id
            if db.session.get(player_data, player_id) != None
        ]
        for passed_game in passed_games
    ]

    passed_json = []

    for i in range(len(passed_games)):
        passed_json.append({"game": passed_games[i], "players": passed_players[i]})

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
        if isinstance(specific_race_data, list):  # Check if the response is a list
            return 0  # No modifier available for the given race
        bonuses = specific_race_data.get("ability_bonuses", [])
        if isinstance(bonuses, list):
            for bonus in bonuses:
                ability = bonus["ability_score"][
                    "name"
                ]  # e.g., "Strength", "Dexterity", etc
                if ability.lower() == skill.lower():
                    return bonus["bonus"]
    # If no modifier for that race and skill, or if the request fails, return 0
    return 0


def determine_ability_modifier(skill, ability_score, race):
    race_modifier = get_race_modifier(skill, race)
    return round((ability_score + race_modifier) - 10) // 2


def roll_ability_scores():
    scores = []
    for i in range(6):
        rolls = sorted([random.randint(1, 6) for j in range(4)], reverse=True)
        scores.append(sum(rolls[1:]))  # Drop the lowest roll and keep the rest
    return scores


def calculate_hp(class_name, constitution_score, race):
    constitution_modifier = determine_ability_modifier(
        "Constitution", constitution_score, race
    )

    if not class_name.startswith("/api/classes/"):
        class_name = f"/api/classes/{class_name}"

    # Fetch the hit die and constitution modifier from the API
    url = f"https://www.dnd5eapi.co{class_name}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception if the request fails
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch class data from {url}: {str(e)}")

    # If the response is successful, extract the hit die
    if response.status_code == 200:
        response_specifc_class = response.json()
        if isinstance(response_specifc_class, list) and len(response_specifc_class) > 0:
            hit_die = response_specifc_class[0].get(
                "hit_die", 0
            )  # Default to 0 if not found
        else:
            hit_die = 0  # No valid hit die found, use default
    else:
        raise ValueError(
            f"Failed to fetch class data. Status code: {response.status_code}"
        )

    return hit_die + constitution_modifier


@app.route("/save_player", methods=["POST"])
def save_character():
    data = request.get_json()

    # Validate required fields
    if not data.get("characterName"):
        return jsonify({"error": "Character name is required"}), 400

    if not data.get("race"):
        return jsonify({"error": "Race is required"}), 400

    if not data.get("class"):
        return jsonify({"error": "Class is required"}), 400

    # Get basic information from the character creation form
    input_character_name = data.get("characterName")
    input_character_race = data.get("race")
    input_character_class = data.get("class")

    # Get ability scores for the character
    input_character_strength = int(data.get("ability1"))
    input_character_dexterity = int(data.get("ability2"))
    input_character_constitution = int(data.get("ability3"))
    input_character_intelligence = int(data.get("ability4"))
    input_character_wisdom = int(data.get("ability5"))
    input_character_charisma = int(data.get("ability6"))

    # Calculate max HP
    max_hp = calculate_hp(
        input_character_class, input_character_constitution, input_character_race
    )
    # Calculate current health (using a placeholder logic for this example)
    current_health = max_hp  # Placeholder; adjust based on your game mechanics

    # Ensure unique player ID
    last_player_id_row = (
        db.session.query(player_data.id).order_by(db.desc(player_data.id)).first()
    )
    player_id = last_player_id_row[0] + 1 if last_player_id_row else 1

    # Set alignment only if provided, else default to 'Neutral'
    alignment = data.get("alignment", "Neutral")

    # Create new character with all fields
    new_character = player_data(
        id=player_id,
        name=input_character_name,
        race=input_character_race,
        class_name=input_character_class,
        skill="",
        abilities=[
            input_character_strength,
            input_character_dexterity,
            input_character_constitution,
            input_character_intelligence,
            input_character_wisdom,
            input_character_charisma,
        ],
        current_health=current_health,
        max_health=max_hp,
        alignement=alignment,  # Ensure alignment is passed properly
    )

    db.session.add(new_character)
    db.session.commit()

    return (
        jsonify({"message": "Character created successfully"}),
        200,
    )  # Return 200 for success with resource creation

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


@app.route("/save", methods=["GET", "POST"])
def save():
    data = request.get_json()

    player_ids = data.get("player_ids")
    current_HP = data.get("currentHPList")

    for i, id in enumerate(player_ids):
        player_data.query.get(id).current_health = current_HP[i]

    db.session.commit()

    return jsonify(state=200)
