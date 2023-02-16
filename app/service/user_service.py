from app.model.db import userCollection
from app.model.model import Users
from ..util.helpers import _throw
from ..util.redis import jwt_redis_blocklist
from ..util.const import Const
from ..util.jwt import create_access_token, create_refresh_token
from bson.objectid import ObjectId
import bcrypt
from datetime import timedelta
class UserService:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_hashed_password(plain_text_password):
        # Hash a password for the first time
        # https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
        #   (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password.encode('utf8'), bcrypt.gensalt())

    @staticmethod
    def check_password(plain_text_password, hashed_password):
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        # https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def authenticate(username: str, password: str):
        if(not username or not password):
            _throw(Exception('missing field '))
        user = userCollection.find_one({ "username":username })
        user = Users(**user)
     
        if user is None or UserService.check_password(password, user.password) == False:
            _throw(Exception('please check your username or password'))
        access_token = create_access_token(payload= {"user_id": str(user.id)})
        refresh_token = create_refresh_token(payload= {"user_id": str(user.id)})

        has_refresh_token = jwt_redis_blocklist.get(name=str(user.id))

        if has_refresh_token == None:
            jwt_redis_blocklist.setex(name=str(user.id),value= refresh_token,time= timedelta(days= Const.JWT_CONFIG.REFRESH_EXPIRES_TIME_D))
            return { "status": 200 ,"access_token": access_token, "refresh_token": refresh_token}
            
        return { "status": 200 ,"access_token": access_token, "refresh_token": has_refresh_token}

    @staticmethod
    def register(data):
        try:
            user = Users(**data)
            user.password = UserService.get_hashed_password(user.password)
            userCollection.insert_one(user.to_bson())
            access_token = create_access_token(payload= {"user_id": user.id})
            refresh_token = create_refresh_token(payload= {"user_id": user.id})
            jwt_redis_blocklist.setex(name=str(user.id),value= refresh_token,time= timedelta(days= Const.JWT_CONFIG.REFRESH_EXPIRES_TIME_D))  
            
            return { "status": 200 ,"access_token": access_token, "refresh_token": refresh_token}
        except Exception as e:
            _throw(e)

    @staticmethod
    def get_lists(page:int = 1, pageSize: int= 30):
        page = int(page)
        pageSize = int(pageSize)
        userList =  userCollection.find().skip((page - 1) * pageSize).limit(pageSize)
        return   list(userList)

    @staticmethod
    def get_by_id(id):
        return userCollection.find_one({"_id": ObjectId(id)})

    @staticmethod
    def get_by_user_name(user_name):
        user=  userCollection.find_one({"username": user_name})
        if user is None:
           raise Exception("Cant find user")
        user = Users(**user)
        return user
