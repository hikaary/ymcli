import logging


def log_play(func):
    def wrapper(*args, **kwargs):
        track_id = kwargs.get("track").id
        logging.warning("Пользователь начал слушать песню %s", track_id)
        return func(*args, **kwargs)

    return wrapper
