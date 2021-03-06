// @VertexShaderDefinition@ 
// @FragmentShaderDefinition@  


var camera, scene, renderer, object, stats, container, shape_material;
var mouseX = 0;
var mouseXOnMouseDown = 0;
var mouseY = 0;
var mouseYOnMouseDown = 0;
var moveForward = false;
var moveBackward = false;
var moveLeft = false;
var moveRight = false;
var moveUp = false;
var moveDown = false;
var windowHalfX = window.innerWidth / 2;
var windowHalfY = window.innerHeight / 2;
var selected_target_color_r = 0;
var selected_target_color_g = 0;
var selected_target_color_b = 0;
var selected_target = null;
var min_screen_width_for_stats = 500;
var animate_stat = false
init();
animate();
function init() {

    var  removeDiv = document.getElementById("WebGL_Div");
    if (removeDiv) {
        document.body.removeChild(removeDiv);
    }

    container = document.createElement('div');
    container.setAttribute('id',"WebGL_Div");
    document.body.appendChild(container);
    camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 200);
    camera.position.z = 100;
    //controls = new THREE.OrbitControls(camera);
    //controls = new THREE.OrbitControls(camera);
    // for selection
    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();
    // create scene
    scene = new THREE.Scene();
    scene.add(new THREE.AmbientLight(0x101010));
    directionalLight = new THREE.DirectionalLight(0xffffff);
    directionalLight.position.x = 1;
    directionalLight.position.y = -1;
    directionalLight.position.z = 2;
    directionalLight.position.normalize();
    scene.add(directionalLight);
    light1 = new THREE.PointLight(0xffffff);
    scene.add(light1);
    //@Uniforms@
    //@ShaderMaterialDefinition@
    {{shape_content|safe}}

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);
    //renderer.gammaInput = true;
    //renderer.gammaOutput = true;
    // for shadow rendering
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFShadowMap;
    controls = new THREE.TrackballControls(camera, renderer.domElement);
    // show stats, is it really useful ?
    animateStats()
    if (animate_stat) {
        stats = new Stats();
        stats.domElement.style.position = 'absolute';
        stats.domElement.style.top = '2%';
        stats.domElement.style.left = '1%';
        container.appendChild(stats.domElement);
    }
    // add events
    document.addEventListener('keypress', onDocumentKeyPress, false);
    document.addEventListener('click', onDocumentMouseClick, false);
    window.addEventListener('resize', onWindowResize, false);
    disableRenderingAnimation();
}
function animateStats() {
    if (screen.width > min_screen_width_for_stats) {
        animate_stat = true
    }
}
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    render();
    if (animate_stat) {
        stats.update();
    }
}
function update_lights() {
    if (directionalLight != undefined) {
        directionalLight.position.copy(camera.position);
    }
}
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}
function onDocumentKeyPress(event) {
    event.preventDefault();
    if (event.key == "t") {  // t key
        if (selected_target) {
            selected_target.material.visible = !selected_target.material.visible;
        }
    }
    else if (event.key == "g") { // g key, toggle grid visibility
        gridHelper.visible = !gridHelper.visible;
    }
    else if (event.key == "a") { // g key, toggle axisHelper visibility
        axisHelper.visible = !axisHelper.visible;
    }
    else if (event.key == "w") { // g key, toggle axisHelper visibility
        if (selected_target) {
            selected_target.material.wireframe = !selected_target.material.wireframe;
        }
    }
}
function onDocumentMouseClick(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;
    // restore previous selected target color
    if (selected_target) {
        selected_target.material.color.setRGB(selected_target_color_r,
            selected_target_color_g,
            selected_target_color_b);
    }
    // perform selection
    raycaster.setFromCamera(mouse, camera);
    var intersects = raycaster.intersectObjects(scene.children);
    if (intersects.length > 0) {
        var target = intersects[0].object;
        selected_target_color_r = target.material.color.r;
        selected_target_color_g = target.material.color.g;
        selected_target_color_b = target.material.color.b;
        target.material.color.setRGB(1., 0.65, 0.);
        console.log(target);
        selected_target = target;
    }
}  
function fit_to_scene() {
    // compute bounding sphere of whole scene
    var center = new THREE.Vector3(0, 0, 0);
    var radiuses = new Array();
    var positions = new Array();
    // compute center of all objects
    scene.traverse(function (child) {
        if (child instanceof THREE.Mesh) {
            child.geometry.computeBoundingBox();
            var box = child.geometry.boundingBox;
            var curCenter = new THREE.Vector3().copy(box.min).add(box.max).multiplyScalar(0.5);
            var radius = new THREE.Vector3().copy(box.max).distanceTo(box.min) / 2.;
            center.add(curCenter);
            positions.push(curCenter);
            radiuses.push(radius);
        }
    });
    if (radiuses.length > 0) {
        center.divideScalar(radiuses.length * 0.7);
    }
    var maxRad = 1.;
    // compute bounding radius
    for (var ichild = 0; ichild < radiuses.length; ++ichild) {
        var distToCenter = positions[ichild].distanceTo(center);
        var totalDist = distToCenter + radiuses[ichild];
        if (totalDist > maxRad) {
            maxRad = totalDist;
        }
    }
    maxRad = maxRad * 0.7; // otherwise the scene seems to be too far away
    camera.lookAt(center);
    var direction = new THREE.Vector3().copy(camera.position).sub(controls.target);
    var len = direction.length();
    direction.normalize();

    // compute new distance of camera to middle of scene to fit the object to screen
    var lnew = maxRad / Math.sin(camera.fov / 180. * Math.PI / 2.);
    direction.multiplyScalar(lnew);

    var pnew = new THREE.Vector3().copy(center).add(direction);
    // change near far values to avoid culling of objects 
    camera.position.set(pnew.x, pnew.y, pnew.z);
    camera.far = lnew * 50;
    camera.near = lnew * 50 * 0.001;
    camera.updateProjectionMatrix();
    controls.target = center;
    controls.update();
    // adds and adjust a grid helper if needed
    gridHelper = new THREE.GridHelper(maxRad * 4, 10)
    gridHelper.geometry.rotateX( Math.PI / 2 )
    scene.add(gridHelper);
    // axisHelper
    axisHelper = new THREE.AxesHelper(maxRad);
    scene.add(axisHelper);
}
function render() {
    //@IncrementTime@  TODO UNCOMMENT
    update_lights();
    renderer.render(scene, camera);
}
