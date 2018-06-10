from view import *
from product import *
import json


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


#searchProductCountKey = 'productCount'
searchPageIndexKey = 'page'
searchPageSizeKey = 'psize'
searchQueryKey = 'query'

searchDefaultPageSize = 5

productCount = 9

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

        for iter in xrange(1, productCount):
            productIDs.append((((iter * 2 - 1) * 3) / 2) * 10 + iter * 2)

        # end TODO

        return json.dumps(productIDs)


class searchProductsView(view):
    def get(self):
        debug('[INFO] searchProductsView reached')

        if not self.urlArgs.has_key(searchPageSizeKey):
            self.urlArgs[searchPageSizeKey] = searchDefaultPageSize

        debug('setting content type')
        self.setContentType('application/json')

        debug('content type set')
        # TODO: get products based on query & filters
        products = []

        debug('reached while loop')
        productIter = 0
        itemKey = 'item{0}'.format(productIter)
        debug('first item key is ' + itemKey)
        debug('first item id is ' + self.urlArgs[itemKey])

        while self.urlArgs.has_key(itemKey):
            debug('loop beginning')
            tmpProduct = product(1, 2, self.urlArgs[itemKey], 'title', 'product description lorem gipsum gaudeamus igitur', 4, 5, 6, 7, 8, 9, 10, 11, 12)
            debug('product: ')
            debug(tmpProduct)
            debug('asdict: ')
            debug(tmpProduct.asDict())
            products.append(tmpProduct.asDict())

            productIter += 1
            itemKey = 'item{0}'.format(productIter)
            debug('next key: ' + itemKey)
        # end TODO

        return json.dumps(products)
