# File to use cli to access and modify database
# Check whetehr we even need to create and populate the database every time we launch the app - seems wrong
from .game_database import db as database
import click
from flask.cli import with_appcontext
from .player import Player
from .game import Game

"""
@click.command("create_all", help="Create tables")
@with_appcontext
def create_all():
    database.create_all()


@click.command("drop_all", help="Drop tables")
@with_appcontext
def drop_all():
    database.drop_all()


@click.command("populate", help="Populate database")
@with_appcontext
def populate():
    initial_player_data = [
        Player(
            id=1,
            name="Arni",
            species="Human",
            abilities="Druid", # class is reserved word in Python, so calling DnD class "abilities"
            alignment="Neutral",
            skill="Stealth",
            current_health=100,
            max_health=100
        ),
        Player(
            id=2,
            name="Molly",
            species="Human",
            abilities="Wizard",  # class is reserved word in Python, so calling DnD class "abilities"
            alignment="Neutral",
            skill="Stealth",
            current_health=90,
            max_health=100
        )
    ]

    # Committing the initial player info
    for player in initial_player_data:
        database.session.add(player)
    database.session.commit()
"""
