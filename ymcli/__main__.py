#!/usr/bin/env python3

import logging
import os

from .config import MUSIC_DIR, create_config, get_config
from .logs.set_up import setup_logger
from .ui import App
from .yandex_music_client import YandexMusicClient

logger = logging.getLogger(__name__)


def run_app():
    if not os.path.exists(MUSIC_DIR):
        os.makedirs(MUSIC_DIR)

    config = get_config()
    if config is None:
        create_config()
        print("Run app again")
        return

    YandexMusicClient(config.token)
    app = App()
    app.run()


def main():
    setup_logger()
    try:
        run_app()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())


if __name__ == "__main__":
    main()
