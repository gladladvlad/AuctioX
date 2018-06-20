import base64
import binascii
import datetime
import hashlib
import os
from hashlib import pbkdf2_hmac
from util import *
import json
import re

from databaseController import *
from bidController import *
from productController import *


#nu stiu daca trebuie :csf:
#CRYPT_SALT_SIZE = 32

class user():
    def __init__(self, newUID, newSessionID, newUsername, newPasswordIterCount, newPasswordSalt, newPasswordHash, newEmail, newPhone, newFirstName, newLastName, newCountry, newState, newCity, newAdress1, newAdress2, newZipCode, newContactInfo, newStatus):
        self.UID = newUID
        self.sessionID = newSessionID
        self.username = newUsername
        self.passwordIterCount = newPasswordIterCount
        self.passwordSalt = newPasswordSalt
        self.passwordHash = newPasswordHash
        self.email = newEmail
        self.phone = newPhone
        self.firstName = newFirstName
        self.lastName = newLastName
        self.country = newCountry
        self.state = newState
        self.city = newCity
        self.adress1 = newAdress1
        self.adress2 = newAdress2
        self.zipCode = newZipCode
        self.contactInfo = newContactInfo
        self.status = newStatus
        self.isAdmin = 0

    def setAdmin(self):
        self.isAdmin = databaseController.getIsAdminById(self.UID)[0]

    def asDict(self):
        result = dict()

        #'iterations' : self.passwordIterCount,
        #'salt' : self.passwordSalt,
        #'passHash' : self.passwordHash,
        result = {'id' : self.UID,
                'username' : self.username,
                'email' : self.email,
                'phone' : self.phone,
                'firstName' : self.firstName,
                'lastName' : self.lastName,
                'country' : self.country,
                'state' : self.state,
                'city' : self.city,
                'adress1' : self.adress1,
                'adress2' : self.adress2,
                'zip' : self.zipCode,
                'contact' : self.contactInfo,
                'status' : self.status}

        return result

    def validatePassword(self, passwordIterCount, passwordSalt, passwordPlain):
        passwordHash = pbkdf2_hmac('sha256', bytearray('passwordPlain'), bytearray('passwordSalt'),
                                   passwordIterCount)

        return passwordHash == self.passwordHash



class transaction():
    def __init__(self, newTransactionId, newProduct, newTransactionSellerId, newTransactionBuyerId, newTransactionProductId, newTransactionStatus, newTransactionDateCreated, newTransactionDateExpires, newTransactionSellerConfirm, newTransactionBuyerConfirm):
        self.id = newTransactionId
        self.product = newProduct
        self.sellerId = newTransactionSellerId
        self.buyerId = newTransactionBuyerId
        self.productId = newTransactionProductId
        self.status = newTransactionStatus
        self.dateCreated = newTransactionDateCreated
        self.dateExpires = newTransactionDateExpires
        self.sellerConfirm = newTransactionSellerConfirm
        self.buyerConfirm = newTransactionBuyerConfirm



class report():
    def __init__(self, newReportId, newReportType, newReportFrom,  newReportTo, newReportProductId,  newReportReason, newReportDetails,  newReportResolved, newReportDateResolved,  newReportIsValid):
        self.id = newReportId
        self.type = newReportType
        self.fromId = newReportFrom
        self.toId = newReportTo
        self.productId = newReportProductId
        self.reason = newReportReason
        self.details = newReportDetails
        self.resolved = newReportResolved
        self.dateResolved = newReportDateResolved
        self.isValid = newReportIsValid



