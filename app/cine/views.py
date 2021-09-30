from http import HTTPStatus
from flask import Blueprint, request, render_template, url_for, redirect
from app.cine.models import crear_cine, get_cines, eliminar_cine, modificar_cine, cine_por_id
from app.ciudad.models import get_ciudades
import copy
from flask_login import login_required

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": []}
cine = Blueprint("cine", __name__, url_prefix="/cine")

@cine.route("/template", methods=["GET"])
@login_required
def template():
    cines = get_cines()
    return render_template("cine/index.html", cines = cines)

@cine.route("/agregar", methods=["POST","GET"])
@login_required
def agregar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if request.method == "POST":
        if not "cin_v_nombre" in request.json: 
            response_body["errors"].append("Campo nombre es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code  
        if not "cin_fk_ciu" in request.json:
            response_body["errors"].append("Debe escoger una ciudad")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code   

        cin_v_nombre = request.json["cin_v_nombre"]
        cin_fk_ciu = request.json["cin_fk_ciu"]

        if cin_v_nombre == "":
            response_body["errors"].append("Campo nombre es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        if cin_fk_ciu == "":
            response_body["errors"].append("Debe escoger una ciudad")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        else:
            cine = crear_cine(cin_v_nombre, cin_fk_ciu)
            response_body["data"] = {"cine": cine, "redirect": url_for('cine.template')}
            response_body["message"] = "Cine creado correctamente"
        return response_body, status_code
    else:
        ciudades = get_ciudades()
        return render_template('cine/agregar.html', ciudades = ciudades)

@cine.route("/editar/<id_cine>", methods=["POST","GET"])
@login_required
def editar(id_cine):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if request.method == "POST":
        if not "cin_v_nombre" in request.json: 
            response_body["errors"].append("Campo nombre es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code

        cin_v_nombre = request.json["cin_v_nombre"]
        if cin_v_nombre == "":
            response_body["errors"].append("Campo nombre es requerido")
            status_code = HTTPStatus.BAD_REQUEST
            return response_body, status_code
        else:
            cine = modificar_cine(id_cine, cin_v_nombre)
            response_body["data"] = {"cine": cine, "redirect": url_for('cine.template')}
            response_body["message"] = "Cine editado correctamente"
        return response_body, status_code
    else:
        cine = cine_por_id(id_cine)
        return render_template('cine/editar.html', cine = cine)

@cine.route("/quitar/<id_cine>", methods=["GET"])
@login_required
def quitar(id_cine):
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    if eliminar_cine(id_cine):
        response_body["data"] = {"cine": cine, "redirect": url_for('cine.template')}
        response_body["message"] = "Cine eliminado correctamente"
    else:
        response_body["errors"].append("El cine no existe")
        status_code = HTTPStatus.BAD_REQUEST

    return redirect(url_for('cine.template'))

@cine.route("/", methods=["GET"])
def index():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    cines = get_cines()
    response_body["message"] = "Cines consultados correctamente!"
    response_body["data"] = cines
    return response_body, status_code

@cine.route("/crear", methods=["POST"])
def crear():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK
    cin_v_nombre = request.json["cin_v_nombre"]
    cin_fk_ciu = request.json["cin_fk_ciu"]

    if cin_v_nombre != "" and cin_v_nombre != None:
        if cin_fk_ciu != "" and cin_fk_ciu != None:
            cine = crear_cine(cin_v_nombre, cin_fk_ciu)

            response_body["message"] = "Cine creado correctamente!"
            response_body["data"] = cine
        else:
            response_body["errors"].append("Nombre vacio")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["errors"].append("fk vacia")
        status_code = HTTPStatus.BAD_REQUEST
    
    return response_body, status_code

@cine.route("/modificar", methods=["PUT"])
def modificar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK

    cin_i_id = request.json["cin_i_id"]
    cin_v_nombre = request.json["cin_v_nombre"]
    
    if cin_i_id != "" and cin_i_id != None:
        if cin_v_nombre != "" and cin_v_nombre != None:
            cine_mod = modificar_cine(cin_i_id, cin_v_nombre)
            if cine_mod != None:
                response_body["message"] = "Cine modificado correctamente!"
                response_body["data"] = cine_mod
            else:
                response_body["message"] = "No se encontro el cine"
                response_body["errors"].append("Error al modificar cine")
                status_code = HTTPStatus.BAD_REQUEST
        else:
            response_body["message"] = "Nombre vacio"
            response_body["errors"].append("Error al modificar cine")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["message"] = "ID vacio"
        response_body["errors"].append("Error al modificar cine")
        status_code = HTTPStatus.BAD_REQUEST

    return response_body, status_code
    
@cine.route("/eliminar", methods=["DELETE"])
def eliminar():
    response_body = copy.deepcopy(RESPONSE_BODY_DEFAULT)
    status_code = HTTPStatus.OK

    cin_i_id = request.json["cin_i_id"]

    if cin_i_id != "" and cin_i_id != None:
        if eliminar_cine(cin_i_id):
            response_body["message"] = "Cine eliminado correctamente!"
        else:
            response_body["message"] = "Error no se encuentra el cine"
            response_body["errors"].append("Error al eliminar el cine")
            status_code = HTTPStatus.BAD_REQUEST
    else:
        response_body["message"] = "Id vacio"
        response_body["errors"].append("Error al eliminar el cine")
        status_code = HTTPStatus.BAD_REQUEST
    
    return response_body, status_code