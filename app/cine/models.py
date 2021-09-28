from app.db import db, ma

class Cine(db.Model):
    cin_i_id = db.Column(db.Integer, primary_key=True)
    cin_v_nombre = db.Column(db.String(100), nullable=False)
    cin_fk_ciu = db.Column(db.Integer, db.ForeignKey("ciudad.ciu_i_id "))


class CineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cine
        fields = ["cin_i_id", "cin_v_nombre", "cin_fk_ciu"]

def obtener_cines_por_ciudad(ciu_i_id):
    cines = Cine.filter_by(cin_fk_ciu=ciu_i_id).all()
    cine_schema = CineSchema()
    cines = [cine_schema.dump(cine) for cine in cines]
    return cines


def get_cines():
    cines = Cine.query.all()
    cine_schema = CineSchema()
    cines = [cine_schema.dump(cine) for cine in cines]
    return cines

def crear_cine(nombre, fk_ciu):
    cine = Cine(cin_v_nombre = nombre, cin_fk_ciu= fk_ciu)
    db.session.add(cine)
    db.session.commit()
    cine_schema = CineSchema()
    return cine_schema.dump(cine)

def eliminar_cine(id):
    cine = Cine.filter_by(cin_i_id=id).first()
    if cine != None:
        Cine.filter_by(cin_i_id=id).delete()
        db.session.commit()
        return True
    else:
        return False

def modificar_cine(id, nombre):
    cine = Cine.filter_by(cin_i_id=id).first()
    if cine != None:
        cine.cin_v_nombre = nombre
        db.session.commit()
        cine_schema = CineSchema()
        return cine_schema.dump(cine)
    return None
