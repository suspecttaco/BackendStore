# File routes/catalogs.py
import logging

from flask import Blueprint, request, jsonify
from models import db
from models.catalogs import Category, Supplier, Customer

logger = logging.getLogger(__name__)

catalogs_bp = Blueprint('catalogs', __name__)


# Categorias CRUD
@catalogs_bp.route('/categories', methods=['GET'])
def get_categories():
    # CORRECCIÓN: Leer parámetro ?all=true
    show_all = request.args.get('all', 'false').lower() == 'true'

    query = Category.query
    if not show_all:
        query = query.filter_by(active=True)

    cats = query.all()
    result = []
    for c in cats:
        result.append({
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'parent_id': c.parent_id,
            'active': c.active
        })

    logger.info("Categorias consultadas - 200")
    return jsonify(result), 200


@catalogs_bp.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get_or_404(id)
    logger.info(f"Categoria #{id} consultada - 200")
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description,
        'parent_id': category.parent_id,
        'active': category.active
    }), 200


@catalogs_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data or 'name' not in data:
        logger.error("Eror al crear categoria - Faltan datos - 400")
        return jsonify({'error': 'Name is required'}), 400

    new_cat = Category(
        name=data['name'],
        description=data.get('description'),
        parent_id=data.get('parent_id'),
        active=data.get('active', True)
    )
    db.session.add(new_cat)
    db.session.commit()
    logger.info("Categoria creada - 200")
    return jsonify({'id': new_cat.id, 'name': new_cat.name}), 201


@catalogs_bp.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.get_json()

    try:
        if 'name' in data: category.name = data['name']
        if 'description' in data: category.description = data['description']
        if 'parent_id' in data: category.parent_id = data['parent_id']
        if 'active' in data: category.active = data['active']

        db.session.commit()
        logger.info(f"Categoria #{id} actualizada - 200")
        return jsonify({'message': 'Category updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al actualizar categoria #{id} - 500 - {str(e)}")
        return jsonify({'error': str(e)}), 500


@catalogs_bp.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    category.active = False
    db.session.commit()
    logger.info(f"Categoria #{id} desactivada - 200")
    return jsonify({'message': 'Category deleted (soft)'}), 200

# Proveedores CRUD
@catalogs_bp.route('/suppliers', methods=['GET'])
def get_suppliers():
    # CORRECCIÓN: Leer parámetro ?all=true
    show_all = request.args.get('all', 'false').lower() == 'true'

    query = Supplier.query
    if not show_all:
        query = query.filter_by(active=True)

    suppliers = query.all()

    logger.info("Proveedores consultados - 200")

    return jsonify([{
        'id': s.id,
        'name': s.name,
        'contact_name': s.contact_name,
        'phone': s.phone,
        'email': s.email,
        'address': s.address,
        'active': s.active
    } for s in suppliers]), 200


@catalogs_bp.route('/suppliers/<int:id>', methods=['GET'])
def get_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    logger.info(f"Proveedor #{id} consultado - 200")
    return jsonify({
        'id': supplier.id,
        'name': supplier.name,
        'contact_name': supplier.contact_name,
        'phone': supplier.phone,
        'email': supplier.email,
        'address': supplier.address,
        'active': supplier.active
    }), 200


@catalogs_bp.route('/suppliers', methods=['POST'])
def create_supplier():
    data = request.get_json()
    if not data or 'name' not in data:
        logger.error("Error al crear Proveedor - Faltan datos - 400")
        return jsonify({'error': 'Name is required'}), 400

    new_sup = Supplier(
        name=data['name'],
        contact_name=data.get('contact_name'),
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get('address'),
        active=data.get('active', True)
    )
    db.session.add(new_sup)
    db.session.commit()
    logger.info("Proveedor creado - 200")
    return jsonify({'id': new_sup.id, 'message': 'Supplier created'}), 201


@catalogs_bp.route('/suppliers/<int:id>', methods=['PUT'])
def update_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    data = request.get_json()

    try:
        if 'name' in data: supplier.name = data['name']
        if 'contact_name' in data: supplier.contact_name = data['contact_name']
        if 'phone' in data: supplier.phone = data['phone']
        if 'email' in data: supplier.email = data['email']
        if 'address' in data: supplier.address = data['address']
        if 'active' in data: supplier.active = data['active']

        db.session.commit()
        logger.info(f"Proveedor #{id} actualizado - 200")
        return jsonify({'message': 'Supplier updated'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al actualizar Proveedor #{id} - 200 - {str(e)}")
        return jsonify({'error': str(e)}), 500


@catalogs_bp.route('/suppliers/<int:id>', methods=['DELETE'])
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    supplier.active = False
    db.session.commit()
    logger.info(f"Proveedor #{id} desactivado - 200")
    return jsonify({'message': 'Supplier deleted'}), 200


# Clientes CRUD
@catalogs_bp.route('/customers', methods=['GET'])
def get_customers():
    # CORRECCIÓN: Leer parámetro ?all=true
    show_all = request.args.get('all', 'false').lower() == 'true'

    query = Customer.query
    if not show_all:
        query = query.filter_by(active=True)

    customers = query.all()
    logger.info("Clientes consultados - 200")
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'phone': c.phone,
        'address': c.address,
        'credit_limit': float(c.credit_limit),
        'balance': float(c.current_balance),
        'active': c.active
    } for c in customers]), 200


@catalogs_bp.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    logger.info(f"Cliente #{id} consultado - 200")
    return jsonify({
        'id': customer.id,
        'name': customer.name,
        'phone': customer.phone,
        'address': customer.address,
        'credit_limit': float(customer.credit_limit),
        'current_balance': float(customer.current_balance),
        'active': customer.active
    }), 200


@catalogs_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    if not data or 'name' not in data:
        logger.error("Error al crear Cliente - Faltan datos - 400")
        return jsonify({'error': 'Name is required'}), 400

    new_cust = Customer(
        name=data['name'],
        phone=data.get('phone'),
        address=data.get('address'),
        credit_limit=data.get('credit_limit', 0),
        active=data.get('active', True)
    )
    db.session.add(new_cust)
    db.session.commit()
    logger.info("Cliente creado - 200")
    return jsonify({'id': new_cust.id, 'message': 'Customer created'}), 201


@catalogs_bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()

    try:
        if 'name' in data: customer.name = data['name']
        if 'phone' in data: customer.phone = data['phone']
        if 'address' in data: customer.address = data['address']
        if 'credit_limit' in data: customer.credit_limit = data['credit_limit']
        if 'active' in data: customer.active = data['active']

        db.session.commit()
        logger.info(f"Cliente #{id} actualizado - 200")
        return jsonify({'message': 'Customer updated'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al actualizar Cliente #{id} - 500 - {str(e)}")
        return jsonify({'error': str(e)}), 500


@catalogs_bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    customer.active = False
    db.session.commit()
    logger.info(f"Cliente #{id} desactivado - 200")
    return jsonify({'message': 'Customer deleted'}), 200