import logging
import os

from .config import MUSIC_DIR, create_config, get_config
from .logs.set_up import setup_logger
from .ui import Ymcli
from .yandex_music_client import YandexMusicClient

logger = logging.getLogger()


def run_app():
    if not os.path.exists(MUSIC_DIR):
        os.makedirs(MUSIC_DIR)

    config = get_config()
    if config is None:
        config = create_config()

    YandexMusicClient(config.token)
    app = Ymcli()
    app.run()


def main():
    setup_logger()
    try:
        run_app()
    except Exception as e:
        import traceback

        logger.warning(traceback.format_exc())
        raise e


if __name__ == "__main__":
    main()
