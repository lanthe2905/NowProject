from app.model.db import foodTypeAndStyleLangsCollection, foodTypeAndStylesCollection
from app.model.model import FoodTypeAndStyles, FoodTypeAndStyleLangs, FoodPlaces
from app.service.food_type_and_style_lang_service import FoodTypeAndStyleLangService
from app.service.food_service import FoodPlaceService
from app.util.exception import NotFoundDataException
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
        food_place = FoodPlaces(**FoodPlaceService.get_by_id(food_type.foodPlaceID))
        FoodPlaceService.assert_food_place(food = food_place, check_auth= True)
        if 'recommendation' in payload:
            food_type_lang['recommendation'] = payload['recommendation']
          
        if 'description' in payload:
            food_type_lang['description'] = payload['description']

        food_type_style_id = foodTypeAndStylesCollection.insert_one(food_type.to_json()).inserted_id
        if food_type_style_id is None: 
            raise Exception("Can't create food style")

        if 'description' in food_type_lang or 'recommendation' in food_type_lang :
            food_type_lang['foodTyleAndStyleID'] = food_type_style_id
            food_type_lang['lang'] = request.cookies.get('lang')
            food_type_lang = FoodTypeAndStyleLangs(**food_type_lang)
            FoodTypeAndStyleLangService.create(food_type_lang.to_bson())
            

        return FoodTypeAndStyleService.get_by_id(food_type_style_id)


    @staticmethod 
    def update(id, payload):
        food_type = FoodTypeAndStyleService.get_by_id(id)
    
        food_type_model = FoodTypeAndStyles( **{**food_type, **payload})
        FoodTypeAndStyleService.assert_food_type(food_type= food_type_model, check_auth= True)


        foodTypeAndStylesCollection.update_one({"_id": ObjectId(id)}, {
            "$set": food_type_model.to_bson()
        })

        if 'description' in payload or 'recommendation' in payload :
            if food_type['langs']: 
                for food_style_lang in food_type['langs']:
                    if request.cookies.get("lang") == food_style_lang['lang']:
                        # print(food_style_lang)
                        food_style_lang = FoodTypeAndStyleLangs(**{**food_style_lang, **payload})
                        FoodTypeAndStyleLangService.update(food_style_lang.id,  food_style_lang.to_bson())
            else:
                food_style_lang_model = FoodTypeAndStyleLangs(**payload)
                FoodTypeAndStyleLangService.create(food_style_lang_model.to_bson())

        return  FoodTypeAndStyleService.get_by_id(id)
    
    @staticmethod
    def delete(id):
        food_type = FoodTypeAndStyleService.get_by_id(id)
        FoodTypeAndStyleService.assert_food_type(food_type= FoodTypeAndStyles(**food_type), check_auth= True)

        if food_type['langs']: 
             for food_style_lang in food_type['langs']:
                if "_id" not in food_style_lang:
                    raise NotFoundDataException("Error...")
                FoodTypeAndStyleLangService.delete(food_style_lang['_id'])

      
        return foodTypeAndStylesCollection.delete_one({"_id": ObjectId(id)}).acknowledged

    @staticmethod
    def assert_food_type(food_type: FoodTypeAndStyles, check_auth = False):
        if not food_type or food_type.id is None: raise(NotFoundDataException("not found data"))
        if check_auth is True:
            food_place = FoodPlaceService.get_by_id(food_type.foodPlaceID)
            food_place = FoodPlaces(**food_place)
            FoodPlaceService.assert_food_place(food= food_place, check_auth=True)
