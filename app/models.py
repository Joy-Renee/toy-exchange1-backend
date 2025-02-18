from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(128), nullable=False)

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     message = db.Column(db.Text, nullable=False)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Toy(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age_group = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(300), nullable=False)


