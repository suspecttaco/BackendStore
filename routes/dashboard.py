# File routes/dashboard.py
import logging

from flask import Blueprint, jsonify
from sqlalchemy import func, cast, Date, extract
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

        # Agrupar ventas por hora del día actual
        hourly_results = db.session.query(
            extract('hour', Sale.date).label('hour'),
            func.sum(Sale.total).label('total')
        ).filter(
            cast(Sale.date, Date) == today
        ).group_by('hour').order_by('hour').all()


        # Diccionario con las 24 horas inicializadas a 0
        hours_map = {h: 0 for h in range(1, 23)}

        for h, total in hourly_results:
            if int(h) in hours_map:
                hours_map[int(h)] = float(total)

        # Convertir a listas para Chart.js
        trend_labels = [f"{h}:00" for h in hours_map.keys()]
        trend_values = list(hours_map.values())
        # -----------------------------------------------------------

        logger.info("Estadisticas consultadas - 200")

        return jsonify({
            'total_sales': float(total_sales_today),
            'sales_count': sales_count_today,
            'low_stock_count': low_stock_count,
            'total_products': total_products,
            'date': today.isoformat(),
            # Enviamos los arrays para la gráfica
            'trend_labels': trend_labels,
            'trend_values': trend_values
        }), 200
    except Exception as e:
        logger.error(f"Error al consultar estadisticas - 500 - {str(e)}")
        return jsonify({'error': str(e)}), 500