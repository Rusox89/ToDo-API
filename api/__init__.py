""" Main entrypoint """
from flask import Flask, request, abort
from api.models import initialize_database
from config import CURRENT_CONFIG
from api.auth import auth


def create_app():
    """ Creates the app """
    app = Flask(__name__)
    app.config.from_object(CURRENT_CONFIG)
    app.register_blueprint(auth)

    @app.before_request
    def only_json():
        if not request.is_json:
            abort(400)

    initialize_database()
    return app
