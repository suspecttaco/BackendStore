# File: config.py
import os
import ssl
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Obtener variables
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    # URI Final: Incluye puerto. Los argumentos SSL se manejan via SQLALCHEMY_ENGINE_OPTIONS
    SQL_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

    SQLALCHEMY_DATABASE_URI = SQL_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Puerto para el servidor (Render usa variable PORT)
    PORT = int(os.getenv('PORT', 5000))