from flask_restx import Resource
from flask import request
from ..dto.user_dto  import UserDto
from app.service.user_service import UserService
from app.util.helpers import  _success, _throw
from app.util.redis import jwt_redis_blocklist
from app.util.const import Const
from app.util.middleware import verify_refresh_token
from app.util.jwt import  create_access_token, create_refresh_token
from datetime import timedelta
import inspect

api = UserDto.api
_resp = UserDto.user_fields
_user = UserDto.user
_user_login = UserDto.user_login_form

@api.route('/get_list')
class UserList(Resource):
    @api.doc(params={'page': '1', 'pageSize' :'50'})
    def get(self):
        try:
            payload = request.args
            page =  payload.get('page') if payload.get('page')  else 1 
            pageSize = payload.get('pageSize') if payload.get('page')  else 50
            return _success(inspect.stack(),UserService.get_lists(page , pageSize ))
        except Exception  as e:
            _throw(e)

@api.route('/login')
class Login(Resource):
    @api.expect(_user_login, validate=True)
    def post(self):
        data = request.get_json()
        return _success(inspect.stack(), UserService.authenticate(data['username'],data['password']))

@api.route('/register')
class Register(Resource):
    @api.expect(_resp)
    def post(self):
        try:
            data = request.get_json()
            return _success(inspect.stack(), UserService.register(data))
        except Exception as e:
            _throw(e)

@api.route('/get_by_id/<id>')
@api.doc(params={'id': 'user id'})
class UserById(Resource):
    @api.marshal_with(_user)
    def get(self, id):
        return _success(inspect.stack(), UserService.get_by_id(id))   


@api.route('/refresh_token')
class RefreshToken(Resource):
    @verify_refresh_token
    def post(self):
        payload = request.payload
        user = UserService.get_by_id(payload['user_id'])
        if user is None: 
            return {"message": "Token not valid", "status": 403}, 200
        refresh_token = request.get_json()['refresh_token']
        user['_id'] = str(user['_id'])
        refresh_token_redis = jwt_redis_blocklist.get(user['_id'] )

        if refresh_token_redis != refresh_token:
            return {"message": "Token not valid", "status": 403}, 200
        
        refresh_token = create_refresh_token(payload={"user_id": user['_id']})
        access_token = create_access_token(payload={"user_id": user['_id']})
        jwt_redis_blocklist.setex(name=user['_id'],value= refresh_token, time= timedelta(days= Const.JWT_CONFIG.REFRESH_EXPIRES_TIME_D))
        
        return {"status": 200, "access_token": access_token, "refresh_token": refresh_token}

@api.route('/logout')
class Logout(Resource):
    def post(self):
        pass