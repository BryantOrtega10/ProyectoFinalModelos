import uuid
from datetime import datetime
from http import HTTPStatus
from flask import Blueprint, request, url_for
import copy

from app.auth.models import crear_usuario, obtener_usuario_por_correo, obtener_usuario_por_correo_password
from app.cliente.models import crear_cliente, get_clientes, eliminar_cliente, modificar_cliente, \
    obtener_cliente_por_usuario, existe_cliente_por_cedula

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": [], "metadata": []}
cliente = Blueprint("cliente", __name__, url_prefix="/cliente")

@cliente.route("/login", methods=["POST"])
def login():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    usr_v_correo = request.json["usr_v_correo"]
    usr_v_pass = request.json["usr_v_pass"]
    if usr_v_correo != "" and usr_v_correo != None:
        if usr_v_pass != "" and usr_v_pass != None:
            usuario = obtener_usuario_por_correo_password(usr_v_correo, usr_v_pass)
            if usuario != None:
                cliente = obtener_cliente_por_usuario(usuario.id)
                if cliente != None:
                    response_body["message"] = "Cliente creado correctamente!"
                    response_body["data"] = {"auth-token":cliente["cli_v_token"]}
                else:
                    response_body["message"] = "Usuario o contraseña incorrectos"
                    response_body["errors"].append("El usuario no esta relacionado con ningun cliente")
                    status_code = HTTPStatus.BAD_REQUEST
            else:
                response_body["message"] = "Usuario o contraseña incorrectos"
                response_body["errors"].append("Credenciales incorrectas")
                status_code = HTTPStatus.BAD_REQUEST
        else:
            response_body["errors"].append("Debe ingresar una contraseña")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["errors"].append("Debe ingresar un correo")
        status_code = HTTPStatus.BAD_REQUEST
    return response_body, status_code


@cliente.route("/registrar", methods=["POST"])
def registrar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    cli_i_cedula = request.json["cli_i_cedula"]
    cli_v_nombre = request.json["cli_v_nombre"]
    cli_d_fecha_nacimiento = request.json["cli_d_fecha_nacimiento"]
    cli_fk_ciu_i = request.json["cli_fk_ciu_i"]
    usr_v_correo = request.json["usr_v_correo"]
    usr_v_pass = request.json["usr_v_pass"]
    if usr_v_correo != "" and usr_v_correo != None:
        if usr_v_pass != "" and usr_v_pass != None:
            if cli_i_cedula != "" and cli_i_cedula != None:
                if cli_v_nombre != "" and cli_v_nombre != None:
                    if cli_d_fecha_nacimiento != "" and cli_d_fecha_nacimiento != None:
                        if cli_fk_ciu_i != "" and cli_fk_ciu_i != None:

                            usuario_verif = obtener_usuario_por_correo(usr_v_correo)
                            if not existe_cliente_por_cedula(cli_i_cedula):
                                if usuario_verif == None:

                                    fecha_nacimiento = datetime.fromisoformat(cli_d_fecha_nacimiento)
                                    usuario = crear_usuario(usr_v_correo, usr_v_pass, 1)
                                    token = str(uuid.uuid4())
                                    cliente = crear_cliente(cli_i_cedula,cli_v_nombre,fecha_nacimiento,cli_fk_ciu_i,usuario.id, token)
                                    response_body["message"] = "Cliente creado correctamente!"
                                    response_body["data"] = {"auth-token":token}
                                else:
                                    response_body["errors"].append("El nombre usuario ya existe")
                                    status_code = HTTPStatus.BAD_REQUEST
                            else:
                                response_body["errors"].append("La cedula ya existe")
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
        else:
            response_body["errors"].append("Debe ingresar una contraseña")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["errors"].append("Debe ingresar un correo")
        status_code = HTTPStatus.BAD_REQUEST
    return response_body, status_code
