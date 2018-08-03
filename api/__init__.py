""" Main entrypoint """
from flask import Flask
from config import CURRENT_CONFIG


def create_app():
    """ Creates the app """
    app = Flask(__name__)
    app.config.from_object(CURRENT_CONFIG)

    return app
