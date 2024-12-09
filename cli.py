import click
from flask.cli import with_appcontext
from .database import database
# from .models.D_D_game import game_data
from .models.D_D_player import player_data


@click.command("create_all", help="Create all tables in the app's database")
@with_appcontext
def create_all():
    database.create_all()


@click.command("drop_all", help="Drop all tables in the app's database")
@with_appcontext
def drop_all():
    database.drop_all()


@click.command("populate", help="Populate the database with initial data")
@with_appcontext
def populate():
    initial_player_data = [
        player_data(
            id=5,
            name="Homer Simpson",
            race="Elf",
            class_name="Bard",
            alignement="Lawful Good",
            abilities="15",
            skill="Deception",
            current_health=100,
            max_health=100,
        ),
        player_data(
            id=6,
            name="Maggie Simpson",
            race="Dwarf",
            class_name="Paladin",
            alignement="Chaotic Neutral",
            abilities="4",
            skill="Perception",
            current_health=100,
            max_health=100,
        ),
    ]

    # Add initial player data to the database and commit changes
    for player in initial_player_data:
        database.session.add(player)

    database.session.commit()
