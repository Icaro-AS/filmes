from flask import Response, request
from flask_jwt_extended import create_access_token
from database.models import User 
from flask_restplus import Resource
import datetime
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import resources.errors as errors

class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User(**body)
            user.hash_password()
            user.save()
            id = user.id
            return {'id': str(id)}, 200
        except FieldDoesNotExist:
            raise errors.SchemaValidationError
        except NotUniqueError:
            raise errors.EmailAlreadyExistsError
        except Exception as e:
            raise errors.InternalServerError
    
class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get("email"))
            authorized = user.check_password(body.get('password')) 
            if not authorized:
                return {'error': "Email or password invalid"}, 401
            
            expires = datetime.timedelta(minutes= 15)
            accesss_token = create_access_token(identity=str(user.id), expires_delta=expires) 
            return {'token': accesss_token}, 200
        except FieldDoesNotExist:
            raise errors.SchemaValidationError
        except NotUniqueError:
            raise errors.EmailAlreadyExistsError
        except Exception as e:
            raise errors.InternalServerError