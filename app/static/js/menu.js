document.querySelector(".close-menu-horizontal").addEventListener("click", (e) => {
    e.preventDefault();
    let menu_icono = document.querySelector(".menu-icono");
    let cont_menu_hor = document.querySelector(".contenedor-menu-horizontal");


    if (cont_menu_hor.classList.contains('activo')) {
        cont_menu_hor.classList.remove('activo');
        menu_icono.classList.remove("fa-arrow-left");
        menu_icono.classList.add("fa-bars");
    }
    else{
        cont_menu_hor.classList.add('activo');
        menu_icono.classList.add("fa-arrow-left");
        menu_icono.classList.remove("fa-bars");
    }
});
