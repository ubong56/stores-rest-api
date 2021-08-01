from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel


class Item(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404



    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)},400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201



    # @jwt_required()
    @classmethod
    @jwt_required()
    def delete(cls, name):
        # connection = sqlite3.connect('C:/Users/hb21315/PycharmProjects/test/rest-apis-flask-python-master/section_6_test/assign/data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()
        #
        # return {'message': 'Item deleted'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()



        # if item is None:
        #     item = ItemModel(name, data['price'])
        #     try:
        #         updated_item.insert()
        #     except:
        #         return {"message": "An error occurred inserting the item."},500
        # else:
        #     try:
        #         updated_item.update()
        #     except:
        #         return {"message": "An error occurred updating the item."},500
        # return updated_item.json()




class ItemList(Resource):
    TABLE_NAME = 'items'

    def get(cls):
        # connection = sqlite3.connect('C:/Users/hb21315/PycharmProjects/test/rest-apis-flask-python-master/section_6_test/assign/data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM {table}".format(table=cls.TABLE_NAME)
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        # connection.close()
        #
        # return {'items': items}
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

