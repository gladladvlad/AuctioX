import BaseHTTPServer
import SocketServer
import shutil
import os
import re
from urlparse import parse_qs, urlparse

#from lib.acx_cookie import *

PORT = 8000

userDB = [
    {'user': ['rbaisan'], 'pass': ['rba135135']},
    {'user': ['gabih'], 'pass': ['dnd']},
    {'user': ['adrenalina'], 'pass': ['yesss']},
    {'user': ['vlad'], 'pass': ['vlad']},
    {'user': ['MLADULARMARE'], 'pass': ['iluvciuliXOXO']},
]

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def get_cookie (self, key):
        requestHandler = self
        #le-am definit pe asta ca... ca sa fie
        affirmative = 'yes'
        negative = 'no'

        #extrag headeru' din request
        header = requestHandler.headers
        #ma asigur ca key-u' are sens
        key = str(key)


        #linia cu cookie-urile din header
        cookies = header.getallmatchingheaders('Cookie')[0]
        #separ stringu' cu cookieuri intr-un vector de forma <key=value>
        cookies = cookies.strip().replace(' ', '').replace('Cookie:', '', 1).split(';')

        for cookie in cookies:
            # elimin key-u'
            value = re.sub(''.join(['^', key, '=']), '', cookie, 1)

            # daca intr-adevar am eliminat ceva
            if value != cookie:
                # si am ramas cu o valoare
                if value != '':
                    return value
                else:
                    return affirmative

        return negative

    def set_cookie (self, key, value='', other=''):
        requestHandler = self
        pair = []

        pair.append(key)
        if value != '':
            pair.append('=')
            pair.append(value)

        if other != '':
            pair.append('; ')
            pair.append(other)

        pair = ''.join(pair)

        requestHandler.send_header('Set-Cookie', pair)


    def do_GET(self):

        path = self.path

        print "Path: [{0}]".format(path)
        #print self.headers

        if path.startswith("/signinrequest/"):
            creds = parse_qs(urlparse(path).query)
            print creds

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Set-Cookie", "tetest")

            #read cookie
            #if 'logged=yes' in self.rfile.read():
                #print 'already LOGGED'

            logged = self.get_cookie('logged')

            if logged == 'yes':
                print 'already logged as someone'

            if creds in userDB:
                # self.send_header("Set-Cookie", "logged=yes")
                # same ting
                self.set_cookie('logged', 'yes', 'path=/')
            else:
                self.send_header("Set-Cookie", "logged=no")

            self.end_headers()
            return

        try:
            if path == '/':
                path = "/public/static/html/home.html"

            filePath = "..{0}".format(path)
            print "Returning file: {0}".format(filePath)
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

        return


Handler = RequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "Serving at port {0}".format(PORT)
httpd.serve_forever()
