from app.db import db, ma
from app.cine.models import Cine, CineSchema
from app.sala.models import Sala, SalaSchema


class Funcion(db.Model):
    fun_i_id = db.Column(db.Integer, primary_key=True)
    fun_dt_fecha_hora = db.Column(db.DateTime, nullable = False)
    fun_fk_sal_i = db.Column(db.Integer, db.ForeignKey("sala.sal_i_id"))
    fun_fk_pel_i = db.Column(db.Integer, db.ForeignKey("pelicula.pel_i_id"))

class FuncionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Funcion
        fields = ["fun_i_id", "fun_dt_fecha_hora", "fun_fk_sal_i", "fun_fk_pel_i"]

def get_funciones():
    funciones = Funcion.query.all()
    funcion_schema = FuncionSchema()
    funciones = [funcion_schema.dump(funcion) for funcion in funciones]
    return funciones

def crear_funcion(fecha, fk_sala, fk_peli):
    funcion = Funcion(fun_dt_fecha_hora=fecha, fun_fk_sal_i=fk_sala, fun_fk_pel_i=fk_peli)
    db.session.add(funcion)
    db.session.commit()
    funcion_schema = FuncionSchema()
    return funcion_schema.dump(funcion)

def eliminar_funcion(id):
    funcion = Funcion.query.filter_by(fun_i_id=id).first()
    if funcion != None:
        Funcion.query.filter_by(fun_i_id=id).delete()
        db.session.commit()
        return True
    else:
        return False

def modificar_funcion(id, fecha):
    funcion = Funcion.query.filter_by(fun_i_id=id).first()
    if funcion != None:
        funcion.fun_dt_fecha_hora = fecha
        db.session.commit()
        funcion_schema = FuncionSchema()
        return funcion_schema.dump(funcion)
    return None

def funcion_por_id(id):
    funcion = Funcion.query.filter_by(fun_i_id=id).first()
    if funcion != None:
        funcion_schema = FuncionSchema()
        return funcion_schema.dump(funcion)
    return None

def funcion_ciudad( fun_fk_pel_i, cin_fk_ciu):
    resultado = db.session.query(Funcion, Cine) \
    .join(Sala, Sala.sal_i_id==Funcion.fun_fk_sal_i)\
    .filter(Cine.cin_i_id==Sala.sal_fk_cin_i)\
    .filter(Cine.cin_fk_ciu==cin_fk_ciu)\
    .filter(Funcion.fun_fk_pel_i==fun_fk_pel_i).all()
    funcion_schema = FuncionSchema()
    cine_schema = CineSchema()

    resultado = [(funcion_schema.dump(funcion), cine_schema.dump(cine))  for (funcion, cine) in resultado]
    return resultado



