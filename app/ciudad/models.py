from app.db import db, ma


class Ciudad(db.Model):
    ciu_i_id = db.Column(db.Integer, primary_key=True)
    ciu_v_nombre = db.Column(db.String(50), nullable=False)


class CiudadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ciudad
        fields = ["ciu_i_id", "ciu_v_nombre"]


def get_ciudades():
    ciudades = Ciudad.query.all()
    ciudad_schema = CiudadSchema()
    ciudades = [ciudad_schema.dump(ciudad) for ciudad in ciudades]
    return ciudades


def crear_ciudad(nombre):
    ciudad = Ciudad(ciu_v_nombre=nombre)
    db.session.add(ciudad)
    db.session.commit()
    ciudad_schema = CiudadSchema()
    return ciudad_schema.dump(ciudad)


def eliminar_ciudad(id):
    ciudad = Ciudad.query.filter_by(ciu_i_id=id).first()
    print(ciudad)
    if ciudad != None:
        Ciudad.query.filter_by(ciu_i_id=id).delete()
        db.session.commit()
        return True
    else:
        return False


def modificar_ciudad(id, nombre):
    ciudad = Ciudad.query.filter_by(ciu_i_id=id).first()
    if ciudad != None:
        ciudad.ciu_v_nombre = nombre
        db.session.commit()
        ciudad_schema = CiudadSchema()
        return ciudad_schema.dump(ciudad)
    return None

def ciudad_por_id(id):
    ciudad = Ciudad.query.filter_by(ciu_i_id=id).first()
    if ciudad != None:
        ciudad_schema = CiudadSchema()
        return ciudad_schema.dump(ciudad)
    return None