import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger():
    """Базовая настройка логирования"""
    LOGS_DIR = os.path.expanduser("~/.local/share/ymcli/")
    LOGS_FILE = os.path.join(LOGS_DIR, "yamcli.logs")
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

        # Check if the file exists, create it if not
    if not os.path.isfile(LOGS_FILE):
        open(LOGS_FILE, 'a').close()
    # Настраиваем логирование в файл
    log_file_handler = RotatingFileHandler(
        LOGS_FILE, maxBytes=10 * 1024 * 1024, backupCount=6
    )
    log_file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    log_file_handler.setFormatter(log_file_format)
    log_file_handler.setLevel(logging.INFO)

    # Добавляем обработчик файлового лога к корневому логгеру
    logger = logging.getLogger()
    logger.propagate = False
    logger.addHandler(log_file_handler)