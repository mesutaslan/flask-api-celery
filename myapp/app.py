# -*- coding: utf-8 -*-
"""The app factory."""
from flask import Flask
from flask_restful import Api
from flask import Blueprint
from myapp.settings import DevConfig
from myapp.exceptions import InvalidUsage
from myapp.contacts.resources import ContactResource, ContactItemResource, ContactByUsernameResource
from myapp.extentions import db, migrate, cache


def create_app(config_object=DevConfig):

    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_endpoints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)


def register_endpoints(app):
    """Register Flask blueprints."""
    api_blue_print = Blueprint('api', __name__)
    api = Api(api_blue_print)
    app.register_blueprint(api_blue_print, url_prefix='/api')
    api.add_resource(ContactResource, '/contacts', endpoint='contacts')
    api.add_resource(ContactItemResource, '/contacts/<int:contact_id>', endpoint='contact')
    api.add_resource(ContactByUsernameResource, '/contacts/<string:username>', endpoint='contactByUsername')


def register_errorhandlers(app):

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)
