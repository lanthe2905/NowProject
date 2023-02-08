from app.model.db import  foodTypeAndStylesCollection, foodPlacesCollection
from app.model.model import FoodTypeAndStyles, FoodTypeAndStyleLangs, FoodPlaces, Users
from app.service.food_type_and_style_lang_service import FoodTypeAndStyleLangService
from app.util.jwt import get_current_user
from flask import request
from bson import ObjectId
class FoodTypeAndStyleService:
    @staticmethod
    def get_by_id(id):
        food_types =  foodTypeAndStylesCollection.aggregate(
            [
                {
                    "$match": {'_id': ObjectId(id)}
                },
                {
                    "$lookup": {
                        "from": "foodTypeAndStyleLangs",
                        "let": {"foodTypeID" : "$_id"},
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$eq": ["$foodTyleAndStyleID", "$$foodTypeID"]
                                    }
                                }
                            }
                        ],
                        "as": "langs"
                    }
                }
            ])
       
        return dict(food_types.next()) if food_types._has_next() else {}
 
    @staticmethod
    def create(payload):
        food_type = FoodTypeAndStyles(**payload)
        food_type_lang = {}
        if 'recommendation' in payload:
            food_type_lang['recommendation'] = payload['recommendation']
          
        if 'description' in payload:
            food_type_lang['description'] = payload['description']

        food_type_style_id = foodTypeAndStylesCollection.insert_one(food_type.to_bson()).inserted_id
        if food_type_style_id is None: 
            return {"message": "Data not valid", "code": 400}

        if 'description' in food_type_lang or 'recommendation' in food_type_lang :
            food_type_lang['foodTyleAndStyleID'] = food_type_style_id
            food_type_lang['lang'] = request.cookies.get('lang')
            food_type_lang = FoodTypeAndStyleLangs(**food_type_lang)
            FoodTypeAndStyleLangService.create(food_type_lang.to_bson())
            

        return {"message": "create successfully", "code": 200, "data": FoodTypeAndStyleService.get_by_id(food_type_style_id)}


    @staticmethod 
    def update(id, payload):
        food_type = FoodTypeAndStyleService.get_by_id(id)
        food_type_model = FoodTypeAndStyles( **{**food_type, **payload})

        if food_type_model.id is None:
            return {"message": "Data not valid", "code": 400}

        FoodTypeAndStyleService.assert_food_type(food_type= food_type_model, check_auth= True)


        foodTypeAndStylesCollection.update_one({"_id": ObjectId(id)}, {
            "$set": food_type_model.to_bson()
        })
        if 'description' in payload or 'recommendation' in payload :
            if food_type['langs']: 
                for food_style_lang in food_type['langs']:
                    if request.cookies.get("lang") == food_style_lang['lang']:
                        food_style_lang = FoodTypeAndStyleLangs(**{**food_style_lang, **payload})
                        FoodTypeAndStyleLangService.update(food_style_lang.id,  food_style_lang.to_bson())
            else:
                food_style_lang_model = FoodTypeAndStyleLangs(**payload)
                FoodTypeAndStyleLangService.create(food_style_lang_model.to_bson())

        return {"message": "updated successfully!", "code": 200, "data": FoodTypeAndStyleService.get_by_id(id)} 
    
    @staticmethod
    def delete(id):
        food_type = FoodTypeAndStyleService.get_by_id(id)

        if "_id" not in food_type: return {"message": "data not valid", "code": 400}
        FoodTypeAndStyleService.assert_food_type(food_type= FoodTypeAndStyles(**food_type), check_auth= True)

        if food_type['langs']: 
             for food_style_lang in food_type['langs']:
                FoodTypeAndStyleLangService.delete(food_style_lang['_id'])

      
        result = foodTypeAndStylesCollection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0: 
            return {"message": "delete not success", "code": 400}

        return {"message": "delete successfully!", "code": 200}


    @staticmethod
    def assert_food_type(food_type: FoodTypeAndStyles, check_auth = False):
        if not food_type or food_type.id is None: raise(Exception("not found data"))
        if check_auth is True:
            food_place = foodPlacesCollection.find_one(food_type.foodPlaceID)

            if food_place == None:
                raise Exception("error..")

            food_place = FoodPlaces(**food_place)
            user: Users = get_current_user()
            if food_place.userID != user.id: raise(Exception("assert food type error.."))