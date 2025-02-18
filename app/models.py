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
    __tablename__ = "customers"

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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age_group = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(300), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    sender_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    receiver_id = db.Coulumn(db.Integer, db.ForeignKey("seller.id"), nullable=False)
    toy_id = db.Column(db.Integer, db.ForeignKey("toy.id"), nullable=False)

class PaymentFromBuyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(50), default="Pending")

    buyer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    toy_id = db.Column(db.Integer, db.ForeignKey("toy.id"), nullable=False)

class PaymentToSeller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(50), default="Pending")

    seller_id = db.Column(db.Integer, db.ForeignKey("seller.id"), nullable=False)
    toy_id = db.Column(db.Integer, db.ForeignKey("toy.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)

class Exchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default="Pending")
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    buyer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("seller.id"), nullable=False)
    buyer_toy_id =db.Column(db.Integer, db.ForeignKey("toy.id"))  # Toy offered by buyer
    seller_toy_id = db.Column(db.Integer, db.ForeignKey("toy.id"))  # Toy offered by seller
    