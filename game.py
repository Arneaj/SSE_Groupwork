# Game table
from .game_database import db

class Game(db.Model):
    __tablename__ = "game_data"
    game_id = db.Column(db.Integer, nullable=False)
    game_name = db.Column(db.String, nullable=False) # Add a check in create new game page that you cant submit form without all fields being filled in
    player_id = db.Column(db.Integer, primary_key=True) # Same as player id, primary key