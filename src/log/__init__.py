import sys
import time
import logging
import logging.handlers

from src.config import *

LOG_LEVEL = logging.DEBUG
logger = logging.getLogger()


def setup_log():
    file_log_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, backupCount=3, encoding='utf')
    file_log_handler.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)

    # formatter.converter = time.gmtime  # if you want UTC time
    file_log_handler.setFormatter(formatter)

    stream_log_handler = logging.StreamHandler(sys.stdout)
    stream_log_handler.setLevel(LOG_LEVEL)
    stream_log_handler.setFormatter(formatter)

    logger.addHandler(file_log_handler)
    logger.addHandler(stream_log_handler)
    # logger.setLevel(LOG_LEVEL)


setup_log()
