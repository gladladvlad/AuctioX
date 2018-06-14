from databaseController import *

class bid():
    def __init__(self, newBidID, newUserID, newProductID, newStatus, newValue):
        self.bidID = newBidID
        self.userID = newUserID
        self.productID = newProductID
        self.status = newStatus
        self.value = newValue

    def asDict(self):
        bidict = dict()

        bidict = { 'bidID' : self.bidID,
                'userID' : self.userID,
                'productID' : self.productID,
                'status' : self.status,
                'value' : self.value }

        return bidict

class bidController():
    def getUserBidInstancesById(self, userID):
        bids = databaseController.executeSQLCommand('select * from userbid where user_id = {0} order by value desc'.format(userID), True)

        bidFinalList = []
        for bidIter in bids:
            bufBid = bid(bidIter[0], bidIter[1], bidIter[2], bidIter[3], bidIter[4])

            bidFinalList.append(bufBid)

        return bidFinalList

bidController = bidController()


