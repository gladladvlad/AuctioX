from view import *
from productController import *
import json
import math
from userController import *
from productController import *
from userViews import *


searchProductCountKey = 'prods'
searchPageIndexKey = 'page'
searchPageSizeKey = 'psize'
searchQueryKey = 'query'

searchFilterPriceMin = 'min_price'
searchFilterPriceMax = 'max_price'
searchFilterCondition = 'conditie'
searchFilterDateAdded = 'date_added'
searchFilterDateExpirese = 'date_expires'

searchDefaultPageSize = 5

#productCount = 12

productIDKey = "prodid"


class createListingView(view):
    def get(self):
        logger.info('[VIEW] createListings')

        if userController.validateUserSession(self) is None:
            logger.debug("No active session. Redirecting to sign in.")
            self.switchView(userSignInView)
            return False

        self.addComponentToContext('createlisting_styles.html', 'style', True)
        self.addComponentToContext('createlisting_content.html', 'content', True)
        self.setContentType('text/html')
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)
        content = self.renderTemplate('createlisting.html')

        return content


class createListingRequestView(view):
    def post(self):
        logger.info('[VIEW] createListingsRequestView')
        user = userController.getUserInstanceById(userController.validateUserSession(self))

        result = productController.createListing(self.parseJsonPost(), user)

        return result


class searchView(view):
    def get(self):
        logger.info('[VIEW] searchView reached')

        self.setContentType('text/html')

        self.addComponentToContext('search_filters.html', 'search_filters', True)
        self.addComponentToContext('search_styles.html', 'search_styles', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)

        content = self.renderTemplate('search.html')

        return content


class searchProductIDsView(view):
    skipUserValidation = True
    def post(self):
        logger.info('[VIEW] searchProductIDsView reached')

        self.setContentType('application/json')


        args = self.parseJsonPost()

        query = args.pop('query', '')
        args.pop('psize', None)

        sortBy, sortHow = None, None
        sort = args.pop('sort', None)
        if not sort is None:
            sortBy = sort[0]
            sortHow = sort[1]

        productsByQuery = productController.getProductsByFilter(args, sortBy, sortHow, query)


        productIDs = []
        for iter in xrange(0, len(productsByQuery)):
            productIDs.append(productsByQuery[iter].productID)


        return json.dumps(productIDs)


class searchPageView(view):
    skipUserValidation = True
    def get(self):
        logger.info('[VIEW] searchPageView')

        if not self.urlArgs.has_key(searchPageSizeKey):
            self.urlArgs[searchPageSizeKey] = searchDefaultPageSize

        if not self.urlArgs.has_key(searchProductCountKey):
            raise ValueError("Did not receive product count!")

        self.setContentType('text/html')

        products = []

        productIter = 0
        productsDone = 0
        itemKey = 'item{0}'.format(productIter)

        for i in xrange(0, (int(self.urlArgs[searchProductCountKey]))):
            if self.urlArgs.has_key(itemKey):
                tmpProduct = productController.getProductInstanceById(int(self.urlArgs[itemKey]))
                tmpProduct.auction = productController.getAuctionTypeStr(tmpProduct.auction)
                tmpProduct.condition = productController.getConditionStr(tmpProduct.condition)


                products.append(tmpProduct.asDict())
                productsDone += 1


            productIter += 1
            itemKey = 'item{0}'.format(productIter)
            if (productsDone == int(self.urlArgs[searchPageSizeKey])):
                break

        logger.debug(len(products))

        pages = [dict()]

        for i in xrange(0, int(math.ceil((float(self.urlArgs[searchProductCountKey]) / float(self.urlArgs[searchPageSizeKey]))))):
            dicterator = {'index' : i}

            pages.append(dicterator)

        self.addItemToContext(pages, 'pages', True)

        self.addComponentToContext('search_filters.html', 'search_filters', True)
        self.addComponentToContext('search_styles.html', 'search_styles', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)

        self.addItemToContext(products, 'products', True)

        page = self.renderTemplate('search_page.html')

        return page


class productView(view):
    def get(self):
        logger.info('[VIEW] productView reached')

        if not self.urlArgs.has_key(productIDKey):
            raise ValueError("No product provided!")



        product = productController.getProductInstanceById(int(self.urlArgs[productIDKey]))
        product.condition = productController.getConditionStr(product.condition)
        product.auction = productController.getAuctionTypeStr(product.auction)

        logger.debug(product.asDict())

        self.addItemToContext(product.asDict(), 'product', True)

        seller = userController.getUserInstanceById(int(product.ownerID))

        logger.debug(seller.asDict())

        self.addItemToContext(seller.asDict(), 'seller', True)

        qaList = list()

        questionList = databaseController.executeSQLCommand("select * from question where product_id={0}".format(product.productID))
        responseList = databaseController.executeSQLCommand("select * from response where product_id={0}".format(product.productID))

        for q in questionList:

            qaPair = dict()

            qaPair["questionText"] = q[QUESTION_CONTENT]

            for r in responseList:

                if r[RESPONSE_ANSWER_KEY] == q[QUESTION_ANSWER_KEY]:
                    qaPair["answerText"] = r[RESPONSE_CONTENT]
                    break

            qaPair["answerKey"] = q[QUESTION_ANSWER_KEY]

            userData = databaseController.getUserById(q[QUESTION_USER_ID])[0]
            print userData

            qaPair["userId"] = q[QUESTION_USER_ID]
            qaPair["username"] = userData[USER_USERNAME]

            qaList.append(qaPair)

        self.addItemToContext(qaList, 'qaList')
        self.addComponentToContext('product_styles.html', 'product_styles', True)
        self.addComponentToContext('navbar.html', 'navbar', True)
        self.addComponentToContext('footer.html', 'footer', True)

        content = self.renderTemplate('product.html')

        databaseController.incrementView(product.productID)

        logger.debug('content rendered!')

        return content


