from datetime import datetime
from http import HTTPStatus
from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required
from app.actor.models import obtener_actores
from app.pelicula.models import obtener_generos, crear_pelicula, crear_genero, crear_pelicula_genero, \
    crear_pelicula_actor, obtener_peliculas, obtener_pelicula_por_id, modificar_pelicula, eliminar_pelicula_genero, \
    eliminar_pelicula_actor, obtener_actores_por_pelicula, obtener_generos_por_pelicula, cuenta_funciones_por_pelicula, \
    eliminar_pelicula, obtener_peliculas_en_cartelera_por_ciudad, obtener_peliculas_mas_vistas_por_ciudad, \
    obtener_peliculas_por_estado
import copy
import base64
import uuid

pelicula = Blueprint("pelicula", __name__, url_prefix="/pelicula")

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": [], "metadata": []}
BASE_PATH = "app/static/peliculas/"

@pelicula.route("/", methods=["GET"])
@login_required
def index():
    peliculas = obtener_peliculas()
    data = {
        "peliculas":peliculas
    }
    return render_template('pelicula/index.html', data=data)


@pelicula.route("/agregar", methods=["POST","GET"])
@login_required
def agregar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if request.method == "POST":



        if not "pel_v_titulo" in request.json:
            response_body["errors"].append("Campo titulo es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_t_sinopsis" in request.json:
            response_body["errors"].append("Campo sinopsis es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_v_director" in request.json:
            response_body["errors"].append("Campo director es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_i_duracion" in request.json:
            response_body["errors"].append("Campo duracion es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_d_estreno" in request.json:
            response_body["errors"].append("Campo estreno es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_v_ruta_poster_data" in request.json:
            response_body["errors"].append("Campo poster es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_v_ruta_banner_data" in request.json:
            response_body["errors"].append("Campo banner es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_v_pais_origen" in request.json:
            response_body["errors"].append("Campo pais origen es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_i_edad_minima" in request.json:
            response_body["errors"].append("Campo edad minima es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_i_estado" in request.json:
            response_body["errors"].append("Campo estado película es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        pel_v_titulo = request.json["pel_v_titulo"]
        pel_t_sinopsis = request.json["pel_t_sinopsis"]
        pel_v_director = request.json["pel_v_director"]
        pel_i_duracion = request.json["pel_i_duracion"]
        pel_d_estreno = request.json["pel_d_estreno"]
        pel_v_ruta_poster = request.json["pel_v_ruta_poster_data"]
        pel_v_ruta_banner = request.json["pel_v_ruta_banner_data"]
        pel_v_pais_origen = request.json["pel_v_pais_origen"]
        pel_i_edad_minima = request.json["pel_i_edad_minima"]
        pel_i_estado = request.json["pel_i_estado"]


        if pel_v_titulo == "":
            response_body["errors"].append("Campo titulo es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_t_sinopsis == "":
            response_body["errors"].append("Campo sinopsis es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_v_director == "":
            response_body["errors"].append("Campo director es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_i_duracion == "":
            response_body["errors"].append("Campo duracion es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_d_estreno == "":
            response_body["errors"].append("Campo estreno es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_v_ruta_poster == "":
            response_body["errors"].append("Campo poster es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_v_ruta_banner == "":
            response_body["errors"].append("Campo banner es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_v_pais_origen == "":
            response_body["errors"].append("Campo pais origen es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_i_edad_minima == "":
            response_body["errors"].append("Campo edad minima es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_i_estado == "":
            response_body["errors"].append("Campo estado película es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code



        pel_v_ruta_poster = pel_v_ruta_poster.replace(" ","+")
        base64Data = pel_v_ruta_poster.split(",")

        extension = ".txt"
        if "jpeg" in base64Data[0]:
            extension = ".jpg"
        elif "png" in base64Data[0]:
            extension = ".png"

        ruta_poster = str(uuid.uuid4())+ extension

        pel_v_ruta_poster = base64Data[1]
        try:
            with open(BASE_PATH + ruta_poster, "wb") as fh:
                fh.write(base64.urlsafe_b64decode(pel_v_ruta_poster))
        except BaseException as e:
           print(str(e))


        pel_v_ruta_banner = pel_v_ruta_banner.replace(" ","+")
        base64Data = pel_v_ruta_banner.split(",")
        extension = ".txt"
        if "jpeg" in base64Data[0]:
            extension = ".jpg"
        elif "png" in base64Data[0]:
            extension = ".png"

        ruta_banner = str(uuid.uuid4())+ extension
        pel_v_ruta_banner = base64Data[1]
        try:
            with open(BASE_PATH + ruta_banner, "wb") as fh:
                fh.write(base64.urlsafe_b64decode(pel_v_ruta_banner))
        except BaseException as e:
           print(str(e))

        fecha_estreno = datetime.strptime(pel_d_estreno, '%Y-%m-%d')

        pelicula = crear_pelicula(pel_v_titulo, pel_t_sinopsis, pel_v_director,
                                  pel_i_duracion, fecha_estreno, ruta_poster,
                                  ruta_banner, pel_v_pais_origen, pel_i_edad_minima, pel_i_estado)

        num_generos = int(request.json["num_generos"])
        for n_genero in range(1,num_generos + 1):
            if "genero_" + str(n_genero) in request.json:
                genero_json = request.json["genero_" + str(n_genero)]
                if genero_json == "otro":
                    genero = crear_genero(request.json["otro_genero_" + str(n_genero)])
                    genero_json = genero["gen_i_id"]
                crear_pelicula_genero(pelicula["pel_i_id"], genero_json)

        num_actores = int(request.json["num_actores"])
        for n_actor in range(1,num_actores + 1):
            if "actor_" + str(n_actor) in request.json:
                actor_json = request.json["actor_" + str(n_actor)]
                crear_pelicula_actor(pelicula["pel_i_id"], actor_json)







        response_body["data"] = {"pel_v_titulo": pel_v_titulo, "redirect": url_for('pelicula.index')}
        response_body["message"] = "Se agregó la película"
        return response_body, status_code
    else:
        generos = obtener_generos()
        actores = obtener_actores()

        data = {
            "generos":generos,
            "actores":actores
        }

        return render_template('pelicula/agregar.html', data=data)


@pelicula.route("/select_generos/<int:num>", methods=["GET"])
@login_required
def select_generos(num):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    num = str(num)
    elemento = '<div class="col-md-3 generos">' \
    '<div class="form-floating">'\
    '<select class="form-control form-select select-otro" id="genero_'+num+'" name="genero_'+num+'" required="" data-otro="otro_genero_'+num+'" >' \
    '<option selected  value="">Seleccione uno</option>'
    generos = obtener_generos()
    for genero in generos:
        print(generos)
        elemento += '<option value="'+str(genero["gen_i_id"])+'">'+genero["gen_v_nombre"]+'</option>'

    elemento += '<option value="otro">Otro</option>' \
    '</select>' \
    '<label for="genero_'+num+'">Genero '+num+'</label>' \
    '<div class="form-floating otro">' \
    '<input autocomplete="off" type="text" class="form-control " id="otro_genero_'+num+'" name="otro_genero_'+num+'" placeholder="Otro Genero '+num+'" value="">' \
    '<label for="otro_genero_'+num+'">Otro Genero '+num+'</label>' \
    '</div></div></div>'

    response_body["data"] = {"elemento": elemento}
    return response_body, status_code


@pelicula.route("/select_actores/<int:num>", methods=["GET"])
@login_required
def select_actores(num):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    num = str(num)

    elemento = '<div class="col-md-3 actores">' \
    '<div class="form-floating">'\
    '<select class="form-control form-select" id="actor_'+num+'" name="actor_'+num+'" required="" >' \
    '<option selected  value="">Seleccione uno</option>'
    actores = obtener_actores()
    for actor in actores:
        elemento += '<option value="'+str(actor["act_i_id"])+'">'+actor["act_v_nombre"]+' '+actor["act_v_apellido"]+'</option>'

    elemento += '</select>'
    elemento += '<label for="actor_">Actor</label></div></div>'

    response_body["data"] = {"elemento": elemento}
    return response_body, status_code


@pelicula.route("/modificar/<int:id>", methods=["POST","GET"])
@login_required
def modificar(id):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    pelicula = obtener_pelicula_por_id(id)
    if pelicula is None:
        return redirect('pelicula.index')

    if request.method == "POST":
        if not "pel_v_titulo" in request.json:
            response_body["errors"].append("Campo titulo es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_t_sinopsis" in request.json:
            response_body["errors"].append("Campo sinopsis es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_v_director" in request.json:
            response_body["errors"].append("Campo director es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_i_duracion" in request.json:
            response_body["errors"].append("Campo duracion es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_d_estreno" in request.json:
            response_body["errors"].append("Campo estreno es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_v_pais_origen" in request.json:
            response_body["errors"].append("Campo pais origen es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if not "pel_i_edad_minima" in request.json:
            response_body["errors"].append("Campo edad minima es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        if not "pel_i_estado" in request.json:
            response_body["errors"].append("Campo estado película es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        pel_v_titulo = request.json["pel_v_titulo"]
        pel_t_sinopsis = request.json["pel_t_sinopsis"]
        pel_v_director = request.json["pel_v_director"]
        pel_i_duracion = request.json["pel_i_duracion"]
        pel_d_estreno = request.json["pel_d_estreno"]
        pel_v_pais_origen = request.json["pel_v_pais_origen"]
        pel_i_edad_minima = request.json["pel_i_edad_minima"]
        pel_i_estado = request.json["pel_i_estado"]


        if pel_v_titulo == "":
            response_body["errors"].append("Campo titulo es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_t_sinopsis == "":
            response_body["errors"].append("Campo sinopsis es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_v_director == "":
            response_body["errors"].append("Campo director es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_i_duracion == "":
            response_body["errors"].append("Campo duracion es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_d_estreno == "":
            response_body["errors"].append("Campo estreno es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_v_pais_origen == "":
            response_body["errors"].append("Campo pais origen es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_i_edad_minima == "":
            response_body["errors"].append("Campo edad minima es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if pel_i_estado == "":
            response_body["errors"].append("Campo estado película es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code


        ruta_poster = pelicula["pel_v_ruta_poster"]

        if "pel_v_ruta_poster_data" in request.json:
            pel_v_ruta_poster = request.json["pel_v_ruta_poster_data"]
            if pel_v_ruta_poster != "":
                pel_v_ruta_poster = pel_v_ruta_poster.replace(" ","+")
                base64Data = pel_v_ruta_poster.split(",")

                extension = ".txt"
                if "jpeg" in base64Data[0]:
                    extension = ".jpg"
                elif "png" in base64Data[0]:
                    extension = ".png"

                ruta_poster = str(uuid.uuid4())+ extension

                pel_v_ruta_poster = base64Data[1]
                try:
                    with open(BASE_PATH + ruta_poster, "wb") as fh:
                        fh.write(base64.urlsafe_b64decode(pel_v_ruta_poster))
                except BaseException as e:
                   print(str(e))


        ruta_banner = pelicula["pel_v_ruta_banner"]
        if "pel_v_ruta_banner_data" in request.json:
            pel_v_ruta_banner = request.json["pel_v_ruta_banner_data"]
            if pel_v_ruta_banner != "":
                pel_v_ruta_banner = pel_v_ruta_banner.replace(" ","+")
                base64Data = pel_v_ruta_banner.split(",")
                extension = ".txt"
                if "jpeg" in base64Data[0]:
                    extension = ".jpg"
                elif "png" in base64Data[0]:
                    extension = ".png"

                ruta_banner = str(uuid.uuid4())+ extension
                pel_v_ruta_banner = base64Data[1]
                try:
                    with open(BASE_PATH + ruta_banner, "wb") as fh:
                        fh.write(base64.urlsafe_b64decode(pel_v_ruta_banner))
                except BaseException as e:
                   print(str(e))

        fecha_estreno = datetime.strptime(pel_d_estreno, '%Y-%m-%d')

        pelicula = modificar_pelicula(id, pel_v_titulo, pel_t_sinopsis, pel_v_director,
                                  pel_i_duracion, fecha_estreno, ruta_poster,
                                  ruta_banner, pel_v_pais_origen, pel_i_edad_minima, pel_i_estado)

        eliminar_pelicula_genero(id)
        num_generos = int(request.json["num_generos"])
        for n_genero in range(1,num_generos + 1):
            if "genero_" + str(n_genero) in request.json:
                genero_json = request.json["genero_" + str(n_genero)]
                if genero_json == "otro":
                    genero = crear_genero(request.json["otro_genero_" + str(n_genero)])
                    genero_json = genero["gen_i_id"]
                crear_pelicula_genero(pelicula["pel_i_id"], genero_json)

        eliminar_pelicula_actor(id)
        num_actores = int(request.json["num_actores"])
        for n_actor in range(1,num_actores + 1):
            if "actor_" + str(n_actor) in request.json:
                actor_json = request.json["actor_" + str(n_actor)]
                crear_pelicula_actor(pelicula["pel_i_id"], actor_json)


        response_body["data"] = {"redirect": url_for('pelicula.index')}
        response_body["message"] = "Se modificó la pelicula"
        return response_body, status_code

    else:
        generos = obtener_generos()
        actores = obtener_actores()
        pelicula["actores"] = obtener_actores_por_pelicula(id)
        pelicula["generos"] = obtener_generos_por_pelicula(id)

        data = {
            "generos":generos,
            "actores":actores,
            "pelicula":pelicula
        }
        return render_template('pelicula/modificar.html', data=data)


@pelicula.route("/eliminar/<int:id>", methods=["GET"])
@login_required
def eliminar(id):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.BAD_REQUEST
    if id != "":

        if cuenta_funciones_por_pelicula(id) > 0:
            response_body["errors"].append("Error la película tiene funciones relacionadas")
            return response_body, status_code

        if eliminar_pelicula(id):
            return redirect(url_for('pelicula.index'))
        else:
            response_body["errors"].append("Error al eliminar la pelicula")
            return response_body, status_code

    else:
        response_body["errors"].append("El id es requerido, para eliminar la película")
        return response_body, status_code



@pelicula.route("/cartelera/<int:id_ciudad>", methods=["GET"])
def cartelera(id_ciudad):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    peliculas = obtener_peliculas_en_cartelera_por_ciudad(id_ciudad)
    response_body["message"] = "Peliculas en cartelera cargadas correctamente!"
    response_body["data"] = peliculas
    return response_body, status_code


@pelicula.route("/mas_vistos/<int:id_ciudad>", methods=["GET"])
def mas_vistos(id_ciudad):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    peliculas = obtener_peliculas_mas_vistas_por_ciudad(id_ciudad)
    response_body["message"] = "Peliculas en cartelera cargadas correctamente!"
    response_body["data"] = peliculas
    return response_body, status_code


@pelicula.route("/proximos_estrenos", methods=["GET"])
def proximos_estrenos():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    peliculas = obtener_peliculas_por_estado(2)
    response_body["message"] = "Peliculas en proximos estrenos cargadas correctamente!"
    response_body["data"] = peliculas
    return response_body, status_code


@pelicula.route("/pelicula_id/<int:id>", methods=["GET"])
def pelicula_id(id):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    pelicula = obtener_pelicula_por_id(id)
    pelicula["actores"] = obtener_actores_por_pelicula(id)
    pelicula["generos"] = obtener_generos_por_pelicula(id)

    response_body["message"] = "Peliculas cargadas por id correctamente!"
    response_body["data"] = pelicula
    return response_body, status_code