class userController():

    def createNewUser(self, registerDetails):
        logger.info("[START] createNewUser()")

        errorList = list()
        success = True

        existingUser = databaseController.getUserByUsername(registerDetails['username'])

        logger.debug("Searched in database for user")

        if existingUser is not None:
            errorList.append("Username already taken")
            success = False

        existingUser = databaseController.getUserByEmail(registerDetails['email'])

        logger.debug("existingUser:")
        logger.debug(existingUser)

        if len(existingUser) > 0:
            errorList.append("Email is already in use")
            success = False

        if re.match("^[0-9A-Za-z\-_.]*[@][0-9A-Za-z]*.[0-9A-Za-z]*$", registerDetails["email"]) is None:
            errorList.append("Invalid email")
            success = False

        if (len(registerDetails["username"]) < 4 or len(registerDetails["username"]) > 16):
            errorList.append("Username length is not between 4 and 16 characters")
            success = False

        if re.match("^[0-9A-Za-z\-_]*$", registerDetails["username"]) is None:
            errorList.append("Username contains invalid characters")
            success = False

        if (len(registerDetails["password"]) < 8 or len(registerDetails["password"]) > 32):
            errorList.append("Password length is not between 8 and 32 characters")
            success = False

        if re.match("^[0-9A-Za-z,.+\-_?!]*$", registerDetails["password"]) is None:
            errorList.append("Password contains invalid characters")
            success = False

        if registerDetails["password"] != registerDetails["confirmPassword"]:
            errorList.append("Passwords do not match")
            success = False

        if len(errorList) == 0:
            salt = os.urandom(16)
            pwd = hashlib.pbkdf2_hmac('sha256', registerDetails["password"], salt, 50000)
            finalPwd = binascii.hexlify(pwd)
            success = True
            info = {"username" : registerDetails["username"],
                    "password" : finalPwd,
                    "first_name" : registerDetails["firstName"],
                    "last_name" : registerDetails["lastName"],
                    "email" : registerDetails["email"],
                    "country": registerDetails["country"],
                    "state": registerDetails["state"],
                    "city" : registerDetails["city"],
                    "adress_1" : registerDetails["address1"],
                    "adress_2" : registerDetails["address2"],
                    "zip_code" : registerDetails["zipCode"],
                    "contact_info" : "",
                    "cell_number" : registerDetails["tel"],
                    "salt": salt,
                    "status" : 1}

            databaseController.insertIntoUser(info)

        logger.debug("User inserted into database")

        result = {"success": success, "errors": errorList}

        return json.dumps(result)

    def processSignInRequest(self, signInDetails, userAgent, clientAddress):
        logger.info("[START] processSignInRequest()")

        errorList = list()

        userData = databaseController.getUserByUsername(signInDetails["username"])

        logger.debug("userData:")
        logger.debug(userData)

        success = False

        if userData is not None:

            salt = userData[USER_SALT]

            pwd = hashlib.pbkdf2_hmac('sha256', signInDetails["password"], salt, 50000)
            finalPwd = binascii.hexlify(pwd)

            logger.debug("finalPwd:")
            logger.debug(finalPwd)
            logger.debug("userData[USER_PASSWORD]:")
            logger.debug(userData[USER_PASSWORD])



            if finalPwd != userData[USER_PASSWORD]:
                logger.debug("Password not valid")
            else:
                success = True
                logger.debug("Password valid")

        result = dict()

        if success:
            session = base64.b64encode(os.urandom(16))

            logger.debug("session:")
            logger.debug(session)

            sessionData = {
                "session_id": session,
                "user_id": userData[USER_ID],
                "date_created": datetime.datetime.now(),
                "last_connected": datetime.datetime.now(),
                "device": userAgent,
                "ip": clientAddress
            }

            logger.debug("sessionData:")
            logger.debug(sessionData)

            databaseController.insertIntoSessions(sessionData)

            logger.debug("New session created")

            result["username"] = userData[USER_USERNAME]
            result["sessionId"] = session
        else:
            errorList.append("Wrong username or password")

        result["success"] = success
        result["errors"] = errorList

        logger.debug("result:")
        logger.debug(result)

        return json.dumps(result), success

    def validateUserSession(self, view):
        logger.info("[START] validateUserSession()")

        if not hasattr(view, "sessionData"):
            return None

        if view.sessionData is None:
            return None

        if view.sessionData == "expired" or view.sessionData is False:
            return None

        userInfo = databaseController.getUserByUsername(view.sessionData["username"])
        sessionList = databaseController.getSessionById(view.sessionData["sessionId"])

        if userInfo is None:
            return None

        logger.debug("Found {0} sessions for user {1}".format(len(sessionList), userInfo[USER_USERNAME]))

        for session in sessionList:
            if userInfo[USER_ID] == session[2]:
                return userInfo[USER_ID]

        return None

    def getUserInstanceById(self, userID):
        logger.info("[START] getUserInstanceById()")

        userBD = databaseController.getUserById(userID)[0]
        session = databaseController.getSessionById(userID)

        resultUser = user(userBD[USER_ID], session, userBD[USER_USERNAME], 50000, userBD[USER_SALT], userBD[USER_PASSWORD], userBD[USER_EMAIL], userBD[USER_CELL_NUMBER], userBD[USER_FIRST_NAME], userBD[USER_LAST_NAME], userBD[USER_COUNTRY], userBD[USER_STATE], userBD[USER_CITY], userBD[USER_ADRESS_1], userBD[USER_ADRESS_2], userBD[USER_ZIP_CODE], userBD[USER_CONTACT_INFO], userBD[USER_STATUS])

        return resultUser

    def getUserInstanceByUsername(self, key):
        logger.info("[START] getUserInstanceByUsername()")

        userBD = databaseController.getUserByUsername(key)

        session = databaseController.getSessionById(userBD[USER_ID])

        resultUser = user(userBD[USER_ID], session, userBD[USER_USERNAME], 50000, userBD[USER_SALT], userBD[USER_PASSWORD], userBD[USER_EMAIL], userBD[USER_CELL_NUMBER], userBD[USER_FIRST_NAME], userBD[USER_LAST_NAME], userBD[USER_COUNTRY], userBD[USER_STATE], userBD[USER_CITY], userBD[USER_ADRESS_1], userBD[USER_ADRESS_2], userBD[USER_ZIP_CODE], userBD[USER_CONTACT_INFO], userBD[USER_STATUS])

        return resultUser


    def getReportsByFromUserId(self, userID):
        logger.info("[START] getReportByFromUserId()")
        repBD = databaseController.getReportByFromUserId(userID)

        resRepList = []
        for rep in repBD:
            repBuf = report(rep[REPORT_ID], rep[REPORT_TYPE], rep[REPORT_FROM], rep[REPORT_TO], rep[REPORT_PRODUCT_ID], rep[REPORT_REASON], rep[REPORT_DETAILS], rep[REPORT_RESOLVED], rep[REPORT_DATE_RESOLVED], rep[REPORT_IS_VALID])

            resRepList.append(repBuf)

        return resRepList


    def getReportsByToUserId(self, userID):
        logger.info("[START] getReportByFromUserId()")
        repBD = databaseController.getReportByToUserId(userID)

        resRepList = []
        for rep in repBD:
            repBuf = report(rep[REPORT_ID], rep[REPORT_TYPE], rep[REPORT_FROM], rep[REPORT_TO], rep[REPORT_PRODUCT_ID], rep[REPORT_REASON], rep[REPORT_DETAILS], rep[REPORT_RESOLVED], rep[REPORT_DATE_RESOLVED], rep[REPORT_IS_VALID])

            resRepList.append(repBuf)

        return resRepList



    def getTransactionInstanceById(self, transID):
        trans = databaseController.getTransactionById(transID)[0]

        resTrans = transaction(trans[TRANSACTION_ID], None, trans[TRANSACTION_SELLER_ID], trans[TRANSACTION_BUYER_ID], trans[TRANSACTION_PRODUCT_ID], trans[TRANSACTION_STATUS], trans[TRANSACTION_DATE_CREATED], trans[TRANSACTION_DATE_EXPIRES], trans[TRANSACTION_SELLER_CONFIRM], trans[TRANSACTION_BUYER_CONFIRM])

        return resTrans



    def getTransactionsBySellerId(self, userID):
        logger.info("[START] getTransactionsBySellerId()")
        transBD = databaseController.getTransactionBySellerId(userID)

        #logger.info(transBD[0])
        #logger.info(transBD[1])

        resTransList = []
        for trans in transBD:
            productBuf = productController.getProductInstanceById(trans[TRANSACTION_PRODUCT_ID])
            productBuf.auction = productController.getAuctionTypeStr(productBuf.auction)
            productBuf.condition = productController.getConditionStr(productBuf.condition)

            transBuf = transaction(trans[TRANSACTION_ID], productBuf, trans[TRANSACTION_SELLER_ID], trans[TRANSACTION_BUYER_ID], trans[TRANSACTION_PRODUCT_ID], trans[TRANSACTION_STATUS], trans[TRANSACTION_DATE_CREATED], trans[TRANSACTION_DATE_EXPIRES], trans[TRANSACTION_SELLER_CONFIRM], trans[TRANSACTION_BUYER_CONFIRM])

            resTransList.append(transBuf)

        return resTransList



    def getTransactionsByBuyerId(self, userID):
        logger.info("[START] getTransactionsByBuyerId()")
        transBD = databaseController.getTransactionByBuyerId(userID)

        #logger.info(transBD[0])
        #logger.info(transBD[1])

        resTransList = []
        for trans in transBD:
            productBuf = productController.getProductInstanceById(trans[TRANSACTION_PRODUCT_ID])
            productBuf.auction = productController.getAuctionTypeStr(productBuf.auction)
            productBuf.condition = productController.getConditionStr(productBuf.condition)

            transBuf = transaction(trans[TRANSACTION_ID], productBuf, trans[TRANSACTION_SELLER_ID], trans[TRANSACTION_BUYER_ID], trans[TRANSACTION_PRODUCT_ID], trans[TRANSACTION_STATUS], trans[TRANSACTION_DATE_CREATED], trans[TRANSACTION_DATE_EXPIRES], trans[TRANSACTION_SELLER_CONFIRM], trans[TRANSACTION_BUYER_CONFIRM])

            resTransList.append(transBuf)

        return resTransList

userController = userController()
