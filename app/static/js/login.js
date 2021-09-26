window.addEventListener("load", (e) => {
    document.getElementById("form-login").addEventListener("submit", (e) => {
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
            console.log(response);
            if(response.errors.length > 0){
                document.getElementById("errors").classList.add('activo');
                let listErrors = document.getElementById("listErrors");
                while (listErrors.firstChild) {
                  listErrors.removeChild(listErrors.firstChild);
                }

                for(err in response.errors){
                    let liError = document.createElement("li");
                    liError.append(response.errors[err]);
                    listErrors.append(liError);
                }

            }else{
                window.open(response.data.redirect,"_self");
            }

        })
        .catch((error) => {
          console.error('Error:', error);
        });

    })
})
