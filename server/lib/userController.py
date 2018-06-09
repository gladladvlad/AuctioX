from hashlib import pbkdf2_hmac 

from util import *

#nu stiu daca trebuie :csf:
#CRYPT_SALT_SIZE = 32

class userController():
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
        passwordHash = pbkdf2_hmac('sha256', bytearray('passwordPlain'), bytearray('passwordSalt'), passwordIterCount)

        return passwordHash == self.passwordHash
