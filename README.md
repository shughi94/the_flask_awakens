
# General

# Installation
Run
`export FLASK_APP=the_flask_awakens`
`export FLASK_ENV=development`
`python3 -m flask run`

## Configuration
under the instance folder, create a `secret.py` file.

example:

```py
DATABASE_URL = '127.0.0.1'
DATABASE_PORT = '27017'
DATABASE_NAME = 'jabbathehutt'
```

# Project

## Users

Users can be created at this following endpoint:

POST to `/user/` with a body like this:

```json
{
  "username": "user",
  "password": "12345"
}
```


