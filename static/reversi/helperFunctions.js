// Update Message
function updateMessage(message) {
  const messageElement = document.getElementById("message");
  messageElement.textContent = message;
}

function updateMessageByPlayerColor(next_player_color) {
  let message;
  if (next_player_color == this_player_color) {
    message = "YOUR(" + next_player_color + ") TURN";
  } else {
    message = "FRIEND(" + next_player_color + ") TURN";
  }

  updateMessage(message);
}

// Get Fov
function getFovByAspect(aspect) {
  const minAspect = 0.1; // 最小横幅
  const maxAspect = 1; // 最大横幅
  const minFov = 125; // 最大視野角
  const maxFov = 75; // 最小視野角

  const fov =
    ((aspect - minAspect) / (maxAspect - minAspect)) * (maxFov - minFov) +
    minFov;
  return Math.max(maxFov, Math.min(minFov, fov));
}
