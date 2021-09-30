import os
from flask import Flask, redirect,url_for
from app.actor.views import actor
from app.auth.models import Usuario
from app.cliente.views import cliente
from app.ciudad.views import ciudad
from app.cine.views import cine
from app.funcion.views import funcion
from app.db import db, ma
from app.auth.views import auth
from app.pelicula.views import pelicula
from flask_migrate import Migrate
from conf.config import DevelpmentConfig
from flask_cors import CORS
from flask_login import LoginManager



ADMINISTRADOR = [('/', auth), ('/pelicula', pelicula), ('/actor', actor)]
SERVICIOS = [('/cliente', cliente), ('/ciudad', ciudad), ('/cine', cine), ('/funcion', funcion)]

def create_app(config=DevelpmentConfig):
    app = Flask(__name__)
    migrate = Migrate(app, db)
    app.config.from_object(config)


    CORS(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        print("here")
        return redirect(url_for("auth.login"))

    with app.app_context():
        db.create_all()

    for url, blueprint in ADMINISTRADOR:
        app.register_blueprint(blueprint, url_prefix=url)

    for url, blueprint in SERVICIOS:
        app.register_blueprint(blueprint, url_prefix=url)

    return app

if __name__ == "__main__":
    app_flask = create_app()
    app_flask.run()
