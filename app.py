# File app.py
from flask import Flask
from config import Config
from models import db

# Importar modelos
from models.user import User
from models.product import Product
from models.sale import Sale
from models.sale_detail import SaleDetail
from models.stock_alert import StockAlert

# Importar Blueprints
from routes.auth import auth_bp
from routes.products import products_bp
from routes.sales import sales_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar BD
    db.init_app(app)

    # Registro de rutas
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(sales_bp, url_prefix='/api/sales')

    return app

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()
        print("all tables and routes created successfully")

    print("Server running at http://localhost:5000")
    app.run(debug=True)