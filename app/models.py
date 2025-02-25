from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    toys = db.relationship('Toy', back_populates='user', cascade='all, delete-orphan')

class Toy(db.Model):
    __tablename__ ="toys"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age_group = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    user = db.relationship('User', back_populates='toys')

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    buyer_toy_id = db.Column(db.Integer, db.ForeignKey("toys.id"))
    seller_toy_id = db.Column(db.Integer, db.ForeignKey("toys.id"))

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver  = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(50), default="Pending")
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    toy_id = db.Column(db.Integer, db.ForeignKey("toys.id"), nullable=False)

    buyer = db.relationship('User', backref='payments')
    toy = db.relationship('Toy', backref='toy_payments')


class Exchange(db.Model):
    __tablename__ = "exchanges"
    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default="Pending")
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    buyer_toy_id =db.Column(db.Integer, db.ForeignKey("toys.id"))  # Toy offered by buyer
    seller_toy_id = db.Column(db.Integer, db.ForeignKey("toys.id"))  # Toy offered by seller
    
    buyer_toy = db.relationship('Toy', foreign_keys=[buyer_toy_id], backref='buyer_exchanges')
    seller_toy = db.relationship('Toy', foreign_keys=[seller_toy_id], backref='seller_exchanges')