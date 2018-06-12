from view import *
import datetime
from databaseController import *

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

        lista = [info["username"],info["password"],info["first_name"],info["last_name"],info["email"],info["country"],info["state"],info["city"],info["adress_1"],info["adress_2"],info["zip_code"],info["contact_info"],info["cell_number"],info["session_id"],info["status"]]

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
                    'session_id' : 'asdasd',
                    'status' : 'ok'}


        databaseController.insertIntoUser(userData)

        return 'ok'


class addProductView(view):
    def get(self):
        debug('[INFO] addProductView')

        prodData = {'title' : 'Air guitar Epiphone les paul vasilescu',
                    'description' : 'cea mia mijtoui s mora mama meu k ii sm3k mkatzash lorem gipsum jajaj jaj as lal qea j2qj h n asdasd, asdasldkj',
                    'condition' : 3,
                    'country' : 'vaslui kong',
                    'state' : 'triburile romane unite',
                    'city' : 'vaslui',
                    'is_auction' : True,
                    'price' : 399,
                    'shipping_type' : 'Malaysia Airways',
                    'shipping_price' : 429,
                    'date_added' : datetime.datetime(1999, 10, 10),
                    'date_expires' : datetime.datetime(2001, 10, 10),
                    'category' : 'lol nu stiu',
                    'subcategory' : 'yes',
                    'views' : 420,
                    'image' : 'THIS IS IMAGE DATA YES',
                    'user_id' : '123'}

        debug('done')

        databaseController.insertIntoProductdata(prodData)
        debug('done')

        return 'done'
