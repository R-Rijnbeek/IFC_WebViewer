function addWebGLSourceToHead(){
    disableButton();

    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');

    var select = document.getElementById('ifc_file');
    var value = select.options[select.selectedIndex].value;

    script.setAttribute('src', js_url+"?ifc="+value);
    head.appendChild(script);
}

function disableButton() {
    var button = document.getElementById("render_ifc");
    button.disabled = true;
}

function enableButton() {
    var button = document.getElementById("render_ifc");
    button.disabled = false;
}