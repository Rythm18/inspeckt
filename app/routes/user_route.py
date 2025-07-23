from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import logging

user_bp = Blueprint('user', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@user_bp.route('/signup', methods=['POST'])
def signup():
    try:
        logger.info(f"Signup attempt from IP: {request.remote_addr}")
        data = request.get_json()

        if not data or not data.get('username') or not data.get('password'):
            logger.warning("Signup failed: Missing username or password")
            return jsonify({'message': 'Username and password are required'}), 400

        if User.query.filter_by(username=data['username']).first():
            logger.warning(f"Signup failed: Username '{data['username']}' already exists")
            return jsonify({'message': 'Username already exists'}), 400
        
        hashed_password = generate_password_hash(data['password'])
        new_user = User(username=data['username'], password_hash=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        logger.info(f"User '{data['username']}' registered successfully")
        return jsonify({'message': 'User registered successfully'}), 201
        
    except Exception as e:
        logger.error(f"Database error during signup: {str(e)}")
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        logger.info(f"Login attempt from IP: {request.remote_addr}")
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            logger.warning("Login failed: Missing username or password")
            return jsonify({'message': 'Username and password are required'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if user and check_password_hash(user.password_hash, data['password']):
            access_token = create_access_token(identity=user.id)
            logger.info(f"User '{data['username']}' logged in successfully")
            
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'user_id': user.id
            }), 200
        
        logger.warning(f"Login failed for username: {data['username']}")
        return jsonify({'message': 'Invalid username or password'}), 401
        
    except Exception as e:
        logger.error(f"Database error during login: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500