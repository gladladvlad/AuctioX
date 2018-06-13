from view import *
from userController import *

class userRegistrationPageView(view):

    def get(self):

        self.addItemToContext('Register', 'title')

        self.addComponentToContext('navbar.html')
        self.addComponentToContext('userRegistration_titlebar.html')
        self.addComponentToContext('userRegistration_styles.html')
        self.addComponentToContext('userRegistration_main.html')

        return self.renderTemplate('userRegistration.html')


class userRegistrationRequestView(view):

    def post(self):
        debug('[INFO] userRegistrationRequestView reached')

        result = userController.createNewUser(self.parseJsonPost())

        debug('[INFO] userRegistrationRequestView generated result')

        return result

class userListingView(view):

    def get(self):
        debug('[INFO] userListings reached')

        self.addComponentToContext('userlisting_styles.html', 'style', True)
        self.setContentType('text/html')
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('userlisting_content.html', 'content', True)
        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('userlistings.html')

        return content

class userSignInView(view):
    def get(self):
        self.addComponentToContext('userSignIn_styles.html', 'style', True)
        self.setContentType('text/html')
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('userSignIn_content.html', 'content', True)
        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('userSignIn.html')

        return content

class userSignInRequestView(view):

    def post(self):
        debug("[VIEW] userSignInRequest")

        result = userController.processSignInRequest(self.parseJsonPost(), self.request.headers["User-Agent"], self.request.client_address[0])

        if result["success"]:
            cookie = "user_session_identifier={data}; Expires={exp}".format(data=base64.b64encode(json.dumps(result)), exp=(datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%a, %d %b %Y %H:%M:%S GMT"))
            self.cookies.append(cookie)

        return result

class userSignOutRequestView(view):

    def get(self):
        debug("[VIEW] userSignOutRequestView")

        cookie = "user_session_identifier={data}; Expires={exp}".format(data="expired",exp=datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"))
        self.cookies.append(cookie)

        if "sessionData" in self.context:
            del self.context["sessionData"]

        return