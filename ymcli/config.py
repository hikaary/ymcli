import configparser
import logging
import os
from dataclasses import dataclass, fields

from textual.binding import Binding, BindingType

logger = logging.getLogger(__name__)


@dataclass
class Config:
    token: str
    basic_sound_volume: str


CONFIG_DIR = os.path.expanduser("~/.config/ymcli/")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")
MUSIC_DIR = os.path.expanduser("~/.ymcli/")

SELECT_BINDINGS: list[BindingType] = [
    Binding("j", "cursor_down", "Down", show=False),  # EU
    Binding("k", "cursor_up", "Up", show=False),  # EU
    Binding("b", "exit", "Exit", show=False),  # EN
    Binding("о", "cursor_down", "Down", show=False),  # RU
    Binding("л", "cursor_up", "Up", show=False),  # RU
    Binding("и", "exit", "Exit", show=False),  # RU
    # Other
    Binding("enter", "select", "Select", show=False),
]
CONTROL_PLAYER_BINDINGS: list[BindingType] = [
    Binding("space", "pause", "Pause track", show=False),
    Binding("up", "volume_up", "Up", show=False),
    Binding("down", "volume_down", "Down", show=False),
    Binding("left", "move_track_pos_left", "Move track position left", show=False),
    Binding("right", "move_track_pos_right", "Move track position right", show=False),
    # Other
    Binding("n", "next", "Next track", show=False),  # EN
    Binding("p", "previous", "Previous track", show=False),  # EN
    Binding("т", "next", "Next track", show=False),  # RU
    Binding("з", "previous", "Previous track", show=False),  # RU
]


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
