from pymongo import MongoClient
from flask_pymongo import PyMongo
import os 
from dotenv import load_dotenv
load_dotenv()
client = MongoClient(os.getenv("MONGO"))
mongo = PyMongo()
db = client.Now
userCollection = db.users
foodDrinksCollection = db.foodDrinks
foodPlacesCollection = db.foodPlaces
foodVideosCollection = db.foodVideos
foodLocationsCollection = db.foodLocations
foodCategoriesCollection = db.foodCategories
foodCategoryLangsCollection = db.foodCategoryLangs
foodOpenTimesCollection = db.foodOpenTimes
foodImagesCollection = db.foodImages
foodSocialNetworkCollection = db.foodSocialNetworks
foodTypeAndStyleLangsCollection = db.foodTypeAndStyleLangs
foodTypeAndStylesCollection = db.foodTypeAndStyles
foodPromotionsCollection = db.foodPromotions
foodPromotionLangsCollection = db.foodPromotionLangs
foodReviewsCollection = db.foodPreviews
foodReviewReportsCollection = db.foodReviewReports


def initialize_db(app):
    mongo.init_app(app)

def dropCollection():
    userCollection.drop({})
    foodDrinksCollection.drop({})
    foodPlacesCollection.drop({})
    foodVideosCollection.drop({})
    foodLocationsCollection.drop({})
    foodCategoriesCollection.drop({})
    foodCategoryLangsCollection.drop({})
    foodOpenTimesCollection.drop({})
    foodImagesCollection.drop({})
    foodSocialNetworkCollection.drop({})
    foodTypeAndStyleLangsCollection.drop({})
    foodTypeAndStylesCollection.drop({})
    foodPromotionsCollection.drop({})
    foodReviewsCollection.drop({})
    foodReviewReportsCollection.drop({})