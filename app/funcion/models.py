from app.db import db, ma

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
    funcion = Funcion(fun_dt_fecha_hora=fecha, fun_fk_sal_i=fk_sala, fun_fk_pel_i=fk_sala)
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

