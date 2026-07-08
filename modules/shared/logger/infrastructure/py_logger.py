import logging
from modules.shared.logger.domain import Logger


class PyLogger(Logger):
    """
    PyLogger:
        Levels:
            DEBUG: -> DEBUG, INFO, WARNING, ERROR, CRITICAL
            INFO: -> INFO, WARNING, ERROR, CRITICAL
            WARNING: -> WARNING, ERROR, CRITICAL
            ERROR: -> ERROR, CRITICAL
            CRITICAL: -> CRITICAL
    """

    def __init__(self, level, format):
        logging.basicConfig(
            level=level,
            format=format
        )

    def debug(self, message):
        logging.debug(message)

    def info(self, message):
        logging.info(message)

    def warning(self, message):
        logging.warning(message)

    def error(self, message):
        logging.error(message)
