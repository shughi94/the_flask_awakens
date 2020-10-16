# THE_FLASK_AWAKENS

# Installation

Under the instance folder, create a `secret.py` file.

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

The requirements.txt file shows which python modules the application need.

Then run:
- `export FLASK_APP=the_flask_awakens`
- `export FLASK_ENV=development`
- `python3 -m flask run`

## Versions
For this project I've used:
- Python 3.8.6
- pip 20.2.1
- MongoDB v3.2.9
- OpenSSL 1.0.2t
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
I used the `username` field for the `sub` attribute in the token payload, since it's unique for each user.
The decorator is not coded to handle error on the Authorization header. If it's setup wrongly, the request will return 500.

## Planet
To get the list of planets: GET `/planets/`

To filter by planet name, use `?search=<filter>`

To get a single planet: GET `/planets/<planet_id>`, and make sure to have the token in the Authorization header in the following format: `Bearer xxxx`

### Notes

There are a lot of exception that makes the service return 500 (e.g. I do not check if `planet_id` is an int), but at least I wrapped the external API calls in a `try except` block to handle some of them.

I'm not happy also on how I clean the mongoDB data and return it:
``` py
# Remove the objectID retrieved from mongo
        planet.pop('_id', None)
        return json_util.dumps(planet, default=json_util.default)
```
If I had more time, I would have created the planet class and used some custom function on there for some code reusability.

The way I get the list of planets is by having a while loop on every 'next' page SWAPI offers, so I get a full list of planets. If planets were a lot more than the 60 that SWAPI have, I would have probably returned a truncated list too with the `next` attribute.
But since SWAPI offers 10000 free calls per day, I was not preoccupied that each `/planets/` call results in 7 SWAPI calls. 

Also, a GET request that creates something in the DB is sketchy for a RESTful application, but since the user has no saying on the informations needed to create the planet I think it's OK.

Could not add the order functionality due to time limit, but I saw that SWAPI offers something like `?ordering=name`.

## General Notes
- I'm not sure if the way i call the mongoDB (with `mongo = PyMongo(current_app)`) in blueprints is good. I don't know if it opens a new connection everytime. The way I implemented it in my password-manager project was to have a separated file (e.g. `db.py`) that handled the connection with the function `get_db()`, and I think this is good practice. Due to time limitation I was not able to make it like this.

- Errors such as `invalid token`, `user not found`, ecc... are returning 200, since I just used `jsonify()`. If I had more time I would have searched for a flask tool to return something like `return Response(404, 'error', json_data)`

- I wanted to create a `docker-compose` project at first to handle all the different versions we might have, but I quickly realized it would take me more than 4 hour, so I went the simple way. I added above all the versions of the stuff I used.

- The way I return the JSON is not generalized. If I had more time, I would have probably used GoogleJSON because it looks cool.

## Timings
I started the timer when I managed to have a working Flask + MongoDB base application. Had couple of problems making Mongo work on my mac (Upgrading to Catalina was the worst trade in history maybe ever).

The git repository here shows that I started at 12:07 and finished when I merged to master

## Ending
Thanks for the project, was fun!
For any questions, feel free to write me an email.


