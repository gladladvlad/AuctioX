import views
from jinja2 import Template

class jinjatest(views.view):

    def get(self):
        self.addComponentToContext('navbar.html')
        return self.renderTemplate('jinjatest.html')

class globalFavicon(views.view):

    def get(self):
        return open("..\\public\\static\\png\\favicon.png", "rb").read()
