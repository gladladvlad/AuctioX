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
        self.addComponentToContext('createlisting_content.html', 'content', True)
        self.setContentType('text/html')
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('createlisting.html')

        return content


class createListingRequestView(view):
    def post(self):
        logger.info('[VIEW] createListingsRequestView')
        user = userController.getUserInstanceById(userController.validateUserSession(self))

        result = productController.createListing(self.parseJsonPost(), user)

        return result


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
    skipUserValidation = True
    def post(self):
        logger.info('[VIEW] searchProductIDsView reached')

        self.setContentType('application/json')


        args = self.parseJsonPost()
        if not args.has_key('query'):
            args['query'] = ''

        info = dict()

        if args.has_key('min_price'):
            info['min_price'] = int(args['min_price'])
        if args.has_key('max_price'):
            info['max_price'] = int(args['max_price'])
        if args.has_key('conditie'):
            info['conditie'] = args['conditie']
        if args.has_key('country'):
            info['country'] = args['country']
        if args.has_key('city'):
            info['city'] = args['city']
        if args.has_key('category'):
            info['category'] = args['category']


        # info <=> {'min_price' : 2,
        #           'max_price' : 5,
        #           'conditie' : 2}
        # order_by <=> string cu campu' dupa care ordonam
        # how <=> asc/desc
        # query <=> string
        productsByQuery = productController.getProductsByFilter(info, None, None, args['query'])

        productIDs = []
        for iter in xrange(0, len(productsByQuery)):
            productIDs.append(productsByQuery[iter].productID)


        return json.dumps(productIDs)


class searchPageView(view):
    skipUserValidation = True
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

        databaseController.incrementView(product.productID)

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

        return productController.bid(userId, int(self.urlArgs['prodid']), bidAmount)


class buyView(view):
    def get(self):
        logger.info("[VIEW] bidView")

        if not self.urlArgs.has_key('prodid'):
            return 'Fail! No product provided!'

        userId = userController.validateUserSession(self)
        if userId is None:
            return 'Fail! You must be logged in!'

        return productController.buy(userId, int(self.urlArgs['prodid']))

