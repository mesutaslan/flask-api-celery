# -*- coding: utf-8 -*-
"""The app factory."""
from flask import Flask
from flask_restful import Api
from flask import Blueprint
from myapp.settings import ProdConfig
from myapp.exceptions import InvalidUsage


def create_app(config_object=ProdConfig):

    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_endpoints(app)
    register_errorhandlers(app)
    return app


def register_endpoints(app):
    """Register Flask blueprints."""
    api_blue_print = Blueprint('api', __name__)
    api = Api(api_blue_print)
    app.register_blueprint(api_blue_print, url_prefix='/api')


def register_errorhandlers(app):

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)