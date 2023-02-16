from app.model.model import FoodCategories, Users, FoodPlaces
from app.model.db import foodCategoryLangsCollection,foodCategoriesCollection, foodPlacesCollection
from bson.objectid import ObjectId
from app.util.helpers import _throw
from app.util.exception import  NotPermissionException
from flask_jwt_extended import current_user
class FoodCategoryService: 

    @staticmethod
    def create(payload):
        for lang in payload['categoryLangs']:
            food_category_id = foodCategoriesCollection.insert_one({
                "foodPlaceID":  ObjectId(payload['foodPlaceID'])
            }).inserted_id

            if "vn" in lang  and lang['vn'] != ""  : 
                FoodCategoryService.save_to_db(lang['vn'], food_category_id, 'vn')
                
            if "en" in lang  and lang['en'] != "": 
                FoodCategoryService.save_to_db(lang['en'], food_category_id, 'en')
                
            # cteLang = FoodCategoriesLangs(**lang)
        return {"message": "save category success!", "status": 200, "data": FoodCategoryService.get_by_id(food_category_id)}
     
    @staticmethod
    def save_to_db(name, foodCategoryID,lang = "vn"):
        foodCategoryLangsCollection.insert_one({
            "categoryName": name,
            "foodCategoryID": ObjectId(foodCategoryID),
            "lang": lang
        })
            
    @staticmethod
    def update(payload):
        category = FoodCategoryService.get_by_id(ObjectId(payload['foodCategoryID']))
        if "_id" not in  category: return {"message": "data not valid", "status": 404}

        category:FoodCategories = FoodCategories(**category)
        FoodCategoryService.assert_category(category=category, check_auth= True)

        if payload['categoryLangs']['vn'] != '' and payload['categoryLangs']['vn']  is not  None:
            foodCategoryLangsCollection.update_one({
                "lang": "vn",
                "foodCategoryID": ObjectId(category.id)
            },{
                "$set": {
                    "categoryName": payload['categoryLangs']['vn']
                }
            })
        if payload['categoryLangs']['en'] != '' and payload['categoryLangs']['en']  is not None:
            foodCategoryLangsCollection.update_one({
                "lang": "en",
                "foodCategoryID": ObjectId(category.id)
            },{
                "$set": {
                    "categoryName": payload['categoryLangs']['en']
                }
            })
        return {"message": "updated success","data":FoodCategoryService.get_by_id(category.id), "status": 200}

    
    @staticmethod
    def get_by_id(id):
        food_category = foodCategoriesCollection.aggregate(
           [
             {"$match": { "_id": ObjectId(id)}},
             {
                "$lookup": {
                    "from": "foodCategoryLangs",
                    "localField": "_id",
                    "foreignField": "foodCategoryID",
                    "as": "categoryLangs"
                }
             }
           ])
        return dict(food_category.next()) if food_category._has_next() else {}

    @staticmethod
    def assert_category(category: FoodCategories, check_auth= True):
        if not category : _throw(Exception("can't find category"))
        user: Users = get_current_user()
        food_place = foodPlacesCollection.find_one(category.foodPlaceID)
        food_place = FoodPlaces(**food_place)
        if food_place is None:
            raise Exception("Can't find food place")
        if check_auth is True:
            if food_place.userID != user.id:
                raise NotPermissionException("not permission")
        # foodPlace = FoodPlaceService.get_by_id(category.foodPlaceID)

    @staticmethod
    def delete_by_id(id):
        category = FoodCategoryService.get_by_id(id)
        if "_id" not in category: return {'message': "cant find data", "status": 400}
        category = FoodCategories(**category)
        FoodCategoryService.assert_category(category= category, check_auth= True)
        if "categoryLangs" in category:
            for categoryLang in category['categoryLangs']:
                foodCategoryLangsCollection.delete_one(categoryLang['_id'])
        result = foodCategoriesCollection.delete_one({"_id": ObjectId(category.id)})
      
        return {'message': "deleted successfully!", "status": 200}
