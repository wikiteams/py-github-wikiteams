import logging

logger = logging.getLogger("wikiteams")
logFileHandler = logging.FileHandler('wikiteams.log')
logFormatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logFileHandler.setFormatter(logFormatter)
logger.addHandler(logFileHandler)
logger.setLevel(logging.INFO)
#logger.addHandler(logging.StreamHandler())