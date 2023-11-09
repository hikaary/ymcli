import argparse

from config import MUSIC_DIR, create_config, get_config
from ui import MyApp
from vlc import os
from yandex_music_client import YandexMusicClient


def run_app():
    if not os.path.exists(MUSIC_DIR):
        os.makedirs(MUSIC_DIR)

    config = get_config()
    if config is None:
        raise AttributeError("Configuration file not found.")
    YandexMusicClient(config.token)
    my_app = MyApp()
    my_app.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Yandex Music CLI Player.")
    subparsers = parser.add_subparsers()

    parser_create_config = subparsers.add_parser(
        "create-config", help="Create configuration file."
    )
    parser_create_config.set_defaults(func=create_config)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func()
    else:
        run_app()
