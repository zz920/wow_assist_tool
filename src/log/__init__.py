import time
import logging
import logging.handlers

LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
LOG_DATE_FORMAT = '%b %d %H:%M:%S'
LOG_LEVEL = logging.DEBUG
LOG_FILENAME = '../log/info.log'

logger = logging.getLogger()

def setup_log():
    log_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, backupCount=3, encoding='utf')
    formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    # formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(LOG_LEVEL)

setup_log()
