from ..database import database as db

# This tells us that the model is a subclass of db.Model
class game_data(db.Model):
    # __tablename__ = "game_data"
    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(100), nullable=False)
    player_id = db.Column(db.Integer, nullable=False)
