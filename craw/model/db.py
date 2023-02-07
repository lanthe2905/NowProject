from pymongo import MongoClient
import os 
from dotenv import load_dotenv
load_dotenv()
client = MongoClient(os.getenv("MONGO"))
print(client.server_info())
db = client['Now']
nowRawCollection = db['nowRaw']
userCollection = db['users']
foodDrinksCollection = db['foodDrinks']
foodPlacesCollection = db['foodPlaces']
foodVideosCollection = db['foodVideos']
foodLocationsCollection = db['foodLocations']
foodCategoriesCollection = db['foodCategories']
foodCategoryLangsCollection = db['foodCategoryLangs']
foodOpenTimesCollection = db['foodOpenTimes']
foodImagesCollection = db['foodImages']
foodSocialNetworkCollection = db['foodSocialNetworks']
foodTypeAndStyleLangsCollection = db['foodTypeAndStyleLangsCollection']
foodTypeAndStylesCollection = db['foodTypeAndStyles']
foodPromotionsCollection = db['foodPromotions']
foodReviewsCollection = db['foodReviews']
foodReviewReportsCollection = db['foodReviewReports']


def dropCollection():
    # userCollection.drop()
    foodDrinksCollection.drop()
    foodPlacesCollection.drop()
    foodVideosCollection.drop()
    foodLocationsCollection.drop()
    foodCategoriesCollection.drop()
    foodCategoryLangsCollection.drop()
    foodOpenTimesCollection.drop()
    foodSocialNetworkCollection.drop()
    foodTypeAndStyleLangsCollection.drop()
    foodTypeAndStylesCollection.drop()
    foodPromotionsCollection.drop()
    foodReviewsCollection.drop()
    foodReviewReportsCollection.drop()