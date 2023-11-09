import vlc
from config import MUSIC_DIR, get_config

CONFIG = get_config()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Player:
    def __init__(self) -> None:
        self.instance = vlc.Instance()
        self.player: vlc.MediaPlayer = self.instance.media_player_new()
        self.player.audio_set_volume(int(CONFIG.basic_sound_volume))
        self.is_paused = False

    def play_pause(self) -> None:
        if self.player.is_playing():
            self.player.pause()
            self.isPaused = True
        else:
            if self.player.play() == -1:
                return
            self.player.play()
            self.isPaused = False

    def play(self, track_id: int) -> None:
        self.media = self.instance.media_new(MUSIC_DIR + str(track_id) + ".mp3")
        self.player.set_media(self.media)
        self.play_pause()

    def set_volume(self, volume: int) -> None:
        self.player.audio_set_volume(volume)

    def get_position(self) -> float:
        return self.player.get_position() * 1000
