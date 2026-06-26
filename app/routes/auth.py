from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app import db
from app.models.customer import Customer

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Username, email and password are required'}), 400

    existing = Customer.query.filter_by(email=email).first()
    if existing:
        return jsonify({'error': 'Email already registered'}), 409

    hashed_password = generate_password_hash(password)

    customer = Customer(
        username=username,
        email=email,
        password_hash=hashed_password
    )

    db.session.add(customer)
    db.session.commit()

    return jsonify({'message': f'Welcome to Kermit Koffee, {username}!'}), 201