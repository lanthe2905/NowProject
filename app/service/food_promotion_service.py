from app.model.model import Users, FoodPlaces, FoodPromotion, FoodPromotionLangs
from app.model.db import  foodPlacesCollection, foodPromotionsCollection, foodPromotionLangsCollection
from app.util.exception import  NotPermissionException
from app.util.jwt import get_current_user
from bson import ObjectId
class FoodPromotionService: 

    @staticmethod
    def create(payload):
        promotion = FoodPromotion(**payload)
        promotion_document = foodPromotionsCollection.insert_one(promotion.to_bson())
        if 'promotionLangs' in payload:
            for promotionLang in payload['promotionLangs']:
                if "lang" not in promotionLang: continue
                if promotionLang['lang'] not in ['vn', 'en']: continue

                promotionLang['foodPromotionID'] =  promotion_document.inserted_id
                promotionLang = FoodPromotionLangs(**promotionLang)
                foodPromotionLangsCollection.insert_one(  promotionLang.to_bson())
             

        return {'message': "successfully!", "status": 200, "data": FoodPromotionService.get_by_id(promotion_document.inserted_id)}     
        

    @staticmethod
    def update(payload, id):
        promotion = FoodPromotionService.get_by_id(id)
        promotion_queue_update = []
        promotion_queue_save = []
        
        if "_id" not in promotion: 
            return {"message": "cant find promotion", "status": 400}
        promotion_updated = FoodPromotion(**{**promotion, **payload})

        FoodPromotionService.assert_promotion(promotion= promotion_updated, check_auth= True)

        if 'promotionLangs' in payload:
            for promotion_payload in payload['promotionLangs']:
                if 'lang' not in promotion_payload:
                    continue
                if promotion_payload['lang'] not in ['en','vn']:
                    continue
                
                if "promotionLangs" in promotion:
                    for promotion_doc in promotion['promotionLangs']:
                        if promotion_doc['foodPromotionID'] != promotion['_id']: 
                            return {"message": "promotion_lang required 'lang' key", "code": 400}

                        if promotion_doc['lang'] == promotion_payload['lang']:
                            promotion_lang_model = FoodPromotionLangs(**{**promotion_doc, **promotion_payload})
                            promotion_queue_update.append(promotion_lang_model.to_bson())
                else:
                    promotion_lang_model = FoodPromotionLangs(**promotion_payload)
                    promotion_queue_save.append(promotion_lang_model.to_bson())

        if len(promotion_queue_update) > 0:
            for promotion_lang in promotion_queue_update:
                promotion_lang_model = FoodPromotionLangs(**promotion_lang)
                query = {"_id": ObjectId(promotion_lang_model.id), "lang": promotion_lang_model.lang}
                foodPromotionLangsCollection.update_one(query, {
                    "$set": promotion_lang_model.to_bson()
                })
                
        if len(promotion_queue_save) > 0:
            foodPromotionLangsCollection.insert_many(promotion_queue_save)

        promotion_document = foodPromotionsCollection.update_one({"_id": ObjectId(id)},{"$set": promotion_updated.to_bson()})
        
        if promotion_document.matched_count == 0:
            return {"message": "Cant find promotion", "code": 400}

        return {'message': "update successfully!", "status": 200}  
    
    @staticmethod
    def get_by_id(id):
        food_promotion = foodPromotionsCollection.aggregate(
           [
             {"$match": { "_id": ObjectId(id)}},
             {
                "$lookup": {
                    "from": "foodPromotionLangs",
                    "localField": "_id",
                    "foreignField": "foodPromotionID",
                    "as": "promotionLangs"
                }
             }
           ])

        return dict(food_promotion.next()) if food_promotion._has_next() else {}

    @staticmethod
    def assert_promotion(promotion: FoodPromotion, check_auth= False):
        if not promotion : raise(Exception("can't find promotion"))
        if check_auth is True:
            food_place = foodPlacesCollection.find_one(promotion.foodPlaceID)
            food_place = FoodPlaces(**food_place)

            if food_place is None:
                raise Exception("Can't find food place")

            user: Users = get_current_user()
            if food_place.userID != user.id:
                raise NotPermissionException("not permission")
      

    @staticmethod
    def delete_by_id(id):
        promotion = FoodPromotionService.get_by_id(id)
        promotion_model = FoodPromotion(**promotion)
        
        FoodPromotionService.assert_promotion(promotion= promotion_model, check_auth= True)

        if "_id" not in promotion:
            return {"message": "cant find doc promotion", "status": 400}
        
        if "promotionLangs" in promotion:
            for promotion_lang in promotion['promotionLangs']:
                foodPromotionLangsCollection.delete_one({'_id': ObjectId(promotion_lang["_id"])})
        
        foodPromotionsCollection.delete_one({"_id": ObjectId(promotion['_id'])})
        
        return {"message": "remove success!", "status": 200}

            
