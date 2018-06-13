from view import *
from product import *
import json
import math
from userController import *
from productController import *
from userViews import *


class createListingView(view):
    def get(self):
        debug('[INFO] createListings reached')

        if userController.validateUserSession(self.sessionData) is None:
            self.switchView(userSignInView)
            return False

        self.addComponentToContext('createlisting_styles.html', 'style', True)
        self.setContentType('text/html')
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('createlisting_content.html', 'content', True)
        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('createlisting.html')

        return content


class createListingRequestView(view):

    def post(self):
        debug('[VIEW] createListingsRequestView')
        result = productController.createListing(self.parseJsonPost())
        return result


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

class searchView(view):
    def get(self):
        debug('[INFO] searchView reached')


        self.setContentType('text/html')

        self.addComponentToContext('search_content.html', 'search_content', True)
        self.addComponentToContext('search_filters.html', 'search_filters', True)
        self.addComponentToContext('search_styles.html', 'search_styles', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)


        content = self.renderTemplate('search.html')

        return content


class searchProductIDsView(view):
    def get(self):
        debug('[INFO] searchProductIDsView reached')

        if not self.urlArgs.has_key(searchQueryKey):
            self.urlArgs[searchQueryKey] = ''

        self.setContentType('application/json')


        info = dict()
        if self.urlArgs.has_key('min_price'):
            info['min_price'] = int(self.urlArgs['min_price'])

        if self.urlArgs.has_key('max_price'):
            info['max_price'] = int(self.urlArgs['max_price'])

        # info <=> {'min_price' : 2,
        #           'max_price' : 5,
        #           'conditie' : 2}
        # order_by <=> string cu campu' dupa care ordonam
        # how <=> asc/desc
        # query <=> string
        productsByQuery = productController.getProductsByFilter(info, None, None, self.urlArgs[searchQueryKey])
        debug('LENGTH OF QUERY')
        debug(len(productsByQuery))

        productIDs = []
        for iter in xrange(0, len(productsByQuery)):
            productIDs.append(productsByQuery[iter][PROD_ID])


        return json.dumps(productIDs)


class searchPageView(view):
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

    def get(self):
        debug('[INFO] searchPageView reached')

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
                # TODO: get products based on query & filters
                #tmpProduct = product(1, 2, self.urlArgs[itemKey], 'title', 'product description lorem gipsum gaudeamus igitur', [4], 4, 5, 6, 7, 8, 9, 10, 11, 12)
                # end TODO
                tmpProduct = productController.getProductInstanceById(int(self.urlArgs[itemKey]))
                tmpProduct.auction = self.getAuctionTypeStr(tmpProduct.auction)
                tmpProduct.condition = self.getConditionStr(tmpProduct.condition)

                products.append(tmpProduct.asDict())
                productsDone += 1


            productIter += 1
            itemKey = 'item{0}'.format(productIter)
            if (productsDone == int(self.urlArgs[searchPageSizeKey])):
                break

        debug(len(products))


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


productIDKey = "prodid"

class productView(view):
    def get(self):
        debug('[INFO] productView reached')

        if not self.urlArgs.has_key(productIDKey):
            raise ValueError("No product provided!")


        # TODO: get product from bd
        tmpProduct = product(1, 2, 3, 'title', 'product description lorem gipsum gaudeamus igitur', [4], 4, 5, 6, 7, 8, 9, 10, 11, 12)
        # end TODO

        self.addItemToContext(tmpProduct, 'product', True)

        # TODO: get seller from bd
        tmpSeller = user(1, 2, 3, 4, 5, 6, 7, 8)
        # end TODO

        self.addItemToContext(tmpSeller, 'seller', True)


        self.addComponentToContext('product_content.html', 'product_content', True)
        self.addComponentToContext('product_styles.html', 'product_styles', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)

        content = self.renderTemplate('product.html')

        return content

class bidView(view):
    def get(self):
        return 'unsupported command error in pony! press F for full stack'

