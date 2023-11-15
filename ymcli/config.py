import configparser
import logging
import os
from dataclasses import dataclass, fields

logger = logging.getLogger(__name__)


@dataclass
class Config:
    token: str
    basic_sound_volume: str


CONFIG_DIR = os.path.expanduser("~/.config/ymcli/")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")
MUSIC_DIR = os.path.expanduser("~/.ymcli/")


def get_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if "DEFAULT" in config:
            try:
                config_data = {
                    field.name: config["DEFAULT"][field.name]
                    for field in fields(Config)
                }
                return Config(**config_data)
            except KeyError as e:
                logger.warning(f"Missing configuration field: {e}")
    return None


def create_config():
    token = input("Enter your Yandex Music token: ")
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    config = configparser.ConfigParser()
    config["DEFAULT"] = {
        "Token": token,
        "basic_sound_volume": "50",
    }
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
    logging.info("Configuration file created successfully.")
    return Config(**config["DEFAULT"])
