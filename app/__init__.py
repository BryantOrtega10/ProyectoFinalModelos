from flask import Flask, redirect,url_for
from app.cliente.views import cliente
from app.ciudad.views import ciudad
from app.db import db, ma
from flask_migrate import Migrate
from conf.config import DevelpmentConfig

SERVICIOS = [('/cliente', cliente), ('/ciudad', ciudad)]

def create_app(config=DevelpmentConfig):
    app = Flask(__name__)
    migrate = Migrate(app, db)
    app.config.from_object(config)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    for url, blueprint in SERVICIOS:
        app.register_blueprint(blueprint, url_prefix=url)

    return app

if __name__ == "__main__":
    app_flask = create_app()
    app_flask.run()
