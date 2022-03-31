var menu_index = 1;

function renderIFC() {
    disableIFCRenderButton();
    switch(menu_index) {
        case 1:
            processIFCSelectRequest();
            resetIFCSelector();
            break;
        case 2:
            processSelectedIFC();
            resetIFCFileSelector();
            break;
        default:
            console.log("ERROR: wrong menu index");
    }
}

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
            var filename = response.filename;
            addWebGLSourceToHead(filename)
        },
        error: function (err) {
            displayMessage(err.responseText);
        }
    });
    return false;
}

function disableIFCRenderButton() {
    document.getElementById("render_ifc").disabled = true;
}

function enableIFCRenderButton() {
    document.getElementById("render_ifc").disabled = false;
}

function resetIFCSelector() {
    document.getElementById('ifc_file').selectedIndex = null;
}

function resetIFCFileSelector() {
    document.getElementById('getFile').value = '';
    document.getElementById("select_ifc_file").innerHTML = "Select IFC File";
}

function ButtonActivationController() {
    switch(menu_index) {
        case 1:
            if (document.getElementById('ifc_file').selectedIndex != 0) {
                enableIFCRenderButton();
            } else {
                disableIFCRenderButton();
            }
            break;
        case 2:
            if (document.getElementById('getFile').value != '') {
                enableIFCRenderButton();
            } else {
                disableIFCRenderButton();
            }
            break;
        default:
            console.log("ERROR: wrong menu index");
    }
}

function selectIFC_Menu() {
    menu_index = 1;
    document.getElementById("menu_1").style.display = "block";
    document.getElementById("menu_2").style.display = "none";
    ButtonActivationController();
}

function uploadIFC_Menu() {
    menu_index = 2;
    document.getElementById("menu_1").style.display = "none";
    document.getElementById("menu_2").style.display = "block";
    ButtonActivationController();
}

function select_IFC_File() {
    document.getElementById('getFile').click();
}

function file_selected(target) {
    document.getElementById("select_ifc_file").innerHTML = target.files[0].name;
    ButtonActivationController();
}

function displayMessage(TEXT) {
    var message = this.document.getElementById("message");
    message.innerHTML = TEXT;
    message.style.opacity = 0.7;
    message.style.display = 'block';
    setTimeout(() => {
        message.style.transition = 'opacity 5s';
        message.style['-webkit-transition'] = 'opacity 5s';
        message.style.opacity = 0.;
        setTimeout(()=> {
            message.style.transition = 'opacity 0.5s';
            message.style['-webkit-transition'] = 'opacity 0.5s';
            setTimeout(()=>{
                message.style.display = 'none';
            },4000)
        },10);
    }, 3000);
}