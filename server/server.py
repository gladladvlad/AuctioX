import BaseHTTPServer
import SocketServer
import shutil
import os

PORT = 8000


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):

        path = self.path

        print "Path: [{0}]".format(path)
        #print self.headers

        try:
            if path == '/':
                path = "/public/static/html/home.html"

            filePath = "..{0}".format(path)
            print filePath
            content = open(filePath, 'rb').read()

            self.send_response(200)

            if path.endswith('.css'):
                self.send_header("Content-type", "text/css")
            elif path.endswith('.png'):
                self.send_header("Content-type", "image/png")
            elif path.endswith('.jpg'):
                self.send_header("Content-type", "image/*")
            elif path.endswith('.html'):
                self.send_header("Content-type", "text/html")
            else:
                self.send_header("Content-type", "text/plain")

            self.end_headers()

            self.wfile.write(content)

        except:

            self.send_response(404)

            self.send_header("Content-type", "text/plain")

            self.end_headers()

            self.wfile.write("Error")


        return


Handler = RequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "Serving at port {0}".format(PORT)
httpd.serve_forever()