import tornado.ioloop
import tornado.web
import json

from database import database

db = database()

try:
    db.create_table()
except:
    pass


class NewProduct(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)

        if 'name' not in data.keys() or 'category' not in data.keys():
            response = {'result': 'error', 'error_message': 'missing product name or category'}
            self.finish(response)

        response = db.insert(data['name'], data['category'])
        self.finish(response)

class Product(tornado.web.RequestHandler):
    def put(self, id=None ):
        data = json.loads(self.request.body)
        if id == None or 'name' not in data.keys() or 'category' not in data.keys():
            response = {'result': 'error', 'error_message': 'missing product id or name or category'}
            self.finish(response)

        response = db.update(id, data['name'], data['category'])
        self.finish(response)

    def delete(self, id=None):
        print(type(id), id)
        if id == None:
            response = {'result': 'error', 'error_message': 'missing product id'}
            self.finish(response)

        response = db.delete(id)
        self.finish(response)

    def get(self, id=None):
        if id == None:
            response = {'result': 'error', 'error_message': 'missing product id'}
            self.finish(response)

        response = db.get_by_id(id)
        self.finish(response)


class Products(tornado.web.RequestHandler):
    def get(self):
        response = db.get_all()
        self.finish(response)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/product", NewProduct),
        (r"/products", Products),
        (r"/([^/]+)?", Product),

    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(1234)
    tornado.ioloop.IOLoop.current().start()