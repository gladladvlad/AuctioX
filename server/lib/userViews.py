from view import *
from userController import *
from productController import *
from bidController import *

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

        result, success = userController.processSignInRequest(self.parseJsonPost(), self.request.headers["User-Agent"], self.request.client_address[0])

        if success:
            cookie = "user_session_identifier={data}; Expires={exp}".format(data=base64.b64encode(result), exp=(datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%a, %d %b %Y %H:%M:%S GMT"))
            self.cookies.append(cookie)

        return result

class userSignOutRequestView(view):

    def get(self):
        debug("[VIEW] userSignOutRequestView")

        cookie = "user_session_identifier={data}; Expires={exp}".format(data="expired",exp=datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"))
        self.cookies.append(cookie)

        if "sessionData" in self.context:
            del self.context["sessionData"]

        self.addComponentToContext('userSignOut_styles.html', 'style', True)
        self.setContentType('text/html')
        self.addComponentToContext('userSignOut_content.html', 'content', True)
        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('userSignOut.html')
        return content

class userMyListingsView(view):

    def get(self):
        debug("[VIEW] userMyListingsView")

        if userController.validateUserSession(self.sessionData) is None:
            debug("[INFO] No active session. Redirecting to sign in.")
            self.switchView(userSignInView)
            return False

        user = userController.getUserInstanceByUsername(self.sessionData['username'])
        products = productController.getUserProductsById(user.UID)

        self.setContentType('text/html')

        self.addItemToContext(products.asDict(), 'products', True)

        self.addComponentToContext('myListings_content.html', 'content', True)
        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('myListings.html')
        return content

class userMyBidsView(view):

    def get(self):
        debug("[VIEW] userMyBidsView")

        if userController.validateUserSession(self.sessionData) is None:
            debug("[INFO] No active session. Redirecting to sign in.")
            self.switchView(userSignInView)
            return False

        user = userController.getUserInstanceByUsername(self.sessionData['username'])
        bids = bidController.getUserBidInstancesById(user.UID)

        bidProdList = []
        for bid in bids:
            bidProduct = productController.getProductInstanceById(bid.productID)

            bidProdList.append((bid, bidProduct))

        self.setContentType('text/html')

        self.addItemToContext(user, 'user', True)
        self.addItemToContext(bidProdList, 'bidprod', True)

        self.addComponentToContext('myBids_content.html', 'content', True)
        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('myBids.html')
        return content
