from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

from . import auth
from .models import user
from .models import planet

import os

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Get confidential info from the instance folder
    app.config.from_pyfile('secrets.py')

    # Database configuration
    app.config["MONGO_URI"] = "mongodb://"+app.config['DATABASE_URL']+":"+app.config['DATABASE_PORT']+"/"+app.config['DATABASE_NAME']
    mongo = PyMongo(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Add blueprints
    app.register_blueprint(user.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(planet.bp)

    return app

