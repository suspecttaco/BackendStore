# File BackendStore/app.py
from flask import Flask
from config import Config
from models import db

# Importar modelos
from models.user import User
from models.product import Product

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar BD
    db.init_app(app)

    return app

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()
        print("all tables created successfully")

    print("Server running at http://localhost:5000")
    app.run(debug=True)