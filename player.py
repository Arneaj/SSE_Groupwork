# File to create a player database

from .game_database import db

class Player(db.Model):
    __tablename__ = "player_data"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False)
    abilities = db.Column(db.String(100), nullable=False)
    alignment = db.Column(db.String(100), nullable=False)
    skill = db.Column(db.String(100), nullable=False)
    current_health = db.Column(db.Integer, nullable=False)
    max_health = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, nullable=False)
