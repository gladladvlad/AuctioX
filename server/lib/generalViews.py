from view import *
from mimetypes import MimeTypes

from productController import *

class publicFileView(view):

    def get(self):

        filePath = "..{0}".format(self.request.path.replace('/', '\\'))
        try:
            self.setContentType(MimeTypes().guess_type(self.request.path)[0])
            # debug(self.contentType)
            content = open(filePath, 'rb').read()
            # debug(content)
        except:
            debug("[ERROR] Could not find file {0}".format(filePath))
            raise Exception

        debug("Sending {0} as {1}".format(filePath, self.contentType))
        return content


class homepageView(view):
    def get(self):
        debug('[INFO] homepageView reached')

        self.setContentType('text/html')

        self.addComponentToContext('home_styles.html', 'style', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('home_content.html', 'content', True)
        self.addComponentToContext('home_homebar.html', 'homebar', True)
        self.addComponentToContext('footer.html', 'footer', True)

        content = self.renderTemplate('home.html')

        return content



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
