from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required



pelicula = Blueprint("pelicula", __name__, url_prefix="/pelicula")

RESPONSE_BODY_DEFAULT = {"message": "", "data": [], "errors": [], "metadata": []}


@pelicula.route("/", methods=["GET"])
@login_required
def index():
    return render_template('pelicula/index.html')


@pelicula.route("/agregar", methods=["POST","GET"])
@login_required
def agregar():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        return 'modificacion exitosa'
    else:
        return render_template('pelicula/index.html')
