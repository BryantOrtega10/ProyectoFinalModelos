from app.db import db, ma


class Actor(db.Model):
    act_i_id = db.Column(db.Integer, primary_key=True)
    act_v_nombre = db.Column(db.String(45), nullable=False)
    act_v_apellido = db.Column(db.String(45), nullable=False)

class ActorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Actor
        fields = ["act_i_id", "act_v_nombre", "act_v_apellido"]


def obtener_actores():
    actores = Actor.query.all()
    actor_schema = ActorSchema()
    actores = [actor_schema.dump(actor) for actor in actores]
    return actores


def obtener_actor_por_id(act_i_id):
    actor = Actor.query.filter_by(act_i_id=act_i_id).first()
    if actor != None:
        actor_schema = ActorSchema()
        actor = actor_schema.dump(actor)
        return actor
    else:
        return None



def crear_actor(nombre, apellido):
    actor = Actor(act_v_nombre=nombre, act_v_apellido=apellido)
    db.session.add(actor)
    db.session.commit()
    actor_schema = ActorSchema()
    return actor_schema.dump(actor)


def eliminar_actor(id):
    actor = Actor.query.filter_by(act_i_id=id).first()
    if actor != None:
        Actor.query.filter_by(act_i_id=id).delete()
        db.session.commit()
        return True
    else:
        return False


def modificar_actor(id, nombre, apellido):
    actor = Actor.query.filter_by(act_i_id=id).first()
    if actor != None:
        actor.act_v_nombre = nombre
        actor.act_v_apellido = apellido
        db.session.commit()
        actor_schema = ActorSchema()
        return actor_schema.dump(actor)
    return None
