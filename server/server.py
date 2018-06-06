import BaseHTTPServer
import SocketServer
import re
from lib import dispatcher

DEBUG = False


def debug(msg):
    if DEBUG:
        print msg


PORT = 8000

disp = dispatcher.dispatcher()


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def getCookie (self, key):
        requestHandler = self

        # extrag headeru' din request
        header = requestHandler.headers
        # ma asigur ca key-u' are sens
        key = str(key)

        # linia cu cookie-urile din header
        cookies = header.getallmatchingheaders('Cookie')[0]
        # separ stringu' cu cookieuri intr-un vector de forma <key=value>
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
                    return True

        return False

    def setCookie (self, key, value='', other=''):
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

    def do_POST(self):
        debug(self.requestline)
        disp.dispatch(self)

    def do_GET(self):
        debug(self.requestline)
        disp.dispatch(self)


Handler = RequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "Serving at port {0}".format(PORT)
httpd.serve_forever()
