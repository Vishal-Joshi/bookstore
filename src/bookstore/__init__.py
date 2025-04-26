from flask import Flask

from .config import Config
from .extensions import db


def create_app(config_object=None):
    app = Flask(__name__)
    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .books import book_bp
    app.register_blueprint(book_bp)
    return app
