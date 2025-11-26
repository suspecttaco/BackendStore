# File services/stock_monitor.py
import time
import threading
import logging
from models import db
from models.product import Product, StockAlert
from services.socket_events import socketio

class StockMonitor(threading.Thread):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.daemon = True
        self.running = True
        self.logger = logging.getLogger('StockMonitor')

    def run(self):
        self.logger.info("Monitor de stock incializado (revisando cada 30s)")

        # Agregar contexto de app
        with self.app.app_context():
            while self.running:
                try:
                    self.check_stock()
                except Exception as e:
                    self.logger.error(f"Fallo en el monitor de stock: {e}")

                db.session.remove()
                time.sleep(30)

    def check_stock(self):
        # Busca productos donde el stock actual es menor al minimo
        low_stock_products = Product.query.filter(
            Product.actual_stock <= Product.minimum_stock,
            Product.active == True
        ).all()

        send_alerts = []
        for prod in low_stock_products:
            # Verificar si ya existe la alerta no resuelta para evitar spam
            existing_alert = StockAlert.query.filter_by(
                product_id=prod.id,
                resolved=False
            ).first()

            if not existing_alert:
                new_alert = StockAlert(
                    product_id=prod.id,
                    actual_stock=prod.actual_stock
                )

                db.session.add(new_alert)

                send_alerts.append({
                    'product_id': prod.id,
                    'product_name': prod.name,
                    'current_stock': float(prod.actual_stock),
                    'min_stock': float(prod.minimum_stock)
                })

        # Cerrar alertas en caso de reposicion de stock
        resolved_alerts = db.session.query(StockAlert).join(Product).filter(
            StockAlert.resolved == False,
            Product.actual_stock > Product.minimum_stock
        ).all()

        resolved_names = []  # Lista para guardar nombres

        for alert in resolved_alerts:
            alert.resolved = True
            # Guardamos el nombre para notificar
            if alert.product:
                resolved_names.append(alert.product.name)

        if send_alerts or resolved_alerts:
            db.session.commit()
            # Emitir alerta via socket
            if send_alerts:
                self.logger.warning(f"Stock bajo para {len(send_alerts)} productos")
                socketio.emit('low_stock_alert', {
                    'products': send_alerts
                })

            # Opcional: Log para ver en consola que se resolvió
            if resolved_alerts:
                self.logger.info(f"{len(resolved_alerts)} alertas resueltas")
                socketio.emit('stock_alert_resolved', {'products': resolved_names})