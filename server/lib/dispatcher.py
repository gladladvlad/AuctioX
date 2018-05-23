import re, os
from dispatcherMap import map
import BaseHTTPServer

class dispatcher:

    def __init__(self, request):

        self.request = request

    # functie pentru gasit view-ul care corespunde path-ului din request
    def matchFunction(self, path):

        func = None

        for item in map:

            if func is not None:
                 break

            if re.match(item['regex'], path) is not None:

                func = item['view']

        return func

    # functie care cauta si apeleaza view-ul corespunzator unui request
    def dispatch(self):

        #args = parse_qs(urlparse(request.path).query)

        func = dispatcher.matchFunction(self, self.request.path)

        print "[INFO] received request for path '{0}'".format(self.request.path)

        if func is None:

            print "[WARNINIG] Could not find function for path '{0}'".format(self.request.path)
            return

        func(self.request)