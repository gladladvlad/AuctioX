from view import *
from userController import *
from productController import *
from bidController import *
from util import *


class userRegistrationPageView(view):

    def get(self):
        logger.info("[VIEW] userRegistrationPageView")
        self.addItemToContext('Register', 'title')

        self.addComponentToContext('navbar.html')
        self.addComponentToContext('userRegistration_titlebar.html')
        self.addComponentToContext('userRegistration_styles.html')
        self.addComponentToContext('userRegistration_main.html')

        return self.renderTemplate('userRegistration.html')


class userRegistrationRequestView(view):

    def post(self):
        logger.info("[VIEW] userRegistrationRequestView")

        result = userController.createNewUser(self.parseJsonPost())

        logger.debug('userRegistrationRequestView generated result')

        return result


class userListingView(view):

    def get(self):
        logger.info("[VIEW] userListingView")

        self.addComponentToContext('userlisting_styles.html', 'style', True)
        self.setContentType('text/html')
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('userlistings.html')

        return content


class userSignInView(view):
    def get(self):
        logger.info("[VIEW] userSignInView")
        self.addComponentToContext('userSignIn_styles.html', 'style', True)
        self.setContentType('text/html')
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('userSignIn_content.html', 'content', True)
        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('userSignIn.html')

        return content


class userSignInRequestView(view):

    def post(self):
        logger.info("[VIEW] userSignInRequestView")

        result, success = userController.processSignInRequest(self.parseJsonPost(), self.request.headers["User-Agent"], self.request.client_address[0])

        if success:
            cookie = "user_session_identifier={data}; Expires={exp}".format(data=base64.b64encode(result), exp=(datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%a, %d %b %Y %H:%M:%S GMT"))
            self.cookies.append(cookie)

        return result


class userSignOutRequestView(view):

    def get(self):
        logger.info("[VIEW] userSignOutRequestView")

        try:
            databaseController.removeSessionId(self.sessionData["sessionId"])
        except:
            pass

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
        logger.info("[VIEW] userMyListingsView")

        if userController.validateUserSession(self) is None:
            logger.warning("No active session. Redirecting to sign in.")
            self.switchView(userSignInView)
            return False

        user = userController.getUserInstanceByUsername(self.sessionData['username'])
        products = productController.getUserProductsById(user.UID)

        self.setContentType('text/html')

        self.addItemToContext(products, 'products', True)

        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('myListings.html')
        return content


class userMyBidsView(view):

    def get(self):
        logger.info("[VIEW] userMyBidsView")

        if userController.validateUserSession(self) is None:
            logger.warning("No active session. Redirecting to sign in.")
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

        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('myBids.html')
        return content

class userTransactionsView(view):
    def get(self):
        logger.info("[VIEW] transactionsView")

        self.setContentType('text/html')

        userId = userController.validateUserSession(self)
        if userId is None:
            return 'Fail! You must be logged in!'


        transactionsSelling = userController.getTransactionsBySellerId(userId)
        transactionsBuying = userController.getTransactionsByBuyerId(userId)
        self.addItemToContext(transactionsSelling, 'transell', True)
        self.addItemToContext(transactionsBuying, 'tranbuy', True)

        self.addComponentToContext('transactions_styles.html', 'style', True)

        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('myTransactions.html')

        return content

class myAccountView(view):
    def get(self):
        logger.info("[VIEW] myAccountView")

        self.setContentType('text/html')

        userId = userController.validateUserSession(self)
        if userId is None:
            logger.warning("No active session. Redirecting to sign in.")
            self.switchView(userSignInView)
            return False

        loggedUser = userController.getUserInstanceByUsername(self.sessionData['username'])
        loggedUser.setAdmin()
        self.addItemToContext(loggedUser, 'userlog', True)


        usernameRequest = ''
        if self.urlArgs.has_key('user'):
            usernameRequest = self.urlArgs['user']
        else:
            usernameRequest = self.sessionData['username']


        user = userController.getUserInstanceByUsername(usernameRequest)
        self.addItemToContext(user, 'userreq', True)


        reportsFrom = userController.getReportsByFromUserId(user.UID)
        reportsTo = userController.getReportsByToUserId(user.UID)

        self.addItemToContext(reportsFrom, 'repfrom', True)
        self.addItemToContext(reportsTo, 'repto', True)


        products = productController.getUserProductsById(user.UID)

        self.addItemToContext(products, 'products', True)


        bids = bidController.getUserBidInstancesById(user.UID)

        bidProdList = []
        for bid in bids:
            bidProduct = productController.getProductInstanceById(bid.productID)

            bidProdList.append((bid, bidProduct))

        self.addItemToContext(user, 'user', True)
        self.addItemToContext(bidProdList, 'bidprod', True)


        transactionsSelling = userController.getTransactionsBySellerId(user.UID)
        transactionsBuying = userController.getTransactionsByBuyerId(user.UID)
        self.addItemToContext(transactionsSelling, 'transell', True)
        self.addItemToContext(transactionsBuying, 'tranbuy', True)


        self.addComponentToContext('myaccount_styles.html', 'style', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('myAccount.html')

        return content

class cancelBidView(view):
    def get(self):
        logger.info("[VIEW] cancelBidView")

        if not self.urlArgs.has_key('bidid'):
            return 'Fail! No bid provided!'

        userId = userController.validateUserSession(self)
        if userId is None:
            return 'Fail! You must be logged in!'


        user = userController.getUserInstanceById(userId)
        user.setAdmin()


        bid = bidController.getBidById(int(self.urlArgs['bidid']))
        if bid.userID != userId and user.isAdmin != 1:
            return 'Fail! You cannot cancel someone else\'s bid!'


        answer = bidController.cancelBid(int(self.urlArgs['bidid']))
        return answer

class cancelReportView(view):
    def get(self):
        logger.info("[VIEW] cancelReport")
        
        if not self.urlArgs.has_key('repid'):
            return 'Fail! No report provided!'

        userId = userController.validateUserSession(self)
        if userId is None:
            return 'Fail! You must be logged in!'


        user = userController.getUserInstanceById(userId)
        user.setAdmin()

        if user.isAdmin != 1:
            return 'Fail! You cannot cancel someone a report unless you are an admin!'


        answer = userController.cancelReport(int(self.urlArgs['repid']))
        return answer

class reportDashboardView(view):

    def get(self):
        logger.info("[VIEW] userRegistrationPageView")

        content =  self.renderTemplate('reportDashboard.html')
        return content
