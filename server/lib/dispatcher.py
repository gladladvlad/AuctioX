import re, os
from dispatcherMap import map
import BaseHTTPServer

class dispatcher:

    def __init__(self, request):

        self.request = request

    # functie pentru gasit view-ul care corespunde path-ului din request
    def matchView(self, path):

        view = None

        for item in map:

            if view is not None:
                 break

            if re.match(item['regex'], path) is not None:

                view = item['view']

        return view

    # functie care cauta si apeleaza view-ul corespunzator unui request
    def dispatch(self):

        #args = parse_qs(urlparse(request.path).query)

        view = dispatcher.matchView(self, self.request.path)

        print "[INFO] received request for path '{0}'".format(self.request.path)

        if view is None:

            print "[WARNINIG] Could not find function for path '{0}'".format(self.request.path)
            return

        view(self.request)