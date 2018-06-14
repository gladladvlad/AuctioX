from view import *
from databaseController import *

class product():
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

        for image in self.images:
            image = str(image)

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

    def getHighestBidById(self, productID):
        highestBid = databaseController.executeSQLCommand('select value from userbid where product_id = {0} order by value desc'.format(productID), True)

        if highestBid == []:
            return 0

        if highestBid[0] == []:
            return 0

        return highestBid

    def getUserBidProduct(self, userID):
        return databaseController.getUserBidProduct(userID)

    def getUserProductsById(self, userID):
        products = databaseController.getUserProducts(userID)

        prodList = []
        for prodDB in products:
            prodBuf = product(prodDB[PROD_USER_ID], prodDB[PROD_ID], prodDB[PROD_STATUS], prodDB[PROD_TITLE], prodDB[PROD_DESCRIPTION], prodDB[PROD_CATEGORY], prodDB[PROD_SUBCATEGORY], [], prodDB[PROD_VIEWS], prodDB[PROD_CONDITIE], prodDB[PROD_COUNTRY], prodDB[PROD_CITY], prodDB[PROD_IS_AUCTION], prodDB[PROD_PRICE], prodDB[PROD_CURRENCY], prodDB[PROD_SHIPPING_TYPE], prodDB[PROD_SHIPPING_PRICE], prodDB[PROD_DATE_ADDED], prodDB[PROD_DATE_EXPIRES])

            prodList.append(prodBuf)

        return prodList

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

    def getConditionStr(self, condInt):
        if condInt == 0:
            return 'boxed'
        elif condInt == 1:
            return 'new'
        elif condInt == 2:
            return 'slightly used'
        elif condInt == 3:
            return 'used'
        elif condInt == 4:
            return 'very used'
        else:
            return 'extremely used'

    def getAuctionTypeStr(self, typeInt):
        if typeInt == 0:
            return 'Buy it now!'
        else:
            return 'Auction'

    def createListing(self, data, user):
        debug("in productController: creating listing")
        debug(data)

        now = datetime.datetime.now()
        expires = datetime.datetime(now.year + int(now.month > 12), (now.month + 1) % 12 + 1, now.day)

        info = {'title': data['title'],
                'description': data['description'],
                'conditie': self.getConditionInt(data['condition']),
                'country': "",
                'state': "",
                'city': "",
                'is_auction': data['is_auction'],
                'price': int(data['price']),
                'currency': data['currency'],
                'shipping_type': "",
                'shipping_price': 0,
                'date_added': now,
                'date_expires': expires,
                'category': data['category'],
                'subcategory': "",
                'views': 0,
                'image': data['photos'],
                'status': 'ongoing',
                'user_id': user.UID
                }

        databaseController.insertIntoProductdata(info)
        debug("in productController: createdlisting")


productController = productController()
