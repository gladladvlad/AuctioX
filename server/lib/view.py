import os
import sys
from mimetypes import MimeTypes
from urlparse import parse_qs, urlparse
from dispatcherMap import *
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape
import json
import traceback
import base64

from userController import *
from util import *

# Aici sunt view-urile. Un view (la noi) este o functie care primeste un request si pregateste raspunsul (care e trimis dupaia inapoi)

# publicFileResponse este view pentru toate fisierele care se afla in directorul public


TEMPLATE_DIRECTORY = '../private/static/html/templates/'
COMPONENT_DIRECTORY = '../private/static/html/components/'


class view:
    # la autoescape puteti sa puneti extensii de fisiere care sa fie escapate automat
    jinja2Env = Environment(loader=FileSystemLoader(TEMPLATE_DIRECTORY), autoescape=select_autoescape(['xml']))

    def __init__(self, request):
        logger.info("[START] __init__ [{0}]".format(self.__class__.__name__))

        self.context = dict()
        self.cookies = list()

        try:
            self.request = request
            self.contentType = "text/plain"  # this is by default

            self.urlArgs = parse_qs(urlparse(request.path).query)  # get args from url
            for key in self.urlArgs:
                self.urlArgs[key] = self.urlArgs[key][0]

            if not hasattr(self, "skipUserValidation"):
                try:
                    self.sessionData = self.request.getCookie('user_session_identifier')
                    self.sessionData = json.loads(base64.b64decode(self.sessionData))
                    if userController.validateUserSession(self):
                        self.context["sessionData"] = self.sessionData
                    else:
                        self.sessionData = None
                except:
                    pass

            self.requestType = self.request.requestline.split(' ')[0]

            if 'POST' in self.requestType:
                content_length = int(self.request.headers['Content-Length'])
                self.postData = self.request.rfile.read(content_length)

                logger.debug("Calling {0}.post()".format(self.__class__.__name__))
                self.response = self.post()

            else:
                logger.debug("Calling {0}.get()".format(self.__class__.__name__))
                self.response = self.get()

            if self.response is False:
                return

            if DEBUG and 'debug' in self.urlArgs:

                self.request.send_response(202)
                self.request.send_header("Content-type", 'text/plain')
                self.request.end_headers()
                oldResponse = self.response
                response = "DEBUG\n\n"
                if DEBUG:
                    response += self.request.requestline + "\n\n"
                    response += "URL arguments:\n" + json.dumps(self.urlArgs, indent=4) + "\n\n"
                    response += "Headers:\n" + str(self.request.headers) + "\n\n"
                    response += "Set cookies:\n" + json.dumps(self.context, indent=4) + "\n\n"
                    response += "Context:\n" + json.dumps(self.context, indent=4).replace('\\n', '\n').replace('\\t', '\t') + "\n\n"
                    response += "Response:\n" + oldResponse + "\n\n"
                self.request.wfile.write(response)
                return

            self.request.send_response(200)
            self.request.send_header("Content-type", self.contentType)
            for cookie in self.cookies:
                self.request.setCookie(cookie)
            self.request.end_headers()
            self.request.wfile.write(self.response)
            return

        except Exception, e:
            self.request.send_response(404)
            self.request.send_header("Content-type", 'text/html')
            self.request.end_headers()
            errorType, value, tb = sys.exc_info()
            response = "<body style='font-family: monospace'><h1>Error</h1><hr>"
            if DEBUG:
                response += self.request.requestline + "<hr>"
                response += "URL arguments:<br><pre>" + json.dumps(self.urlArgs, indent=4) + "</pre><hr>"
                response += "Headers:<br><pre>" + str(self.request.headers) + "</pre><hr>"
                response += "Error:<br><pre>" + "({0})".format(traceback.format_exception_only(errorType, value)) + "</pre><hr>"
                try:
                    response += "Traceback:<br><pre>"
                    for entry in traceback.extract_tb(tb):
                        response += "File {0}, line {1}, in {2}\n".format(entry[0], entry[1], entry[2])
                        response += "\t{0}\n\n".format(entry[3])
                    response += "</pre>"
                except:
                    logger.warning("Could not get traceback")
                    pass
            self.request.wfile.write(response)
            return

    def get(self):

        self.contentType = "text/html"
        response = "<body style='font-family: monospace'><h1>No view found</h1><hr>"
        if DEBUG:
            response += self.request.requestline + "<hr>"
            response += "URL arguments:<br><pre>" + json.dumps(self.urlArgs, indent=4) + "</pre><hr>"
            response += "Headers:<br><pre>" + str(self.request.headers) + "</pre><hr>"
            response += "View:<br><pre>" + self.__class__.__name__ + "</pre>"
        return response

    def post(self):

        self.contentType = "text/html"
        response = "<body style='font-family: monospace'><h1>No view found</h1><hr>"
        if DEBUG:
            response += self.request.requestline + "<hr>"
            response += "URL arguments:<br><pre>" + json.dumps(self.urlArgs, indent=4) + "</pre><hr>"
            response += "POST data:<br><pre>" + json.dumps(self.postData) + "</pre><hr>"
            response += "Headers:<br><pre>" + str(self.request.headers) + "</pre><hr>"
            response += "View:<br><pre>" + self.__class__.__name__ + "</pre>"
        return response

    def parseJsonPost(self):
        return json.loads(self.postData)

    def setContentType(self, contentType):
        self.contentType = contentType

    def renderTemplate(self, templateName):

        template = self.jinja2Env.get_template(templateName)
        content = template.render(self.context)
        self.setContentType('text/html')
        return content

    def addComponentToContext(self, componentName, key=None, override=False):

        if key is None:
            if len(componentName.split('.')) > 1:
                key = componentName[0:-(1 + len(componentName.split('.')[-1]))]
            else:
                key = componentName

        if key in self.context and override is False:
            logger.warning(
                "Could not add component '{componentName}' to context because the key '{key}' is already used. Use override=True in order to overwrite the old context entry".format(
                    componentName=componentName, key=key))
            return

        component = open(os.path.join(COMPONENT_DIRECTORY, componentName)).read()
        self.context[key] = component

    def addItemToContext(self, item, key, override=False):

        if key in self.context and override is False:
            logger.warning(
                "Could not add {itemType} item to context because the key '{key}' is already used. Use override=True in order to overwrite the old context entry".format(
                    itemType=type(item), key=key))
            return

        self.context[key] = item

    def switchView(self, newView):

        newView(self.request)
