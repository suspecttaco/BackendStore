# File routes/dashboard.py
import logging

from flask import Blueprint, jsonify
from sqlalchemy import func, cast, Date
from datetime import datetime, date
from models import db
from models.sale import Sale
from models.product import Product, StockAlert

dashboard_bp = Blueprint('dashboard', __name__)

logger = logging.getLogger(__name__)

@dashboard_bp.route('/stats', methods=['GET'])
def get_dashboard_stats():
    try:
        today = date.today()

        # Total vendido hoy
        total_sales_today = db.session.query(func.sum(Sale.total))\
            .filter(cast(Sale.date, Date) == today).scalar() or 0

        # Total ventas hoy
        sales_count_today = db.session.query(func.count(Sale.total))\
        .filter(cast(Sale.date, Date) == today).scalar() or 0

        # Conteo de productos con stock bajo
        low_stock_count = Product.query.filter(
            Product.actual_stock < Product.minimum_stock,
            Product.active == True
        ).count()

        # Total de productos activos
        total_products = Product.query.filter_by(active=True).count()

        logger.info("Estadisticas consultadas - 200")
        return jsonify({
            'total_sales': float(total_sales_today),
            'sales_count': sales_count_today,
            'low_stock_count': low_stock_count,
            'total_products': total_products,
            'date': today.isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error al consultar estadisticas - 500 - {str(e)}")
        return jsonify({'error': str(e)}), 500