import requests
import json 
from app.model.db import foodPlacesCollection,foodCategoriesCollection, foodCategoryLangsCollection, foodTypeAndStylesCollection, foodTypeAndStyleLangsCollection, foodLocationsCollection
from app.model.model import FoodPlaces,FoodCategories,FoodImages,FoodOpenTimes,FoodTypeAndStyleLangs, FoodTypeAndStyles, FoodLocations
from app.util.time import  time_to_second, string_to_date
from craw.model.db import nowRawCollection
from bson.objectid import ObjectId
import traceback, os

class DeliveryService:

    @staticmethod
    def rawToDB(delivery, userID, cloneImages = False):
        foodPlace = {
            "userID" : ObjectId(userID),
            "oldRestaurentID" : delivery['id'],
            "name" : delivery['name'],
            "phone" : delivery['phones'][0],
            # "email" : delivery['email'],
            "website" : delivery['url'],
            "images" : json.dumps([delivery['photos'][-1]['value'].split('/')[-1]]),
            "openTimes": None,
        }
        if delivery['operating'] is not None and delivery['operating']['status'] == 1: 
            openTime = string_to_date(delivery['operating']['open_time'])
            closeTime = string_to_date(delivery['operating']['close_time'])
            openTimes = {
                    "MONDAY": [
                        {
                            "OPEN": time_to_second(openTime),
                            "CLOSE": time_to_second(closeTime)
                        } 
                    ],
                    "TUESDAY": [
                        {
                            "OPEN": time_to_second(openTime),
                            "CLOSE": time_to_second(closeTime)
                        } 
                    ],
                    "WEDNESDAY": [
                        {
                            "OPEN": time_to_second(openTime),
                            "CLOSE": time_to_second(closeTime)
                        } 
                    ],
                    "THURSDAY": [
                        {
                            "OPEN": time_to_second(openTime),
                            "CLOSE": time_to_second(closeTime)
                        } 
                    ],
                    "FRIDAY": [
                        {
                            "OPEN": time_to_second(openTime),
                            "CLOSE": time_to_second(closeTime)
                        } 
                    ],
                    "SATURDAY": [
                        {
                            "OPEN": time_to_second(openTime),
                            "CLOSE": time_to_second(closeTime)
                        } 
                    ],
                    "SUNDAY": [
                        {
                            "OPEN": time_to_second(openTime),
                            "CLOSE": time_to_second(closeTime)
                        } 
                    ]
                }
            foodPlace['openTimes'] = json.dumps(openTimes)
            
        foodPlace = FoodPlaces(**foodPlace)
        id = foodPlacesCollection.insert_one(foodPlace.to_json()).inserted_id

        for category in delivery['categories']:
            id = foodCategoriesCollection.insert_one({
                "foodPlaceID": id
            }).inserted_id

            foodCategoryLangsCollection.insert_one({
                "foodCategoryID": id,
                "lang": "vn",
                "categoryName": category
            })

        if delivery['location_url'] is not None: 
            foodLocationsCollection.insert_one({
                "foodPlaceID": id,
                "address": delivery['address'],
                "city": delivery["location_url"],
                "country": "Việt Nam"
            })

        if  cloneImages is True:
            if delivery['photos'] is not None:
                length = len(delivery['photos'])
                photo = delivery['photos'][-1]
                response = requests.get(photo['value'])
                pathUrl = f"app/static/photos/{photo['value'].split('/')[-1]}"
                os.makedirs(os.path.dirname(pathUrl), exist_ok=True)
                with open(pathUrl, "wb+") as f: 
                        f.write(response.content)
