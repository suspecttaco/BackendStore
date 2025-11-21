# File routes/sales.py
import threading

from flask import Blueprint, request, jsonify
from models import db
from models.product import Product
from models.sale import Sale
from models.sale_detail import SaleDetail
from services.socket_events import socketio

sales_bp = Blueprint('sales', __name__)

sale_lock = threading.Lock()

@sales_bp.route('/', methods=['POST'])
def register_sale():
    data = request.get_json()

    if not data or 'user_id' not in data or 'products' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400

    user_id = data['user_id']
    items = data['products']

    if not items:
        return jsonify({'error': 'El carrito esta vacio'}), 400

    with sale_lock:
        try:
            # Inicio de transaccion segura
            # Crear header de venta
            new_sale = Sale(
                user_id=user_id,
                total=0,
            )
            db.session.add(new_sale)
            db.session.flush()

            total = 0

            # Procesado de cada producto
            for item in items:
                product_id = item['product_id']
                amount = float(item['amount'])

                product = Product.query.get(product_id)

                if not product or not product.active:
                    raise Exception(f"Producto ID {product_id} no disponible")

                if float(product.actual_stock) < amount:
                    raise Exception(f"Stock insuficiente para: {product.name}")

                # Descontar stock
                product.actual_stock = float(product.actual_stock) - amount

                # Calcular subtotal
                price = float(product.sell_price)
                subtotal = price * amount
                total += subtotal

                # Crear Detalle de Venta
                detail = SaleDetail(
                    sale_id=new_sale.id,
                    product_id=product.id,
                    amount=amount,
                    unit_price=price,
                    subtotal=subtotal
                )

                db.session.add(detail)

            # Actualizar total final y guardar
            new_sale.total = total
            db.session.commit()
            # Fin de transaccion segura

            # Notificacion por socket
            socketio.emit('inventory updated',{
                'message': 'Nueva venta registrada',
                'sale_id': new_sale.id
            })

            return jsonify({
                'message': 'Venta registrada',
                'sale_id': new_sale.id,
                'total': total
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400