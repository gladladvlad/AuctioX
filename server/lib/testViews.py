from view import *
import datetime
from databaseController import *
import os

class jinjatest(view):

    def get(self):
        self.addComponentToContext('navbar.html')
        self.addItemToContext('Jinja Test Page', 'title')
        return self.renderTemplate('jinjatest.html')


class globalFavicon(view):

    def get(self):
        return open("..\\public\\static\\png\\favicon.png", "rb").read()

class addUserView(view):
    def get(self):
        debug('[INFO] addUserView')


        userData = {'username' : 'gunondwarf',
                    'password' : 'pass123',
                    'first_name': 'gigi',
                    'last_name': 'vasile',
                    'email' : 'asd@mail.com',
                    'country' : 'yes',
                    'state' : 'tes',
                    'city' : 'abcd',
                    'adress_1' : 'str 1',
                    'adress_2' : 'str 2',
                    'zip_code' : '1230',
                    'contact_info' : 'llakjsdlsakjdlask',
                    'cell_number' : '123123123',
                    'salt' : os.urandom(16),
                    'status' : 'ok'}


        databaseController.insertIntoUser(userData)

        return 'ok'


class getUserView(view):
    def get(self):
        debug('[INFO] addUserView')

        user = databaseController.getUserByUsername('gunondwarf')

        return user


class addProductView(view):
    def get(self):
        debug('[INFO] addProductView')

        prodData = {'title' : 'Air guitar Epiphone les paul vasilescu',
                    'description' : 'cea mia mijtoui s mora mama meu k ii sm3k mkatzash lorem gipsum jajaj jaj as lal qea j2qj h n asdasd, asdasldkj',
                    'conditie' : 3,
                    'country' : 'vaslui kong',
                    'state' : 'triburile romane unite',
                    'city' : 'vaslui',
                    'is_auction' : 1,
                    'price' : 399,
                    'shipping_type' : 'Malaysia Airways',
                    'shipping_price' : 429,
                    'date_added' : datetime.datetime.now(),
                    'date_expires' : datetime.datetime.now(),
                    'category' : 'lol nu stiu',
                    'subcategory' : 'yes',
                    'views' : 420,
                    'image' : [bytearray('asdasdasd')],
                    'user_id' : 1}

        databaseController.insertIntoProductdata(prodData)

        return 'done'
