from hashlib import pbkdf2_hmac
import os

from util import *
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

        existingUser = databaseController.getUserByUsername(registerDetails['user'])

        if existingUser is not None:
            errorList.append("Username already taken")

        if registerDetails["password"] != registerDetails["confirmPassword"]:
            errorList.append("Passwords do not match")

    def processSignInRequest(self, signInDetails):

        errorList = list()

        userData = databaseController.getUserByUsername(signInDetails["username"])

        if((userData is None) or (signInDetails["password"]!=userData["password"]))
            errorList.append("Wrong username or password")

        if(len(errorList)==0)
            session = os.urandom()
            hashinfo={
                "session_id" : session,
                "user_id": userData["user_id"],
                
            }
            databaseController.insertIntoSessions()


userController = userController()