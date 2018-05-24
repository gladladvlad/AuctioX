import os
from mimetypes import MimeTypes
from urlparse import parse_qs, urlparse
from dispatcherMap import *
from jinja2 import Template

# Aici sunt view-urile. Un view (la noi) este o functie care primeste un request si pregateste raspunsul (care e trimis dupaia inapoi)

# publicFileResponse este view pentru toate fisierele care se afla in directorul public

DEBUG_MODE = True

DEFAULT_HTML_PATH = '../public/static/html/'

def debug(msg):
    if DEBUG_MODE:
        print msg

class view:

    def __init__(self, request):

        debug("View: {0}".format(self.__class__.__name__))
        try:
            self.request = request
            self.contentType = "text/plain"  # this is by default

            self.urlArgs = parse_qs(urlparse(request.path).query)  # get args from url
            # debug(self.urlAargs)
            self.response = self.generateResponse()  # generate response
            # debug(self.response)
        except Exception:
            self.request.send_response(404)
            self.request.send_header("Content-type", 'text/plain')
            self.request.end_headers()
            self.request.wfile.write("Error")
            return

        self.request.send_response(200)
        self.request.send_header("Content-type", self.contentType)
        self.request.end_headers()
        self.request.wfile.write(self.response)
        return

    def generateResponse(self):

        return "No view found."

    def setContentType(self, contentType):
        self.contentType = contentType

class publicFileView(view):

    def generateResponse(self):

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

class jinjatest(view):

    def generateResponse(self):
        navbar = open('{path}/navbar.html'.format(path=DEFAULT_HTML_PATH)).read()
        context = {'navbar': navbar}
        self.setContentType('text/html')

        template = Template(open('{path}/jinjatest.html'.format(path=DEFAULT_HTML_PATH)).read())
        content = template.render(context)
        return content