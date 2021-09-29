from http import HTTPStatus

from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required
import copy

from app.actor.models import obtener_actores, crear_actor, eliminar_actor, obtener_actor_por_id, modificar_actor
from app.pelicula.models import cuenta_peliculas_por_actor

actor = Blueprint("actor", __name__, url_prefix="/actor")

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": [], "metadata": []}


@actor.route("/", methods=["GET"])
@login_required
def index():
    actores = obtener_actores()
    data = {
        "actores":actores
    }
    return render_template('actor/index.html', data=data)


@actor.route("/agregar", methods=["POST","GET"])
@login_required
def agregar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if request.method == "POST":

        if not "act_v_nombre" in request.json:
            response_body["errors"].append("Campo nombre es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        if not "act_v_apellido" in request.json:
            response_body["errors"].append("Campo apellido es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code



        act_v_nombre = request.json["act_v_nombre"]
        act_v_apellido = request.json["act_v_apellido"]


        if act_v_nombre == "":
            response_body["errors"].append("Campo nombre es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        if act_v_apellido == "":
            response_body["errors"].append("Campo apellido es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        actor = crear_actor(act_v_nombre, act_v_apellido)


        response_body["data"] = {"redirect": url_for('actor.index')}
        response_body["message"] = "Se agregó el actor"
        return response_body, status_code
    else:

        return render_template('actor/agregar.html')


@actor.route("/eliminar/<int:id>", methods=["GET"])
@login_required
def eliminar(id):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.BAD_REQUEST
    if id != "":

        if cuenta_peliculas_por_actor(id) > 0:
            response_body["errors"].append("Error el actor tiene películas relacionadas")
            return response_body, status_code

        if eliminar_actor(id):
            return redirect(url_for('actor.index'))
        else:
            response_body["errors"].append("Error al eliminar el actor")
            return response_body, status_code

    else:
        response_body["errors"].append("El id es requerido, para eliminar el actor")
        return response_body, status_code


@actor.route("/modificar/<int:id>", methods=["POST","GET"])
@login_required
def modificar(id):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if request.method == "POST":
        if not "act_v_nombre" in request.json:
            response_body["errors"].append("Campo nombre es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        if not "act_v_apellido" in request.json:
            response_body["errors"].append("Campo apellido es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        act_v_nombre = request.json["act_v_nombre"]
        act_v_apellido = request.json["act_v_apellido"]


        if act_v_nombre == "":
            response_body["errors"].append("Campo nombre es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        if act_v_apellido == "":
            response_body["errors"].append("Campo apellido es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        actor = modificar_actor(id,act_v_nombre, act_v_apellido)
        response_body["data"] = {"redirect": url_for('actor.index')}
        response_body["message"] = "Se modificó el actor"
        return response_body, status_code

    else:
        actor = obtener_actor_por_id(id)
        if actor is None:
            return redirect('actor.index')
        else:
            data = {
                "actor":actor
            }
            return render_template('actor/modificar.html', data=data)
