from http import HTTPStatus
from flask import Blueprint, request
from app.funcion.models import crear_funcion, get_funciones, eliminar_funcion, modificar_funcion
import copy

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": []}
funcion = Blueprint("funcion", __name__, url_prefix="/funcion")

@funcion.route("/", methods=["GET"])
def index():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    funciones = get_funciones()
    response_body["message"] = "Funciones consultadas correctamente!"
    response_body["data"] = funciones
    return response_body, status_code

@funcion.route("/crear", methods=["POST"])
def crear():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK

    fun_dt_fecha_hora = request.json["fun_dt_fecha_hora"]
    fun_fk_sal_i = request.json["fun_fk_sal_i"]
    fun_fk_pel_i = request.json["fun_fk_pel_i"]

    if fun_dt_fecha_hora != "" and fun_dt_fecha_hora != None:
        if fun_fk_sal_i != "" and fun_fk_sal_i != None:
            if fun_fk_pel_i != "" and fun_fk_pel_i != None:
                funcion = crear_funcion(fun_dt_fecha_hora, fun_fk_sal_i, fun_fk_pel_i)

                response_body["message"] = "Funcion creada correctamente!"
                response_body["data"] = funcion
            else:
                response_body["errors"].append("FK pelicula vacia")
                status_code = HTTPStatus.BAD_REQUEST
        else:
            response_body["errors"].append("FK sala vacia")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["errors"].append("Fecha vacia")
        status_code = HTTPStatus.BAD_REQUEST
    return response_body, status_code

@funcion.route("/modificar", methods=["PUT"])
def modificar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK

    fun_i_id = request.json["fun_i_id"]
    fun_dt_fecha_hora = request.json["fun_dt_fecha_hora"]
    if fun_i_id != "" and fun_i_id != None:
        if fun_dt_fecha_hora != "" and fun_dt_fecha_hora != None:
            funcion_mod = modificar_funcion(fun_i_id, fun_dt_fecha_hora)
            if funcion_mod != None:
                response_body["message"] = "Funcion modificada correctamente!"
                response_body["data"] = funcion_mod
            else:
                response_body["message"] = "La funcion no existe"
                response_body["errors"].append("Error al modificar funcion")
                status_code = HTTPStatus.BAD_REQUEST
        else:
            response_body["message"] = "Fecha vacia"
            response_body["errors"].append("Error al modificar funcion")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["message"] = "ID vacio"
        response_body["errors"].append("Error al modificar funcion")
        status_code = HTTPStatus.BAD_REQUEST
    
    return response_body, status_code

@funcion.route("/eliminar", methods=["DELETE"])
def eliminar():
    fun_i_id = request.json["fun_i_id"]
    if fun_i_id != "" and fun_i_id != None:
        if eliminar_funcion(fun_i_id):
            response_body["message"] = "Funcion eliminada correctamente!"
        else:
            response_body["message"] = "Error no se encuentra la funcion"
            response_body["errors"].append("Error al eliminar funcion")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["message"] = "ID vacio"
        response_body["errors"].append("Error al eliminar funcion")
        status_code = HTTPStatus.BAD_REQUEST
    
    return response_body, status_code