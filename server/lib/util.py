import logging

DEBUG = True

consoleDebugLevel = logging.INFO
fileDebugLevel = logging.DEBUG

logger = logging.getLogger("Logger")
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("server.log", "w")
fileHandler.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] %(funcName)s: %(message)s')
fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
logging.root = logger

logger.info("Started Collector Logger!")