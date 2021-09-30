from flask_sqlalchemy import model
from marshmallow import Schema, fields

from app.cine.models import Cine, CineSchema
from app.db import db, ma

class Sala(db.Model):
    sal_i_id = db.Column(db.Integer, primary_key=True)
    sal_i_numero = db.Column(db.SMALLINT, nullable=False)
    sal_t_sillas = db.Column(db.Text, nullable=False)
    sal_fk_cin_i = db.Column(db.Integer, db.ForeignKey("cine.cin_i_id"))

class SalaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sala
        fields = ["sal_i_id", "sal_i_numero", "sal_t_sillas", "sal_fk_cin_i"]


def get_salas_con_cine():
    dupla_sala_cine = db.session.query(Sala,Cine) \
        .filter(Cine.cin_i_id==Sala.sal_fk_cin_i)\
        .order_by(Cine.cin_v_nombre.asc()) \
        .all()

    sala_schema = SalaSchema()
    cine_schema = CineSchema()
    dupla_sala_cine = [(sala_schema.dump(sala),cine_schema.dump(cine)) for (sala,cine) in dupla_sala_cine]
    return dupla_sala_cine

def get_salas():
    salas = Sala.query.all()
    sala_schema = SalaSchema()
    salas = [sala_schema.dump(sala) for sala in salas]
    return salas

def crear_sala(num_sillas, texto, fk_cine):
    sala = Sala(sal_i_numero=num_sillas, sal_t_sillas=texto, sal_fk_cin_i=fk_cine)
    db.session.add(sala)
    db.session.commit()
    sala_schema = SalaSchema()
    return sala_schema.dump(sala)

def eliminar_sala(id):
    sala = Sala.query.filter_by(sal_i_id=id).first()
    if sala != None:
        Sala.query.filter_by(sal_i_id=id).delete()
        db.session.commit()
        return True
    else:
        return False

def modificar_sala(id, num_sillas, texto, cine):
    sala = Sala.query.filter_by(sal_i_id=id).first()
    if sala != None:
        sala.sal_i_numero = num_sillas
        sala.sal_t_sillas = texto
        sala.sal_fk_cin_i = cine
        db.session.commit()
        sala_schema = SalaSchema()
        return sala_schema.dump(sala)
    return None

def obtener_sala_por_id(id):
    sala = Sala.query.filter_by(sal_i_id=id).first()
    if sala != None:
        sala_schema = SalaSchema()
        return sala_schema.dump(sala)
    else:
        return None
