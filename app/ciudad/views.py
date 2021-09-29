from http import HTTPStatus
from flask import Blueprint, request, render_template, url_for, redirect
from app.ciudad.models import crear_ciudad, get_ciudades, eliminar_ciudad, modificar_ciudad, ciudad_por_id
from app.cine.models import obtener_cines_por_ciudad
import copy
from flask_login import login_required

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": []}
ciudad = Blueprint("ciudad", __name__, url_prefix="/ciudad")

@ciudad.route("/template", methods=["GET"])
@login_required
def template():
    ciudades = get_ciudades()
    return render_template('ciudad/index.html', ciudades = ciudades)

@ciudad.route("/agregar", methods=["POST","GET"])
@login_required
def agregar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if request.method == "POST":
        if not "ciu_v_nombre" in request.json: 
            response_body["errors"].append("Campo nombre es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        ciu_v_nombre = request.json["ciu_v_nombre"]
        if ciu_v_nombre == "":
            response_body["errors"].append("Campo nombre es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        else:
            ciudad = crear_ciudad(ciu_v_nombre)
            response_body["data"] = {"ciudad": ciudad, "redirect": url_for('ciudad.template')}
            response_body["message"] = "Ciudad creada correctamente"
        return response_body, status_code
    else:
        return render_template('ciudad/agregar.html')

@ciudad.route("/editar/<id_ciudad>", methods=["POST","GET"])
@login_required
def editar(id_ciudad):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if request.method == "POST":
        if not "ciu_v_nombre" in request.json: 
            response_body["errors"].append("Campo nombre es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        ciu_v_nombre = request.json["ciu_v_nombre"]
        if ciu_v_nombre == "":
            response_body["errors"].append("Campo nombre es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        else:
            ciudad = modificar_ciudad(id_ciudad, ciu_v_nombre)
            response_body["data"] = {"ciudad": ciudad, "redirect": url_for('ciudad.template')}
            response_body["message"] = "Ciudad editada correctamente"
        return response_body, status_code
    else:
        ciudad = ciudad_por_id(id_ciudad)
        return render_template('ciudad/editar.html', ciudad = ciudad)

@ciudad.route("/quitar/<id_ciudad>", methods=["GET"])
@login_required
def quitar(id_ciudad):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if len(obtener_cines_por_ciudad(id_ciudad)) == 0:
        if eliminar_ciudad(id_ciudad):
            response_body["data"] = {"ciudad": ciudad, "redirect": url_for('ciudad.template')}
            response_body["message"] = "Ciudad eliminada correctamente"
        else:
            response_body["errors"].append("La ciudad no existe")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["errors"].append("La ciudad tiene datos relacionados")
        status_code = HTTPStatus.BAD_REQUEST

    return redirect(url_for('ciudad.template'))

@ciudad.route("/", methods=["GET"])
def index():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    ciudades = get_ciudades()
    response_body["message"] = "Ciudades consultadas correctamente!"
    response_body["data"] = ciudades
    return response_body, status_code

@ciudad.route("/crear", methods=["POST"])
def crear():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    ciu_v_nombre = request.json["ciu_v_nombre"]

    if ciu_v_nombre != "" and ciu_v_nombre != None:
        ciudad = crear_ciudad(ciu_v_nombre)

        response_body["message"] = "Ciudad creada correctamente!"
        response_body["data"] = ciudad
    else:
        response_body["errors"].append("Nombre vacio")
        status_code = HTTPStatus.BAD_REQUEST

    return response_body, status_code


@ciudad.route("/modificar", methods=["PUT"])
def modificar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK

    id = request.json["ciu_i_id"]
    nombre = request.json["ciu_v_nombre"]
    if id != "" and nombre != "" and id != None and nombre != None:
        ciudad_mod = modificar_ciudad(id, nombre)
        if ciudad_mod != None:
            response_body["message"] = "Ciudad modificada correctamente!"
            response_body["data"] = ciudad_mod
        else:
            response_body["message"] = "Error al modificar ciudad"
            response_body["errors"].append("Error al modificar ciudad")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["message"] = "Error al modificar ciudad"
        response_body["errors"].append("Nombre vacio")
        response_body["errors"].append("Id vacio")
        status_code = HTTPStatus.BAD_REQUEST

    return response_body, status_code


@ciudad.route("/eliminar", methods=["DELETE"])
def eliminar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK

    id = request.json["ciu_i_id"]

    if id != None and id != "":
        #FALTA VERIFICAR QUE LA CIUDAD NO ESTE RELACIONADA CON OTRAS TABLAS.
        if len(obtener_cines_por_ciudad(id)) == 0:

            if eliminar_ciudad(id):
                response_body["message"] = "Ciudad eliminada correctamente!"
            else:
                response_body["message"] = "Error no se encuentra la ciudad"
                response_body["errors"].append("Error no se encuentra la ciudad")
                status_code = HTTPStatus.BAD_REQUEST
        else:
            response_body["message"] = "Error tiene datos relacionados"
            response_body["errors"].append("Error al eliminar ciudad")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["message"] = "Error al eliminar ciudad"
        response_body["errors"].append("Error al eliminar ciudad")
        status_code = HTTPStatus.BAD_REQUEST

    return response_body, status_code
