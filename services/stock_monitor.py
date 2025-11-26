# File services/stock_monitor.py
import time
import threading
from models import db
from models.product import Product, StockAlert
from services.socket_events import socketio

class StockMonitor(threading.Thread):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.daemon = True
        self.running = True

    def run(self):
        print("Stock monitoring started (checking every 30s)")

        # Agregar contexto de app
        with self.app.app_context():
            while self.running:
                try:
                    self.check_stock()
                except Exception as e:
                    print(f"[ERROR] stock monitor fail: {e}")

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

        for alert in resolved_alerts:
            alert.resolved = True

        if send_alerts or resolved_alerts:
            db.session.commit()
            # Emitir alerta via socket
            if send_alerts:
                print(f"[ALERT] Low stock for {len(send_alerts)} products")
                socketio.emit('low_stock_alert', {
                    'products': send_alerts
                })

            # Opcional: Log para ver en consola que se resolvió
            if resolved_alerts:
                print(f"[INFO] Resolved {len(resolved_alerts)} alerts")