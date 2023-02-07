from flask_restx import Resource
from flask import request
from ..dto.user_dto  import UserDto
from app.util.helpers import  _success
from app.service.user_service import UserService
from app.util.helpers import _throw
import inspect

api = UserDto.api
_resp = UserDto.user_fields
_user = UserDto.user
_user_login = UserDto.user_login_form

@api.route('/getLists')
class UserList(Resource):
    @api.doc(params={'page': '1', 'pageSize' :'50'})
    # @jwt_required()
    def get(self):
        try:
            payload = request.args
            page =  payload.get('page') if payload.get('page')  else 1 
            pageSize = payload.get('pageSize') if payload.get('page')  else 50

            return _success(inspect.stack(),UserService.getLists(page , pageSize ))
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

@api.route('/getUserById/<id>')
@api.doc(params={'id': 'user id'})
class UserById(Resource):
    @api.doc('')
    @api.marshal_with(_user)
    def get(self, id):
        return _success(inspect.stack(), UserService.get_by_id(id))   