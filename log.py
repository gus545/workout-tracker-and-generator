import logging
from logging.handlers import RotatingFileHandler
import structlog

def initialize_logger():
    """
    Initializes and configures the logger for the Notion client.
    Returns:
        structlog.BoundLogger: A bound logger instance.
    """
    # Configure the logger

    logger = structlog.wrap_logger(
        logging.getLogger("notion-client"),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
    )
    logger.setLevel(logging.DEBUG)

    # Set up the file handler
    logger.addHandler(initialize_file_handler())

    return logger

def initialize_file_handler():
    """
    Initializes and configures a file handler for logging.
    Returns:
        logging.FileHandler: A file handler instance.
    """
    # Set up the file handler
    file_handler = RotatingFileHandler("notion_client.log", maxBytes=5*1024*1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    return file_handler