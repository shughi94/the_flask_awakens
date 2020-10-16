
# THE_FLASK_AWAKENS

# Installation
Run:
- `export FLASK_APP=the_flask_awakens`
- `export FLASK_ENV=development`
- `python3 -m flask run`

## Configuration
under the instance folder, create a `secret.py` file.

example:

```py
# database configuration
DATABASE_URL = '127.0.0.1'
DATABASE_PORT = '27017'
DATABASE_NAME = 'jabbathehutt'

# jwt configuration
JWT_SECRET = 'JarJarBinksWasASithLord'
TOKEN_DURATION = 360 #seconds
```

## Versions
For this project I've used:
- Python 3.8.6
- MongoDB v3.2.9
- Flask 1.1.2
- Flask-Bcrypt 0.7.1
- Flask-PyMongo 2.3.0
- PyJWT 1.4.2
- requests 2.24.0

# Project

## User

Users can be created at this following endpoint:

POST to `/user/` with a body like this:

```json
{
  "username": "user",
  "password": "12345"
}
```

### Notes

## Auth
To login, send a POST request to `/auth/` with a body like this:

```json
{
  "username": "user",
  "password": "12345"
}
```
This will return (if info are correct) a valid JWT token.


### Notes

## Planet
To get the list of planets: GET `/planets/`

### Notes


