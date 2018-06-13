from view import *
from databaseController import *

class product():
    conditionMap = ['new', 'slightly used', 'used', 'broken']

    def __init__(self, newOwnerID, newProductID, newStatus, newTitle, newDesc, newCategory, newSubCategory, newImages, newViews, newCondition, newCountry, newCity, newAuction, newPrice, newShippingType, newShippingPrice, newDateAdded, newDateExpires):
        self.ownerID = newOwnerID
        self.productID = newProductID
        self.status = newStatus
        self.title = newTitle
        self.desc = newDesc
        self.category = newCategory
        self.subCategory = newSubCategory
        self.images = newImages
        self.views = newViews
        self.condition = newCondition
        self.country = newCountry
        self.city = newCity
        self.auction = newAuction
        self.price = newPrice
        self.shippingType = newShippingType
        self.shippingPrice = newShippingPrice
        self.dateAdded = newDateAdded
        self.dateExpires = newDateExpires

    def asDict(self):
        result = dict()
        result = {'ownerID' : str(self.ownerID),
                'productID' : str(self.productID),
                'status' : str(self.status),
                'title' : str(self.title),
                'desc' : str(self.desc),
                'category' : str(self.category),
                'subcategory' : str(self.category),
                'images' : str(self.images),
                'condition' : str(self.condition),
                'country' : str(self.country),
                'city' : str(self.city),
                'auction' : str(self.auction),
                'price' : str(self.price),
                'shippingType' : str(self.shippingType),
                'shippingPrice' : str(self.shippingPrice),
                'dateAdded' : str(self.dateAdded),
                'dateExpires' : str(self.dateExpires)}

        return result

class productController():
    def viewPostData(self, postData):
        debug(postData)

    def getProductsByQuery(self, query):
        #make sure query is string
        query = str(query)

        #get all products from DB
        products = databaseController.getProducts()

        return products

    def getProductById(self, productID):
        prodDB = databaseController.getProductDataById(productID)[0]
        images = databaseController.getImages(productID)

        productResult = product(prodDB[PROD_USER_ID], prodDB[PROD_ID], prodDB[PROD_STATUS], prodDB[PROD_TITLE], prodDB[PROD_DESCRIPTION], prodDB[PROD_CATEGORY], prodDB[PROD_SUBCATEGORY], images, prodDB[PROD_VIEWS], prodDB[PROD_CONDITIE], prodDB[PROD_COUNTRY], prodDB[PROD_CITY], prodDB[PROD_IS_AUCTION], prodDB[PROD_PRICE], prodDB[PROD_SHIPPING_TYPE], prodDB[PROD_SHIPPING_PRICE], prodDB[PROD_DATE_ADDED], prodDB[PROD_DATE_EXPIRES])

        return productResult


productController = productController()
