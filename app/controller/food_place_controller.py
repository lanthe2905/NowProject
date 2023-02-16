

from ..dto.food_place_dto import FoodPlaceDto
from  ..service.food_service import FoodPlaceService
from ..util.helpers import _success, _throw
from ..util.middleware import cookie_required, verify_access_token
from ..util.file import save_file_local, remove_file
from ..model.model import FoodPlaces
from flask import request
from flask_restx import Resource
import inspect
api = FoodPlaceDto.api
_foodFields= FoodPlaceDto.food_place_fields

@api.route('/get_by_id/<id>')
class FoodPlace(Resource):
    @cookie_required
    def get(self, id):
        try:
            foodPlace = FoodPlaceService.get_by_id(id, required_lang= True)
            return  _success(inspect.stack(), foodPlace)
        except Exception as e:
            _throw(e)

@api.route('/update/<id>')
class FoodPlaceUpdate(Resource):
    @api.expect(_foodFields)
    @verify_access_token
    @cookie_required
    def post(self, id):
        try:
            payload = request.get_json()
            return _success(inspect.stack(), FoodPlaceService.update(id=id, payload=payload))
        
        except Exception as e:
            _throw(e)
    

@api.route('/get_list')
class FoodPlaceList(Resource):
    @api.doc(params={'page': '1', 'pageSize' :'50'})
    def get(self):
        payload = request.args
        page = payload.get('page') if payload.get('page') is not None else 1
        page_size = payload.get('pageSize') if payload.get('pageSize') is not None else 50

        return _success(inspect.stack(),  FoodPlaceService.get_lists(page = page, page_size= page_size))

@api.route("/create")
@api.expect(_foodFields)
class FoodCreate(Resource):
    @verify_access_token
    def post(self):
            payload = request.get_json()
            return _success(inspect.stack(),  FoodPlaceService.create(payload))
  

@api.route('/delete/<id>')
class FoodDelete(Resource):
    @verify_access_token
    def delete(self, id):
        try:
            return _success(inspect.stack(), FoodPlaceService.delete_by_id(id))
        except Exception as e:
            _throw(e)

@api.route("/upload/<id>")
class UploadImageFoodPlace(Resource):
    @verify_access_token
    def post(self, id):
        try:
            food_place = FoodPlaceService.get_by_id(id= id)
            food_place = FoodPlaces(**food_place)
            FoodPlaceService.assert_food_place(food_place, True)
            files = request.files.getlist("images")
            
            # food_place['images'].extend(save_file_local(files= files))
            if food_place.images is None:
                food_place.images = save_file_local(files= files)
            else:
                food_place.images.extend(save_file_local(files= files))

            return _success(inspect.stack(), FoodPlaceService.update(id= id, payload= food_place.to_bson()))
        except Exception as e :
            _throw(e)
    
@api.route("/remove_file/<food_id>")
class RemoveFile(Resource):
    @verify_access_token
    def get(self, food_id):
        try:
            name = request.form.get("image_name")
            food_place = FoodPlaceService.get_by_id(id= food_id)
            food_place = FoodPlaces(**food_place)
            FoodPlaceService.assert_food_place(food= food_place, check_auth= True)

            if food_place.images is None: 
                return _success(inspect.stack(), {"message": "You not have images", "code": 400})

            if name not in food_place.images:
                raise _success(inspect.stack(), {"message": "Images invalid", "code": 400})

            if remove_file(file_name= name):
                if food_place.images is not None:
                    food_place.images.remove(name)
                    FoodPlaceService.update(id= food_id, payload= food_place.to_bson())
                    
                return _success(inspect.stack(), {"message": "Remove success!", "code": 200})
            else: 
                return _success(inspect.stack(), {"message": "Images not exist", "code": 400}) 
        except Exception as e:
            _throw(e)