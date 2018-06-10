from view import *
from mimetypes import MimeTypes

from productController import *

class searchView(view):
    def get(self):
        debug('[INFO] searchView reached')

        debug('ajuns aici')
        # TODO: get products by filters
        products = []

        products.append(productController(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))
        products.append(productController(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))
        products.append(productController(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))
        # end TODO

        debug('ajuns aici')


        self.setContentType('text/html')
        debug('ajuns aici')

        self.addComponentToContext('search_content.html', 'search_content', True)
        debug('ajuns aici')
        self.addComponentToContext('search_filters.html', 'search_filters', True)
        self.addComponentToContext('search_styles.html', 'search_styles', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)
        debug('ajuns aici')

        content = self.renderTemplate('search.html')
        debug('ajuns aici')

        return content
