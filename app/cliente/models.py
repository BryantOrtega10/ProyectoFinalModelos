import uuid

from app.db import db, ma

class Cliente(db.Model):
    cli_i_cedula = db.Column(db.BigInteger, primary_key=True)
    cli_v_nombre = db.Column(db.String(100), nullable=False)
    cli_v_foto = db.Column(db.String(200), nullable=True)
    cli_d_fecha_nacimiento = db.Column(db.Date, nullable=False)
    cli_fk_ciu_i = db.Column(db.Integer, db.ForeignKey("ciudad.ciu_i_id"))
    cli_fk_usr_i = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    cli_v_token = db.Column(db.String(100), nullable=True)

class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        fields = ["cli_i_cedula","cli_v_nombre", "cli_v_foto","cli_d_fecha_nacimiento","cli_fk_ciu_i","cli_fk_usr_i", "cli_v_token"]


def obtener_cliente_por_token(cli_v_token):
    cliente = Cliente.query.filter_by(cli_v_token=cli_v_token).first()
    if cliente != None:
        cliente_schema = ClienteSchema()
        cliente = cliente_schema.dump(cliente)
        return cliente
    return None


def obtener_cliente_por_usuario(cli_fk_usr_i):
    cliente = Cliente.query.filter_by(cli_fk_usr_i=cli_fk_usr_i).first()
    if cliente != None:
        token = str(uuid.uuid4())
        cliente.cli_v_token = token
        db.session.commit()
        cliente_schema = ClienteSchema()
        cliente = cliente_schema.dump(cliente)
        return cliente
    return None

def get_clientes():
    clientes = Cliente.query.all()
    cliente_schema = ClienteSchema()
    clientes = [cliente_schema.dump(cliente) for cliente in clientes]
    return clientes


def existe_cliente_por_cedula(cli_i_cedula):
    cliente = Cliente.query.filter_by(cli_i_cedula=cli_i_cedula).first()
    if cliente != None:
        return True
    else:
        return False

def crear_cliente(cedula,nombre,fecha,fk_ciu,fk_usr, token):
    cliente = Cliente(cli_i_cedula=cedula,cli_v_nombre=nombre,cli_d_fecha_nacimiento=fecha,cli_fk_ciu_i=fk_ciu,cli_fk_usr_i=fk_usr, cli_v_token=token)
    db.session.add(cliente)
    db.session.commit()
    cliente_schema = ClienteSchema()
    return cliente_schema.dump(cliente)

def eliminar_cliente(id):
    cliente = Cliente.query.filter_by(cli_i_cedula=id).first()
    if cliente != None:
        Cliente.query.filter_by(cli_i_cedula=id).delete()
        db.session.commit()
        return True
    else:
        return False

def modificar_cliente(cedula,nombre,foto,fecha):
    cliente = Cliente.query.filter_by(cli_i_cedula=id).first()
    if cliente != None:
        cliente.cli_v_nombre = nombre
        cliente.cli_v_foto = foto
        cliente.cli_d_fecha_nacimiento = fecha
        db.session.commit()
        cliente_schema = ClienteSchema()
        return cliente_schema.dump(cliente)
    return None
