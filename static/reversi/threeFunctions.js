

// Define Scene
function generateScene(){
    return new THREE.Scene();
}

// Define Camera
function generateCamera(){
    const initialAspectRatio = initialInnerWidth / initialInnerHeight;
    const initialFov = getFovByAspect(initialAspectRatio);
    
    const camera = new THREE.PerspectiveCamera(initialFov, initialAspectRatio, 0.1, 1000);
    camera.position.set(0, 36, -12);
    camera.lookAt(scene.position);
    return camera;
}

// Define Render
function generateRenderer(){
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(initialInnerWidth, initialInnerHeight);
    document.body.appendChild(renderer.domElement);
    return renderer;
}

// Define onResizeEvent
function onResizeEvent(camera, renderer) {
    return function(){
        const newInnerWidth = window.innerWidth;
        const newInnerHeight = window.innerHeight;
        const newAspectRatio = newInnerWidth / newInnerHeight;
        const newFov = getFovByAspect(newAspectRatio);
    
        camera.aspect = newAspectRatio;
        camera.fov = newFov;
        camera.updateProjectionMatrix();
    
        renderer.setSize(newInnerWidth, newInnerHeight);
    }
}

// Define Board
function generateBoard(){
    const boardGeometry = new THREE.BoxGeometry(35, 2, 35);
    const boardMaterial = new THREE.MeshPhongMaterial({color: 0x005000, shininess: 10});
    const boardMesh = new THREE.Mesh(boardGeometry, boardMaterial);
    return boardMesh;
}

// Define GridLines
function generateGridLines(){
    const lineMaterial = new THREE.LineBasicMaterial({color: 0x000000});
    const lineGeometry = new THREE.BufferGeometry();
    
    const vertices = [];
    const size = 33;
    const divisions = 8;
    const step = size / divisions;
    
    for (let i = 0; i <= divisions; i++) {
        vertices.push(-size / 2, 1.1, i * step - size / 2);
        vertices.push(size / 2, 1.1, i * step - size / 2);
    
        vertices.push(i * step - size / 2, 1.1, -size / 2);
        vertices.push(i * step - size / 2, 1.1, size / 2);
    }
    
    lineGeometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    const gridLines = new THREE.LineSegments(lineGeometry, lineMaterial);
    return gridLines;
}

// Add AmbientLight
function generateAmbientLight(){
    return new THREE.AmbientLight(0xffffff, 0.5);
}

// Add PointLight
function generatePointLight(){
    const pointLight = new THREE.PointLight(0xffffff, 0.6);
    pointLight.position.set(5, 100, -20);
    return pointLight;
}

// Add Stone
function generateStone(x, y, stoneKind) {    
    // Define stoneMaterial
    let stoneMaterial;
    if (stoneKind == "BLACK") {
        const blackMaterial = new THREE.MeshPhongMaterial({color: 0x111111});
        stoneMaterial = blackMaterial;
    } else if (stoneKind == "WHITE") {
        const whiteMaterial = new THREE.MeshPhongMaterial({color: 0xeeeeee});
        stoneMaterial = whiteMaterial;
    } else if (stoneKind == "CANDIDATE") {
        const candidateMaterial = new THREE.MeshPhongMaterial({color: 0x009000, opacity: 0.2, transparent: true});
        stoneMaterial = candidateMaterial;
    } else {
        return;
    }

    // Generate stoneMesh
    const stoneGeometry = new THREE.SphereGeometry(0.8, 32, 32);
    stoneGeometry.scale(2, 1, 2);
    const stoneMesh = new THREE.Mesh(stoneGeometry, stoneMaterial);
    stoneMesh.position.set(x * 4 - 14, 2, y * 4 - 14);
    return stoneMesh
}

// Add Click and Touch Event
function playAudio(audio){
    audio.stop();
    audio.play();
}

function onMouseDownAndTouchStartEvent(clientX, clientY, socket) {
    const mouse = new THREE.Vector2();
    mouse.x = (clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(clientY / window.innerHeight) * 2 + 1;
    
    const raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(mouse, camera);
    
    const intersects = raycaster.intersectObjects(scene.children);
    if (intersects.length == 0) {
        return;
    }

    const intersect = intersects[0];
    const x = Math.round((intersect.point.x + 14) / 4);
    const y = Math.round((intersect.point.z + 14) / 4);

    if (x >= 0 && x < 8 && y >= 0 && y < 8) {
        socket.emit('reversi_put_stone', {x: x, y: y});
    }
}