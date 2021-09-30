from app.db import db, ma


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


class PeliculaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pelicula
        fields = ["pel_i_id", "pel_v_titulo", "pel_t_sinopsis", "pel_v_director",
                  "pel_i_duracion", "pel_d_estreno", "pel_v_ruta_poster",
                  "pel_v_ruta_banner", "pel_v_pais_origen", "pel_i_edad_minima"]


class PeliculaGenero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fk_pel_i_id = db.Column(db.Integer, db.ForeignKey("pelicula.pel_i_id"))
    fk_gen_i_id = db.Column(db.Integer, db.ForeignKey("genero.gen_i_id"))


class PeliculaActor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fk_pel_i_id = db.Column(db.Integer, db.ForeignKey("pelicula.pel_i_id"))
    fk_act_i_id = db.Column(db.Integer, db.ForeignKey("actor.act_i_id"))


def obtener_generos():
    generos = Pelicula.query.all()
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


def obtener_peliculas():
    peliculas = Pelicula.query.all()
    pelicula_schema = PeliculaSchema()
    peliculas = [pelicula_schema.dump(pelicula) for pelicula in peliculas]
    return peliculas


def crear_pelicula(titulo, sinopsis, director, duracion, estreno, ruta_poster, ruta_banner, pais_origen, edad_minima):
    pelicula = Pelicula(pel_v_titulo=titulo, pel_t_sinopsis=sinopsis, pel_v_director=director,
                        pel_i_duracion=duracion, pel_d_estreno=estreno, pel_v_ruta_poster=ruta_poster,
                        pel_v_ruta_banner=ruta_banner, pel_v_pais_origen=pais_origen, pel_i_edad_minima=edad_minima)
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


def modificar_pelicula(id, titulo, sinopsis, director, duracion, estreno, ruta_poster, ruta_banner, pais_origen, edad_minima):
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
        db.session.commit()
        pelicula_schema = PeliculaSchema()
        return pelicula_schema.dump(pelicula)
    return None
