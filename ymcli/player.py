import threading
import time

import vlc
from npyscreen import notify_confirm
from yandex_music import Track

from .config import MUSIC_DIR, get_config
from .logs.actions import log_play

CONFIG = get_config()


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
        self.now_playing: Track | None = None
        self.is_paused = False
        self.palying = False
        self.track_list: list | None = []

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

    @log_play
    def play(self, track: Track) -> None:
        self.media = self.instance.media_new(MUSIC_DIR + str(track.id) + ".mp3")
        self.player.set_media(self.media)
        self.play_pause()
        self._start_progress_thread()
        self.now_playing = track

    def set_volume(self, volume: int) -> None:
        self.player.audio_set_volume(volume)

    def get_volume(self) -> int:
        return self.player.audio_get_volume()

    def get_position(self) -> float | bool:
        """Возвращает позицию относительно максимальной длинны. return 0.0-1.0"""
        if self.now_playing is not None:
            return self.player.get_position()
        return False

    def get_current_track(self) -> Track | None:
        if self.now_playing is not None:
            return self.now_playing

    def move_track_position(self, right: bool):
        if not self.player.is_playing:
            return
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
        if self.progress_thread.is_alive():
            self.progress_thread.join()

    def _progress_update_loop(self):
        while self.playing:
            position = self.player.get_position()
            if position is None:
                time.sleep(1)
                continue
            if position == 1.0:
                last_track_index = self.track_list.index(self.now_playing)
                self.play(track=self.track_list[last_track_index + 1])
            time.sleep(0.01)
