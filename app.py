# File app.py
import eventlet
from sqlalchemy import nullsfirst

eventlet.monkey_patch()

import os
import logging
from logging.config import dictConfig

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
from routes.dashboard import dashboard_bp

# Importar servicio de sockets
from services.socket_events import socketio, register_socket_events
from services.stock_monitor import StockMonitor

logger = logging.getLogger(__name__)

def configure_logging():
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S' # Formato de fecha limpio
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    })

def create_app():

    configure_logging()

    _app = Flask(__name__)
    _app.config.from_object(Config)

    # Permitir CORS
    CORS(_app)

    # Inicializar BD
    try:
        db.init_app(_app)
        logger.info("Conectado a BD")
    except Exception as e:
        logger.critical(f"Error al conectar a BD: {str(e)}")

    # Inicializar SocketIO con la app
    # cors_allowed_origins="*" para que no de lata a la hora de conectarse en C#
    socketio.init_app(_app, cors_allowed_origins="*")
    register_socket_events(socketio)

    # Registro de rutas
    _app.register_blueprint(auth_bp, url_prefix='/api/auth')
    _app.register_blueprint(products_bp, url_prefix='/api/products')
    _app.register_blueprint(sales_bp, url_prefix='/api/sales')
    _app.register_blueprint(catalogs_bp, url_prefix='/api/catalogs')
    _app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not _app.config['DEBUG']:
        if not getattr(_app, 'monitor_started', False):
            monitor = StockMonitor(_app)
            socketio.start_background_task(monitor.run)
            _app.monitor_started = True
            logger.info("Monitor de stock corriendo en segundo plano")

    return _app

app = create_app()

if __name__ == "__main__":

    with app.app_context():
        db.create_all()
        logger.info("Tablas de BD actualizadas")

    # Para desarrollo local
    if os.getenv('FLASK_ENV') == 'development':
        logger.info("Server running at http://localhost:5000")
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    else:
        # Para producción
        print("Production mode - use gunicorn")