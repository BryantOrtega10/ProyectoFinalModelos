from http import HTTPStatus
from flask import Blueprint, request, url_for

RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}
cliente = Blueprint("cliente", __name__, url_prefix="/cliente")


@cliente.route("/registrar", methods=["POST"])
def registrar():
    status_code = HTTPStatus.OK
    return RESPONSE_BODY, status_code
