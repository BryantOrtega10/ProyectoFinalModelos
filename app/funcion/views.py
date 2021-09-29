from http import HTTPStatus
from flask import Blueprint, request, render_template, url_for, redirect
from app.funcion.models import crear_funcion, get_funciones, eliminar_funcion, modificar_funcion, funcion_por_id
from app.sala.models import get_salas
import copy
from flask_login import login_required

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": []}
funcion = Blueprint("funcion", __name__, url_prefix="/funcion")

@funcion.route("/template", methods=["GET"])
@login_required
def template():
    funciones = get_funciones()
    return render_template("funcion/index.html", funciones = funciones)

@funcion.route("/agregar", methods=["POST","GET"])
@login_required
def agregar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if request.method == "POST":
        if not "fun_fk_sal_i" in request.json: 
            response_body["errors"].append("Debe escoger una sala")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        if not "fun_fk_pel_i" in request.json: 
            response_body["errors"].append("Debe escoger una pelicula")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        fun_dt_fecha_hora = request.json["fun_dt_fecha_hora"]
        fun_fk_sal_i = request.json["fun_fk_sal_i"]
        fun_fk_pel_i = request.json["fun_fk_pel_i"]

        if fun_dt_fecha_hora == "":
            response_body["errors"].append("Campo de fecha requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        elif fun_fk_sal_i == "":
            response_body["errors"].append("Debe escoger una sala")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        elif fun_fk_pel_i == "":
            response_body["errors"].append("Debe escoger una sala")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        else:
            funcion = crear_funcion(fun_dt_fecha_hora, fun_fk_sal_i, fun_fk_pel_i)
            response_body["data"] = {"funcion": funcion, "redirect": url_for('funcion.template')}
            response_body["message"] = "Funcion creado correctamente"
        return response_body, status_code
    else:
        salas = get_salas()
        return render_template('cine/agregar.html', salas = salas)

@funcion.route("/editar/<id_funcion>", methods=["POST","GET"])
@login_required
def editar(id_funcion):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if request.method == "POST":
        if not "fun_dt_fecha_hora" in request.json: 
            response_body["errors"].append("Campo de fecha requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        fun_dt_fecha_hora = request.json["fun_dt_fecha_hora"]

        if fun_dt_fecha_hora == "":
            response_body["errors"].append("Campo de fecha requerido")
            status_code = HTTPStatus.BAD_REQUEST
        else:
            funcion = modificar_funcion(id_funcion, fun_dt_fecha_hora)
            response_body["data"] = {"funcion": funcion, "redirect": url_for('funcion.template')}
            response_body["message"] = "Cine editado correctamente"
        return response_body, status_code
    else:
        funcion = funcion_por_id(id_funcion)
        return render_template('cine/editar.html', funcion = funcion)

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