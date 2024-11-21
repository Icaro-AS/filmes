import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask import Flask
from flask_restx  import Api
from flask_bcrypt import Bcrypt
from database.db import initialize_db 
from flask_jwt_extended import JWTManager
from resources.errors import errors
from flask_mail import Mail


app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')
mail = Mail(app)
api = Api(app, errors=errors)

from resources.routes import initialize_routes

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_db(app)
initialize_routes(api)

