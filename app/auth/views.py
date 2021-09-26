from http import HTTPStatus
from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_user, logout_user, login_required
from app.auth.models import obtener_usuario_por_correo_password, crear_usuario
import copy


auth = Blueprint("auth", __name__, url_prefix="/")

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": [], "metadata": []}


@auth.route("/", methods=["POST","GET"])
def login():
    status_code = HTTPStatus.OK
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    if request.method == "POST":
        usuario_t = request.json["email"]
        contrasena_t = request.json["password"]
        recordar = ("recordar" in request.json)

        usuario = obtener_usuario_por_correo_password(usuario_t, contrasena_t)
        if not usuario:
            response_body["errors"].append("Credenciales incorrectas.")
            status_code = HTTPStatus.UNAUTHORIZED
            return response_body, status_code

        login_user(usuario, remember=recordar)
        response_body["message"] = "Bienvenido!"
        if (usuario.usr_i_rol == 1):
            response_body["errors"].append("Debe ser administrador para ingresar.")
        else:
            response_body["data"] = {"redirect": url_for('pelicula.index')}
        status_code = HTTPStatus.OK
        return response_body, status_code
    else:
        return render_template('login.html')


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
