#!/usr/bin/env python3

import argparse
import logging

from config import MUSIC_DIR, create_config, get_config
from logs.set_up import setup_logger
from ui import MyApp
from vlc import os
from yandex_music_client import YandexMusicClient

logger = logging.getLogger(__name__)


def run_app():
    if not os.path.exists(MUSIC_DIR):
        os.makedirs(MUSIC_DIR)

    config = get_config()
    if config is None:
        raise AttributeError("Configuration file not found.")
    YandexMusicClient(config.token)
    my_app = MyApp()
    my_app.run()


def main():
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
        setup_logger()
        try:
            run_app()
        except Exception:
            import traceback

            logger.warning(traceback.format_exc())


if __name__ == "__main__":
    main()
