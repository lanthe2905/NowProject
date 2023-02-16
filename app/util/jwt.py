import jwt
from app.util.const import Const
from datetime import timedelta, datetime, timezone
from app.model import db
from flask import request
from bson import ObjectId
def decode_token(token, secrect_key):
    data = jwt.decode(
        token = token ,secrect_key= secrect_key, options= {"verify_exp": False}
    )
    return data
   

def create_access_token(payload):
    if isinstance(payload,dict) == False: return False
    utc_exp = datetime.now() + timedelta(minutes= Const.JWT_CONFIG.SECRET_KEY_TIME_M )
    timestamp_exp = datetime.timestamp(utc_exp)
    payload['exp'] = timestamp_exp
    return jwt.encode(payload= payload, key= Const.JWT_CONFIG.SECRET_KEY)

def create_refresh_token(payload):
    if isinstance(payload,dict) == False: return False
    utc_exp = datetime.now() + timedelta(days= Const.JWT_CONFIG.REFRESH_EXPIRES_TIME_D)
    timestamp_exp = datetime.timestamp(utc_exp)
    payload['exp'] = timestamp_exp
    return jwt.encode(payload= payload, key= Const.JWT_CONFIG.REFRESH_KEY)

def get_current_user():
    auth_header = request.headers.get("Authorization")
    if auth_header is None: 
        raise Exception('Required bearer token')
        
    bear_token = auth_header.split(' ').pop()
    payload = verify_token(bear_token, Const.JWT_CONFIG.SECRET_KEY)
    user = db.userCollection.find_one({"_id": ObjectId(payload['user_id'])})

    return user

def verify_token(token, secret_key):
    return jwt.decode(
       token,  secret_key, algorithms= "HS256", options={"verify_exp": True}
    )
