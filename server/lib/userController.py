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



class userController():

    def createNewUser(self, registerDetails):

        errorList = list()
        success = True

        existingUser = databaseController.getUserByUsername(registerDetails['username'])

        debug("searched in database for user")

        if existingUser is not None:
            errorList.append("Username already taken")
            success = False

        existingUser = databaseController.getUserByEmail(registerDetails['email'])
        debug(existingUser)
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

        debug("inserted user into database")

        result = {"success": success, "errorList": errorList}

        return json.dumps(result)

    def processSignInRequest(self, signInDetails, userAgent, clientAddress):

        debug("[FUNC] processSignInRequest()")

        errorList = list()

        userData = databaseController.getUserByUsername(signInDetails["username"])

        debug("[INFO] Obtained user data")

        debug(userData)

        success = False

        if userData is not None:

            salt = userData[USER_SALT]

            pwd = hashlib.pbkdf2_hmac('sha256', signInDetails["password"], salt, 50000)
            finalPwd = binascii.hexlify(pwd)

            debug(finalPwd)
            debug(userData[USER_PASSWORD])



            if finalPwd != userData[USER_PASSWORD]:
                debug("[INFO] Password not valid")
            else:
                success = True
                debug("[INFO] Password valid")

        result = dict()

        if success:
            session = base64.b64encode(os.urandom(16))

            debug(session)

            sessionData = {
                "session_id": session,
                "user_id": userData[USER_ID],
                "date_created": datetime.datetime.now(),
                "last_connected": datetime.datetime.now(),
                "device": userAgent,
                "ip": clientAddress
            }

            debug(sessionData)

            databaseController.insertIntoSessions(sessionData)

            debug("[INFO] New session created")

            result["username"] = userData[USER_USERNAME]
            result["sessionId"] = session
        else:
            errorList.append("Wrong username or password")

        result["success"] = success
        result["errors"] = errorList

        debug(result)

        return json.dumps(result), success

    def validateUserSession(self, sessionData):

        debug("[FUNC] validateUserSession()")

        if sessionData == "expired" or sessionData is None or sessionData is False:
            return None

        userInfo = databaseController.getUserByUsername(sessionData["username"])
        sessionList = databaseController.getSessionById(sessionData["sessionId"])

        for session in sessionList:
            debug(session)
            if userInfo[USER_ID] == session[2]:
                return userInfo[USER_ID]

        return None


    def getUserInstanceById(self, userID):
        userBD = databaseController.getUserById(userID)[0]
        session = databaseController.getSessionById(userID)


        resultUser = user(userBD[USER_ID], session, userBD[USER_USERNAME], 50000, userBD[USER_SALT], userBD[USER_PASSWORD], userBD[USER_EMAIL], userBD[USER_CELL_NUMBER], userBD[USER_FIRST_NAME], userBD[USER_LAST_NAME], userBD[USER_COUNTRY], userBD[USER_STATE], userBD[USER_CITY], userBD[USER_ADRESS_1], userBD[USER_ADRESS_2], userBD[USER_ZIP_CODE], userBD[USER_CONTACT_INFO], userBD[USER_STATUS])

        return resultUser


userController = userController()
