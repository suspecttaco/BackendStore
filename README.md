# Servidor (Backend) - Tiendita POS Ultimate

El núcleo del sistema encargado de la lógica de negocio, gestión de datos y comunicación en tiempo real. Expone una API RESTful para operaciones transaccionales y un servidor WebSocket para eventos en vivo.

## Tecnologías Utilizadas

### Core
* **Python 3.11+**: Lenguaje principal.
* **Flask**: Microframework web para la API REST.
* **Flask-RESTful**: Extensión para estructurar recursos REST.

### Base de Datos & ORM
* **MySQL 8.0**: Motor de base de datos relacional (compatible con Aiven Cloud).
* **SQLAlchemy**: ORM para mapeo de objetos y consultas seguras.
* **PyMySQL + Cryptography**: Drivers de conexión segura (SSL).

### Tiempo Real & Concurrencia
* **Flask-SocketIO**: Manejo de conexiones WebSocket bidireccionales.
* **Eventlet**: Servidor asíncrono para soportar miles de conexiones concurrentes.
* **Threading & Locks**: Manejo de hilos para el monitor de stock y bloqueos para integridad en ventas.

### Utilidades
* **Python-Dotenv**: Gestión de variables de entorno.
* **Logging**: Sistema de logs estructurado para auditoría y depuración.

---

## ⚙️ Instalación y Ejecución

### 1. Requisitos Previos
* Tener instalado Python 3.11 o superior.
* Tener acceso a una instancia de MySQL (Local o Cloud).

### 2. Configuración del Entorno
Se recomienda usar un entorno virtual para aislar las dependencias.

```bash
# Crear entorno virtual
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Activar (Linux/Mac)
source .venv/bin/activate