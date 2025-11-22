# File routes/catalogs.py
from flask import Blueprint, request, jsonify

from models import db
from models.catalogs import Category, Supplier, Customer

catalogs_bp = Blueprint('catalogs', __name__)

# Categorias
@catalogs_bp.route('/categories', methods=['GET'])
def get_categories():
    cats = Category.query.filter_by(active=True).all()
    result = []

    for c in cats:
        result.append({
            'id': c.id,
            'name': c.name,
            'parent_id': c.parent_id
        })

    return jsonify(result), 200

@catalogs_bp.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get_or_404(id)
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
        return jsonify({'error': 'Datos incompletos'}), 400

    new_cat = Category(
        name=data['name'],
        description=data.get('description'),
        parent_id=data.get('parent_id')
    )

    db.session.add(new_cat)
    db.session.commit()
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
        return jsonify({'message': 'Categoria actualizada'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@catalogs_bp.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    category.active = False # Soft-delete
    db.session.commit()
    return jsonify({'message': 'Categoria desactivada'}), 200

# Proveedores
@catalogs_bp.route('/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.filter_by()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'contact': s.contact_name
    } for s in suppliers])

@catalogs_bp.route('/suppliers/<int:id>', methods=['GET'])
def get_supplier(id):
    supplier = Supplier.query.get_or_404(id)
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

    new_sup = Supplier(
        name=data['name'],
        contact_name=data.get('contact_name'),
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get['address']
    )

    db.session.add(new_sup)
    db.session.commit()
    return jsonify({'id': new_sup.id, 'message': 'Proveedor creado'}), 201

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
        return jsonify({'message': 'Proveedor actualizado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@catalogs_bp.route('/suppliers/<int:id>', methods=['DELETE'])
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    supplier.active = False  # Soft-delete
    db.session.commit()
    return jsonify({'message': 'Proveedor desactivado'}), 200

# Clientes
@catalogs_bp.route('/customers', methods=['POST'])
def get_customers():
    customers = Customer.query.filter_by(active=True).all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'credit_limit': float(c.credit_limit),
        'balance': float(c.current_balance)
    } for c in customers]), 200

@catalogs_bp.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
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
    new_cust = Customer(
        name=data['name'],
        phone=data.get('phone'),
        address=data.get('address'),
        credit_limit=data.get('credit_limit', 0)
    )
    db.session.add(new_cust)
    db.session.commit()
    return jsonify({'id': new_cust.id, 'message': 'Cliente creado'}), 201

@catalogs_bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()

    try:
        if 'name' in data: customer.name = data['name']
        if 'phone' in data: customer.phone = data['phone']
        if 'address' in data: customer.address = data['address']
        if 'credit_limit' in data: customer.credit_limit = data['credit_limit']
        # OJO: current_balance no se edita aquí, se edita por ventas/pagos
        if 'active' in data: customer.active = data['active']

        db.session.commit()
        return jsonify({'message': 'Cliente actualizado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@catalogs_bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    customer.active = False  # Soft-delete
    db.session.commit()
    return jsonify({'message': 'Cliente desactivado'}), 200