# File services/socket_events.py
from flask_socketio import SocketIO, emit

# Instacia global de socketio
socketio = SocketIO()

def register_socket_events(socketio_app):
    # Registrar eventos del websocket

    @socketio_app.on('connect')
    def handle_connect():
        print('Client connected to websocket')

    @socketio_app.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio_app.on('join_inventory')
    def handle_join_inventory(data):
        # Cliente se une a sala de actualizaciones de inventario
        print('Client joined to inventory room')