class bidView(view):
    def get(self):
        logger.info("[VIEW] bidView")

        if not self.urlArgs.has_key('prodid'):
            return 'Fail! No product provided!'

        if not self.urlArgs.has_key('amount'):
            return 'Fail! No amount provided!'

        userId = userController.validateUserSession(self)
        if userId is None:
            return 'Fail! You must be logged in!'


        bidAmount = int(self.urlArgs['amount'])

        return productController.bid(userId, int(self.urlArgs['prodid']), bidAmount)


class buyView(view):
    def get(self):
        logger.info("[VIEW] bidView")

        if not self.urlArgs.has_key('prodid'):
            return 'Fail! No product provided!'

        userId = userController.validateUserSession(self)
        if userId is None:
            return 'Fail! You must be logged in!'

        return productController.buy(userId, int(self.urlArgs['prodid']))



class cancelProductView(view):
    def get(self):
        logger.info("[VIEW] bidView")

        if not self.urlArgs.has_key('prodid'):
            return 'Fail! No product provided!'

        userId = userController.validateUserSession(self)
        if userId is None:
            return 'Fail! You must be logged in!'

        logger.info("======================")
        logger.info("======================")
        logger.info("======================")
        logger.info("DONE")
        user = userController.getUserInstanceById(userId)
        logger.info("DONE")
        user.setAdmin()
        logger.info("DONE")
        product = productController.getProductInstanceById(int(self.urlArgs['prodid']))
        logger.info("DONE")

        if userId != product.ownerID and user.isAdmin != 1:
            return 'Fail! You cannot cancel someone else\'s listing!'

        logger.info("DONE")
        return productController.cancelProduct(int(self.urlArgs['prodid']))



class cancelTransactionView(view):
    def get(self):
        logger.info("[VIEW] cancelTransactionView")

        if not self.urlArgs.has_key('prodid'):
            return 'Fail! No product provided!'

        userId = userController.validateUserSession(self)
        if userId is None:
            return 'Fail! You must be logged in!'

        user = userController.getUserInstanceById(userId)
        user.setAdmin()

        if userID != transaction.sellerId and userID != transaction.buyerId and user.isAdmin != 1:
            return 'Fail! You cannot cancel someone else\'s transaction!'

        return productController.cancelTransaction(userId, int(self.urlArgs['prodid']))



class confirmTransactionView(view):
    def get(self):
        logger.info("[VIEW] confirmTransactionView")

        if not self.urlArgs.has_key('prodid'):
            return 'Fail! No product provided!'

        userId = userController.validateUserSession(self)
        if userId is None:
            return 'Fail! You must be logged in!'


        user = userController.getUserInstanceById(userId)
        user.setAdmin()

        if userID != transaction.sellerId and userID != transaction.buyerId and user.isAdmin != 1:
            return 'Fail! You cannot confirm someone else\'s transaction!'


        return productController.confirmTransaction(userId, int(self.urlArgs['prodid']))



class postQuestionRequestView(view):
    def post(self):
        logger.info("[VIEW] postQuestionRequestView")
        data = self.parseJsonPost()

        userId = None
        productData = None

        try:
            logger.debug("Validating user session")
            userId = userController.validateUserSession(self)
            logger.debug("Gathering product data")
            productData = databaseController.getProductDataById(data["productId"])[0]
        except:
            pass

        logger.debug("Validating question")

        errors = list()
        success = False

        if data["text"] == "":
            errors.append("You must enter a question.")
            logger.debug("User question is empty.")

        if userId is None:
            errors.append("You must be signed in in order to post questions.")
            logger.debug("User is not signed in")

        if productData is None:
            errors.append("Product non existent.")
            logger.debug("Product non existent")

        if productData is not None and userId is not None:
            if productData[PROD_USER_ID] == userId:
                errors.append("You cannot ask questions about your own product.")
                logger.debug("User tried asking question on own listing")

        if len(errors) == 0:
            logger.debug("No errors found. Inserting question")

            answerKey = "{0}_{1}".format(data["productId"], binascii.hexlify(os.urandom(2)))

            databaseController.insertIntoQuestion({"product_id": data["productId"], "user_id": userId, "title": answerKey, "content": data["text"]})

            success = True
        else:
            logger.debug("Errors have been found.")

        return json.dumps({"success": success, "errors": errors})


class postAnswerRequestView(view):
    def post(self):
        logger.info("[VIEW] postAnswerRequestView")
        data = self.parseJsonPost()

        userId = None
        productData = None

        try:
            logger.debug("Validating user session")
            userId = userController.validateUserSession(self)
            logger.debug("Gathering product data")
            productData = databaseController.getProductDataById(data["productId"])[0]
        except:
            pass

        logger.debug("Validating question")

        errors = list()
        success = False

        if data["text"] == "":
            errors.append("You must enter an answer.")
            logger.debug("User answer is empty.")

        if userId is None:
            errors.append("You must be signed in in order to answer questions.")
            logger.debug("User is not signed in")

        if productData is None:
            errors.append("Product non existent.")
            logger.debug("Product non existent")

        if productData is not None and userId is not None:
            if productData[PROD_USER_ID] != userId:
                errors.append("You can only answer questions about your listing.")
                logger.debug("User tried answering question on someone else's listing")

        if len(errors) == 0:
            logger.debug("No errors found. Inserting question")

            answerKey = data["answerKey"]

            databaseController.insertIntoResponse({"product_id": data["productId"], "user_id": userId, "title": answerKey, "content": data["text"]})

            success = True
        else:
            logger.debug("Errors have been found.")

        return json.dumps({"success": success, "errors": errors})

