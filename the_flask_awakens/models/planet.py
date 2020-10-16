from flask import (
    Blueprint, request, url_for, current_app, jsonify
)

from bson import json_util

from ..auth import token_required
from flask_pymongo import PyMongo
import requests
import re

bp = Blueprint('planet', __name__, url_prefix='/planets')

# function that clean the data received from the swapi api, and prepares it to be stored in mongo
def cleanSwapiData(data, planet_id):

    if planet_id is None:
        # when we return the list we need to extract the id 
        planet_id = re.findall('\d+', data['url'] )[0]

    data['residents'] = None
    data['films'] = None
    data['planet_id'] = planet_id

    return data

@bp.route('/', methods=['GET'])
def listPlanets():

    planets = []
    
    endpoint = 'http://swapi.dev/api/planets/'

    # if filter is applied
    if request.args.get('search'):
        endpoint += '?search='+request.args.get('search')

    # call swapi
    try:
        r = requests.get(endpoint)
        data = r.json()
        for planet in data['results']:
            planets.append(cleanSwapiData(planet, None))

        while data['next'] is not None:
            r = requests.get(data['next'])
            data = r.json()
            for planet in data['results']:
                planets.append(cleanSwapiData(planet, None))
    except:
        return jsonify({'error': 'something went wrong'})
    
    return jsonify({'planets': planets})

@bp.route('/<planet_id>/', methods=['GET'])
@token_required
def getPlanet(payload, planet_id):

    mongo = PyMongo(current_app)

    # check if planet already exists in DB
    planetsCollection = mongo.db.planets
    planet = planetsCollection.find_one({'planet_id': planet_id})

    # if no call swapi, add it to mongo, and return it
    if planet is None:
        try:
            r = requests.get('http://swapi.dev/api/planets/'+planet_id+'/')
            data = r.json()
        except:
            return jsonify({'error': 'something went wrong'})

        clean_data = cleanSwapiData(data, planet_id)

        # return newly created planet
        new_planet_id = planetsCollection.insert(clean_data)
        new_planet = planetsCollection.find_one({'planet_id': planet_id })

        # Remove the objectID retrieved from mongo
        new_planet.pop('_id', None)
        return json_util.dumps(new_planet, default=json_util.default)
    # if yes return it
    else:
        # Remove the objectID retrieved from mongo
        planet.pop('_id', None)
        return json_util.dumps(planet, default=json_util.default)