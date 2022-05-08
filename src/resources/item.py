from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import Item


class ItemRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
       type=str,
       required=True,
       help="This field cannot be left blank!"
    )
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
  
    @jwt_required()
    def get(self, name=None):
        if name:
            item = Item(0, name, None)
            if item.find_by_name():
                return item.to_json(), 200
            else:
                return {'message': 'Item not found'}, 404
        else:
            res = Item.get_items()
            if res:
                return {'items': res}, 200
            else:
                return {'message': 'No items found'}, 404

    def post(self):
        data = ItemRegister.parser.parse_args()
        item = Item(0, data['name'], data['price'])
        if (item.find_by_name()):
            return {"message": "Item already exists"}, 400
        else:
            if (item.insert()):
                return {'item': item.to_json()}, 201
            else:
                return {'message': 'An error occurred inserting the item.'}, 500

    def put(self):
        data = ItemRegister.parser.parse_args()
        item = Item(0, data['name'], data['price'])
        try:
            if (item.find_by_name().price == data['price']):
                return {'message': 'No changes detected'}, 400
        except:
            if (item.find_by_name()):
                item = Item(0, data['name'], data['price'])
                if (item.update()):
                    return {'item updated': item.to_json()}, 202
                else:
                    return {'message': 'An error occurred updating the item.'}, 500
            else:
                if (item.insert()):
                    return {'item': item.to_json()}, 201


    def delete(self, name):
        item = Item(0, name, None)
        if (item.find_by_name()):
            if (item.delete()):
                return {'item deleted': item.to_json()}, 200
            else:
                return {'message': 'An error occurred deleting the item.'}, 500
        else:
            return {'message': 'Item not found'}, 404