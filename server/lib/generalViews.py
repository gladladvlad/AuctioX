from view import *
from mimetypes import MimeTypes

from productController import *


class publicFileView(view):

    skipUserValidation = True

    def get(self):
        logger.info("[VIEW] publicFileView")


        filePath = "..{0}".format(self.request.path.replace('/', '\\'))
        try:
            self.setContentType(MimeTypes().guess_type(self.request.path)[0])
            content = open(filePath, 'rb').read()
        except:
            raise Exception
        return content


class homepageView(view):
    def get(self):
        logger.info("[VIEW] homepageView")

        self.setContentType('text/html')

        if "category" in self.urlArgs:
            category = self.urlArgs['category']
        else:
            category = "newest"

        products = []

        if category == "newest":
            category = "Newest listings"
            products = productController.getProductsByFilter(None, "date_added", "desc", "")
        elif category == "mostPopular":
            category = "Most popular listings"
            products = productController.getProductsByFilter(None, "views", "desc", "")
        elif category == "clothingAndAccessories":
            category = "Clothing & Accessories"
            products = productController.getProductsByFilter({"category": category}, "date_added", "desc", "")
        elif category == "electronics":
            category = "Electronics"
            products = productController.getProductsByFilter({"category": category}, "date_added", "desc", "")
        elif category == "homeAndOutdoors":
            category = "Home & Outdoors"
            products = productController.getProductsByFilter({"category": category}, "date_added", "desc", "")
        elif category == "vehicles":
            category = "Vehicles"
            products = productController.getProductsByFilter({"category": category}, "date_added", "desc", "")
        elif category == "collectiblesAndArt":
            category = "Collectibles & Art"
            products = productController.getProductsByFilter({"category": category}, "date_added", "desc", "")
        elif category == "consumables":
            category = "Consumables"
            products = productController.getProductsByFilter({"category": category}, "date_added", "desc", "")

        products = productController.getProductImages(products)
        products = products[0:13]

        self.addComponentToContext('home_styles.html', 'style', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('home_homebar.html', 'homebar', True)
        self.addComponentToContext('footer.html', 'footer', True)

        self.addItemToContext(category, 'category', True)
        self.addItemToContext(products, 'products', True)

        content = self.renderTemplate('home.html')

        return content


class globalFavicon(view):

    def get(self):
        logger.info("[TEST VIEW] globalFavicon")
        return open("..\\public\\static\\png\\favicon.png", "rb").read()


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