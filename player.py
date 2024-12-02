# File to create a player database

from game_database import db

class Player(db.Model):
    __tablename = 