from view import *
from mimetypes import MimeTypes


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