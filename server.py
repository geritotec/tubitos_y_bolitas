from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import random

from utilities.generar_tubitos import generar_tubitos
from utilities.mover_bolita import mover_bolita

app = Flask(__name__)
socketio = SocketIO(app)

game_states = {}

@socketio.on("join_game")
def join_session(data):
    room = data['room_id']
    session_id = request.sid

    join_room(room)

    if room not in game_states:
        game_states[room] = {}

    emit('game_state', game_states[room], to=session_id)


@socketio.on("create_level")
def create_level(data):
    difficulty = data["difficulty"]
    room = data["room_id"]

    tubitos = generar_tubitos(difficulty)

    game_states[room] = {"tubitos": tubitos}

    emit("game_state", game_states[room], room=room)

@socketio.on("mover_volita")
def mover_volita(data):
    room = data["room_id"]
    tubitos = game_states[room]["tubitos"]
    source_index = data["source_index"]
    destination_index = data["destination_index"]

    mover_bolita(tubitos, source_index, destination_index)

    game_states[room]["tubitos"] = tubitos

    emit("game_state", game_states[room], room=room)

@socketio.on("solved") # terminar
def solved(data):
    room = data["room_id"]

    game_states[room]["solved"] = "true"

    emit("game_state", game_states[room], room=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
