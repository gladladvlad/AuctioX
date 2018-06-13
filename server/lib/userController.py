import base64
import binascii
import datetime
import hashlib
import os
from hashlib import pbkdf2_hmac

from databaseController import databaseController


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
        status = True;

        existingUser = databaseController.getUserByUsername(registerDetails['user'])

        debug("searched in database for user")

        if existingUser is not None:
            errorList.append("Username already taken")
            success = False;

        if registerDetails["password"] != registerDetails["confirmPassword"]:
            errorList.append("Passwords do not match")
            success = False;

        if len(errorList) == 0:
            salt = os.urandom(16);
            pwd = hashlib.pbkdf2_hmac('sha256', registerDetails["password"], salt, 50000)
            binascii.hexlify(pwd);
            success = True;
            info = {"username" : registerDetails["username"],
                    "password" : registerDetails["password"],
                    "first_name" : registerDetails["first_name"],
                    "last_name" : registerDetails["last_name"],
                    "email" : registerDetails["email"],
                    "country": registerDetails["country"],
                    "state": registerDetails["state"],
                    "city" : registerDetails["city"],
                    "adress_1" : registerDetails["adress_1"],
                    "adress_2" : registerDetails["adress_2"],
                    "zip_code" : registerDetails["zip_code"],
                    "contact_info" : registerDetails["contact_info"],
                    "cell_number" : registerDetails["cell_number"],
                    "salt": salt,
                    "status" : 1}
            databaseController.controller.insertIntoUser(info)
        result = {"success": success, "errorList": errorList}

        return result;

    def processSignInRequest(self, signInDetails):

        errorList = list()

        userData = databaseController.getUserByUsername(signInDetails["username"])

        if((userData is None) or (signInDetails["password"]!=userData["password"])):
            errorList.append("Wrong username or password")

        if(len(errorList)==0):
            session = base64.b64ncode(os.urandom(16))
            hashinfo={
                "session_id" : session,
                "user_id": userData["user_id"],
                "date_created": datetime.datetime.now(),
                "date_espires": datetime.datetime.now() + datetime.timedelta(days=5),
                "device": signInDetails["device"],
                "ip":signInDetails["ip"]
            }
            databaseController.insertIntoSessions(hashinfo)
            result={
                "errors":errorList,
                "success": (len(errorList)==0),
                "username":userData["username"],
                "sessionId":session
                }
            return result
        else:
            result={
                "errors":errorList,
                "success":(len(errorList)==0)
            }
            return result


userController = userController()