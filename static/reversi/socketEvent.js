
// Define socket
const socket = io();

// Prepare Event Listener
function onMouseDownEvent(event) {
  onMouseDownAndTouchStartEvent(event.clientX, event.clientY, socket);
}
window.addEventListener("mousedown", onMouseDownEvent, false);

function onTouchStartEvent(event) {
  const touch = event.touches[0] || event.changedTouches[0];
  onMouseDownAndTouchStartEvent(touch.clientX, touch.clientY, socket);
}
window.addEventListener("touchstart", onTouchStartEvent, false);

window.addEventListener("resize", onResizeEvent(camera, renderer), false);

// Emmit Connect Event and Disconnect Event
socket.on("connect", function () {
  socket.emit("reversi_join_room", {
    room_name: room_name,
    player_color: this_player_color,
  });
});

socket.on("reversi_game_start", function (data) {
  const next_player_color = data.next_player_color;
  updateMessageByPlayerColor(next_player_color);
});

socket.on("reversi_left_room", function (data) {
  const leftPlayerColor = data.player_color;
  const message = "Friend (" + leftPlayerColor + " player) has left the room.";
  updateMessage(message);
});

socket.on("disconnect", function () {
  const message = "Disconnected from server. Please refresh the page.";
  updateMessage(message);
});

// Update turn message
function gameFinishEvent(black_stone_count, white_stone_count) {
  updateMessage("COUNTING");

  // Prepare Empty state
  for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {
      updateStoneMesh(i, j, null, false);
    }
  }

  // Put Black Stones
  for (let i = 0; i < black_stone_count; i++) {
    setTimeout(function () {
      const x = Math.floor(i / 8);
      const y = i % 8;
      updateStoneMesh(x, y, "BLACK", true);
    }, 150 * (i + 1));
  }

  // Put White Stones
  for (let i = 0; i < white_stone_count; i++) {
    setTimeout(function () {
      const x = Math.floor(i / 8);
      const y = i % 8;
      updateStoneMesh(7 - x, 7 - y, "WHITE", true);
    }, 150 * (i + 1));
  }

  // Update Message
  let result_message;
  let wait_count;
  if (black_stone_count > white_stone_count) {
    wait_count = black_stone_count;
    if (this_player_color == "BLACK") {
      result_message = "YOU(BLACK) WIN";
    } else {
      result_message = "FRIEND(BLACK) WIN";
    }
  } else if (black_stone_count < white_stone_count) {
    wait_count = white_stone_count;
    if (this_player_color == "WHITE") {
      result_message = "YOU(WHITE) WIN";
    } else {
      result_message = "FRIEND(WHITE) WIN";
    }
  } else {
    result_message = "DRAW";
    wait_count = black_stone_count;
  }
  setTimeout(function () {
    updateMessage(result_message);
  }, 150 * wait_count);
}

socket.on("reversi_update_board", function (data) {
  const next_board = data.next_board;
  const current_board = data.current_board;
  const xy_put = data.xy_put;
  const xy_flips = data.xy_flips;
  const xy_candidates = data.xy_candidates;
  const next_player_color = data.next_player_color;
  const black_stone_count = data.black_stone_count;
  const white_stone_count = data.white_stone_count;
  const next_state = data.next_state;

  // Prepare Previous state
  for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {
      updateStoneMeshByBoard(i, j, current_board, false);
    }
  }

  // Put Stone
  updateStoneMeshByBoard(xy_put[0], xy_put[1], next_board, true);

  // Flip stones
  for (let i = 0; i < xy_flips.length; i++) {
    setTimeout(function () {
      updateStoneMeshByBoard(xy_flips[i][0], xy_flips[i][1], next_board, true);
    }, 150 * (i + 1));
  }

  // Put Candidate stones
  setTimeout(function () {
    for (let i = 0; i < xy_candidates.length; i++) {
      updateStoneMeshByBoard(
        xy_candidates[i][0],
        xy_candidates[i][1],
        next_board,
        true
      );
    }

    if (next_state == "FINISHED") {
      gameFinishEvent(black_stone_count, white_stone_count);
    } else {
      updateMessageByPlayerColor(next_player_color);
    }
  }, 150 * xy_flips.length);
});
