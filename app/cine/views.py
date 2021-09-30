from http import HTTPStatus
from flask import Blueprint, request
from app.cine.models import crear_cine, get_cines, eliminar_cine, modificar_cine
import copy

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": []}
cine = Blueprint("cine", __name__, url_prefix="/cine")

@cine.route("/", methods=["GET"])
def index():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    cines = get_cines()
    response_body["message"] = "Cines consultados correctamente!"
    response_body["data"] = cines
    return response_body, status_code

@cine.route("/crear", methods=["POST"])
def crear():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    cin_v_nombre = request.json["cin_v_nombre"]
    cin_fk_ciu = request.json["cin_fk_ciu"]

    if cin_v_nombre != "" and cin_v_nombre != None:
        if cin_fk_ciu != "" and cin_fk_ciu != None:
            cine = crear_cine(cin_v_nombre, cin_fk_ciu)

            response_body["message"] = "Cine creado correctamente!"
            response_body["data"] = cine
        else:
            response_body["errors"].append("Nombre vacio")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["errors"].append("fk vacia")
        status_code = HTTPStatus.BAD_REQUEST
    
    return response_body, status_code

@cine.route("/modificar", methods=["PUT"])
def modificar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK

    cin_i_id = request.json["cin_i_id"]
    cin_v_nombre = request.json["cin_v_nombre"]
    
    if cin_i_id != "" and cin_i_id != None:
        if cin_v_nombre != "" and cin_v_nombre != None:
            cine_mod = modificar_cine(cin_i_id, cin_v_nombre)
            if cine_mod != None:
                response_body["message"] = "Cine modificado correctamente!"
                response_body["data"] = cine_mod
            else:
                response_body["message"] = "No se encontro el cine"
                response_body["errors"].append("Error al modificar cine")
                status_code = HTTPStatus.BAD_REQUEST
        else:
            response_body["message"] = "Nombre vacio"
            response_body["errors"].append("Error al modificar cine")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["message"] = "ID vacio"
        response_body["errors"].append("Error al modificar cine")
        status_code = HTTPStatus.BAD_REQUEST

    return response_body, status_code
    
@cine.route("/eliminar", methods=["DELETE"])
def eliminar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK

    cin_i_id = request.json["cin_i_id"]

    if cin_i_id != "" and cin_i_id != None:
        if eliminar_cine(cin_i_id):
            response_body["message"] = "Cine eliminado correctamente!"
        else:
            response_body["message"] = "Error no se encuentra el cine"
            response_body["errors"].append("Error al eliminar el cine")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["message"] = "Id vacio"
        response_body["errors"].append("Error al eliminar el cine")
        status_code = HTTPStatus.BAD_REQUEST
    
    return response_body, status_code