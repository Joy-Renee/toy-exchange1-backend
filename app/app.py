from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from models import db, User, Message, Toy  # Import models

app = Flask(__name__)

# Configure Flask app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///toy_trading.db"  # Change for production
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "supersecretkey"  # Change in production

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable real-time chat

# ============================
# 1️⃣ USER SIGNUP (REGISTER)
# ============================
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    phone_number = data.get("phone_number")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username, email=email, phone_number=phone_number, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

# ============================
# 2️⃣ USER LOGIN
# ============================
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token, "user_id": user.id}), 200
    return jsonify({"error": "Invalid email or password"}), 401

# ============================
# 3️⃣ HOME PAGE (SHOW TOYS)
# ============================
@app.route("/home", methods=["GET"])
def home():
    toys = Toy.query.all()
    toy_list = [{"id": toy.id, "name": toy.name, "price": toy.price, "image": toy.image_filename} for toy in toys]
    return jsonify(toy_list), 200

# ============================
# 4️⃣ REAL-TIME CHAT (WebSockets)
# ============================

# Store chat rooms
rooms = {}

# Handle user joining a room
@socketio.on("join")
def handle_join(data):
    username = data["user"]
    room = data["room"]
    
    join_room(room)
    emit("message", {"user": "System", "text": f"{username} has joined the chat."}, room=room)

# Handle sending messages
@socketio.on("message")
def handle_message(data):
    room = data["room"]
    message = {"user": data["user"], "text": data["message"]}
    
    # Store messages in room
    if room in rooms:
        rooms[room].append(message)
    else:
        rooms[room] = [message]
    
    emit("message", message, room=room)

# Handle user leaving a room
@socketio.on("leave")
def handle_leave(data):
    username = data["user"]
    room = data["room"]
    
    leave_room(room)
    emit("message", {"user": "System", "text": f"{username} has left the chat."}, room=room)

# ============================
# 5️⃣ PROFILE PAGE
# ============================
@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_info = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "toys": [{"id": toy.id, "name": toy.name, "price": toy.price} for toy in user.toys]
    }
    return jsonify(user_info), 200

# ============================
# 6️⃣ RUN SERVER
# ============================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don’t exist
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)  # Run with SocketIO
