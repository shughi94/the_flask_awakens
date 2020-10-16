from flask import (
    Blueprint, g, redirect, request, session, url_for, current_app
)

from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

from functools import wraps

from flask_bcrypt import Bcrypt
import datetime, jwt

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Decorator to check if token is valid
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        # Token is taken from Authorization header set like 'Bearer xxxxx'
        auth_header = request.headers.get('Authorization')
        payload=''
        if auth_header:
            token = auth_header.split(" ")[1]
        else:
            token = ' '
        if token:
            try:
                payload = jwt.decode(token, current_app.config['JWT_SECRET'],)
            except jwt.ExpiredSignatureError:
                return "Expired token"
                #return redirect(url_for('auth.loginGet'))
            except jwt.InvalidTokenError:
                return "Invalid token"
                #return redirect(url_for('auth.loginGet'))
        # when using the decorator, the payload is passed too!
        return f(payload, *args, **kwargs)
    return decorator

# dummy route for the login page
@bp.route('/', methods=['GET'])
def loginGet():
    return "login page"

# login route
@bp.route('/', methods=['POST'])
def loginPost():
    username = request.json['username']
    password = request.json['password']

    bcrypt = Bcrypt(current_app)
    mongo = PyMongo(current_app)

    usersCollection = mongo.db.users
    user = usersCollection.find_one({'username': username})
    error = None

    # check the login info
    if user is None:
        error = 'Incorrect login attempt'
    elif not bcrypt.check_password_hash(user['password'], password):
        error = 'Incorrect login attempt'
    if error is None:

        # don't know if sub should be username or str(user['_id'])
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=current_app.config['TOKEN_DURATION']),
            'iat': datetime.datetime.utcnow(),
            'sub': user['username']
        }
        # separate in different function so it can be modified better in future? (e.g. add new info)
        jwt_token = jwt.encode(
            payload,
            current_app.config['JWT_SECRET'],
            algorithm='HS256'
        )
        return {
                'status': 'Success',
                'message': 'Successfully registered.',
                'auth_token': jwt_token.decode()
            }
        
    return error

@bp.route('/test', methods=['GET'])
@token_required
def test1(payload):
    return "Authorization authorized! -> {}".format(payload['sub'])