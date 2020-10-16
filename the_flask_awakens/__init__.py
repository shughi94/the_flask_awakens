from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

from . import auth
from .models import user

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

    # # a simple page that says hello
    # @app.route('/planet', methods=['GET'])
    # def getOnePlanet():
    #      # get collection
    #     planetsCollection = mongo.db.planets

    #     # find planet
    #     planet = planetsCollection.find_one({'name' : 'planet1'})
    #     if planet:
    #         output = {'name' : planet['name'], 'distance' : planet['distance']}
    #     else:
    #         output = "No such planet with that name"

    #     return jsonify({'result' : output})

    # @app.route('/planet', methods=['POST'])
    # def createPlanet():
    #     # get collection
    #     planetsCollection = mongo.db.planets

    #     # get JSON data from body
    #     name = request.json['name']
    #     distance = request.json['distance']

    #     # insert new planet and return it
    #     planet_id = planetsCollection.insert({'name': name, 'distance': distance})
    #     new_planet = planetsCollection.find_one({'_id': planet_id })
    #     output = {'name' : new_planet['name'], 'distance' : new_planet['distance']}

    #     return jsonify({'result' : output})

    # Add blueprints
    app.register_blueprint(user.bp)
    app.register_blueprint(auth.bp)

    return app

