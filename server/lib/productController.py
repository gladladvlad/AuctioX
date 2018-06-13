from view import *
from databaseController import *

class product():
    conditionMap = ['new', 'slightly used', 'used', 'broken']

    def __init__(self, newOwnerID, newProductID, newStatus, newTitle, newDesc, newCategory, newSubCategory, newImages, newViews, newCondition, newCountry, newCity, newAuction, newPrice, newCurrency, newShippingType, newShippingPrice, newDateAdded, newDateExpires):
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
        self.currency = newCurrency
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
                'images' : self.images,
                'condition' : str(self.condition),
                'country' : str(self.country),
                'city' : str(self.city),
                'auction' : str(self.auction),
                'price' : str(self.price),
                'currency' : str(self.currency),
                'shippingType' : str(self.shippingType),
                'shippingPrice' : str(self.shippingPrice),
                'dateAdded' : str(self.dateAdded),
                'dateExpires' : str(self.dateExpires)}

        return result

class productController():
    def viewPostData(self, postData):
        debug(postData)

    def getAllProducts(self):
        return databaseController.getProducts()

    # info <=> {'min_price' : 2,
    #           'max_price' : 5,
    #           'conditie' : 2}
    # order_by <=> string cu campu' dupa care ordonam
    # how <=> asc/desc
    # query <=> string
    def getProductsByFilter(self, info, order_by, how, query):
        #get all products from DB
        debug('===========================')
        debug(info)
        products = databaseController.getProductsByFilter(info, order_by, how, query)

        debug(products)

        return products

    def getProductInstanceById(self, productID):
        prodDB = databaseController.getProductDataById(productID)[0]
        images = databaseController.getImages(productID)

        productResult = product(prodDB[PROD_USER_ID], prodDB[PROD_ID], prodDB[PROD_STATUS], prodDB[PROD_TITLE], prodDB[PROD_DESCRIPTION], prodDB[PROD_CATEGORY], prodDB[PROD_SUBCATEGORY], images, prodDB[PROD_VIEWS], prodDB[PROD_CONDITIE], prodDB[PROD_COUNTRY], prodDB[PROD_CITY], prodDB[PROD_IS_AUCTION], prodDB[PROD_PRICE], prodDB[PROD_CURRENCY], prodDB[PROD_SHIPPING_TYPE], prodDB[PROD_SHIPPING_PRICE], prodDB[PROD_DATE_ADDED], prodDB[PROD_DATE_EXPIRES])

        return productResult

    def getConditionInt(self, condStr):
        if condStr == 'boxed':
            return 0
        elif condStr == 'new':
            return 1
        elif condStr == 'slightly used':
            return 2
        elif condStr == 'used':
            return 3
        elif condStr == 'very used':
            return 4
        else:
            return 5

    def createListing(self, data):
        debug("in productController: creating listing")
        debug(data)

        info = {'title' : data['title'],
                    'description' : data['description'],
                    'conditie' : getConditionInt(data['description']),
                    'country' : "",
                    'state' : "",
                    'city' : "",
                    'is_auction' : data['is_auction'],
                    'price' : data['price'],
                    'currency' : data['currency'],
                    'shipping_type' : "",
                    'shipping_price' : 0,
                    'date_added' : datetime.datetime.now(),
                    'date_expires' : datetime.datetime.now(),
                    'category' : getConditionInt(data['category']),
                    'subcategory' : "",
                    'views' : 0,
                    'image' : getConditionInt(data['photos']),
                    'user_id' : ""
                }

        databaseController.insertIntoProductdata(info)
        debug("in productController: createdlisting")


productController = productController()
