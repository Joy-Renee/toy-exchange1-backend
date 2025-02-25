from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    toys = db.relationship('Toy', back_populates='user', cascade='all, delete-orphan')
    sent_messages = db.relationship('Message', foreign_keys="Message.sender_id", back_populates='user', cascade='all, delete-orphan')
    received_messages = db.relationship('Message', foreign_keys="Message.receiver_id", back_populates='user', cascade='all, delete-orphan')

class Toy(db.Model):
    __tablename__ ="toys"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age_group = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    sent_messages = db.relationship('Message', back_populates='toy', cascade='all, delete-orphan')
    received_messages = db.relationship('Message', back_populates='toy', cascade='all, delete-orphan')

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    buyer_toy_id = db.Column(db.Integer, db.ForeignKey("toy.id"))
    seller_toy_id = db.Column(db.Integer, db.ForeignKey("toy.id"))

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(50), default="Pending")
    buyer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    toy_id = db.Column(db.Integer, db.ForeignKey("toy.id"), nullable=False)

class Exchange(db.Model):
    __tablename__ = "exchanges"
    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default="Pending")
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    buyer_toy_id =db.Column(db.Integer, db.ForeignKey("toy.id"))  # Toy offered by buyer
    seller_toy_id = db.Column(db.Integer, db.ForeignKey("toy.id"))  # Toy offered by seller
    