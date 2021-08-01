import sys
sys.path.append(r"C:\Users\hb21315\PycharmProjects\test\rest-apis-flask-python-master\section4")
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# config JWT auth key name to be 'email' instead of default 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
jwt = JWT(app, authenticate, identity_function)

@app.before_first_request
def create_tables():
    db.create_all()



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

# class Student(Resource):
#     def get (self, name):
#         return {'student': name}
#
#
# api.add_resource(Student, '/student/<string:name>')
#
# app.run(port=5000)

# items = []
#
# class Item(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('price',
#                         type=float,
#                         required=True,
#                         help="This field cannot be left blank!"
#                         )
#
#     @jwt_required()
#     def get(self, name):
#         # for item in items:
#         #     if item['name'] == name:
#         #         return item
#         # return {'item': None}, 404
#         item = next(filter(lambda x: x['name'] == name, items), None)
#
#         return {'item':  item}, 200 if item else 404
#
#     def post(self, name):
#         # data = request.get_json()
#         if next(filter(lambda x: x['name'] == name, items), None) is not None:
#             return {'message': "An item with name '{}' already exists.".format(name)}, 400
#         # data = request.get_json()
#         data = Item.parser.parse_args()
#
#         item = {'name': name, 'price': data['price']}
#         items.append(item)
#         return item, 201
#
#     @jwt_required()
#     def delete(self, name):
#         global items
#         items = list(filter(lambda x: x['name'] != name, items))
#         return {'message': 'Item deleted'}
#
#     @jwt_required()
#     def put(self, name):
#         data = Item.parser.parse_args()
#         # data = request.get_json()
#         # Once again, print something not in the args to verify everything works
#         item = next(filter(lambda x: x['name'] == name, items), None)
#         if item is None:
#             item = {'name': name, 'price': data['price']}
#             items.append(item)
#         else:
#             item.update(data)
#         return item
#
# class ItemList(Resource):
#     def get(self):
#         return {'items': items}

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
