import tornado.ioloop
import tornado.web
import json


products = {}

class Product:
    def __init__(self, n, id, c):
        self.name = n
        self.id = id
        self.category = c


class CreateHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)


        if 'name' not in data.keys() and 'category' not in data.keys():
            self.set_status(400)
            self.finish("Set the name and the category of the product.")
        if 'name' not in data.keys():
            self.set_status(400)
            self.finish("Set the name of the product.")
        if 'category' not in data.keys():
            self.set_status(400)
            self.finish("Set the category of the product.")


        if 'id' not in data.keys():
            self.set_status(400)
            self.finish("Set the id of the product.")

        if data['id'] in products:
            self.set_status(400)
            self.finish("There is already product with such id.")




        product = Product(data['name'], data['id'], data['category'])
        products[data['id']] = product



class PrintAllHandler(tornado.web.RequestHandler):
    def get(self):
        all_products = []
        for key in products:
            product = products[key]
            all_products.append({'name': product.name, 'id': product.id, 'category': product.category})
        if len(all_products) == 0:
            self.set_status(400)
            self.finish("No products to print.")

        self.write({'products': all_products})


class DeleteHandler(tornado.web.RequestHandler):
    def delete(self):
        data = json.loads(self.request.body)
        if 'id' not in data.keys():
            self.set_status(400)
            self.finish("Set the id of the product.")
        if data['id'] not in products:
            self.set_status(400)
            self.finish("There is no product with such id.")
        products.pop(data['id'])


class PrintHandler(tornado.web.RequestHandler):
    def get(self):
        data = json.loads(self.request.body)
        if 'id' not in data.keys():
            self.set_status(400)
            self.finish("Set the id of the product.")

        if data['id'] not in products:
            self.set_status(400)
            self.finish("There is no product with such id.")
        product = products.get(data['id'])
        self.write({'name': product.name, 'id': product.id, 'category': product.category})


class EditHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        if 'id' not in data.keys():
            self.set_status(400)
            self.finish("Set the id of the product.")

        id = data['id']
        if data['id'] not in products:
            self.set_status(400)
            self.finish("There is no product with such id.")

        product = products.get(data['id'])

        if 'name' not in data.keys() and 'category' not in data.keys():
            self.set_status(400)
            self.finish("Set the name or the category of the product.")

        if 'name' in data.keys():
            product.name = data['name']

        if 'category' in data.keys():
            product.category = data['category']


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/create", CreateHandler),
        (r"/printall", PrintAllHandler),
        (r"/delete", DeleteHandler),
        (r"/print", PrintHandler),
        (r"/edit", EditHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(1234)
    tornado.ioloop.IOLoop.current().start()