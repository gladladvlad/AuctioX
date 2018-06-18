import time
import logging
from threading import Thread
from productController import *
from databaseController import *

daemonLog = logging.getLogger("Daemon Logger")
daemonLog.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("daemon.log", "w")
fileHandler.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] %(funcName)s: %(message)s')
fileHandler.setFormatter(formatter)
daemonLog.addHandler(fileHandler)
consoleHandler.setFormatter(formatter)
daemonLog.addHandler(consoleHandler)


class daemon(Thread):

    running = True

    def run(self):

        print "Daemon Started"

        while self.running:
            self.update()
            time.sleep(30)

    def update(self):
        daemonLog.debug("Starting Update")

        productList = databaseController.executeSQLCommand("select * from productdata where status='ongoing'")

        daemonLog.debug("There are currently {0} ongoing listings in the database".format(len(productList)))

        for product in productList:

            if product[PROD_DATE_EXPIRES] < datetime.datetime.now():

                daemonLog.debug("Product {0} ({1}) has expired".format(product[PROD_ID], product[PROD_TITLE]))

                isAuction = product[PROD_IS_AUCTION]

                if isAuction == 1:

                    daemonLog.debug("Listing {0} is AUCTION".format(product[PROD_ID]))

                    highestBid = databaseController.getBiggestBidForProduct(product[PROD_ID])

                    if highestBid == 0:
                        daemonLog.debug("There are no bids for the product {0}".format(product[PROD_ID]))
                    else:

                        daemonLog.debug(
                            "Highest bid is {value} {currency} by user {id}".format(value=highestBid[BID_VALUE],
                                                                                    currency=product[PROD_CURRENCY],
                                                                                    id=highestBid[BID_USER_ID]))

                        transactionData = {
                            "seller_user_id": product[PROD_USER_ID],
                            "buyer_user_id": highestBid[BID_USER_ID],
                            "product_data_id": product[PROD_ID],
                            "has_ended": "ongoing"
                        }

                        daemonLog.debug("Creating transaction")

                        databaseController.insertIntoTransaction(transactionData)

                        daemonLog.debug("Transaction has been created")

                else:

                    daemonLog.debug("Listing {0} is BUY IT NOW".format(product[PROD_ID]))

                databaseController.setInactiveInProduct(product[PROD_ID])

                daemonLog.debug("Product {0} ({1}) is now inactive".format(product[PROD_ID], product[PROD_TITLE]))

        transactionList = databaseController.executeSQLCommand("select * from transaction where has_ended='ongoing'")

        daemonLog.debug("There are {0} ongoing transactions".format(len(transactionList)))

        for transaction in transactionList:

            daemonLog.debug("Analyzing transaction {0}".format(transaction[TRANSACTION_ID]))

            if transaction[TRANSACTION_BUYER_CONFIRM] and transaction[TRANSACTION_SELLER_CONFIRM]:

                daemonLog.debug("Both parties have confirmed the transaction. Setting status to 'ended'")

                databaseController.setInactiveInTransaction(transaction[TRANSACTION_ID])

            elif transaction[TRANSACTION_DATE_EXPIRES] < datetime.datetime.now():

                daemonLog.debug("Transaction took too long to confirm. Generating admin report.")

                reportData = {
                    "type": "Transaction unconfirmed",
                    "product_id": transaction[TRANSACTION_PRODUCT_ID],
                    "details": "One of the parties did not confirm the transaction",
                    "reason": 1,
                    "resolved": False,
                    "date_resolved": datetime.datetime.now(),
                    "is_valid": True
                }

                if not transaction[TRANSACTION_SELLER_CONFIRM]:
                    daemonLog.debug(
                        "The seller {0} did not confirm transaction {1}".format(transaction[TRANSACTION_SELLER_ID],
                                                                                transaction[TRANSACTION_ID]))

                    reportData["from_uid"] = transaction[TRANSACTION_BUYER_ID]
                    reportData["to_uid"] = transaction[TRANSACTION_SELLER_ID]

                    databaseController.insertIntoReport(reportData)

                if not transaction[TRANSACTION_BUYER_ID]:
                    daemonLog.debug(
                        "The buyer {0} did not confirm transaction {1}".format(transaction[TRANSACTION_BUYER_ID],
                                                                               transaction[TRANSACTION_ID]))

                    reportData["from_uid"] = transaction[TRANSACTION_SELLER_ID]
                    reportData["to_uid"] = transaction[TRANSACTION_BUYER_ID]

                    databaseController.insertIntoReport(reportData)

                daemonLog.debug("Setting transaction {0} status to 'failed'.".format(transaction[TRANSACTION_ID]))


daemon = daemon()
