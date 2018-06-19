from apiController import *
from view import *
from xhtml2pdf import pisa
import cStringIO as StringIO

class jsonExportView(view):

    def get(self):

        return apiController.jsonExport(self.urlArgs)

class feedView(view):
    def get(self):
        logger.info('[INFO] feedView reached')

        self.setContentType('text/atom')

        tim = datetime.datetime.now()
        date = tim.strftime("%Y-%m-%dT%XZ")

        products = []
        products = productController.getProductsByFilter(None, "date_added", "desc", "")
        products = products[0:20]

        for i in range(0, len(products)):
            products[i].condition = productController.getConditionStr(products[i].condition)
            products[i].ownerID = userController.getUserInstanceById(products[i].ownerID).username

        self.addItemToContext("localhost:8000", 'domain', True)
        self.addItemToContext(date, 'dateUpdated', True)
        self.addItemToContext(products, 'products', True)
        content = self.renderTemplate('feed.atom')
        return content

class xmlView(view):
    def get(self):
        logger.info('[INFO] feedView reached')

        self.setContentType('text/xml')

        tim = datetime.datetime.now()
        date = tim.strftime("%Y-%m-%dT%XZ")

        products = []
        products = productController.getProductsByFilter(None, "date_added", "desc", "")

        for i in range(0, len(products)):
            products[i].condition = productController.getConditionStr(products[i].condition)
            products[i].ownerID = userController.getUserInstanceById(products[i].ownerID).username

        self.addItemToContext("localhost:8000", 'domain', True)
        self.addItemToContext(date, 'dateUpdated', True)
        self.addItemToContext(products, 'products', True)
        content = self.renderTemplate('products.xml')
        return content

class pdfView(view):
    def get(self):
        logger.info('[INFO] feedView reached')

        tim = datetime.datetime.now()
        date = tim.strftime("%Y-%m-%dT%XZ")

        products = []
        products = productController.getProductsByFilter(None, "date_added", "desc", "")

        for i in range(0, len(products)):
            products[i].condition = productController.getConditionStr(products[i].condition)
            products[i].ownerID = userController.getUserInstanceById(products[i].ownerID).username

        self.addItemToContext("localhost:8000", 'domain', True)
        self.addItemToContext(date, 'dateUpdated', True)
        self.addItemToContext(products, 'products', True)
        content = self.renderTemplate('products_html')

        self.setContentType('application/pdf')

        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(content), dest=result)
        return result.getvalue()