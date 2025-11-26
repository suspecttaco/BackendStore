# File routes/auth.py
import logging

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.user import User

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Verificar existencia
    if User.query.filter_by(username=data['username']).first():
        logger.error(f"El usuario '{data['username']}' ya existe")
        return jsonify({'error': 'El usuario ya existe'}), 400

    # Hash de password antes de guardar
    hashed_password = generate_password_hash(data['password'])

    new_user = User(
        username=data['username'],
        password=hashed_password,
        full_name=data.get('full_name', ''),
        role=data.get('role', 'cashier')
    )

    db.session.add(new_user)
    db.session.commit()

    logger.info(f"Usuario '{data['username']}' creado exitosamente")
    return jsonify({'message': 'Usuario creado exitosamente'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validar que enviaron datos
    if not data or 'username' not in data or 'password' not in data:
        logger.warning("Intento de login - Faltan datos")
        return jsonify({'error': 'Faltan datos'}), 400

    user = User.query.filter_by(username=data['username']).first()

    # Validacion usando hash
    if user and check_password_hash(user.password, data['password']):
        if not user.active:
            logger.error("Intento de login - Usuario inactivo")
            return jsonify({'error': 'Usuario inactivo'}), 403

        logger.info(f"Login exitoso para '{data.get('username')}'")
        return jsonify({
            'message': 'Login exitoso',
            'user': user.to_dict(),
            'token': 'dummy_token_for_mvp'
        }), 200

    logger.error("Credenciales invalidas")
    return jsonify({'error': 'Credenciales invalidas'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Nota: hacer que el cliente olvide el token despues de esto
    logger.info("Sesion cerrada exitosamente")
    return jsonify({'message': 'Sesion cerrada exitosamente'}), 200