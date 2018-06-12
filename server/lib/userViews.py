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
        debug("[INFO] userSignInRequest reached")


        return self.postData
