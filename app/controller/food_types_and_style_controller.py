from flask_restx import Resource
from flask import request
from app.util.helpers import  _success
from app.dto.food_type_style_dto import FoodTypeAndStyleDto
from app.service.food_type_and_style import FoodTypeAndStyleService
from flask_jwt_extended import jwt_required
import inspect

api = FoodTypeAndStyleDto.api
_foodTypeAndStyleField = FoodTypeAndStyleDto.food_type_field

@api.route("/create")
class FoodTypeAndStyleController(Resource):
    @api.expect(_foodTypeAndStyleField)
    def post(self):
        payload = request.get_json()
        return _success(inspect.stack(), FoodTypeAndStyleService.create(payload= payload)) 

@api.route('/update</id>')
class FoodTypeAndStyleUpdate(Resource):
    # @jwt_required
    def post(self):
        pass

@api.route('/delete/<id>')
class DeleteFoodTypeAndStyle(Resource):
    def get(self):
        pass