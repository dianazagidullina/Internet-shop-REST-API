import tornado.ioloop
import tornado.web
import json

from database import database
from authconfig import AUTH_PORT

db = database()


class SignUp(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)

        if 'login' not in data.keys() or 'password' not in data.keys():
            response = {'result': 'error', 'error_message': 'missing login or password'}
            self.finish(response)

        response = db.signup(data['login'], data['password'])
        self.finish(response)


class SignIn(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)

        if 'login' not in data.keys() or 'password' not in data.keys():
            response = {'result': 'error', 'error_message': 'missing login or password'}
            self.finish(response)

        response = db.signin(data['login'], data['password'])
        self.finish(response)


class Validate(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)

        if 'access_token' not in data.keys():
            response = {'result': 'error', 'error_message': 'missing access token'}
            self.finish(response)

        response = db.validate(data['access_token'])
        self.finish(response)


class Refresh(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)

        if 'refresh_token' not in data.keys():
            response = {'result': 'error', 'error_message': 'missing refresh token'}
            self.finish(response)

        response = db.refresh(data['refresh_token'])
        self.finish(response)



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/signup", SignUp),
        (r"/signin", SignIn),
        (r"/validate", Validate),
        (r"/refresh", Refresh),

    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(AUTH_PORT)
    tornado.ioloop.IOLoop.current().start()