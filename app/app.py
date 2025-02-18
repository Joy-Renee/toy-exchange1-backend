from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from models import db, User, Message

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSocket connections

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your_secret_key"

# db = SQLAlchemy(app)
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Welcome to the Chat App of the toy exchange project website!"

# User signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_user = User(username=data["username"], email=data["email"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201

# User login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Handle sending messages
@socketio.on("send_message")
def handle_send_message(data):
    sender_id = data["sender_id"]
    receiver_id = data["receiver_id"]
    message_text = data["message"]

    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, message=message_text)
    db.session.add(new_message)
    db.session.commit()

    room = f"chat_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"
    emit("receive_message", data, room=room)

# Start Flask App
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
