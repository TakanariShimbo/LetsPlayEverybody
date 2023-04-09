import os
from typing import cast

from flask import Flask, render_template, request, redirect, url_for, abort
from flask_socketio import SocketIO, emit, join_room, leave_room
from dotenv import load_dotenv

from manager.manager import ReversiRoom, ReversiUser, RoomUserManager


load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


room_user_manager = RoomUserManager()


"""
共通
"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    # Get
    if request.method == "GET":
        return render_template("create.html")

    # Post
    # Early return
    room_name = request.form["room_name"]
    if room_user_manager.is_exists_room(room_name):
        abort(400, f"{room_name} is already used.")

    game_name = request.form["game_name"]
    return redirect(url_for(game_name, room_name=room_name))


@app.route("/enter", methods=["GET", "POST"])
def enter():
    # Get
    if request.method == "GET":
        return render_template("enter.html", room_dict=room_user_manager.room_dict)

    # Post
    # Early return
    room_name = request.form["room_name"]
    if not room_user_manager.is_exists_room(room_name):
        abort(400, f"{room_name} is not exists.")

    room = room_user_manager.get_room(room_name)
    if room is None:
        abort(403, f"{room_name} is not exists.")

    if room.is_full():
        abort(400, f"{room_name} is full. Please try again later.")

    return redirect(url_for(room.game_name, room_name=room_name))


@socketio.on("disconnect")
def on_disconnect():
    session_id = request.sid  # type: ignore

    # Early return
    user = room_user_manager.get_user(session_id)
    if user is None:
        return

    # Leave room
    room_user_manager.remove_user(session_id)
    leave_room(user.room_name)

    # Early return
    room = room_user_manager.get_room(user.room_name)
    if room is None:
        return

    # Emit leave room event
    if type(room) == ReversiRoom:
        reversi_user = cast(ReversiUser, user)
        emit(
            "reversi_left_room",
            {"player_color": reversi_user.player_color.name},
            room=user.room_name,
        )

    # If empty, delete room
    if room.is_empty():
        room_user_manager.remove_room(room.room_name)


"""
リバーシ
"""


@app.route("/reversi/<room_name>")
def reversi(room_name):
    if room_user_manager.is_exists_room(room_name):
        # If exists -> get room
        room = room_user_manager.get_room(room_name)
        if room is None:
            abort(400, f"{room_name} is not exists.")
        reversi_room = cast(ReversiRoom, room)
    else:
        # If not exists -> create room
        reversi_room = room_user_manager.create_reversi_room(room_name)

    # Early return
    if reversi_room.is_full():
        abort(400, f"{room_name} is full. Please try again later.")

    # Render toom.html
    player_color = reversi_room.get_empty_player_color()
    return render_template(
        "reversi.html",
        room_name=room_name,
        this_player_color=player_color.name,
        board=reversi_room.controller.current_board_str,
        enumerate=enumerate,
    )


@socketio.on("reversi_join_room")
def on_reversi_join_room(message):
    session_id = request.sid  # type: ignore
    room_name = message["room_name"]
    player_color = message["player_color"]

    # Join room
    room_user_manager.create_reversi_user_and_assign_to_room(
        session_id, room_name, player_color
    )
    join_room(room_name)

    # Game start
    room = room_user_manager.get_room(room_name)
    if room is not None and room.is_full():
        reversi_room = cast(ReversiRoom, room)
        emit(
            "reversi_game_start",
            {"next_player_color": reversi_room.controller.current_player_color_str},
            room=room_name,
        )


@socketio.on("reversi_put_stone")
def on_reversi_put_stone(message):
    session_id = request.sid  # type: ignore

    # Early return
    user = room_user_manager.get_user(session_id)
    if user is None:
        abort(403, "Error happened. User not found.")
    room = room_user_manager.get_room(user.room_name)
    if room is None:
        abort(403, "Error happened. Room not found.")
    reversi_room = cast(ReversiRoom, room)
    reversi_user = cast(ReversiUser, user)

    if not reversi_room.is_full():
        return
    if reversi_user.player_color != reversi_room.controller.current_player_color:
        return

    # Update board
    x = int(message["x"])
    y = int(message["y"])
    if reversi_room.controller.can_put(x, y):
        reversi_room.controller.put(x, y)
        emit(
            "reversi_update_board",
            {
                "next_board": reversi_room.controller.current_board_str,
                "current_board": reversi_room.controller.previous_board_str,
                "xy_put": reversi_room.controller.previous_xy_put,
                "xy_flips": reversi_room.controller.previous_xy_flips,
                "xy_candidates": reversi_room.controller.previous_xy_candidates,
                "next_player_color": reversi_room.controller.current_player_color_str,
                "black_stone_count": reversi_room.controller.black_stone_count,
                "white_stone_count": reversi_room.controller.white_stone_count,
                "next_state": reversi_room.controller.current_state_str,
            },
            room=room.room_name,
        )


if __name__ == "__main__":
    socketio.run(app)
