from pymongo import MongoClient
from authconfig import MONGO_HOST, MONGO_PORT
from os import urandom
import time

REFRESH_TIME_LIMIT = 300
ACCESS_TIME_LIMIT = 60

class database:
    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client.db
        self.table = self.db.users
        print("creating authorization database...")


    def signup(self, login, password):
        if self.exists(login):
            return {'result': 'error', 'error_message': 'user with such login already exists'}

        try:
            self.table.insert_one({"login": login, "password": password})
            response = {'result': 'ok'}
        except Exception as e:
            response = {'result': 'error', 'error_message': '{}'.format(e)}
        return response


    def signin(self, login, password):
        if not self.exists(login):
            return {'result': 'error', 'error_message': 'no user with such login'}

        try:
            user = self.table.find_one({"login": login})
            if (user["password"] != password):
                return {'result': 'error', 'error_message': 'wrong login or password'}
            access_token = urandom(32).hex()
            refresh_token = urandom(32).hex()
            self.table.update_one({'login': login},
                                  {'$set': {'access_token': access_token, 'refresh_token': refresh_token,
                                            'time': int(round(time.time()))}})
            response = {'result': 'ok', 'access_token': access_token, 'refresh_token': refresh_token}
        except Exception as e:
            response = {'result': 'error', 'error_message': '{}'.format(e)}
        return response

    def validate(self, access_token):
        user = self.table.find_one({'access_token': access_token})
        if (not user):
            return {'result': 'error', 'error_message': 'Invalid access token'}
        if (int(round(time.time())) - user['time'] > ACCESS_TIME_LIMIT):
            return {'result': 'error', 'error_message': 'Access token expired'}
        return {'result': 'ok'}


    def refresh(self, refresh_token):
        try:
            user = self.table.find_one({"refresh_token":refresh_token})
            if (int(round(time.time())) - user['time'] > REFRESH_TIME_LIMIT):
                return {'result': 'error', 'error_message': 'Refresh token expired'}

            access_token = urandom(32).hex()
            refresh_token = urandom(32).hex()
            self.table.update_one({'login': user['login']},
                                  {'$set': {'access_token': access_token, 'refresh_token': refresh_token,
                                            'time': int(round(time.time()))}})
            response = {'result': 'ok', 'access_token': access_token, 'refresh_token': refresh_token}
        except Exception as e:
            response = {'result': 'error', 'error_message': '{}'.format(e)}
        return response

    def exists(self, login):
        user = self.table.find_one({'login': login})
        return (user != None)


