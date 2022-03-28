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

function selectIFC_Menu() {
    document.getElementById("menu_1").style.display = "block"
    document.getElementById("menu_2").style.display = "none"

}

function uploadIFC_Menu() {
    document.getElementById("menu_1").style.display = "none"
    document.getElementById("menu_2").style.display = "block"
}

function select_IFC_File() {
    document.getElementById('getFile').click();
}

function file_selected(target) {
    document.getElementById("select_ifc_file").innerHTML = target.files[0].name;
}