import views
from jinja2 import Template

class jinjatest(views.view):

    def get(self):
        navbar = open('{path}/navbar.html'.format(path=views.DEFAULT_HTML_PATH)).read()
        context = {'navbar': navbar}
        self.setContentType('text/html')

        template = Template(open('{path}/jinjatest.html'.format(path=views.DEFAULT_HTML_PATH)).read())
        content = template.render(context)
        return content