from ..database import database as db

# This tells us that the model is a subclass of db.Model
class game_data(db.Model):
    # __tablename__ = "game_data"
    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(100), nullable=False)
    player_id = db.Column(db.Integer, nullable=False)
    
    def __init__(self, id, name, p_ids):
        self.game_id = id
        self.game_name = name
        self.player_id = p_ids
