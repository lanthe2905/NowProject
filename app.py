#document :
#  
# https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
# https://www.imaginarycloud.com/blog/flask-python/

from flask_jwt_extended import JWTManager
from app import create_app, blueprint
from app.service.user_service import UserService
from app.util.i18n import run as translate, beforeRequest as i18nBeforeRequest

app = create_app(__name__)
jwt = JWTManager(app)
app.register_blueprint(blueprint)

@app.before_request
def before_request():
    i18nBeforeRequest() 

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = UserService.get_by_id(identity)
    return user 

if __name__ == '__main__':  
    translate(__file__+"/translate/lang")
    app.run(debug=True)
  
