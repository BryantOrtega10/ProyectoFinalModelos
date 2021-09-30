from http import HTTPStatus
from flask import Blueprint, request
from app.ciudad.models import crear_ciudad, get_ciudades, eliminar_ciudad, modificar_ciudad
from app.cine.models import obtener_cines_por_ciudad
import copy

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": []}
ciudad = Blueprint("ciudad", __name__, url_prefix="/ciudad")


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
