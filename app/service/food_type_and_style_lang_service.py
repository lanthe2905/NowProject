from app.model.db import foodTypeAndStyleLangsCollection
from bson import ObjectId

class FoodTypeAndStyleLangService:
    @staticmethod
    def get_by_id(id):
        return foodTypeAndStyleLangsCollection.find_one(id)

    @staticmethod
    def create(payload):
        result = foodTypeAndStyleLangsCollection.insert_one(payload)
        if result.inserted_id is not None:
            return payload
            
        return {"message": "created successfully", "status": 200, "data": FoodTypeAndStyleLangService.get_by_id(result.inserted_id)}

    @staticmethod
    def update(id, payload):
        result =  foodTypeAndStyleLangsCollection.update_one({"_id": ObjectId(id)}, {
            "$set": payload
        })
        if result.matched_count == 0:
            return {"message": "Updated failed", "status": 400}
        return {"message":"updated successfully", "status": 200, "data": FoodTypeAndStyleLangService.get_by_id(id)}
    
    @staticmethod
    def delete(id):
        result =  foodTypeAndStyleLangsCollection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0 :
            return {"message": "deleted not success", "status": 400}
        return {"message": "delete success", "status": 200}
        