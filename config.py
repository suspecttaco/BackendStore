# File: BackendStore/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Obtener variables
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    ssl_ca = os.getenv('DB_SSL_CA')

    # Construir la ruta absoluta al certificado para evitar errores de "archivo no encontrado"
    # Esto busca el archivo ca.pem en la misma carpeta donde corre la app
    ssl_args = ""
    if ssl_ca:
        ca_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ssl_ca)
        ssl_args = f"?ssl_ca={ca_path}&ssl_check_hostname=false"

    # URI Final: Incluye puerto y argumentos SSL
    SQL_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}{ssl_args}"

    SQLALCHEMY_DATABASE_URI = SQL_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')