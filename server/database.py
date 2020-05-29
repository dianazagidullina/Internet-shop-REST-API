from bson.objectid import ObjectId
from pymongo import MongoClient
from config import MONGO_HOST, MONGO_PORT

class database:
    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client.db
        self.table = self.db.products
        print("creating database...")


    def insert(self, name, category):
        """ insert a new product into the products table """
        try:
            product = self.table.insert_one({"name": name, "category": category})
            response = {'result': 'ok', 'id': str(product.inserted_id)}
        except Exception as e:
            response = {'result': 'error', 'error_message': '{}'.format(e)}
        return response


    def update(self, id, name, category):
        """ update product name and category based on the product id """
        if (self.get_by_id(id)['result'] != 'ok'):
            response = {'result': 'error', 'error_message': 'no product with such id'}
            return response

        obj_id = ObjectId(id)
        self.table.update_one({"_id": obj_id}, {"$set": {"name": name, "category": category}})
        response = {'result': 'ok'}
        return response

    def delete(self, id):
        """ delete product by product id """

        if (self.get_by_id(id)['result'] != 'ok'):
            response = {'result': 'error', 'error_message': 'no product with such id'}
            return response

        obj_id = ObjectId(id)
        self.table.delete_one({'_id': obj_id})
        response = {'result': 'ok'}
        return response

    def get_by_id(self, id):
        """ get product name and category based on the product id """
        obj_id = ObjectId(id)
        product = self.table.find_one({"_id": obj_id})
        if product == None:
            response = {'result': 'error', 'error_message': 'no product with such id'}
            return response
        product["_id"] = str(product["_id"])
        response = {'result': 'ok', 'product': product}
        return response

    def get_all(self):
        """ get all products from the products table"""
        products = list(self.table.find({}))
        for product in products:
            product["_id"] = str(product["_id"])
        response = {'result': 'ok', 'products': products}
        return response


