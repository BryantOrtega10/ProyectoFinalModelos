from app.db import db, ma

class Reserva(db.Model):
    res_i_id = db.Column(db.Integer, primary_key=True)
    res_t_sillas = db.Column(db.Text, nullable=False)
    res_i_modo_pago = db.Column(db.Integer, nullable=False)
    res_i_estado = db.Column(db.Integer, nullable=False)
    res_fk_fun_i = db.Column(db.Integer, db.ForeignKey("funcion.fun_i_id"))
    res_fk_cli_i = db.Column(db.Integer, db.ForeignKey("cliente.cli_i_cedula"))

class ReservaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reserva
        fileds = ["res_i_id", "res_t_sillas", "res_i_modo_pago", "res_i_estado", "res_fk_fun_i", "res_fk_cli_i"]

def get_reservas():
    reservas = Reserva.query.all()
    reserva_schema = ReservaSchema()
    reservas = [reserva_schema.dump(reserva) for reserva in reservas]
    return reservas

def crear_reserva(sillas, modo_pago, estado, fk_funcion, fk_cliente):
    reserva = Reserva(res_t_sillas=sillas, res_i_modo_pago=modo_pago, res_i_estado=estado, res_fk_fun_i=fk_funcion, res_fk_cli_i=fk_cliente)
    db.session.add(reserva)
    db.session.commit()
    reserva_schema = ReservaSchema()
    return reserva_schema.dump(reserva)

def eliminar_reserva(id):
    reserva = Reserva.filter_by(res_i_id=id).first()
    if reserva != None:
        Reserva.filter_by(res_i_id=id).delete()
        db.session.commit()
        return True
    else:
        return False

def modificar_reserva(id, sillas, modo_pago, estado):
    reserva = Reserva.filter_by(res_i_id=id).first()
    if reserva != None:
        reserva.res_i_id = id
        reserva.res_t_sillas = sillas
        reserva.res_i_modo_pago = modo_pago
        reserva.res_i_estado = estado
        db.session.commit()
        reserva_schema = ReservaSchema()
        return reserva_schema.dump(reserva)
    return None

def obtener_reservas_por_funcion(fun_i_id):
    reservas = Reserva.query.filter_by( res_fk_fun_i=fun_i_id).all()
    reserva_schema = ReservaSchema()
    reservas = reservas = [reserva_schema.dump(reserva) for reserva in reservas]
    return reservas