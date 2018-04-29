import os
from mimetypes import MimeTypes
from urlparse import parse_qs, urlparse

# Aici sunt view-urile. Un view (la noi) este o functie care primeste un request si pregateste raspunsul (care e trimis dupaia inapoi)

# PublicFileResponse este view pentru toate fisierele care se afla in directorul public
def PublicFileResponse(request):
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

    return