from view import *


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


class searchView(view):
    def get(self):
        debug('[INFO] searchView reached')


        self.setContentType('text/html')

        self.addComponentToContext('search_content.html', 'search_content', True)
        self.addComponentToContext('search_filters.html', 'search_filters', True)
        self.addComponentToContext('search_styles.html', 'search_styles', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)


        # TODO: get products by filters
        products = []

        products.append(productController(1, 2, 3, 'bepis', 'abasdkajsd', 5, 6, 7, 8, 9, 10, 11, 12, 13))
        products.append(productController(1, 2, 3, 'foo', 'hohohohohohoohoohohoohhhhhhh', 5, 6, 7, 8, 9, 10, 11, 12, 13))
        products.append(productController(1, 2, 3, 'bar', 'merge :hnnn:', 5, 6, 7, 8, 9, 10, 11, 12, 13))
        # end TODO


        #add products to context
        self.addItemToContext(products, 'products', True)


        content = self.renderTemplate('search.html')

        return content
