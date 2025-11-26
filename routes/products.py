# File routes/products.py
import logging

from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from models import db
from models.product import Product

products_bp = Blueprint('products', __name__)

logger = logging.getLogger(__name__)

# Listar todos
@products_bp.route('/', methods=['GET'])
def get_products():
    # Detectar parámetro ?all=true en la URL
    show_all = request.args.get('all', 'false').lower() == 'true'

    query = Product.query

    # Si NO piden todos, filtramos solo los activos (comportamiento por defecto)
    if not show_all:
        query = query.filter_by(active=True)

    products = query.all()
    logger.info("Productos consultados - 200")
    return jsonify([p.to_dict() for p in products]), 200

# Obtener uno
@products_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    logger.info(f"Producto #{id} consultado - 200")
    return jsonify(product.to_dict()), 200

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

    logger.info("Busqueda de productos realizada - 200")
    return jsonify([p.to_dict() for p in products]), 200

# CREAR
@products_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()

    try:
        new_product = Product(
            code=data.get('code'),
            name=data.get('name'),
            description=data.get('description'),
            buy_price=data.get('buy_price'),
            sell_price=data.get('sell_price'),
            actual_stock=data.get('stock', 0),
            minimum_stock=data.get('min_stock', 5)
        )

        db.session.add(new_product)
        db.session.commit()

        logger.info("Producto creado - 201")
        return jsonify(new_product.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al crear producto - 500 - {str(e)}")
        return jsonify({'error': str(e)}), 500

# ACTUALIZAR
@products_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()

    try:
        if 'code' in data and data['code'] != product.code:
            existing = Product.query.filter_by(code=data['code']).first()
            if existing:
                logger.error("El codigo del producto ya existe - 400")
                return jsonify({'error': 'EL codigo del producto ya existe'}), 400
            product.code = data['code']

        if 'name' in data: product.name = data['name']
        if 'description' in data: product.description = data['description']
        if 'category_id' in data: product.category_id = data['category_id']
        if 'buy_price' in data: product.buy_price = data['buy_price']
        if 'sell_price' in data: product.sell_price = data['sell_price']
        if 'stock' in data: product.actual_stock = data['stock']
        if 'min_stock' in data: product.minimum_stock = data['min_stock']
        if 'active' in data: product.active = data['active']

        db.session.commit()
        logger.info(f"Producto #{id} actualizado - 200")
        return jsonify(product.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al actualziar producto #{id} - 500 - {str(e)}")
        return jsonify({'error': str(e)}), 500

# ELIMINAR (Soft Delete)
@products_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    product.active = False # No borramos, solo desactivamos (en este tipo de sistemas es crucial conservar los registros)
    db.session.commit()
    logger.info(f"Producto #{id} desactivado - 200")
    return jsonify({'message': 'Producto eliminado correctamente'}), 200