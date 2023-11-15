import logging
import os
import threading
import time

import npyscreen
import vlc
from yandex_music import Track

from ymcli.yandex_music_client import YandexMusicClient

from .config import MUSIC_DIR, get_config

CONFIG = get_config()
logger = logging.getLogger(__file__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Player(metaclass=Singleton):
    def __init__(self) -> None:
        self.instance = vlc.Instance()
        self.player: vlc.MediaPlayer = self.instance.media_player_new()
        self.player.audio_set_volume(int(CONFIG.basic_sound_volume))
        self.ym_client = YandexMusicClient()
        self.radio = self.ym_client.radio

        self.now_playing: Track | None = None
        self.is_paused = False
        self.palying = False
        self.track_list: list[Track] = []

    def stop(self) -> None:
        self.player.stop()
        self._stop_progress_thread()

    def play_pause(self) -> None:
        if self.player.is_playing():
            self.player.pause()
            self.isPaused = True
        else:
            if self.player.play() == -1:
                return
            self.player.play()
            self.isPaused = False

    def play(self, track: Track) -> None:
        logger.debug(f"Start play {track.id}")

        saved_tracks = os.listdir(MUSIC_DIR)
        if f"{track.id}.mp3" not in saved_tracks:
            npyscreen.notify("Трек не загружен. Начинаю загрузку...")

            logger.debug(f"Start download {track.id}")
            self.ym_client.download(track)

        self.media = self.instance.media_new(MUSIC_DIR + str(track.id) + ".mp3")
        self.player.set_media(self.media)
        self.play_pause()
        if self.now_playing is None:
            self._start_progress_thread()
        self.now_playing = track

    def set_volume(self, volume: int) -> None:
        self.player.audio_set_volume(volume)

    def get_volume(self) -> int:
        return self.player.audio_get_volume()

    def get_position(self) -> float | bool:
        if self.now_playing is not None:
            return self.player.get_position()
        return False

    def get_current_track(self) -> Track | None:
        if self.now_playing is not None:
            return self.now_playing

    def next_track(self):
        logger.debug("Get next track called")
        if self.now_playing is None:
            return

        if self.radio.current_track:
            logger.debug("Radio enabled, call get next track")
            track = self.radio.get_next_track()
            self.play(track=track)
            return

        last_track_index = self.track_list.index(self.now_playing)
        if last_track_index == len(self.track_list) + 1:  # type: ignore
            logger.debug("Track list ended. Stopping player")
            self.stop()
            return

        logger.debug("Next track finded")
        self.play(track=self.track_list[last_track_index + 1])

    def previous_track(self):
        logger.debug("Get previous track called")
        if self.now_playing is None or self.radio.current_track:
            return

        last_track_index = self.track_list.index(self.now_playing)
        if last_track_index == len(self.track_list) - 1:  # type: ignore
            logger.debug("The previous track could not be found")
            self.stop()
            return

        logger.debug("Previous track finded")
        self.play(track=self.track_list[last_track_index - 1])

    def move_track_position(self, right: bool):
        if not self.player.is_playing:
            return
        logger.debug("Move track position")

        current_position = self.player.get_position()
        next_position = current_position + 0.05 if right else current_position - 0.05

        next_position = max(0, min(1, next_position))

        self.player.set_position(next_position)

    def _start_progress_thread(self):
        self.playing = True
        self.progress_thread = threading.Thread(
            target=self._progress_update_loop,
            daemon=True,
        )
        self.progress_thread.start()

    def _stop_progress_thread(self):
        self.playing = False
        self.now_playing = None
        if self.progress_thread.is_alive():
            self.progress_thread.join()

    def _progress_update_loop(self):
        while self.playing:
            position = self.player.get_position()
            if position is None:
                time.sleep(1)
                continue

            if self.now_playing is None:
                time.sleep(0.01)
                continue

            if position > 1.0 - 0.005:
                if self.radio.current_track is not None:
                    track = self.radio.get_next_track()
                    self.play(track=track)
                    time.sleep(0.01)
                    continue

                last_track_index = self.track_list.index(self.now_playing)
                if last_track_index == len(self.track_list) + 1:  # type: ignore
                    self.stop()
                else:
                    self.play(track=self.track_list[last_track_index + 1])
            time.sleep(0.01)
