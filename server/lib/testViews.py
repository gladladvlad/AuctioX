from view import *

class jinjatest(view):

    def get(self):
        self.addComponentToContext('navbar.html')
        self.addItemToContext('Jinja Test Page', 'title')
        return self.renderTemplate('jinjatest.html')


class globalFavicon(view):

    def get(self):
        return open("..\\public\\static\\png\\favicon.png", "rb").read()
