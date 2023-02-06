from app.model.db import foodTypeAndStyleLangsCollection
from bson import ObjectId

class FoodTypeAndStyleLangService:
    @staticmethod
    def get_by_id(id):
        return foodTypeAndStyleLangsCollection.find_one(id)

    @staticmethod
    def create(payload):
        is_success = foodTypeAndStyleLangsCollection.insert_one(payload).acknowledged
        if is_success is True:
            return payload
        raise Exception("Can't create food type langs") 

    @staticmethod
    def update(id, payload):
        return foodTypeAndStyleLangsCollection.update_one({"_id": ObjectId(id)}, {
            "$set": payload
        })
    
    @staticmethod
    def delete(id):
        return foodTypeAndStyleLangsCollection.delete_one({"_id": ObjectId(id)}).acknowledged