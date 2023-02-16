from flask_restx import Namespace, fields
class FoodPlaceDto:
    api =  Namespace("FoodPromotion",  description="Api food promotion document")
    food_promotion_fields = api.model("FoodPromotionModel", {
        "_id": fields.String(),
        "foodPLaceID":fields.String(),
        "foodPromotionCode": fields.String(),
        "expireAt": fields.String(),
        "createTime": fields.String(),
    })



