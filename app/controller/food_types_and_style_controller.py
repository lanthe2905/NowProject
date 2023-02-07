from flask_restx import Resource
from flask import request
from app.util.helpers import  _success, _throw, _validation_exception
from app.dto.food_type_style_dto import FoodTypeAndStyleDto
from app.service.food_type_and_style_service import FoodTypeAndStyleService
from app.util.middleware import cookie_required
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
import inspect

api = FoodTypeAndStyleDto.api
_foodTypeAndStyleField = FoodTypeAndStyleDto.food_type_field


@api.route('/get_by_id/<id>')
class GetFoodTypeAndStyleController(Resource):
    def get(self, id):
        try:
            food_style = FoodTypeAndStyleService.get_by_id(id)
            return _success(inspect.stack(), food_style)
        except Exception as e:
            _throw(e)

@api.route("/create")
class FoodTypeAndStyleController(Resource):
    @api.expect(_foodTypeAndStyleField)
    @cookie_required
    @jwt_required()
    def post(self):
        try:
            payload = request.get_json()
            return _success(inspect.stack(), FoodTypeAndStyleService.create(payload= payload)) 
        except ValidationError as e:
            return  _validation_exception(e)
        except Exception as e:
            _throw(e)

@api.route('/update/<id>')
class FoodTypeAndStyleUpdate(Resource):
    @jwt_required()
    @api.expect(_foodTypeAndStyleField)
    def post(self, id):
        try:
            payload = request.get_json()
            return _success(inspect.stack(), FoodTypeAndStyleService.update(id, payload= payload))
        except ValidationError as e:
            return  _validation_exception(e)
        except Exception as e:
            _throw(e)


@api.route('/delete/<id>')
class DeleteFoodTypeAndStyle(Resource):
    @jwt_required()
    def get(self, id):
        try:
            return _success(inspect.stack(), FoodTypeAndStyleService.delete(id))
        except ValidationError as e:
            return  _validation_exception(e)
        except Exception as e:
            _throw(e)