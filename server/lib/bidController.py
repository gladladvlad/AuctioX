from databaseController import *
from util import *

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
        logger.info("[START] getUserBidInstancesById()")
        bids = databaseController.getUserBidsById(userID)

        bidFinalList = []
        for bidIter in bids:
            bufBid = bid(bidIter[0], bidIter[1], bidIter[2], bidIter[3], bidIter[4])

            bidFinalList.append(bufBid)

        return bidFinalList

    def getBidById(self, bidId):
        bidBD = databaseController.getBidById(bidId)

        resBid = bid(bidBD[0], bidBD[1], bidBD[2], bidBD[3], bidBD[4])

        return resBid

    def cancelBid(self, bidId):
        logger.info('done')
        bid = self.getBidById(bidId)
        logger.info('done')
        highestBid = databaseController.getBiggestBidForProduct(bid.productID)[0]
        logger.info('done')
        logger.info(type(bid.productID))
        logger.info(type(highestBid))
        databaseController.setNewPrice(bid.productID, highestBid)
        logger.info('done')

        databaseController.stergeBid(bidId)
        logger.info('done')

        return "Success!"

bidController = bidController()


