from view import *
from product import *
import json
import math


class createListingView(view):
    def get(self):
        debug('[INFO] createListings reached')

        self.addComponentToContext('createlisting_styles.html', 'style', True)
        self.setContentType('text/html')
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('createlisting_content.html', 'content', True)
        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('createlisting.html')

        return content


searchProductCountKey = 'prods'
searchPageIndexKey = 'page'
searchPageSizeKey = 'psize'
searchQueryKey = 'query'

searchDefaultPageSize = 5

productCount = 14

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


        # TODO: get product IDs based on query & filters
        productIDs = []

        for iter in xrange(0, productCount):
            productIDs.append((((iter * 2 - 1) * 3) / 2) * 10 + iter * 2)

        # end TODO


        return json.dumps(productIDs)


##################################################
# WILL BE UNUSED
##################################################
class searchProductsView(view):
    def get(self):
        debug('[INFO] searchProductsView reached')

        if not self.urlArgs.has_key(searchPageSizeKey):
            self.urlArgs[searchPageSizeKey] = searchDefaultPageSize

        self.setContentType('application/json')

        # TODO: get products based on query & filters
        products = []

        productIter = 0
        itemKey = 'item{0}'.format(productIter)

        while self.urlArgs.has_key(itemKey):
            tmpProduct = product(1, 2, self.urlArgs[itemKey], 'title', 'product description lorem gipsum gaudeamus igitur', 4, 5, 6, 7, 8, 9, 10, 11, 12)
            products.append(tmpProduct.asDict())

            productIter += 1
            itemKey = 'item{0}'.format(productIter)
        # end TODO



        return json.dumps(products)
####################################################################################


class searchPageView(view):
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


        #while self.urlArgs.has_key(itemKey):
        for i in xrange(0, (int(self.urlArgs[searchProductCountKey]) - 1)):
            if self.urlArgs.has_key(itemKey):
                # TODO: get products based on query & filters
                tmpProduct = product(1, 2, self.urlArgs[itemKey], 'title', 'product description lorem gipsum gaudeamus igitur', 4, 5, 6, 7, 8, 9, 10, 11, 12)
                # end TODO
                products.append(tmpProduct.asDict())
                productsDone += 1


            productIter += 1
            itemKey = 'item{0}'.format(productIter)
            if (productsDone == int(self.urlArgs[searchPageSizeKey])):
                break


        pages = [dict()]

        for i in xrange(0, int(math.ceil((float(self.urlArgs[searchProductCountKey]) / float(self.urlArgs[searchPageSizeKey]))))):
            dicterator = {'index' : i}

            pages.append(dicterator)

        self.addItemToContext(pages, 'pages', True)


        #self.addComponentToContext('search_content.html', 'search_content', True)
        self.addComponentToContext('search_filters.html', 'search_filters', True)
        self.addComponentToContext('search_styles.html', 'search_styles', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)

        self.addItemToContext(products, 'products', True)

        page = self.renderTemplate('search_page.html')

        return page

