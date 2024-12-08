# File to create a player table

from .game_database import db

class player_data(db.Model):
    __tablename__ = 'player_data'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    race = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(100), nullable=False)
    abilities = db.Column(db.ARRAY(db.Integer), nullable=False)
    current_health = db.Column(db.Integer, nullable=False)
    max_health = db.Column(db.Integer, nullable=False)
    alignment = db.Column(db.String(50), nullable=False)  # Ensure this field is correctly set up

    def __init__(self, name, race, class_name, abilities, current_health, max_health, alignment):
        self.name = name
        self.race = race
        self.class_name = class_name
        self.abilities = abilities
        self.current_health = current_health
        self.max_health = max_health
        self.alignment = alignment

    def __repr__(self):
        return f"Player('{self.name}', '{self.race}', '{self.class_name}', '{self.abilities}', '{self.current_health}', '{self.max_health}', '{self.alignment}')"

