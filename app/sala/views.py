from http import HTTPStatus
from flask import Blueprint, request, render_template, url_for
from flask_login import login_required
from werkzeug.utils import redirect

from app.cine.models import get_cines
from app.sala.models import crear_sala, get_salas, eliminar_sala, modificar_sala, get_salas_con_cine, \
    obtener_sala_por_id
import copy
import json

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": []}
sala = Blueprint("sala", __name__, url_prefix="/sala")

@sala.route("/template", methods=["GET"])
@login_required
def template():
    dupla_sala_cine = get_salas_con_cine()

    data = {
        "sala_cine":dupla_sala_cine
    }

    return render_template('salas/index.html', data = data)


@sala.route("/agregar", methods=["GET","POST"])
@login_required
def agregar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if request.method == "POST":
        sal_i_numero = request.json["sal_i_numero"]
        sal_t_sillas = request.json["sal_t_sillas"]
        sal_fk_cin_i = request.json["sal_fk_cin_i"]

        if sal_i_numero != "" and sal_i_numero != None:
            if sal_t_sillas != "" and sal_t_sillas != None:
                if sal_fk_cin_i != "" and sal_fk_cin_i != None:
                    sala = crear_sala(sal_i_numero, sal_t_sillas, sal_fk_cin_i)

                    response_body["message"] = "Sala creada correctamente!"
                    response_body["data"] = {"sala": sala, "redirect": url_for("sala.template")}

                else:
                    response_body["errors"].append("Cine sin seleccionar")
                    status_code = HTTPStatus.BAD_REQUEST
            else:
                response_body["errors"].append("Sillas vacias")
                status_code = HTTPStatus.BAD_REQUEST
        else:
            response_body["errors"].append("Numero de sillas vacio")
            status_code = HTTPStatus.BAD_REQUEST

        return response_body, status_code
    else:
        cines = get_cines()
        data = {
            "cines" : cines
        }
        return render_template('salas/agregar.html', data = data)

@sala.route("/editar/<int:id>", methods=["GET","POST"])
@login_required
def editar(id):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if request.method == "POST":
        sal_i_numero = request.json["sal_i_numero"]
        sal_t_sillas = request.json["sal_t_sillas"]
        sal_fk_cin_i = request.json["sal_fk_cin_i"]

        if sal_i_numero != "" and sal_i_numero != None:
            if sal_t_sillas != "" and sal_t_sillas != None:
                if sal_fk_cin_i != "" and sal_fk_cin_i != None:
                    sala = modificar_sala(id, sal_i_numero, sal_t_sillas, sal_fk_cin_i)

                    response_body["message"] = "Sala modificada correctamente!"
                    response_body["data"] = {"sala": sala, "redirect": url_for("sala.template")}

                else:
                    response_body["errors"].append("Cine sin seleccionar")
                    status_code = HTTPStatus.BAD_REQUEST
            else:
                response_body["errors"].append("Sillas vacias")
                status_code = HTTPStatus.BAD_REQUEST
        else:
            response_body["errors"].append("Numero de sillas vacio")
            status_code = HTTPStatus.BAD_REQUEST

        return response_body, status_code
    else:
        cines = get_cines()
        sala = obtener_sala_por_id(id)
        silla_obj = json.loads(sala["sal_t_sillas"])
        sala["sillas"] = silla_obj
        data = {
            "cines" : cines,
            "sala": sala
        }



        return render_template('salas/modificar.html', data = data)


@sala.route("/borrar/<int:id>", methods=["GET"])
@login_required
def borrar(id):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK

    sal_i_id = id

    if sal_i_id != None and sal_i_id != "":
        if eliminar_sala(id):
            return redirect(url_for('sala.template'))
        else:
            response_body["message"] = "No existe la sala"
            response_body["errors"].append("Error al eliminar la sala")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["message"] = "ID vacio"
        response_body["errors"].append("Error al eliminar la sala")
        status_code = HTTPStatus.BAD_REQUEST

    return response_body, status_code


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
    sal_fk_cin_i = request.json["sal_fk_cin_i"]

    if sal_i_id != "" and sal_i_id != None:
        if sal_i_numero != "" and sal_i_numero != None:
            if sal_t_sillas != "" and sal_t_sillas != None:
                if sal_fk_cin_i != "" and sal_fk_cin_i != None:
                    sala_mod = modificar_sala(sal_i_id, sal_i_numero, sal_t_sillas, )
                    if sala_mod != None:
                        response_body["message"] = "Sala modificada correctamente!"
                        response_body["data"] = sala_mod
                    else:
                        response_body["message"] = "La sala no existe"
                        response_body["errors"].append("Error al modificar sala")
                        status_code = HTTPStatus.BAD_REQUEST
                else:
                    response_body["message"] = "Cine vacio"
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


