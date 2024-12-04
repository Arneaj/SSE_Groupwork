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