from http import HTTPStatus
from flask import Blueprint, request
from app.sala.models import crear_sala, get_salas, eliminar_sala, modificar_sala
import copy

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": []}
sala = Blueprint("sala", __name__, url_prefix="/sala")

@sala.route("/", methods=["GET"])
def index():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    salas = get_salas()
    response_body["message"] = "Salas consultadas correctamente!"
    response_body["data"] = salas
    return response_body, status_code

@sala.route("/crear", methods=["POST"])
def crear():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    sal_i_numero = request.json["sal_i_numero"]
    sal_t_sillas = request.json["sal_t_sillas"]
    sal_fk_cin_i = request.json["sal_fk_cin_i"]

    if sal_i_numero != "" and sal_i_numero != None:
        if sal_t_sillas != "" and sal_t_sillas != None:
            if sal_fk_cin_i != "" and sal_fk_cin_i != None:
                sala = crear_sala(sal_i_numero, sal_t_sillas, sal_fk_cin_i)

                response_body["message"] = "Ciudad creada correctamente!"
                response_body["data"] = sala
            else:
                response_body["errors"].append("FK vacia")
                status_code = HTTPStatus.BAD_REQUEST
        else:
            response_body["errors"].append("Texto vacio")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["errors"].append("Numero de sillas vacio")
        status_code = HTTPStatus.BAD_REQUEST
    
    return response_body, status_code

@sala.route("/modificar", methods=["PUT"])
def modificar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    
    sal_i_id = request.json["sal_i_id"]
    sal_i_numero = request.json["sal_i_numero"]
    sal_t_sillas = request.json["sal_t_sillas"]

    if sal_i_id != "" and sal_i_id != None:
        if sal_i_numero != "" and sal_i_numero != None:
            if sal_t_sillas != "" and sal_t_sillas != None:

                sala_mod = modificar_sala(sal_i_id, sal_i_numero, sal_t_sillas)
                if sala_mod != None:
                    response_body["message"] = "Sala modificada correctamente!"
                    response_body["data"] = sala_mod
                else:
                    response_body["message"] = "La sala no existe"
                    response_body["errors"].append("Error al modificar ciudad")
                    status_code = HTTPStatus.BAD_REQUEST
            else:
                response_body["message"] = "Texto vacio"
                response_body["errors"].append("Error al modificar ciudad")
                status_code = HTTPStatus.BAD_REQUEST
        else:
            response_body["message"] = "Numero de sillas vacio"
            response_body["errors"].append("Error al modificar ciudad")
            status_code = HTTPStatus.BAD_REQUEST 
    else:
        response_body["message"] = "ID vacio"
        response_body["errors"].append("Error al modificar ciudad")
        status_code = HTTPStatus.BAD_REQUEST 
    
    return response_body, status_code

@sala.route("/eliminar", methods=["DELETE"])
def eliminar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK

    sal_i_id = request.json["sal_i_id"]

    if sal_i_id != None and sal_i_id != "":
        if eliminar_sala(id):
            response_body["message"] = "Sala eliminada correctamente!"
        else:
            response_body["message"] = "No existe la sala"
            response_body["errors"].append("Error al eliminar la sala")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["message"] = "ID vacio"
        response_body["errors"].append("Error al eliminar la sala")
        status_code = HTTPStatus.BAD_REQUEST
    
    return response_body, status_code
