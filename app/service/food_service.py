from app.model.db import foodPlacesCollection
from app.model.model import FoodPlaces, Users
from bson.objectid import ObjectId
from app.util.jwt import get_current_user
from app.util.exception import NotPermissionException
from app.service.food_type_and_style_service import FoodTypeAndStyleService
from app.service.food_category_service import FoodCategoryService
from app.util.file  import remove_file
from flask import request
import json
class FoodPlaceService:
    @staticmethod
    def get_lists(page= 1, page_size = 30):
        page = int(page)
        page_size = int(page_size)
        list_food =  foodPlacesCollection.find().skip((page -1) * page_size).limit(page_size)
        return list(list_food)

    @staticmethod
    #required_lang: dùng khi muốn giới hạn data trả về, true nếu muốn lấy hết data đang có để phục vụ thao tác xoá dữ liệu 
    def get_by_id(id, required_lang= False):
        lang = request.cookies.get('lang')
        expr_food_category_lang = {"$eq": ["$lang",lang]} 
        expr_food_style_lang = {"$eq": ["$lang",lang]} 

        result = foodPlacesCollection.aggregate([
            {"$match": {"_id": ObjectId(id)}},
            {"$lookup" : {
                "from": "foodCategories",
                "let": {"foodPlaceID": "$_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$eq": ["$foodPlaceID", "$$foodPlaceID"] 
                            }
                        }
                    },
                    {"$lookup" : {
                        "from": "foodCategoryLangs",
                        "let": {"categoryID": "$_id"},
                        "pipeline": [
                           { 
                                "$match": {
                                    "$expr": {
                                        "$and": [
                                            { "$eq": ["$foodCategoryID", "$$categoryID"] },
                                            expr_food_category_lang if required_lang is True else None
                                        ]
                                       
                                    }  
                                }
                            },
                            {"$project": {"_id": 0, "categoryName": 1,"lang": 1}}
                        ],
                        "as": "categoryLangs"
                    }},
                    {"$project": {"_id": 1, "categoryLangs": 1}}
                ],
                "as": "categories"
            }},
            {"$lookup": {
                    "from": "foodTypeAndStyles",
                    "let": {"foodPlaceID": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": ["$foodPlaceID", "$$foodPlaceID"]
                                }
                            }
                        },
                        {
                            "$lookup": {
                                "from": "foodTypeAndStyleLangs",
                                "let": {"foodStyleID": "$_id"},
                                "pipeline": [
                                    {
                                        "$match": {
                                            "$expr": {
                                                "$and": [
                                                    {"$eq": ["$foodTyleAndStyleID", "$$foodStyleID"]},
                                                    expr_food_style_lang if required_lang is True else None
                                                ]
                                                
                                            }
                                        }
                                    }
                                ],
                                "as": "langs"
                            }
                        }
                    ],
                    "as": "foodTypeAndStyles"
                }
            }


        ])
        return dict(result.next()) if result._has_next() else {}

    @staticmethod
    def create(payload):
        if payload['openTimes'] != None : 
            payload['openTimes'] = json.dumps(payload['openTimes'])

        food = FoodPlaces(**payload)

        inserted_id = foodPlacesCollection.insert_one(food.to_bson())
        if inserted_id is None: return {"message": "Create not successfully", "code": 204}
        return {"message": "create success", "data": FoodPlaceService.get_by_id(inserted_id), "code": 200}


    @staticmethod
    def delete_by_id(id):
        food_place = FoodPlaceService.get_by_id(id, required_lang= True)
        food_place_model = FoodPlaces(**food_place)
        if food_place_model.id is None:
            return {}

        FoodPlaceService.assert_food_place(food_place_model, True)
        if food_place_model.images is not None:
            for image in food_place_model.images:
                remove_file(image)
        if "foodTypeAndStyles" in food_place: 
            for food_style in food_place['foodTypeAndStyles']:
                if "_id" in food_style: FoodTypeAndStyleService.delete(food_style['_id'])
                
        if 'categories' in food_place:
            for category in food_place['categories']:
                if "_id" in category: FoodCategoryService.delete_by_id(category['_id'])
        
        result = foodPlacesCollection.delete_one({"_id": ObjectId(id) })
        if result.deleted_count == 0: return {"message": "delete not success!", "code": 204}
        
        return {"message": "delete success", "code": 200}


    @staticmethod
    def update(id,payload):
        food = FoodPlaceService.get_by_id(id)
        food = {**food,**payload}
        food = FoodPlaces(**food)
        if food.id is None: return {}

        FoodPlaceService.assert_food_place(food, True)
        result = foodPlacesCollection.update_one({"_id": ObjectId(id) }, {"$set":  food.to_bson()})
        if result.matched_count == 0 : return {}

        return food.to_json()

    @staticmethod
    def assert_food_place(food:FoodPlaces, check_auth = False):
        if food is None or food.id is None: raise(Exception("can't find food place"))

        if check_auth is True:
            user: Users = get_current_user()
            if food.userID != user.id: raise(NotPermissionException("Not permission"))




    
