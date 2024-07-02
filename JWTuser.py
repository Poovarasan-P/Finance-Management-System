from flask import Blueprint, request, jsonify
from ..models import db, User
import bcrypt
import jwt
import datetime

users = Blueprint('users', __name__)

# Register a new user
@users.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})

# Login a user
@users.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, 'secretKey')
        return jsonify({'token': token.decode('UTF-8')})
    return jsonify({"message": "Invalid credentials"}), 401
