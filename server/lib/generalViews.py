from view import *
from mimetypes import MimeTypes

from productController import *

class publicFileView(view):
    def get(self):
        logger.info("[VIEW] publicFileView")


        filePath = "..{0}".format(self.request.path.replace('/', '\\'))
        try:
            self.setContentType(MimeTypes().guess_type(self.request.path)[0])
            content = open(filePath, 'rb').read()
        except:
            raise Exception
        return content


class homepageView(view):
    def get(self):
        logger.info("[VIEW] homepageView")

        self.setContentType('text/html')

        self.addComponentToContext('home_styles.html', 'style', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('home_content.html', 'content', True)
        self.addComponentToContext('home_homebar.html', 'homebar', True)
        self.addComponentToContext('footer.html', 'footer', True)

        content = self.renderTemplate('home.html')

        return content


