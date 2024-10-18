# auth.py
from flask import Blueprint, request, jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models import db, User

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/register', methods=['POST'])
def register():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return _corsify_actual_response(jsonify({'message': 'User registered successfully'})), 201

@auth.route('/login', methods=['POST'])
def login():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 400

    access_token = create_access_token(identity={'id': user.id})
    return _corsify_actual_response(jsonify({'token': access_token})), 200

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
