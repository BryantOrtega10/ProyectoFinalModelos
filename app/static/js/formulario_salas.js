window.addEventListener("load", (e) => {
    let json_sillas = [];

    document.body.addEventListener("click", function (event) {
        if (event.target.parentNode.id == "mas_col") {
            document.querySelector("#num_cols").value = parseInt(document.querySelector("#num_cols").value) + 1;
            render_grilla();
        }
        else if (event.target.parentNode.id == "menos_col") {
            if(document.querySelector("#num_cols").value > 0){
                document.querySelector("#num_cols").value = parseInt(document.querySelector("#num_cols").value) - 1;
                render_grilla();
            }
        }
        else if (event.target.parentNode.id == "mas_fil") {
            document.querySelector("#num_filas").value = parseInt(document.querySelector("#num_filas").value) + 1;
            render_grilla();
        }
        else if (event.target.parentNode.id == "menos_fil") {
            if(document.querySelector("#num_filas").value > 0){
                document.querySelector("#num_filas").value = parseInt(document.querySelector("#num_filas").value) - 1;
                render_grilla();
            }
        }
        else if (event.target.classList.contains("celda")) {

            let celdas = document.querySelectorAll("#grilla div.celda");
            let indexCelda = 0;
            for(let i=0; i<celdas.length; i++){
                if(celdas[i] == event.target){
                    indexCelda = i;
                }
            }

            let filas = parseInt(document.querySelector("#num_filas").value);
            let columnas = parseInt(document.querySelector("#num_cols").value);
            let fila = Math.floor((indexCelda/columnas) % filas);
            let col = indexCelda % columnas;
            if(event.target.classList.contains("preferencial")){
                event.target.classList.remove("preferencial");
                event.target.classList.add("discapacitados");
                json_sillas[fila][col] = 3;
            }
            else if(event.target.classList.contains("discapacitados")){
                event.target.classList.remove("discapacitados");
                event.target.classList.add("vacia");
                json_sillas[fila][col] = 4;
            }
            else if(event.target.classList.contains("vacia")){
                event.target.classList.remove("vacia");
                json_sillas[fila][col] = 1;
            }
            else{
                event.target.classList.add("preferencial");
                json_sillas[fila][col] = 2;
            }
            console.log(json_sillas);
            document.getElementById("sal_t_sillas").value = JSON.stringify(json_sillas);
        }



    });


    document.getElementById('num_filas').addEventListener("change", function (event) {
        let num = parseInt(document.getElementById('num_filas').value);
        if(num>0){
            render_grilla();
        }
        else{
            document.getElementById('num_filas').value = "0";
            render_grilla();
        }
    });

    document.getElementById('num_cols').addEventListener("change", function (event) {
        let num = parseInt(document.getElementById('num_cols').value);
        if(num>0){
            render_grilla();
        }
        else{
            document.getElementById('num_cols').value = "0";
            render_grilla();
        }
    });





    const render_grilla = () => {
        let columnas = parseInt(document.querySelector("#num_cols").value);
        let filas = parseInt(document.querySelector("#num_filas").value);
        json_sillas = [];
        if(columnas > 0 && filas > 0){
            let grilla = document.querySelector("#grilla");
            while (grilla.firstChild) {
                grilla.removeChild(grilla.lastChild);
            }
            let tamGrilla = grilla.offsetWidth;
            let col_conId = columnas + 1;
            let tamCelda = 0;
            let separator = 10;
            if(col_conId>filas){
                tamCelda = (tamGrilla - (separator * columnas)) / col_conId;
            }
            else{
                tamCelda = (tamGrilla - (separator * (filas - 1))) / filas;
            }


            grilla.style.gridTemplateColumns = "repeat("+col_conId+","+tamCelda+"px)";
            grilla.style.gridTemplateRows = "repeat("+filas+","+tamCelda+"px)";


            for(let i = 0; i < filas; i++){
                let letraFila = document.createElement("div");
                letraFila.innerHTML = String.fromCharCode(65 + i);
                grilla.append(letraFila);
                let fila_json = [];
                for(let j = 0; j < columnas; j++){
                    let celda = document.createElement("div");
                    celda.classList.add("celda");
                    celda.innerHTML = String.fromCharCode(65 + i) + (j + 1);
                    grilla.append(celda);
                    fila_json.push(1);
                }
                json_sillas.push(fila_json);
            }



        }
        document.getElementById("sal_t_sillas").value = JSON.stringify(json_sillas);


    }


     const render_grillaInicial = () => {
        let columnas = parseInt(document.querySelector("#num_cols").value);
        let filas = parseInt(document.querySelector("#num_filas").value);
        json_sillas = JSON.parse(document.getElementById("sal_t_sillas").value);
        if(columnas > 0 && filas > 0){
            let grilla = document.querySelector("#grilla");
            while (grilla.firstChild) {
                grilla.removeChild(grilla.lastChild);
            }
            let tamGrilla = grilla.offsetWidth;
            let col_conId = columnas + 1;
            let tamCelda = 0;
            let separator = 10;
            if(col_conId>filas){
                tamCelda = (tamGrilla - (separator * columnas)) / col_conId;
            }
            else{
                tamCelda = (tamGrilla - (separator * (filas - 1))) / filas;
            }


            grilla.style.gridTemplateColumns = "repeat("+col_conId+","+tamCelda+"px)";
            grilla.style.gridTemplateRows = "repeat("+filas+","+tamCelda+"px)";


            for(let i = 0; i < filas; i++){
                let letraFila = document.createElement("div");
                letraFila.innerHTML = String.fromCharCode(65 + i);
                grilla.append(letraFila);



                for(let j = 0; j < columnas; j++){
                    let celda = document.createElement("div");
                    celda.classList.add("celda");
                    if(json_sillas[i][j] == 2){
                        celda.classList.add("preferencial");
                    }
                    else if(json_sillas[i][j] == 3){
                        celda.classList.add("discapacitados");
                    }
                    else if(json_sillas[i][j] == 4){
                        celda.classList.add("vacia");
                    }


                    celda.innerHTML = String.fromCharCode(65 + i) + (j + 1);

                    grilla.append(celda);

                }

            }



        }
        document.getElementById("sal_t_sillas").value = JSON.stringify(json_sillas);
    }


    if(document.getElementById("sal_t_sillas").value != ""){
        render_grillaInicial();
    }



});
