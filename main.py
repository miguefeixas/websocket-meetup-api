# backend/app.py
from flask import Flask, request
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para el cliente Angular
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return 'WebSocket Server Running!'

@socketio.on('connect')
def handle_connect():
    print('Client connected:', request.sid)
    emit('message', {'user': 'Server', 'text': 'Welcome to the chat!'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected:', request.sid)

@socketio.on('chat_message')
def handle_message(data):
    print('Received message:', data)
    emit('message', data, broadcast=True)  # broadcast para enviar a todos

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
