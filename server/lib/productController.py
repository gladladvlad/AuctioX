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

        result = {'ownerID' : self.ownerID,
                'productID' : self.productID,
                'status' : self.status,
                'title' : self.title,
                'desc' : self.desc,
                'category' : self.category,
                'subcategory' : self.category,
                'images' : self.images,
                'condition' : self.condition,
                'country' : self.country,
                'city' : self.city,
                'auction' : self.auction,
                'price' : self.price,
                'currency' : self.currency,
                'shippingType' : self.shippingType,
                'shippingPrice' : self.shippingPrice,
                'dateAdded' : self.dateAdded,
                'dateExpires' : self.dateExpires}

        return result

class productController():

    def getAllProducts(self):
        logger.info('[START] getAllProducts()')
        return databaseController.getProducts()

    # info <=> {'min_price' : 2,
    #           'max_price' : 5,
    #           'conditie' : 2}
    # order_by <=> string cu campu' dupa care ordonam
    # how <=> asc/desc
    # query <=> string
    def getProductsByFilter(self, info, order_by, how, query):
        logger.info('[START] getProductsByFilter()')
        products = databaseController.getProductsByFilter(info, order_by, how, query)

        prodList = []
        for prodDB in products:
            prodBuf = product(prodDB[PROD_USER_ID], prodDB[PROD_ID], prodDB[PROD_STATUS], prodDB[PROD_TITLE], prodDB[PROD_DESCRIPTION], prodDB[PROD_CATEGORY], prodDB[PROD_SUBCATEGORY], [], prodDB[PROD_VIEWS], prodDB[PROD_CONDITIE], prodDB[PROD_COUNTRY], prodDB[PROD_CITY], prodDB[PROD_IS_AUCTION], prodDB[PROD_PRICE], prodDB[PROD_CURRENCY], prodDB[PROD_SHIPPING_TYPE], prodDB[PROD_SHIPPING_PRICE], prodDB[PROD_DATE_ADDED], prodDB[PROD_DATE_EXPIRES])

            prodList.append(prodBuf)

        return prodList



    def getProductImages(self, prodList):
        logger.info('[START] getProductImages()')


        newProdList = []

        for product in prodList:
            images = databaseController.getImages(product.productID)
            product.images = images

            newProdList.append(product)

        return newProdList



    def getProductInstanceById(self, productID):
        logger.info('[START] getProductInstanceById()')
        prodDB = databaseController.getProductDataById(productID)[0]
        images = databaseController.getImages(productID)

        productResult = product(prodDB[PROD_USER_ID], prodDB[PROD_ID], prodDB[PROD_STATUS], prodDB[PROD_TITLE], prodDB[PROD_DESCRIPTION], prodDB[PROD_CATEGORY], prodDB[PROD_SUBCATEGORY], images, prodDB[PROD_VIEWS], prodDB[PROD_CONDITIE], prodDB[PROD_COUNTRY], prodDB[PROD_CITY], prodDB[PROD_IS_AUCTION], prodDB[PROD_PRICE], prodDB[PROD_CURRENCY], prodDB[PROD_SHIPPING_TYPE], prodDB[PROD_SHIPPING_PRICE], prodDB[PROD_DATE_ADDED], prodDB[PROD_DATE_EXPIRES])

        return productResult



    def getHighestBidById(self, productID):
        logger.info('[START] getHighestBidById()')
        highestBid = databaseController.executeSQLCommand('select value from userbid where product_id = {0} order by value desc'.format(productID), True)

        logger.info('for ' + str(productID) + ' bid is ' + str(highestBid))

        if highestBid == []:
            return 0

        if highestBid[0] == []:
            return 0

        return highestBid[0][0]



    def bid(self, userID, productID, bidAmount):
        product = self.getProductInstanceById(productID)
        if product.status != 'ongoing':
            return 'Fail! You cannot bid on a product that doesn\'t exist!'

        highestBid = self.getHighestBidById(productID)
        if highestBid != 0:
            if bidAmount <= highestBid:
                return 'Fail! You cannot bid lower than the highest bid!'
        else:
            if bidAmount <= product.price:
                return 'Fail! You cannot bid lower than the highest bid!'


        if product.auction != 1:
            return 'Fail! You cannot bid on a product that\'s not up for auction!'

        if product.ownerID == userID:
            return 'Fail! You cannot bid on a product that you sell!'

        bidEntry = {'user_id': userID,
                    'product_id': productID,
                    'status': 'ongoing',
                    'value': bidAmount}

        databaseController.insertIntoUserbid(bidEntry)

        databaseController.setNewPrice(productID, bidAmount)

        return 'Success! You bid {0}'.format(bidAmount)



    def buy(self, userID, productID):
        product = self.getProductInstanceById(productID)
        if product.status  !=  'ongoing':
            return 'Fail! You cannot bid on a product that doesn\'t exist!'

        if product.auction != 0:
            return 'Fail! You cannot buy an auctioned product!'

        if product.ownerID == userID:
            return 'Fail! You cannot buy a product that you sell!'

        transactionEntry = {'seller_user_id' : product.ownerID,
                            'product_data_id' : productID,
                            'buyer_user_id' : userID,
                            'has_ended' : 'ongoing'}

        databaseController.insertIntoTransaction(transactionEntry)

        databaseController.setInactiveInProduct(productID)

        return 'Success! Please look out for your transaction page.'



    def getUserBidProduct(self, userID):
        logger.info('[START] getUserBidProduct()')
        return databaseController.getUserBidProduct(userID)



    def getUserProductsById(self, userID):
        logger.info('[START] getUserProductsById()')
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
        logger.info("[START] createListing()")

        errors = list()
        resultDict = dict()
        now = datetime.datetime.now()
        endTime = now

        if data["price"] == "":
            errors.append("You must specify a price")
        else:
            logger.debug("Price OK")

        if data["title"] == "":
            errors.append("You must provide a title")
        else:
            logger.debug("Title OK")

        if data["description"] == "":
            errors.append("You must provide a description")
        else:
            logger.debug("Description OK")

        if data["is_auction"]:

            logger.debug("Checking auction end time")

            datetimeString = "{0} {1}".format(data['endDate'], data["endTime"]).split(',')[0]

            logger.debug("Received {0}, (now is {1})".format(datetimeString, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

            validTime = False
            correctTime = False

            try:
                endTime = datetime.datetime.strptime(datetimeString, "%Y-%m-%d %H:%M")
                validTime = True
                logger.debug("Time validated OK")
            except:
                logger.error("Could not parse date string '{0}'".format(datetimeString))
                errors.append("Bad date/time.")
                pass

            if validTime and endTime > datetime.datetime.now():
                logger.debug("Time is correct")
                correctTime = True
            else:
                errors.append("Invalid auction end time")

            if correctTime and (endTime - datetime.datetime.now()).seconds/3600 > 1:
                logger.debug("Timedelta is ok")
            else:
                errors.append("Auctions must be available for at least 1 hour")

        if len(errors) == 0:

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
                    'date_expires': endTime,
                    'category': data['category'],
                    'subcategory': "",
                    'views': 0,
                    'image': data['photos'],
                    'status': 'ongoing',
                    'user_id': user.UID
                    }

            logger.debug("Database insertion starting")
            prodId = databaseController.insertIntoProductdata(info)
            logger.debug("Database insertion done")

            if prodId is not None:
                logger.debug("Created listing")
                resultDict["prodId"] = prodId
            else:
                errors.append("Could not add product")
        else:
            logger.warning("Product not valid. Not adding to database.")

        resultDict["success"] = False
        if len(errors) == 0:
            resultDict["success"] = True

        resultDict["errors"] = errors

        logger.debug(resultDict)

        return json.dumps(resultDict)


productController = productController()
