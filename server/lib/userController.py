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
    def __init__(self, newUID, newSessionID, newUsername, newPasswordIterCount, newPasswordSalt, newPasswordHash, newEmail, newPhone):
        self.UID = str(newUID)
        self.sessionID = str(newSessionID)
        self.username = str(newUsername)
        self.passwordIterCount = int(newPasswordIterCount)
        self.passwordSalt = bytearray(newPasswordSalt)
        self.passwordHash = bytearray(newPasswordHash)
        self.email = str(newEmail)
        self.phone = str(newPhone)

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

        return result


userController = userController()