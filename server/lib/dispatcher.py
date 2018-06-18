import re
from dispatcherMap import map
import BaseHTTPServer
from util import *


class dispatcher:

    # functie pentru gasit view-ul care corespunde path-ului din request

    def matchView(self, path):

        view = None

        for pair in map:

            if view is not None:
                 break

            try:
                if re.match(pair[0], path) is not None:
                    view = pair[1]
            except:
                logger.error("Could not find mathing view for regex '{0}'".format(pair[0]))

        return view

    # functie care cauta si apeleaza view-ul corespunzator unui request

    def dispatch(self, request):

        view = dispatcher.matchView(request.path)
        if view is None:
            logger.error("[WARNINIG] Could not find view for path '{0}'".format(request.path))
            return

        view(request)


dispatcher = dispatcher()