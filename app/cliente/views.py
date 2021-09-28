from http import HTTPStatus
from flask import Blueprint, request, url_for
import copy
from app.cliente import crear_cliente, get_clientes, eliminar_cliente, modificar_cliente

RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}
cliente = Blueprint("cliente", __name__, url_prefix="/cliente")


@cliente.route("/registrar", methods=["POST"])
def registrar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    cli_i_cedula = request.json["cli_i_cedula"]
    cli_v_nombre = request.json["cli_v_nombre"]
    cli_d_fecha_nacimiento = request.json["cli_d_fecha_nacimiento"]
    cli_fk_ciu_i = request.json["cli_fk_ciu_i"]
    cli_fk_usr_i = request.json["cli_fk_usr_i"]

    if cli_i_cedula != "" and cli_i_cedula != None:
        if cli_v_nombre != "" and cli_v_nombre != None:
            if cli_d_fecha_nacimiento != "" and cli_d_fecha_nacimiento != None:
                if cli_fk_ciu_i != "" and cli_fk_ciu_i != None:
                    if cli_fk_usr_i != "" and cli_fk_usr_i != None:
                        cliente = crear_cliente(cli_i_cedula,cli_v_nombre,cli_d_fecha_nacimiento,cli_fk_ciu_i,cli_fk_usr_i)
                        response_body["message"] = "Cliente creado correctamente!"
                        response_body["data"] = cliente
                    else:
                        response_body["errors"].append("FK de usuario vacia")
                        status_code = HTTPStatus.BAD_REQUEST
                else:
                    response_body["errors"].append("FK de ciudad vacia")
                    status_code = HTTPStatus.BAD_REQUEST
            else:
                response_body["errors"].append("Fecha de nacimiento vacia")
                status_code = HTTPStatus.BAD_REQUEST
        else:
            response_body["errors"].append("Nombre vacio")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["errors"].append("Cedula vacia")
        status_code = HTTPStatus.BAD_REQUEST        
    return RESPONSE_BODY, status_code
