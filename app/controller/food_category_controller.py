

from flask_restx import Resource
from flask import request
from ..util.helpers import _success, _throw
from ..service.food_service import FoodPlaceService
from ..service.food_category_service import FoodCategoryService
from ..dto.food_category import FoodCategoryDto
from ..util.middleware import verify_access_token
import inspect

api = FoodCategoryDto.api
_category_create_field = FoodCategoryDto.category_create_form

@api.route('/create')
@api.expect(_category_create_field)
class CreateCategory(Resource):
    def post(self):
        try:
            payload = request.get_json() 
            if "foodPlaceID" not in payload  or payload['foodPlaceID'] == ""  :  raise Exception("missing field foodPlaceID") 
            
            return _success(inspect.stack(),  FoodCategoryService.create(payload= payload))
        except Exception as e:
            _throw(e)

@api.route('/update')
@api.expect(FoodCategoryDto.category_update_form)
class UpdateCategory(Resource):
    @verify_access_token
    def post(self):
        try:
            payload = request.get_json()
            return _success(inspect.stack(), FoodCategoryService.update(payload))
        except Exception as e:
            _throw(e)   

@api.route('/delete/<id>')
class DeleteCategory(Resource):
    @verify_access_token
    def get(self, id):
        try:
            return _success(inspect.stack(), FoodCategoryService.delete_by_id(id))
        except Exception as e: 
            _throw(e)

@api.route('/get_by_id/<id>')
class GetCategoryByID(Resource):
    def get(self, id):
        return _success(inspect.stack(), FoodCategoryService.get_by_id(id))