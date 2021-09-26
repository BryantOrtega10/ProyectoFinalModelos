window.addEventListener("load", (e) => {
    document.querySelector(".formulario-general").addEventListener("submit", (e) => {
        e.preventDefault();
        let formData = new FormData(e.srcElement);
        let data = JSON.stringify(Object.fromEntries(formData));
        fetch(e.srcElement.action,
            {
                method: 'POST',
                cache: 'no-cache',
                headers: {
                'Content-Type': 'application/json',
                },
                body: data
           }
        )
        .then(response => response.json())
        .then(response => {
            let listErrors = document.getElementById("listErrors");
            let popup = new bootstrap.Modal(document.getElementById('popup'));

            let titulo_popup = document.getElementById('titulo_popup');
            let cerrar_pop = document.getElementById('cerrar_pop');
            let redirect_pop = document.getElementById('redirect_pop');

            popup.show();
            if(response.errors.length > 0){

                redirect_pop.style.display = 'none';
                cerrar_pop.style.display = 'inline-block';
                titulo_popup.innerHTML = 'Error(es)';
                listErrors.style.display = 'block';

                while (listErrors.firstChild) {
                  listErrors.removeChild(listErrors.firstChild);
                }

                for(err in response.errors){
                    let liError = document.createElement("li");
                    liError.append(response.errors[err]);
                    listErrors.append(liError);
                }

            }else{
                redirect_pop.style.display = 'inline-block';
                cerrar_pop.style.display = 'none';
                listErrors.style.display = 'none';
                titulo_popup.innerHTML = response.message;
                redirect_pop.href = response.data.redirect;

            }

        })
        .catch((error) => {
          console.error('Error:', error);
        });

    })
})
