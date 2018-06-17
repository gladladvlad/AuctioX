from apiController import *
from view import *

class jsonExportView(view):

    def get(self):

        return apiController.jsonExport(self.urlArgs)