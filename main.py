import eventlet

eventlet.monkey_patch()

from flask_cors import CORS
from flask import Flask, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return 'WebSocket Server Running!'

@socketio.on('connect')
def handle_connect():
    print('Client connected:', request.sid)

@socketio.on('new_connection')
def handle_new_connection(data):
    if data is not None:
        welcome = f'{data} se ha unido al chat, bienvenido/a! 🤖'
    else:
        welcome = 'Alguien se ha unido al chat, bienvenido/a! 🤖'

    emit('message', {'user': 'BipBop el robot', 'text': welcome}, broadcast=True)

@socketio.on('long_chat_message')
def handle_new_connection(data):
    if data['user'] is not None:
        message = f'🚨🚨 Vaya, parece que {data["user"]} ha intentado mandar un mensaje de más de 300 caracteres... Sin duda es un texto bastante largo, no creo que haya copiado un lorem ipsum para intentar romper la página ¿verdad? 🤖'
    else:
        message = f'🚨🚨 Vaya, parece que alguien ha intentado mandar un mensaje de más de 300 caracteres... Sin duda es un texto bastante largo, no creo que haya copiado un lorem ipsum para intentar romper la página ¿verdad? 🤖'

    emit('message', {'user': 'BipBop el robot', 'text': message}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected:', request.sid)

@socketio.on('chat_message')
def handle_message(data):
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
