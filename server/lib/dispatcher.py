import re, os
from dispatcherMap import map

# functie pentru gasit view-ul care corespunde path-ului din request
def matchFunction(path):

    func = None

    for item in map:

        if func is not None:
             break

        if re.match(item['regex'], path) is not None:

            func = item['view']

    return func

# functie care cauta si apeleaza view-ul corespunzator unui request
def dispatch(request):

    #args = parse_qs(urlparse(request.path).query)

    func = matchFunction(request.path)

    print "[INFO] received request for path '{0}'".format(request.path)

    if func is None:

        print "[WARNINIG] Could not find function for path '{0}'".format(request.path)
        return

    func(request)