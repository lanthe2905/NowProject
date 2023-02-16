from functools import wraps
from flask import  request, Response
from app.util.jwt import verify_token
from app.util.const import Const
import jwt, traceback

def cookie_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.cookies.get('lang') is None:
            return {'message': 'required cookie "lang"'}
        return f(*args, **kwargs)
    return decorated_function

def verify_access_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try: 
            auth_header = request.headers.get("Authorization")
            if auth_header is None: 
                return {'code': 403,'message': "required auth" }
            bear_token = auth_header.split(' ').pop()
            payload = verify_token(bear_token, Const.JWT_CONFIG.SECRET_KEY)
            if payload == False:
                return {"code": 400, "message": "You cant access in data"}

            request.payload = payload
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError as e:
            return "token expried", 403
        except Exception as e:
            traceback.print_exc()
            return "you cant access data", 403

    return decorated_function
   
def verify_refresh_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try: 
            payload = request.get_json()
            bear_token = payload['refresh_token'] if 'refresh_token' in payload else None
            if bear_token == None: return {"Required refresh token"}, 403

            payload = verify_token(bear_token, Const.JWT_CONFIG.REFRESH_KEY)
            if payload == False or payload == None:
                return {"code": 400, "message": "You cant access in data"}
            request.payload = payload
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError as e:
            return "token expried", 403
        except Exception as e:
            traceback.print_exc()
            return "you cant access data", 403

    return decorated_function