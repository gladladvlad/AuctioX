from view import *


class userRegistrationPage(view):

    def get(self):

        self.addItemToContext('Register', 'title')

        self.addComponentToContext('navbar.html')
        self.addComponentToContext('userRegistration_titlebar.html')
        self.addComponentToContext('userRegistration_main.html')

        return self.renderTemplate('userRegistration.html')


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

