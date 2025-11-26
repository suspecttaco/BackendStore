# File services/socket_events.py
import logging

from flask_socketio import SocketIO, emit

# Instacia global de socketio
socketio = SocketIO()

logger = logging.getLogger(__name__)

def register_socket_events(socketio_app):
    # Registrar eventos del websocket

    @socketio_app.on('connect')
    def handle_connect():
        logger.info("Cliente conectado a websocket")

    @socketio_app.on('disconnect')
    def handle_disconnect():
        logger.info("Cliente desconectado de websocket")

    @socketio_app.on('join_inventory')
    def handle_join_inventory(data):
        # Implementacion detallada a futuro
        logger.info("Cliente añadido a sala de actualizacion de inventario")