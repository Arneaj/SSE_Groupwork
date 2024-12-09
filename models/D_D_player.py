from ..database import database as db  # Database from parent folder

# This tells us that the model is a subclass of db.Model


class player_data(db.Model):
    # __tablename__ = "player_data"
    id = db.Column(db.Integer, primary_key=True)
    # Integer id is used as the primary key, to link tables
    name = db.Column(db.String(100), nullable=False)
    race = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(100), nullable=False)
    alignement = db.Column(db.String(100), nullable=False)
    abilities = db.Column(db.Integer, nullable=False)
    skill = db.Column(db.String(100), nullable=False)
    current_health = db.Column(db.Integer, nullable=False)
    max_health = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return (
            f"Player('{self.name}', "
            f"'{self.race}', "
            f"'{self.class_name}', "
            f"'{self.alignement}', "
            f"'{self.abilities}', "
            f"'{self.skill}', "
            f"'{self.current_health}', "
            f"'{self.max_health}')"
        )
