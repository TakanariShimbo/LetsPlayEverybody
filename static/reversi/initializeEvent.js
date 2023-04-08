
const putStoneAudio = new Howl({
  src: [path_put_stone_sound],
});

// Prepare Static instance
const scene = generateScene();

const camera = generateCamera();

const renderer = generateRenderer();

const boardMesh = generateBoard();
scene.add(boardMesh);

const gridLines = generateGridLines();
scene.add(gridLines);

const ambientLight = generateAmbientLight();
scene.add(ambientLight);

const pointLight = generatePointLight();
scene.add(pointLight);

const stoneMeshs = [];
for (let i = 0; i < 8; i++) {
  stoneMeshs[i] = [];
  for (let j = 0; j < 8; j++) {
    stoneMeshs[i][j] = null;
  }
}

// threeFunction
async function updateStoneMesh(x, y, stoneKind, is_play_sound) {
  // Remove current stoneMaterial
  if (stoneMeshs[x][y] != null) {
    scene.remove(stoneMeshs[x][y]);
  }

  // Add stoneMesh
  const stoneMesh = generateStone(x, y, stoneKind);
  if (stoneMesh != null) {
    scene.add(stoneMesh);
  }
  stoneMeshs[x][y] = stoneMesh;

  // Play audio when a black or white stone is placed
  if (
    (stoneKind === "BLACK" || stoneKind === "WHITE") &&
    is_play_sound &&
    putStoneAudio != null
  ) {
    playAudio(putStoneAudio);
  }
}

function updateStoneMeshByBoard(x, y, board, is_play_sound) {
  updateStoneMesh(x, y, board[x][y], is_play_sound);
}

// Initialize
for (let i = 0; i < 8; i++) {
  for (let j = 0; j < 8; j++) {
    updateStoneMesh(i, j, initial_board[i][j], false);
  }
}

// Define and Run animation
const animate = function () {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
};
animate();
