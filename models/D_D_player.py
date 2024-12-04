from ..database import database as db

# This tells us that the model is a subclass of db.Model
class DungeonsandDragons_player(db.Model):
    # __tablename__ = "player_data"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    race = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(100), nullable=False)
    alignment = db.Column(db.String(100), nullable=False)
    abilities = db.Column(db.Integer, nullable=False)
    skill = db.Column(db.String(100), nullable=False)
    current_health = db.Column(db.Integer, nullable=False)
    max_health = db.Column(db.Integer, nullable=False)
