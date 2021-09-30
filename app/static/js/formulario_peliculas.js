window.addEventListener("load", (e) => {
    document.body.addEventListener("click", function (event) {
        if (event.target.classList.contains("upload-btn")) {
            event.preventDefault();
            let input = event.target.getAttribute("data-input");
            document.querySelector("#"+input).click();
        }
    });
    document.body.addEventListener("dragover", function (event) {
        if (event.target.classList.contains("upload-box")) {
            event.preventDefault();
            event.target.setAttribute("drop-active",true);
        }
    });
    document.body.addEventListener("dragleave", function (event) {
        if (event.target.classList.contains("upload-box")) {
            event.preventDefault();
            event.target.removeAttribute("drop-active");
        }
    });

    document.body.addEventListener("drop", function (ev) {
        if (ev.target.classList.contains("upload-box")) {
            ev.preventDefault();
            let input = event.target.getAttribute("data-input");
            let data = event.target.getAttribute("data-input-data");
            let preview = event.target.getAttribute("data-preview");
            if (ev.dataTransfer.items) {
                for (var i = 0; i < ev.dataTransfer.items.length; i++) {
                    // Si los elementos arrastrados no son ficheros, rechazarlos
                    if (ev.dataTransfer.items[i].kind === 'file') {
                        let file = ev.dataTransfer.items[i].getAsFile();
                        mostrarImgNew(file, preview);
                        addHiddenFile(file, input, data);

                    }
                }
            }
            else {
                for (var i = 0; i < ev.dataTransfer.files.length; i++) {
                    let file = ev.dataTransfer.files[i];
                    mostrarImgNew(file, preview);
                    addHiddenFile(file, input, data);
                }
            }

            if (ev.dataTransfer.items) {
                ev.dataTransfer.items.clear();
            } else {
                ev.dataTransfer.clearData();
            }
            event.target.removeAttribute("drop-active");
        }
    });

    document.getElementById('pel_v_ruta_poster').addEventListener("change", function (event){
        event.preventDefault();
        document.querySelector('#pel_v_ruta_poster_data').value = '';
        let file = event.target.files[0];
        console.log(file);
        mostrarImgNew(file, "preview");
        addHiddenFile(file, "pel_v_ruta_poster", "pel_v_ruta_poster_data");
    });

    document.getElementById('pel_v_ruta_banner').addEventListener("change", function (event){
        event.preventDefault();
        document.querySelector('#pel_v_ruta_banner_data').value = '';
        let file = event.target.files[0];
        console.log(file);
        mostrarImgNew(file, "preview_banner");
        addHiddenFile(file, "pel_v_ruta_banner", "pel_v_ruta_banner_data");
    });

    const mostrarImgNew = function(file, idImage, idOtherTypes = null) {
        let previewImg = document.getElementById(idImage);


        let imageType = /image.*/;
        if(file.type.match(imageType)){
            let reader = new FileReader();
            reader.onloadend = function() {
                console.log(reader);
                previewImg.src = reader.result;
            }

            if (file) {
                reader.readAsDataURL(file);
            } else {
                previewImg.src = "";
            }
            previewImg.style.display = 'block';
            if(idOtherTypes){
                let previewText = document.getElementById(idOtherTypes);
                previewText.style.display = 'none';
            }

        }
        else{

            previewImg.style.display = 'none';

            if(idOtherTypes){
                let previewText = document.getElementById(idOtherTypes);
                previewText.style.display = 'block';
                previewText.innerHTML = file.name;
            }

        }
    }
    const addHiddenFile = function(file, inputClassic, inputHidden){

        document.getElementById(inputClassic).value = '';
        let input = document.getElementById(inputHidden);
        let reader = new FileReader();
        reader.onloadend = function() {
            input.value = reader.result;
        }
        if (file) {
            reader.readAsDataURL(file);
        }
    }


});
