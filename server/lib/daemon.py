import time
import logging
from threading import Thread
from productController import *

daemonLog = logging.getLogger("Daemon Logger")
daemonLog.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("daemon.log", "w")
fileHandler.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] %(funcName)s: %(message)s')
fileHandler.setFormatter(formatter)
daemonLog.addHandler(fileHandler)


class daemon(Thread):

    running = True

    def run(self):

        print "Daemon Started"

        while self.running:
            self.update()
            time.sleep(30)

    def update(self):
        daemonLog.debug("Update")




daemon = daemon()
