from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()

        return {"message": "store not found"}, 404

    def post(self, name: str):
        if StoreModel.find_by_name(name):
            return {
                "message": 'a store with name "{}" is already exists'.format(name)
            }, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "an error occurred while created store"}, 500

        return store.json(), 201

    def delete(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "store deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.find_all()]}
