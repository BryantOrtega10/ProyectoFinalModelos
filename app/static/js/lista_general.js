window.addEventListener("load", (e) => {
    document.body.addEventListener("click", function (event) {
        if (event.target.parentNode.classList.contains("eliminar")) {
            event.preventDefault();
            let confirm = new bootstrap.Modal(document.getElementById('popup_confirm'));
            let msj = event.target.parentNode.getAttribute("data-msj");
            let url_red = event.target.parentNode.getAttribute("href");
            document.getElementById('titulo_confirm').innerHTML = "En verdad desea eliminar " + msj + "?";
            document.getElementById('confirm_btn').href = url_red;
            confirm.show();
        }
    });
});
