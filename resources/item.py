# from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
# import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
    type=int,
    required=True,
    help="Every item needs a store_id!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists"}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            # item.insert()
            item.save_to_db()
        except:
             return{"message": "An error occurred inserting the item"}, 500


        return item.json(), 201

    def delete(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))

        # connection.commit()
        # connection.close()
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        # print(request_data)
        # item = next(filter(lambda x: x['name']==name,items),None)
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                # updated_item.insert()
                item = ItemModel(name, data['price'], data['store_id'])
            except:
                return{"message": "An error occurred inserting the item"}, 500
        else:
            try:
                # updated_item.update()
                item.price = data['price']
                item.store_id = data['store_id']

            except:
                return{"message": "An error occurred updating the item"}, 500
        item.save_to_db()
        # return updated_item.json(), 201
        return item.json(), 201


class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items"
        # result = cursor.execute(query)

        # items=[]
        # for row in result:
        #     items.append({'name': row[1], 'price': row[2]})

        # connection.commit()
        # connection.close()

        # return {'items': [item.json() for item in ItemModel.query.all()]}
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}