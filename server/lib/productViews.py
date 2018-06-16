from view import *
from product import *
import json
import math
from userController import *
from productController import *
from userViews import *


searchProductCountKey = 'prods'
searchPageIndexKey = 'page'
searchPageSizeKey = 'psize'
searchQueryKey = 'query'

searchFilterPriceMin = 'min_price'
searchFilterPriceMax = 'max_price'
searchFilterCondition = 'conditie'
searchFilterDateAdded = 'date_added'
searchFilterDateExpirese = 'date_expires'

searchDefaultPageSize = 5

#productCount = 12

productIDKey = "prodid"


class createListingView(view):
    def get(self):
        logger.info('[VIEW] createListings')

        if userController.validateUserSession(self) is None:
            logger.debug("No active session. Redirecting to sign in.")
            self.switchView(userSignInView)
            return False

        self.addComponentToContext('createlisting_styles.html', 'style', True)
        self.setContentType('text/html')
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('createlisting.html')

        return content


class createListingRequestView(view):
    def post(self):
        logger.info('[VIEW] createListingsRequestView')
        logger.debug('asd')
        user = userController.getUserInstanceById(userController.validateUserSession(self))
        logger.debug('got the user')
        result = productController.createListing(self.parseJsonPost(), user)
        success = False
        if result is not None:
            success = True
        return json.dumps({'success': success, 'prodId': result})


class searchView(view):
    def get(self):
        logger.info('[VIEW] searchView reached')

        self.setContentType('text/html')

        self.addComponentToContext('search_filters.html', 'search_filters', True)
        self.addComponentToContext('search_styles.html', 'search_styles', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)

        content = self.renderTemplate('search.html')

        return content


class searchProductIDsView(view):
    def get(self):
        logger.info('[VIEW] searchProductIDsView reached')

        if not self.urlArgs.has_key(searchQueryKey):
            self.urlArgs[searchQueryKey] = ''

        self.setContentType('application/json')

        info = dict()
        if self.urlArgs.has_key('min_price'):
            info['min_price'] = int(self.urlArgs['min_price'])
        if self.urlArgs.has_key('max_price'):
            info['max_price'] = int(self.urlArgs['max_price'])
        if self.urlArgs.has_key('condition'):
            info['conditie'] = int(self.urlArgs['conditie'])
        if self.urlArgs.has_key('country'):
            info['country'] = int(self.urlArgs['country'])
        if self.urlArgs.has_key('city'):
            info['city'] = int(self.urlArgs['city'])

        # info <=> {'min_price' : 2,
        #           'max_price' : 5,
        #           'conditie' : 2}
        # order_by <=> string cu campu' dupa care ordonam
        # how <=> asc/desc
        # query <=> string
        productsByQuery = productController.getProductsByFilter(info, None, None, self.urlArgs[searchQueryKey])
        logger.debug('LENGTH OF QUERY')
        logger.debug(len(productsByQuery))

        productIDs = []
        for iter in xrange(0, len(productsByQuery)):
            productIDs.append(productsByQuery[iter][PROD_ID])


        return json.dumps(productIDs)


class searchPageView(view):
    def get(self):
        logger.info('[VIEW] searchPageView')

        if not self.urlArgs.has_key(searchPageSizeKey):
            self.urlArgs[searchPageSizeKey] = searchDefaultPageSize

        if not self.urlArgs.has_key(searchProductCountKey):
            raise ValueError("Did not receive product count!")

        self.setContentType('text/html')

        products = []

        productIter = 0
        productsDone = 0
        itemKey = 'item{0}'.format(productIter)

        for i in xrange(0, (int(self.urlArgs[searchProductCountKey]))):
            if self.urlArgs.has_key(itemKey):
                tmpProduct = productController.getProductInstanceById(int(self.urlArgs[itemKey]))
                tmpProduct.auction = productController.getAuctionTypeStr(tmpProduct.auction)
                tmpProduct.condition = productController.getConditionStr(tmpProduct.condition)
                if (tmpProduct.auction == 'Auction'):
                    highestBid = productController.getHighestBidById(tmpProduct.productID)
                    tmpProduct.price = highestBid


                products.append(tmpProduct.asDict())
                productsDone += 1


            productIter += 1
            itemKey = 'item{0}'.format(productIter)
            if (productsDone == int(self.urlArgs[searchPageSizeKey])):
                break

        logger.debug(len(products))

        pages = [dict()]

        for i in xrange(0, int(math.ceil((float(self.urlArgs[searchProductCountKey]) / float(self.urlArgs[searchPageSizeKey]))))):
            dicterator = {'index' : i}

            pages.append(dicterator)

        self.addItemToContext(pages, 'pages', True)

        self.addComponentToContext('search_filters.html', 'search_filters', True)
        self.addComponentToContext('search_styles.html', 'search_styles', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)

        self.addItemToContext(products, 'products', True)

        page = self.renderTemplate('search_page.html')

        return page


class productView(view):
    def get(self):
        logger.info('[VIEW] productView reached')

        if not self.urlArgs.has_key(productIDKey):
            raise ValueError("No product provided!")

        product = productController.getProductInstanceById(int(self.urlArgs[productIDKey]))
        product.condition = productController.getConditionStr(product.condition)
        product.auction = productController.getAuctionTypeStr(product.auction)

        logger.debug(product.asDict())

        self.addItemToContext(product, 'product', True)

        seller = userController.getUserInstanceById(int(product.ownerID))

        logger.debug(seller.asDict())

        self.addItemToContext(seller, 'seller', True)


        self.addComponentToContext('product_styles.html', 'product_styles', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)

        content = self.renderTemplate('product.html')
        
        logger.debug('content rendered!')

        return content


class bidView(view):
    def get(self):
        logger.info("[VIEW] bidView")

        if not self.urlArgs.has_key('prodid'):
            return 'Fail! No product provided!'

        if not self.urlArgs.has_key('amount'):
            return 'Fail! No amount provided!'

        userId = userController.validateUserSession(self)
        if userId is None:
            return 'Fail! You must be logged in!'


        bidAmount = int(self.urlArgs['amount'])
        highestBid = int(productController.getHighestBidById(self.urlArgs['prodid']))

        if not bidAmount > highestBid:
            return 'Fail! You cannot bid lower than the highest bid!'

        bidEntry = {'user_id': userId,
                    'product_id': int(self.urlArgs['prodid']),
                    'status': 'ongoing',
                    'value': bidAmount}

        databaseController.insertIntoUserbid(bidEntry)

        return 'Success! You bid ' + str(bidAmount)

