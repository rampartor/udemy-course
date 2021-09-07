from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel

BLANK_ERROR = "'{}' cannot be blank"
NAME_ALREADY_EXISTS = "item {} is already exists"
ERROR_INSERTING = "an error occurred inserting item"
ITEM_NOT_FOUND = "item not found"
ITEM_DELETED = "item deleted"


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help=BLANK_ERROR.format("price")
    )
    parser.add_argument(
        "store_id", type=int, required=True, help=BLANK_ERROR.format("store_id")
    )

    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @jwt_required(refresh=True)
    def post(cls, name: str):
        if ItemModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return item.json(), 201

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED}

        return {"message": ITEM_NOT_FOUND}

    @classmethod
    def put(cls, name: str):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, **data)
        else:
            item["price"] = data["price"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {"items": [item.json() for item in ItemModel.find_all()]}, 200
