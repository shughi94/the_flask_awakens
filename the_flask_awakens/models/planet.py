from flask import (
    Blueprint, request, url_for, current_app, jsonify
)

import requests

bp = Blueprint('planet', __name__, url_prefix='/planets')

@bp.route('/', methods=['GET'])
def listPlanets():

    planets = []
    
    endpoint = 'http://swapi.dev/api/planets/'

    # call swapi
    try:
        r = requests.get(endpoint)
        data = r.json()
        for planet in data['results']:
            planets.append(planet)

        while data['next'] is not None:
            r = requests.get(data['next'])
            data = r.json()
            for planet in data['results']:
                planets.append(planet)
    except:
        return jsonify({'error': 'something went wrong'})
    
    return jsonify({'planets': planets})