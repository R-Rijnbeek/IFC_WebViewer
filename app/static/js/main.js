function addWebGLSourceToHead(value){
    var head = document.getElementsByTagName('head')[0];
    
    var script = document.getElementById("WebGLScript");
    if (script) {
        script.remove(); 
    } 
    script = document.createElement('script');
    script.setAttribute('id', "WebGLScript");
    script.setAttribute('src', js_url+"?ifc="+value);

    head.appendChild(script);
}

function processIFCSelectRequest(){
    disableButton("render_ifc_1");

    var select = document.getElementById('ifc_file');
    var filename = select.options[select.selectedIndex].value;

    addWebGLSourceToHead(filename);
}

function processSelectedIFC() {
    let files = new FormData();
    files.append('fileName', $('#getFile')[0].files[0]);
    $.ajax({
        type: 'post',
        url: "fileUpload" ,
        processData: false,
        contentType: false,
        data: files,
        success: function (response) {
            var  filename = response.filename;
            addWebGLSourceToHead(filename)
        },
        error: function (err) {
            alert(err.responseText);
        }
    });
    return false;
}

function disableButton(ID) {
    var button = document.getElementById(ID);
    button.disabled = true;
}

function enableButton(ID) {
    var button = document.getElementById(ID);
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
