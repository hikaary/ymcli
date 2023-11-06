import argparse

from config import get_config, save_token
from ui import MyApp
from yandex_music_client import YandexMusicClient


def create_config():
    token = input("Enter your Yandex Music token: ")
    save_token(token)
    print("Configuration file created successfully.")


def run_app():
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
