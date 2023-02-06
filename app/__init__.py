from flask import Flask, Blueprint, jsonify
from flask_restx import Api
from app.util.const import Const
from app.model.db import initialize_db
from .controller.user_controller import api as user_namespace
from .controller.food_place_controller import api as food_place_namespace
from .controller.delivery_controller import api as delivery_namespace
from .controller.food_category_controller import api as category_namespace
from .controller.food_types_and_style_controller import api as food_type_style
from app.util.exception import DuplicateDataException
from app.util.jwt import get_exprive_time

blueprint = Blueprint('api',__name__, url_prefix="/api")

@blueprint.app_errorhandler(DuplicateDataException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}


api = Api(blueprint,   authorizations=authorizations)
api.add_namespace(user_namespace,path='/user')
api.add_namespace(food_place_namespace, path="/food_place")
api.add_namespace(delivery_namespace, path="/delivery")
api.add_namespace(category_namespace,path="/category")
api.add_namespace(food_type_style,path="/food_type_style")

def create_app(name="default"):
    app = Flask(name, static_folder="app/static")
    app.config["MONGO_URI"] = "mongodb://localhost:27017/"
    app.config["JWT_SECRET_KEY"] = Const.JWT_CONFIG.SECRET_KEY    

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = get_exprive_time()
    initialize_db(app)
    return app