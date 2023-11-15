import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger():
    LOGS_DIR = os.path.expanduser("~/.local/share/ymcli/")
    LOGS_FILE = os.path.join(LOGS_DIR, "ymcli.logs")

    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    if not os.path.isfile(LOGS_FILE):
        open(LOGS_FILE, "a").close()

    log_file_handlers = [
        create_file_handler(logging.INFO, LOGS_FILE),
        create_file_handler(logging.DEBUG, LOGS_FILE),
    ]
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=log_file_handlers,
    )


def create_file_handler(level, LOGS_FILE):
    handler = RotatingFileHandler(
        LOGS_FILE,
        maxBytes=10 * 1024 * 1024,
        backupCount=6,
    )
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(file_format)
    handler.setLevel(level)
    return handler
