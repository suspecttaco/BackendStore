# File routes/sales.py
import threading
from datetime import datetime

from dns.e164 import query
from flask import Blueprint, request, jsonify
from models import db
from models.product import Product
from models.sale import Sale, SaleDetail
from services.socket_events import socketio

sales_bp = Blueprint('sales', __name__)

sale_lock = threading.Lock()

# Obtener ventas
@sales_bp.route('/', methods=['GET'])
def get_sales():
    # Filtro de fecha
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    query = Sale.query.order_by(Sale.date.desc())

    if start_date:
        query = query.filter(Sale.date >= start_date)
    if end_date:
        query = query.filter(Sale.date <= end_date)

    sales = query.all()

    result = []

    for s in sales:
        result.append({
            'id': s.id,
            'date': s.date.isoformat(),
            'total': float(s.total),
            'payment_method': s.payment_method,
            'user': s.user.full_name if s.user else 'Desconocido',
            'customer': s.customer.name if s.customer else 'Publico General'
        })

    return jsonify(result), 200

# Obtener venta especifica
@sales_bp.route('/<int:id>', methods=['GET'])
def get_sale_details(id):
    sale = Sale.query.get_or_404(id)

    # Regresar venta con productos
    return jsonify({
        'id': sale.id,
        'date': sale.date.isoformat(),
        'total': float(sale.total),
        'payment_method': sale.payment_method,
        'user': sale.user.full_name if sale.user else 'N/A',
        'customer': sale.customer.name if sale.customer else 'Público General',
        'products': [{
            'product_name': d.product.name if d.product else 'Borrado',
            'amount': float(d.amount),
            'unit_price': float(d.unit_price),
            'subtotal': float(d.subtotal)
        } for d in sale.details]
    }), 200

@sales_bp.route('/', methods=['POST'])
def register_sale():
    data = request.get_json()

    if not data or 'user_id' not in data or 'products' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400

    items = data['products']

    if not items:
        return jsonify({'error': 'El carrito esta vacio'}), 400

    with sale_lock:
        try:
            # Inicio de transaccion segura
            # Crear header de venta
            new_sale = Sale(
                user_id=data['user_id'],
                customer_id=data.get('customer_id'),
                total=0,
                payment_method=data.get('payment_method', 'cash'),
                date=datetime.utcnow()
            )
            db.session.add(new_sale)
            db.session.flush()

            total_amount = 0

            # Procesado de cada producto
            for item in items:
                product = Product.query.get(item['product_id'])
                amount = float(item['amount'])

                if not product or not product.active:
                    raise Exception(f"Producto ID {item['id']} no disponible")

                if float(product.actual_stock) < amount:
                    raise Exception(f"Stock insuficiente para: {product.name}")

                # Descontar stock
                product.actual_stock = float(product.actual_stock) - amount

                # Calcular subtotal
                price = float(product.sell_price)
                subtotal = price * amount
                total_amount += subtotal

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
            new_sale.total = total_amount
            db.session.commit()
            # Fin de transaccion segura

            # Notificacion por socket
            socketio.emit('inventory_updated',{
                'message': 'Nueva venta registrada',
                'sale_id': new_sale.id
            })

            return jsonify({
                'message': 'Venta registrada',
                'sale_id': new_sale.id,
                'total': total_amount
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400