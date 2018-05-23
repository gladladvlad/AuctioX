import os
from mimetypes import MimeTypes
from urlparse import parse_qs, urlparse
from dispatcherMap import pageMap

# Aici sunt view-urile. Un view (la noi) este o functie care primeste un request si pregateste raspunsul (care e trimis dupaia inapoi)

# publicFileResponse este view pentru toate fisierele care se afla in directorul public

class view:

    def __init__(self, request):

        self.response = 'Null response'
        self.args = parse_qs(urlparse(request.path).query)



        #self.response =

    def getResponse



def publicFileResponse(request):
    filePath = "..{0}".format(request.path)

    if not os.path.exists(filePath):
        request.send_response(404)
        print "Could not acces file '{0}'".format(filePath)
        return

    content = open(filePath, 'rb').read()

    request.send_response(200)
    contentType = MimeTypes().guess_type(request.path)
    request.send_header("Content-type", contentType[0])
    request.end_headers()

    request.wfile.write(content)

def pageFileResponse(request):
    for name in pageMap:
        if name in request.path:
            request.path = pageMap[name]
            publicFileResponse(request)
            break