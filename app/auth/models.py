from datetime import datetime
from app.db import db, ma
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usr_v_correo = db.Column(db.String(100), unique=True)
    usr_v_pass = db.Column(db.String(100))
    usr_i_rol = db.Column(db.Integer, default=2)


def crear_usuario(usr_v_correo, usr_v_pass, usr_i_rol):
    usuario = Usuario(usr_v_correo=usr_v_correo, usr_v_pass=generate_password_hash(usr_v_pass, method="sha256"), usr_i_rol = usr_i_rol)
    db.session.add(usuario)
    db.session.commit()
    return usuario


def obtener_usuario_por_correo(usr_v_correo):
    usuario = Usuario.query.filter_by(
            usr_v_correo=usr_v_correo
        ).first()
    return usuario


def obtener_usuario_por_correo_password(usr_v_correo, usr_v_pass):
    usuario = obtener_usuario_por_correo(usr_v_correo)
    if not usuario or not check_password_hash(usuario.usr_v_pass, usr_v_pass):
        return None
    return usuario
