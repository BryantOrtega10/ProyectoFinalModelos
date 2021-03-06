from app.actor.models import Actor, ActorSchema
from app.cine.models import Cine
from app.db import db, ma
from app.funcion.models import Funcion, FuncionSchema
from app.reserva.models import Reserva
from app.sala.models import Sala


class Genero(db.Model):
    gen_i_id = db.Column(db.Integer, primary_key=True)
    gen_v_nombre = db.Column(db.String(45), nullable=False)


class GeneroSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genero
        fields = ["gen_i_id", "gen_v_nombre"]


class Pelicula(db.Model):
    pel_i_id = db.Column(db.Integer, primary_key=True)
    pel_v_titulo = db.Column(db.String(100), nullable=False)
    pel_t_sinopsis = db.Column(db.String(400))
    pel_v_director = db.Column(db.String(45), nullable=False)
    pel_i_duracion = db.Column(db.Integer, nullable=False)
    pel_d_estreno = db.Column(db.Date, nullable=False)
    pel_v_ruta_poster = db.Column(db.String(200), nullable=False)
    pel_v_ruta_banner = db.Column(db.String(200), nullable=False)
    pel_v_pais_origen = db.Column(db.String(45), nullable=False)
    pel_i_edad_minima = db.Column(db.Integer, nullable=False)
    pel_i_estado = db.Column(db.Integer, nullable=False)


class PeliculaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pelicula
        fields = ["pel_i_id", "pel_v_titulo", "pel_t_sinopsis", "pel_v_director",
                  "pel_i_duracion", "pel_d_estreno", "pel_v_ruta_poster",
                  "pel_v_ruta_banner", "pel_v_pais_origen", "pel_i_edad_minima","pel_i_estado"]


class PeliculaGenero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fk_pel_i_id = db.Column(db.Integer, db.ForeignKey("pelicula.pel_i_id"))
    fk_gen_i_id = db.Column(db.Integer, db.ForeignKey("genero.gen_i_id"))


class PeliculaActor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fk_pel_i_id = db.Column(db.Integer, db.ForeignKey("pelicula.pel_i_id"))
    fk_act_i_id = db.Column(db.Integer, db.ForeignKey("actor.act_i_id"))


def obtener_generos():
    generos = Genero.query.all()
    genero_schema = GeneroSchema()
    generos = [genero_schema.dump(genero) for genero in generos]
    return generos


def crear_genero(nombre):
    genero = Genero(gen_v_nombre=nombre)
    db.session.add(genero)
    db.session.commit()
    genero_schema = GeneroSchema()
    return genero_schema.dump(genero)


def crear_pelicula_genero(pel_i_id, gen_i_id):
    pel_genero = PeliculaGenero(fk_pel_i_id=pel_i_id, fk_gen_i_id=gen_i_id)
    db.session.add(pel_genero)
    db.session.commit()
    return True


def eliminar_pelicula_genero(pel_i_id):
    PeliculaGenero.query.filter_by(fk_pel_i_id=pel_i_id).delete()
    db.session.commit()
    return True


def crear_pelicula_actor(pel_i_id, act_i_id):
    pel_actor = PeliculaActor(fk_pel_i_id=pel_i_id, fk_act_i_id=act_i_id)
    db.session.add(pel_actor)
    db.session.commit()
    return True


def eliminar_pelicula_actor(pel_i_id):
    PeliculaActor.query.filter_by(fk_pel_i_id=pel_i_id).delete()
    db.session.commit()
    return True


def cuenta_peliculas_por_actor(act_i_id):
    peliculas = PeliculaActor.query.filter_by(fk_act_i_id=act_i_id).count()
    return peliculas


def cuenta_funciones_por_pelicula(pel_i_id):
    funciones = Funcion.query.filter_by(fun_fk_pel_i=pel_i_id).count()
    return funciones




def obtener_actores_por_pelicula(pel_i_id):
    actores = db.session.query(Actor) \
    .join(PeliculaActor, PeliculaActor.fk_act_i_id==Actor.act_i_id)\
    .filter(PeliculaActor.fk_pel_i_id==pel_i_id).all()

    actor_schema = ActorSchema()
    actores = [actor_schema.dump(actor) for actor in actores]
    return actores


def obtener_generos_por_pelicula(pel_i_id):
    generos = db.session.query(Genero) \
    .join(PeliculaGenero, PeliculaGenero.fk_gen_i_id==Genero.gen_i_id)\
    .filter(PeliculaGenero.fk_pel_i_id==pel_i_id).all()

    genero_schema = GeneroSchema()
    generos = [genero_schema.dump(genero) for genero in generos]
    return generos


def obtener_peliculas():
    peliculas = Pelicula.query.all()
    pelicula_schema = PeliculaSchema()
    peliculas = [pelicula_schema.dump(pelicula) for pelicula in peliculas]
    for p in peliculas:
        p["generos"] = obtener_generos_por_pelicula(p["pel_i_id"])
        p["actores"] = obtener_actores_por_pelicula(p["pel_i_id"])
    return peliculas


def crear_pelicula(titulo, sinopsis, director, duracion, estreno, ruta_poster, ruta_banner, pais_origen, edad_minima, estado):
    pelicula = Pelicula(pel_v_titulo=titulo, pel_t_sinopsis=sinopsis, pel_v_director=director,
                        pel_i_duracion=duracion, pel_d_estreno=estreno, pel_v_ruta_poster=ruta_poster,
                        pel_v_ruta_banner=ruta_banner, pel_v_pais_origen=pais_origen, pel_i_edad_minima=edad_minima, pel_i_estado=estado)
    db.session.add(pelicula)
    db.session.commit()
    pelicula_schema = PeliculaSchema()
    return pelicula_schema.dump(pelicula)


