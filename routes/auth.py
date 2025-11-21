# File routes/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Faltan datos'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'El usuario ya existe'}), 400

    # Hash de password antes de guardar
    hashed_password = generate_password_hash(data['password'])

    new_user = User(
        username=data['username'],
        password=hashed_password,
        full_name=data.get('full_name'),
        role=data.get('role', 'cashier')
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario creado exitosamente'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validar que enviaron datos
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Faltan datos'}), 400

    user = User.query.filter_by(username=data['username'].first())

    # Validacion usando hash
    if user and check_password_hash(user.password, data['password']):
        if not user.active:
            return jsonify({'error': 'Usuario inactivo'}), 403

        return jsonify({
            'message': 'Login exitoso',
            'user': user.to_dict()
        }), 200

    return jsonify({'error': 'Credenciales invalidas'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Nota: hacer que el cliente olvide el token despues de esto
    return jsonify({'message': 'Sesion cerrada exitosamente'}), 200