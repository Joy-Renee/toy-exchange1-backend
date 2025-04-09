from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_migrate import Migrate
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
migrate = Migrate(app, db)

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
        access_token = create_access_token(identity=str(user.id))
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
    sender = data["user"]
    message_text = data["message"]
    room = data["room"]

    sender_user = User.query.filter_by(username=sender).first()
    if not sender_user:
        return  # Don't store messages from unknown users

    # Get receiver from the room (assuming room names are unique for users)
    receiver_user = User.query.filter(User.username != sender).first()  

    # Store in database
    new_message = Message(
        message_text=message_text,
        sender_id=sender_user.id,
        receiver_id=receiver_user.id if receiver_user else None,
        room=room # ✅ Store room in the database
    )

    db.session.add(new_message)
    db.session.commit()

    # Emit the message back to all clients
    emit("message", {"user": sender, "text": message_text, "room": room}, room=room)

# Handle user leaving a room
@socketio.on("leave")
def handle_leave(data):
    username = data["user"]
    room = data["room"]

    leave_room(room)
    emit("message", {"user": "System", "text": f"{username} has left the chat."}, room=room)

# ============================
# 5️⃣ Fetch messages from database
# ============================

@app.route("/messages/<room>", methods=["GET"])
def get_messages(room):
    messages = Message.query.filter_by(room=room).all()  # 🔥 Filter by room!
    
    messages_data = [
        {
            "id": msg.id,
            "message": msg.message_text,
            "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "sender": User.query.get(msg.sender_id).username,
        }
        for msg in messages
    ]
    return {"messages": messages_data}, 200


# ============================
# 5️⃣ PROFILE PAGE
# ============================
@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    toys = [
        {
            "id": toy.id,
            "name": toy.name,
            "age_group": toy.age_group,
            "description": toy.description,
            "condition": toy.condition,
            "price": toy.price,
            "image_filename": toy.image_filename
        } for toy in user.toys
    ]

    return jsonify({
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "toys": toys
    }), 200


@app.route('/create-toy', methods=['POST'])
@jwt_required()
def create_toy():
    user_id = get_jwt_identity()
    data = request.get_json()
    print("Received toy data:", data)  # Add this line to debug

    required_fields = ["name", "age_group", "description", "condition", "price", "image_filename"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "Missing or invalid toy data"}), 422

    toy = Toy(
        name=data['name'],
        age_group=data['age_group'],
        description=data['description'],
        condition=data['condition'],
        price=data['price'],
        image_filename=data['image_filename'],
        user_id=user_id
    )
    db.session.add(toy)
    db.session.commit()
    return jsonify({"message": "Toy created successfully"}), 201

# ============================
# 6️⃣ RUN SERVER
# ============================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don’t exist
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)  # Run with SocketIO
