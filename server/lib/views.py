import os
from mimetypes import MimeTypes
from urlparse import parse_qs, urlparse
from dispatcherMap import *

# Aici sunt view-urile. Un view (la noi) este o functie care primeste un request si pregateste raspunsul (care e trimis dupaia inapoi)

# publicFileResponse este view pentru toate fisierele care se afla in directorul public

DEBUG_MODE = True

def debug(msg):
    if DEBUG_MODE:
        print msg

class view:

    def __init__(self, request):

        debug("View: {0}".format(self.__class__.__name__))
        try:
            self.request = request
            self.contentType = "text/plain"

            self.args = parse_qs(urlparse(request.path).query)
            #debug(self.args)
            self.response = self.getResponse()
            #debug(self.response)
        except:
            self.request.send_response(404)
            self.request.send_header("Content-type", self.contentType)
            self.request.end_headers()
            self.request.wfile.write("Error")
            return

        self.request.send_response(200)
        self.request.send_header("Content-type", self.contentType)
        self.request.end_headers()
        self.request.wfile.write(self.response)
        return

    def getResponse(self):

        return "Default View"

    def setContentType(self, contentType):
        self.contentType = contentType

class publicPageView(view):

    def getResponse(self):

        filePath = "..{0}".format(self.request.path)
        if not os.path.exists(filePath):
            debug("[ERROR] Could not find file {0}".format(filePath))
        else:
            if filePath.endswith('.html'):
                self.setContentType('text/html')
            else:
                self.setContentType(MimeTypes().guess_type(self.request.path))
            return open(filePath, 'rb').read()