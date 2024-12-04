from flask import Blueprint, render_template, redirect, url_for, request
from sqlalchemy.orm import joinedload

from sqlalchemy import select

# This will import the database object, which is an instance of SQLAlchemy that is configured to connect to the database
from ..database import database

# Imports the DungeonsandDragons_game and DungeonsandDragons_player models, which 
# maps to two separate tables in the database 
from ..models.D_D_game import game_data
from ..models.D_D_player import player_data

# Define Blueprint for dungeons_and_dragons 
dungeons_and_dragons = Blueprint("dungeons_and_dragons", __name__, url_prefix="/dungeons_and_dragons")

# Route to show all games 
@dungeons_and_dragons.route("/games", methods=["GET"])
def show_games():
    # Query all games from the game_data database
    games = database.session.query(game_data).all()
    return render_template("games_index.html", games=games)

# Route to show all players 
@dungeons_and_dragons.route("/players", methods=["GET"])
def show_players():
    # Query all players from the player_data database
    players = database.session.query(player_data).all()
    return render_template("players_index.html", players=players)

# Route to create a new game
@dungeons_and_dragons.route("/create_game", methods=["GET", "POST"])
def create_game():
    if request.method == "POST":

        name = request.form.get("name")
        race = request.form.get("race")
        class_name = request.form.get("class_name")
        alignement = request.form.get("alignement")
        abilities = request.form.get("abilities")
        skill = request.form.get("skill")
        current_health = request.form.get("current_health")
        max_health = request.form.get("max_health")


        # Create a new player in the player_data database
        new_player = player_data(
            name=name, 
            race=race, 
            class_name=class_name,
            alignement=alignement, 
            abilities=abilities, 
            skill=skill, 
            current_health=current_health, 
            max_health=max_health
        )

        database.session.add(new_player)
        database.session.commit()
        return redirect(url_for(".show_players"))

    return render_template("create_game.html")




        
        
