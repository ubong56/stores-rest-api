
import os
import sys

sys.path

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity


from security import authenticate, identity as identity_function
from resources.user import UserRegister
from resources.item import Item, ItemList
from datetime import timedelta
from resources.store import Store, StoreList

app = Flask(__name__)
app.secret_key = 'composition'
api = Api(app)


# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_UR','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# config JWT auth key name to be 'email' instead of default 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
jwt = JWT(app, authenticate, identity_function)




@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
 return jsonify({
 'access_token': access_token.decode('utf-8'),
 'user_id': identity.id
 })

@jwt.jwt_error_handler
def customized_error_handler(error):
 return jsonify({
 'message': error.description,
 'code': error.status_code
 }), error.status_code



api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

# app.run(port=5000, debug=True)

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port = 5000, debug=True)  # important to mention debug=True
