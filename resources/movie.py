from flask import Response, request
from database.models import Movie, User
from flask_restx  import Resource,fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, \
                                DoesNotExist,ValidationError
import resources.errors as errors  
from app import api

class MoviesApi(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    def get(self):
        movies = Movie.objects().to_json()
        return Response(movies, mimetype="application/json", status = 200)
     
    @jwt_required()
    def post(self):
        try: 
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            movie = Movie(**body, added_by= user)
            movie.save()
            user.update(push__movies=movie)
            user.save()
            id = movie.id
            return {"id": str(id)}, 200
        except(FieldDoesNotExist, ValidationError):
            raise errors.SchemaValidationError
        except(NotUniqueError):
            raise errors.MovieAlreadyExistsError
        except Exception as e:
            raise errors.InternalServerError


class MoviesApiId(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    def get(self, id):
        movie = Movie.objects(id=id).to_json()
        return Response(movie, mimetype="application/json", status = 200)

    @jwt_required()
    def put(self,id):
        try:
            user_id = get_jwt_identity()
            Movie.objects.get(id=id, added_by=user_id)
            body = request.get_json()
            Movie.objects.get(id = id).update(**body)
            return '', 200
        except errors.InvalidQueryError:
           raise errors.SchemaValidationError
        except DoesNotExist:
           raise errors.UpdatingMovieError
        except Exception:
           raise errors.InternalServerError
    
    @jwt_required()
    def delete(self, id):
        try:
            user_id = Movie.objects.get(id=id).delete()
            movie = Movie.objects.get(id=id, added_by=user_id)
            movie.delete()
            return '', 200
        except DoesNotExist:
            raise errors.MovieNotExistsError
        except Exception:
            raise errors.InternalServerError



