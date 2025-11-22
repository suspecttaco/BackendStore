# File app.py
from flask import Flask
from config import Config
from models import db
from flask_cors import CORS

# Importar modelos
from models.user import User, Permission, AuditLog, Shift, CashWithdrawal
from models.catalogs import Category, Supplier, Customer
from models.product import Product, StockAlert, Promotion
from models.sale import Sale, SaleDetail, Return, ReturnDetail
from models.finance import Purchase, PurchaseDetail, AccountReceivable, Payment

# Importar Blueprints
from routes.auth import auth_bp
from routes.products import products_bp
from routes.sales import sales_bp
from routes.catalogs import catalogs_bp

# Importar servicio de sockets
from services.socket_events import socketio, register_socket_events
from services.stock_monitor import StockMonitor

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Permitir CORS
    CORS(app)

    # Inicializar BD
    db.init_app(app)

    # Inicializar SocketIO con la app
    # cors_allowed_origins="*" para que no de lata a la hora de conectarse en C#
    socketio.init_app(app, cors_allowed_origins="*")
    register_socket_events(socketio)

    # Registro de rutas
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(sales_bp, url_prefix='/api/sales')
    app.register_blueprint(catalogs_bp, url_prefix='/api/catalogs')

    if not getattr(app, 'monitor_started', False):
        # Iniciar monitor de stock
        monitor = StockMonitor(app)
        monitor.start()
        app.monitor_started = True
        print("monitor started")

    return app

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()
        print("all tables and routes created successfully")

    print("Server running at http://localhost:5000")
    # Cambio de app.run a sockekio.run
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)