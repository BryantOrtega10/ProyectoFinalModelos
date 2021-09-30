window.addEventListener("load", (e) => {
    document.body.addEventListener("click", function (event) {
        if (event.target.classList.contains("upload-btn")) {
            event.preventDefault();
            let input = event.target.getAttribute("data-input");
            document.querySelector("#"+input).click();
        }
        else if (event.target.parentNode.id == "mas_gen") {
            document.querySelector("#num_generos").value = parseInt(document.querySelector("#num_generos").value) + 1;
            const i = document.querySelector("#num_generos").value;

            fetch('/pelicula/select_generos/'+i,
            {
                    method: 'GET',
                    cache: 'no-cache',
                    headers: {
                    'Content-Type': 'application/json',
                    }
               }
            )
            .then(response => response.json())
            .then(response => {
                console.log(response)
                const element = response.data.elemento;
                document.querySelector("#cont_generos").insertAdjacentHTML('beforeend', element);
            })
            .catch((error) => {
              console.error('Error:', error);
            });
        }
        else if(event.target.parentNode.id == "menos_gen"){
            document.querySelector("#num_generos").value = parseInt(document.querySelector("#num_generos").value) - 1;
            if(document.querySelector("#num_generos").value <= 0){
                document.querySelector("#num_generos").value = 1;
            }
            else{
                let generos = document.querySelector("#cont_generos")
                generos.removeChild(generos.lastChild);
            }
        }
        else if (event.target.parentNode.id == "mas_act") {
            document.querySelector("#num_actores").value = parseInt(document.querySelector("#num_actores").value) + 1;
            const i = document.querySelector("#num_actores").value;

            fetch('/pelicula/select_actores/'+i,
            {
                    method: 'GET',
                    cache: 'no-cache',
                    headers: {
                    'Content-Type': 'application/json',
                    }
               }
            )
            .then(response => response.json())
            .then(response => {
                console.log(response)
                const element = response.data.elemento;
                document.querySelector("#cont_actores").insertAdjacentHTML('beforeend', element);
            })
            .catch((error) => {
              console.error('Error:', error);
            });
        }
        else if(event.target.parentNode.id == "menos_act"){
            document.querySelector("#num_actores").value = parseInt(document.querySelector("#num_actores").value) - 1;
            if(document.querySelector("#num_actores").value <= 0){
                document.querySelector("#num_actores").value = 1;
            }
            else{
                let actores = document.querySelector("#cont_actores")
                actores.removeChild(actores.lastChild);
            }
        }
    });

    document.getElementById('num_generos').addEventListener("change", function (event) {
        let num = parseInt(document.getElementById('num_generos').value);
        let cant_actual = document.getElementsByClassName('generos').length;
        let generos = document.querySelector("#cont_generos")
        if(num > 0){
            if(cant_actual > num){
                for (let i = cant_actual; i > num; i--) {
                    generos.removeChild(generos.lastChild);
                }
            }
            else{
                for (let i = cant_actual + 1; i <= num; i++) {
                    fetch('/pelicula/select_generos/'+i,
                    {
                            method: 'GET',
                            cache: 'no-cache',
                            headers: {
                            'Content-Type': 'application/json',
                            }
                       }
                    )
                    .then(response => response.json())
                    .then(response => {
                        console.log(response)
                        const element = response.data.elemento;
                        document.querySelector("#cont_generos").insertAdjacentHTML('beforeend', element);
                    })
                    .catch((error) => {
                      console.error('Error:', error);
                    });
                }
            }
        }
        else {
            for (let i = 0; i < cant_actual ; i++) {
                document.getElementsByClassName('generos')[0].remove();
            }
            document.getElementById('num_generos').value = 1;
            fetch('/pelicula/select_generos/' + 1,
            {
                    method: 'GET',
                    cache: 'no-cache',
                    headers: {
                    'Content-Type': 'application/json',
                    }
               }
            )
            .then(response => response.json())
            .then(response => {
                console.log(response)
                const element = response.data.elemento;
                document.querySelector("#cont_generos").insertAdjacentHTML('beforeend', element);
            })
            .catch((error) => {
              console.error('Error:', error);
            });
        }
    });

    document.getElementById('num_actores').addEventListener("change", function (event) {
        let num = parseInt(document.getElementById('num_actores').value);
        let cant_actual = document.getElementsByClassName('actores').length;
        let actores = document.querySelector("#cont_actores")
        if(num > 0){
            if(cant_actual > num){
                for (let i = cant_actual; i > num; i--) {
                    actores.removeChild(actores.lastChild);
                }
            }
            else{
                for (let i = cant_actual + 1; i <= num; i++) {
                    fetch('/pelicula/select_actores/'+i,
                    {
                            method: 'GET',
                            cache: 'no-cache',
                            headers: {
                            'Content-Type': 'application/json',
                            }
                       }
                    )
                    .then(response => response.json())
                    .then(response => {
                        console.log(response)
                        const element = response.data.elemento;
                        document.querySelector("#cont_actores").insertAdjacentHTML('beforeend', element);
                    })
                    .catch((error) => {
                      console.error('Error:', error);
                    });
                }
            }
        }
        else {
            for (let i = 0; i < cant_actual ; i++) {
                document.getElementsByClassName('actores')[0].remove();
            }
            document.getElementById('num_actores').value = 1;
            fetch('/pelicula/select_actores/' + 1,
            {
                    method: 'GET',
                    cache: 'no-cache',
                    headers: {
                    'Content-Type': 'application/json',
                    }
               }
            )
            .then(response => response.json())
            .then(response => {
                console.log(response)
                const element = response.data.elemento;
                document.querySelector("#cont_actores").insertAdjacentHTML('beforeend', element);
            })
            .catch((error) => {
              console.error('Error:', error);
            });
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
