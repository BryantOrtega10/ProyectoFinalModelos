from http import HTTPStatus
from flask import Blueprint, request, render_template, url_for, redirect
from app.funcion.models import crear_funcion, get_funciones, eliminar_funcion, modificar_funcion, funcion_por_id, funcion_ciudad
from app.sala.models import get_salas_con_cine
from app.reserva.models import obtener_reservas_por_funcion
from app.pelicula.models import obtener_peliculas, get_funciones_con_pelicula
import copy
from datetime import datetime
from flask_login import login_required

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": []}
funcion = Blueprint("funcion", __name__, url_prefix="/funcion")

@funcion.route("/template", methods=["GET"])
@login_required
def template():
    funciones = get_funciones_con_pelicula()
    return render_template("funcion/index.html", funciones = funciones)

@funcion.route("/agregar", methods=["POST","GET"])
@login_required
def agregar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if request.method == "POST":
        if not "fun_dt_fecha_hora" in request.json: 
            response_body["errors"].append("Campo de fecha requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        
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
        elif fun_fk_pel_i == "":
            response_body["errors"].append("Debe escoger una sala")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        elif fun_fk_sal_i == "":
            response_body["errors"].append("Debe escoger una sala")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
       
        else:
            fecha_hora=fun_dt_fecha_hora.split("T")
            fecha = fecha_hora[0].split("-")
            hora = fecha_hora[1].split(":")
            f_int = []
            f_int.extend([int(num) for num in fecha])
            f_int.extend([int(num) for num in hora])
            fecha_format = datetime(f_int[0], f_int[1], f_int[2], f_int[3], f_int[4])
            print(fun_fk_pel_i)
            funcion = crear_funcion(fecha_format, fun_fk_sal_i, fun_fk_pel_i)
            response_body["data"] = {"funcion": funcion, "redirect": url_for('funcion.template')}
            response_body["message"] = "Funcion creada correctamente"
        return response_body, status_code
    else:
        salas_cine = get_salas_con_cine()
        peliculas = obtener_peliculas()
        return render_template('funcion/agregar.html', salas_cine = salas_cine, peliculas = peliculas)

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
            fecha_hora=fun_dt_fecha_hora.split("T")
            fecha = fecha_hora[0].split("-")
            hora = fecha_hora[1].split(":")
            f_int = []
            f_int.extend([int(num) for num in fecha])
            f_int.extend([int(num) for num in hora])
            fecha_format = datetime(f_int[0], f_int[1], f_int[2], f_int[3], f_int[4])
            funcion = modificar_funcion(id_funcion, fecha_format)
            response_body["data"] = {"funcion": funcion, "redirect": url_for('funcion.template')}
            response_body["message"] = "Funcion editada correctamente"
        return response_body, status_code
    else:
        funcion = funcion_por_id(id_funcion)
        return render_template('funcion/editar.html', funcion = funcion)

@funcion.route("/quitar/<id_funcion>", methods=["GET"])
@login_required
def quitar(id_funcion):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if len(obtener_reservas_por_funcion(id_funcion)) == 0:
        if eliminar_funcion(id_funcion):
            response_body["data"] = {"funcion": funcion, "redirect": url_for('funcion.template')}
            response_body["message"] = "Funcion eliminada correctamente"
        else:
            response_body["errors"].append("La funcion no existe")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["errors"].append("La funcion tiene datos relacionados")
        status_code = HTTPStatus.BAD_REQUEST

    return redirect(url_for('funcion.template'))

@funcion.route("/obtener_por_ciudad", methods=["GET"])
def obtener_por_ciudad():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK

    fun_fk_pel_i  = request.json["fun_fk_pel_i"]
    cin_fk_ciu = request.json["cin_fk_ciu"]

    if fun_fk_pel_i != "" and fun_fk_pel_i != None:
        if  cin_fk_ciu != "" and  cin_fk_ciu != None:
            resultado = funcion_ciudad(fun_fk_pel_i, cin_fk_ciu)
            response_body["message"] = "Consulta realizada!"
            response_body["data"] = resultado
        else:
            response_body["errors"].append("FK ciudad vacia")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["errors"].append("FK pelicula vacia")
        status_code = HTTPStatus.BAD_REQUEST
    return response_body, status_code


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

    id_funcion = request.json["id_funcion"]
    fun_dt_fecha_hora = request.json["fun_dt_fecha_hora"]
    if id_funcion != "" and id_funcion != None:
        if fun_dt_fecha_hora != "" and fun_dt_fecha_hora != None:
            funcion_mod = modificar_funcion(id_funcion, fun_dt_fecha_hora)
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
    id_funcion = request.json["id_funcion"]
    if id_funcion != "" and id_funcion != None:
        if eliminar_funcion(id_funcion):
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
