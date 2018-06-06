import os
from mimetypes import MimeTypes
from urlparse import parse_qs, urlparse
from dispatcherMap import *
from jinja2 import Template
import json

# Aici sunt view-urile. Un view (la noi) este o functie care primeste un request si pregateste raspunsul (care e trimis dupaia inapoi)

# publicFileResponse este view pentru toate fisierele care se afla in directorul public

DEBUG = True


def debug(msg):
    if DEBUG:
        print msg


DEFAULT_HTML_PATH = '../public/static/html/'


class view:

    def __init__(self, request):

        self.context = dict()
        debug("View: {0}".format(self.__class__.__name__))
        try:
            self.request = request
            self.contentType = "text/plain"  # this is by default

            self.urlArgs = parse_qs(urlparse(request.path).query)  # get args from url
            # debug(self.urlAargs)

            self.requestType = self.request.requestline.split(' ')[0]

            if 'POST' in self.requestType:
                debug("POST")
                content_length = int(self.request.headers['Content-Length'])
                self.postData = self.request.rfile.read(content_length)
                self.response = self.post()

            else:
                debug("GET")
                self.response = self.get()

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

    def get(self):

        self.contentType = "text/html"
        response = "<body style='font-family: monospace'><h1>No view found</h1><hr>"
        if DEBUG:
            response += self.request.requestline + "<hr>"
            response += "URL arguments:<br><pre>" + json.dumps(self.urlArgs, indent=4) + "</pre><hr>"
            response += "Headers:<br><pre>" + str(self.request.headers) + "</pre>"
        return response

    def post(self):

        self.contentType = "text/html"
        response = "<body style='font-family: monospace'><h1>No view found</h1><hr>"
        if DEBUG:
            response += self.request.requestline + "<hr>"
            response += "URL arguments:<br><pre>" + json.dumps(self.urlArgs, indent=4) + "</pre><hr>"
            response += "POST data:<br><pre>" + self.postData + "</pre><hr>"
            response += "Headers:<br><pre>" + str(self.request.headers) + "</pre>"
        return response

    def setContentType(self, contentType):
        self.contentType = contentType

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
