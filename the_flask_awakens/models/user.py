from flask import (
    Blueprint, g, request, url_for, current_app, jsonify
)
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

bp = Blueprint('user', __name__, url_prefix='/user')

# # User class with functions to simplify handling users
# class User:
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password

#     def toJson(self):
#         return jsonify({'username': self.username})

@bp.route('/', methods=['POST'])
def createUser():

    # does this initialize a new connection or reuse the one created in the factory?
    # Switch to db.py file with a get_db() function?
    mongo = PyMongo(current_app)
    bcrypt = Bcrypt(current_app)

    # get JSON data from body
    username = request.json['username']
    password = request.json['password']

    # get collection
    usersCollection = mongo.db.users

    # check if username already exist
    user = usersCollection.find_one({'username': username})
    if user is not None:
        return jsonify({'error': 'Username already exists'})

    # bcrypt password. the decode is needed by python3
    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    # insert new user and return it
    user_id = usersCollection.insert({'username': username, 'password': pw_hash})
    new_user = usersCollection.find_one({'_id': user_id })
    
    output = {'username': new_user['username']}

    return jsonify({'result': output})