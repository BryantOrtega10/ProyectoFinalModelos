from http import HTTPStatus
from flask import Blueprint, request
from app.reserva.models import crear_reserva, get_reservas, eliminar_reserva, modificar_reserva
import copy

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": []}
reserva = Blueprint("reserva", __name__, url_prefix="/reserva")

@reserva.route("/", methods=["GET"])
def index():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    reservas = get_reservas()
    response_body["message"] = "Reservas consultadas correctamente!"
    response_body["data"] = reservas
    return response_body, status_code

@reserva.route("/crear", methods=["POST"])
def crear():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK

    res_t_sillas = request.json["res_t_sillas"]
    res_i_modo_pago = request.json["res_i_modo_pago"]
    res_i_estado = request.json["res_i_estado"]
    res_fk_fun_i = request.json["res_fk_fun_i"]
    res_fk_cli_i = request.json["res_fk_cli_i"]

    if res_t_sillas != "" and res_t_sillas != None:
        if res_i_modo_pago != "" and res_i_modo_pago != None:
            if res_i_estado != "" and res_i_estado != None:
                if res_fk_fun_i != "" and res_fk_fun_i != None:
                    if res_fk_cli_i != "" and res_fk_cli_i != None:
                        reserva = crear_reserva(res_t_sillas, res_i_modo_pago, res_i_estado, res_fk_fun_i, res_fk_cli_i)

                        response_body["message"] = "Reserva creada correctamente!"
                        response_body["data"] = reserva
                    else:
                        response_body["errors"].append("FK cliente vacia")
                        status_code = HTTPStatus.BAD_REQUEST
                else:
                    response_body["errors"].append("FK funcion vacia")
                    status_code = HTTPStatus.BAD_REQUEST
            else:
                response_body["errors"].append("Estado vacio")
                status_code = HTTPStatus.BAD_REQUEST
        else:
            response_body["errors"].append("Modo de pago vacio")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["errors"].append("Texto vacio")
        status_code = HTTPStatus.BAD_REQUEST
    return response_body, status_code

@reserva.route("/modificar", methods=["PUT"])
def modificar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK

    res_i_id = request.json["res_i_id"]
    res_t_sillas = request.json["res_t_sillas"]
    res_i_modo_pago = request.json["res_i_modo_pago"]
    res_i_estado = request.json["res_i_estado"]

    if res_i_id != "" and res_i_id != None:
        if res_t_sillas != "" and res_t_sillas != None:
            if res_i_modo_pago != "" and res_i_modo_pago != None:
                if res_i_estado != "" and res_i_estado != None:
                    reserva_mod = modificar_reserva(res_i_id, res_t_sillas, res_i_modo_pago, res_i_estado)
                    if reserva_mod != None:
                        response_body["message"] = "Reserva modificada correctamente!"
                        response_body["data"] = reserva_mod
                    else:
                        response_body["message"] = "La reserva no existe"
                        response_body["errors"].append("Error al modificar reserva")
                        status_code = HTTPStatus.BAD_REQUEST
                else:
                    response_body["message"] = "Estado vacio"
                    response_body["errors"].append("Error al modificar reserva")
                    status_code = HTTPStatus.BAD_REQUEST
            else:
                response_body["message"] = "Modo de pago vacio"
                response_body["errors"].append("Error al modificar reserva")
                status_code = HTTPStatus.BAD_REQUEST
        else:
            response_body["message"] = "Texto vacio"
            response_body["errors"].append("Error al modificar reserva")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["message"] = "ID vacio"
        response_body["errors"].append("Error al modificar reserva")
        status_code = HTTPStatus.BAD_REQUEST
    return response_body, status_code

@reserva.route("/eliminar", methods=["DELETE"])
def eliminar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK

    res_i_id = request.json["res_i_id"]

    if res_i_id != "" and res_i_id != None:
        if eliminar_reserva(res_i_id):
            response_body["message"] = "Reserva eliminada correctamente!"
        else:
            response_body["message"] = "Error no se encuentra la reserva"
            response_body["errors"].append("Error al eliminar reserva")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["message"] = "ID vacio"
        response_body["errors"].append("Error al eliminar reserva")
        status_code = HTTPStatus.BAD_REQUEST
    return response_body, status_code