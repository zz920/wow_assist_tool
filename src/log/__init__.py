import time
import logging
import logging.handlers

from src.config import *

LOG_LEVEL = logging.DEBUG
logger = logging.getLogger()


def setup_log():
    log_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, backupCount=3, encoding='utf')
    formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    # formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(LOG_LEVEL)


setup_log()