def eliminar_pelicula(id):
    pelicula = Pelicula.query.filter_by(pel_i_id=id).first()
    if pelicula != None:
        Pelicula.query.filter_by(pel_i_id=id).delete()
        db.session.commit()
        return True
    else:
        return False


def modificar_pelicula(id, titulo, sinopsis, director, duracion, estreno, ruta_poster, ruta_banner, pais_origen, edad_minima, estado):
    pelicula = Pelicula.query.filter_by(pel_i_id=id).first()
    if pelicula != None:
        pelicula.pel_v_titulo = titulo
        pelicula.pel_t_sinopsis = sinopsis
        pelicula.pel_v_director = director
        pelicula.pel_i_duracion = duracion
        pelicula.pel_d_estreno = estreno
        pelicula.pel_v_ruta_poster = ruta_poster
        pelicula.pel_v_ruta_banner = ruta_banner
        pelicula.pel_v_pais_origen = pais_origen
        pelicula.pel_i_edad_minima = edad_minima
        pelicula.pel_i_estado = estado
        db.session.commit()
        pelicula_schema = PeliculaSchema()
        return pelicula_schema.dump(pelicula)
    return None


def obtener_pelicula_por_id(pel_i_id):
    pelicula = Pelicula.query.filter_by(pel_i_id=pel_i_id).first()
    if pelicula != None:
        pelicula_schema = PeliculaSchema()
        pelicula = pelicula_schema.dump(pelicula)
        return pelicula
    else:
        return None

def get_funciones_con_pelicula():
    dupla_funcion_pelicula = db.session.query(Funcion,Pelicula) \
    .filter(Pelicula.pel_i_id==Funcion.fun_fk_pel_i)\
    .order_by(Pelicula.pel_v_titulo.asc()).all()
    funcion_schema = FuncionSchema()
    pelicula_schema = PeliculaSchema()
    dupla_funcion_pelicula = [(funcion_schema.dump(funcion),pelicula_schema.dump(pelicula)) for (funcion,pelicula) in dupla_funcion_pelicula]
    return dupla_funcion_pelicula


def obtener_peliculas_en_cartelera_por_ciudad(ciudad):

    peliculas =  db.session.query(Pelicula) \
    .join(Funcion, Pelicula.pel_i_id == Funcion.fun_fk_pel_i)\
    .join(Sala, Funcion.fun_fk_sal_i == Sala.sal_i_id)\
    .join(Cine, Sala.sal_fk_cin_i == Cine.cin_i_id)\
    .filter(Cine.cin_fk_ciu == ciudad)\
    .filter(Pelicula.pel_i_estado == 1)\
    .all()

    pelicula_schema = PeliculaSchema()

    peliculas = [pelicula_schema.dump(pelicula) for pelicula in peliculas]
    for p in peliculas:
        p["generos"] = obtener_generos_por_pelicula(p["pel_i_id"])
        p["actores"] = obtener_actores_por_pelicula(p["pel_i_id"])


    return peliculas


def obtener_peliculas_mas_vistas_por_ciudad(ciudad):

    peliculas = db.session.query(Pelicula) \
    .join(Funcion, Pelicula.pel_i_id == Funcion.fun_fk_pel_i)\
    .join(Sala, Funcion.fun_fk_sal_i == Sala.sal_i_id)\
    .join(Cine, Sala.sal_fk_cin_i == Cine.cin_i_id)\
    .filter(Pelicula.pel_i_estado == 1)\
    .filter(Cine.cin_fk_ciu == ciudad).all()

    pelicula_schema = PeliculaSchema()

    peliculas = [pelicula_schema.dump(pelicula) for pelicula in peliculas]
    for p in peliculas:
        p["generos"] = obtener_generos_por_pelicula(p["pel_i_id"])
        p["actores"] = obtener_actores_por_pelicula(p["pel_i_id"])

        reservas = db.session.query(Reserva) \
        .join(Funcion, Reserva.res_fk_fun_i == Funcion.fun_i_id)\
        .filter(Funcion.fun_fk_pel_i == p["pel_i_id"]).count()

        p["reservas"] = reservas

    peliculas = sorted(peliculas, key=lambda k: k['reservas'])
    return peliculas


def obtener_peliculas_por_estado(estado):

    peliculas =  db.session.query(Pelicula) \
    .filter(Pelicula.pel_i_estado == estado)\
    .all()

    pelicula_schema = PeliculaSchema()

    peliculas = [pelicula_schema.dump(pelicula) for pelicula in peliculas]
    for p in peliculas:
        p["generos"] = obtener_generos_por_pelicula(p["pel_i_id"])
        p["actores"] = obtener_actores_por_pelicula(p["pel_i_id"])


    return peliculas


def generos_por_cliente(cliente):
    generos = db.session.query(Genero) \
    .join(PeliculaGenero, PeliculaGenero.fk_gen_i_id==Genero.gen_i_id)\
    .join(Pelicula, Pelicula.pel_i_id == PeliculaGenero.fk_pel_i_id)\
    .join(Funcion, Pelicula.pel_i_id == Funcion.fun_fk_pel_i)\
    .join(Reserva, Funcion.fun_i_id == Reserva.res_fk_fun_i)\
    .filter(Reserva.res_fk_cli_i == cliente).all()

    generos_schema = GeneroSchema()
    generos = [generos_schema.dump(genero) for genero in generos]
    return generos
