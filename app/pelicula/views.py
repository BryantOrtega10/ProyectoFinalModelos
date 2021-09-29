from http import HTTPStatus

from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required
import copy

from app.actor.models import get_actores
from app.pelicula.models import get_generos

pelicula = Blueprint("pelicula", __name__, url_prefix="/pelicula")

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": [], "metadata": []}


@pelicula.route("/", methods=["GET"])
@login_required
def index():
    return render_template('pelicula/index.html')


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

        pel_v_titulo = request.json["pel_v_titulo"]
        if pel_v_titulo == "":
            response_body["errors"].append("Campo titulo es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code




        response_body["data"] = {"pel_v_titulo": pel_v_titulo, "redirect": url_for('pelicula.index')}
        response_body["message"] = "Se agregó la película"
        return response_body, status_code
    else:
        generos = get_generos()
        actores = get_actores()

        data = {
            "generos":generos,
            "actores":actores
        }

        return render_template('pelicula/agregar.html', data=data)
