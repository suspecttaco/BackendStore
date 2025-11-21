# File routes/products.py
from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from models import db
from models.product import Product

products_bp = Blueprint('products', __name__)

# Listar todos
@products_bp.route('/', methods=['GET'])
def get_products():
    # Mostrar solo productos activos
    products = Product.query.filter_by(active=True).all()
    return jsonify([p.to_dict() for p in products]), 200

# BUSCAR (Nombre o codigo)
@products_bp.route('/search', methods=['GET'])
def search_products():
    q = request.args.get('q', '')
    if not  q:
        return jsonify([]), 200

    search = f"%{q}%"
    products = Product.query.filter(
        Product.active == True,
        or_(Product.name.ilike(search), Product.code.ilike(search))
    ).all()

    return jsonify([p.to_dict() for p in products]), 200

# CREAR
@products_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()

    try:
        new_product = Product(
            code=data.get('code'),
            name=data['name'],
            description=data.get('description'),
            buy_price=data.get('buy_price'),
            sell_price=data['sell_price'],
            actual_stock=data.get('actual_stock', 0),
            minimum_stock=data.get('minimum_stock', 5)
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify(new_product.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ACTUALIZAR
@products_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()

    try:
        if 'code' in data: product.code = data['code']
        if 'name' in data: product.name = data['name']
        if 'description' in data: product.description = data['description']
        if 'buy_price' in data: product.buy_price = data['buy_price']
        if 'sell_price' in data: product.sell_price = data['sell_price']
        if 'actual_stock' in data: product.actual_stock = data['actual_stock']
        if 'minimum_stock' in data: product.minimum_stock = data['minimum_stock']
        if 'active' in data: product.active = data['active']

        db.session.commit()

        return jsonify(product.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ELIMINAR (Soft Delete)
@products_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    product.active = False # No borramos, solo desactivamos (en este tipo de sistemas es crucial conservar los registros)
    db.session.commit()
    return jsonify({'message': 'Producto eliminado correctamente'}), 200