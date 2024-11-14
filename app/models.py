from app import db


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_food = db.Column(db.String(30), nullable=False)
    category = db.Column(db.Integer, nullable=False)
    weight_gr = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    ingredients = db.Column(db.Text)
    image = db.Column(db.String(30))
    time_create = db.Column(db.DateTime)
    time_update = db.Column(db.DateTime)



