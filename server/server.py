import BaseHTTPServer
import SocketServer
import shutil

PORT = 8000


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):

        print self.path

        self.send_response(200)

        print self.headers

        if self.path.endswith('.css'):
            self.send_header("Content-type", "text/css")
        elif self.path.endswith('.png'):
            self.send_header("Content-type", "image/png")
        else:
            self.send_header("Content-type", "text/html")

        self.end_headers()

        if self.path == '/login':

            f = open('..\\AuctioX\\signin.html')
            shutil.copyfileobj(f, self.wfile)

        if self.path == '/style.css':

            f = open('..\\AuctioX\\style.css')
            shutil.copyfileobj(f, self.wfile)

        if self.path == '/style_signin.css':

            f = open('..\\AuctioX\\style_signin.css')
            shutil.copyfileobj(f, self.wfile)

        if self.path == '/navbar.html':

            f = open('..\\AuctioX\\navbar.html')
            shutil.copyfileobj(f, self.wfile)

        if self.path == '/style_navbar.css':

            f = open('..\\AuctioX\\style_navbar.css')
            shutil.copyfileobj(f, self.wfile)

        if self.path == '/static/png/logo.png':

            f = open('..\\AuctioX\\static\\png\\logo.png')
            shutil.copyfileobj(f, self.wfile)

        return


Handler = RequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "Serving at port {0}".format(PORT)
httpd.serve_forever()