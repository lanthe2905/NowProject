

from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required
from ..util.helpers import _success, _throw
from ..util.middleware import verify_access_token
from ..service.food_promotion_service import FoodPromotionService
from ..dto.food_promotion_dto import FoodPlaceDto
import inspect

api = FoodPlaceDto.api
_food_promotion_field = FoodPlaceDto.food_promotion_fields

@api.route('/create')
@api.expect(_food_promotion_field)
class CreatePromotion(Resource):
    def post(self):
        try:
            payload = request.get_json() 
            return _success(inspect.stack(),  FoodPromotionService.create(payload= payload))
        except Exception as e:
            _throw(e)

@api.route('/update/<id>')
@api.expect(_food_promotion_field)
class UpdatePromotion(Resource):
    @verify_access_token
    def post(self, id):
        try:
            payload = request.get_json()
            return _success(inspect.stack(), FoodPromotionService.update(payload, id=id))
        except Exception as e:
            _throw(e)   

@api.route('/delete/<id>')
class DeletePromotion(Resource):
    @verify_access_token
    def get(self, id):
        try:
            return _success(inspect.stack(), FoodPromotionService.delete_by_id(id))
        except Exception as e: 
            _throw(e)

@api.route('/get_by_id/<id>')
class GetPromotionByID(Resource):
    def get(self, id):
        return _success(inspect.stack(), FoodPromotionService.get_by_id(id))