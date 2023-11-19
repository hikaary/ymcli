import asyncio
import os

import vlc
from textual.app import App
from textual.message import Message
from yandex_music import Playlist, StationResult, Track, TracksList

from .config import MUSIC_DIR, get_config
from .yandex_music_client import YandexMusicClient

CONFIG = get_config()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TrackInfoUpdate(Message):
    def __init__(self, track: Track, widget_selector: str) -> None:
        self.track = track
        self.widget_selector = widget_selector
        super().__init__()


class BarInfoUpdate(Message):
    def __init__(self, track: Track) -> None:
        self.track = track
        super().__init__()


class Player(metaclass=Singleton):
    def __init__(self, app: App | None = None) -> None:
        self.instance = vlc.Instance()
        self.player: vlc.MediaPlayer = self.instance.media_player_new()
        self.player.audio_set_volume(int(CONFIG.basic_sound_volume))
        self.ym_client = YandexMusicClient()
        self.radio = self.ym_client.radio

        self.now_playing: Track | None = None
        self.is_paused = False
        self.palying = False
        self.repeat = False
        self.app = app

        self.track_list: list[Track] = []
        self.playlists: list[Playlist | TracksList] = []
        self.stations: list[StationResult] = []

    def stop(self) -> None:
        self.repeat = False
        self.playing = False
        self.now_playing = None
        self.player.stop()

    async def play_pause(self) -> None:
        if self.player.is_playing():
            self.player.pause()
            self.isPaused = True
        else:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self.player.play)
            self.isPaused = False

    async def play(self, track: Track) -> None:
        saved_tracks = os.listdir(MUSIC_DIR)
        if f"{track.id}.mp3" not in saved_tracks:
            load_indicatopr = self.app.query_one("LoadingIndicator")
            load_indicatopr.styles.visibility = "visible"
            await self.ym_client.download(track)
            load_indicatopr.styles.visibility = "hidden"

        self.media = self.instance.media_new(f"{MUSIC_DIR}{track.id}.mp3")
        self.player.set_media(self.media)

        self.app.post_message(BarInfoUpdate(track))
        await self.play_pause()
        if self.now_playing is None:
            loop = asyncio.get_event_loop()
            loop.create_task(self.update_bar())
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

    async def next_track(self) -> None:
        if self.now_playing is None:
            return

        if self.radio.current_track:
            track = await self.radio.get_next_track()
            self.app.post_message(TrackInfoUpdate(track, "station_track_info"))
            await self.play(track=track)
            return

        last_track_index = self.track_list.index(self.now_playing)
        if last_track_index == len(self.track_list) + 1:  # type: ignore
            self.stop()
            return

        track = self.track_list[last_track_index + 1]
        self.app.post_message(TrackInfoUpdate(track, "playlist_track_info"))
        await self.play(track=track)

    async def previous_track(self) -> None:
        if self.now_playing is None or self.radio.current_track:
            return

        last_track_index = self.track_list.index(self.now_playing)
        if last_track_index == len(self.track_list) - 1:  # type: ignore
            self.stop()
            return

        await self.play(track=self.track_list[last_track_index - 1])

    def move_track_position(self, right: bool):
        if not self.player.is_playing:
            return

        current_position = self.player.get_position()
        next_position = current_position + 0.05 if right else current_position - 0.05

        next_position = max(0, min(1, next_position))

        self.player.set_position(next_position)

    async def update_bar(self):
        self.playing = True
        try:
            while self.playing:
                position = self.player.get_position()
                if position is None or self.now_playing is None:
                    await asyncio.sleep(1)
                    continue

                if position > 1.0 - 0.008:
                    if self.repeat:
                        self.player.set_position(0.01)
                        await asyncio.sleep(0.01)
                        continue

                    if self.radio.current_track is not None:
                        track = await self.radio.get_next_track()
                        self.app.post_message(
                            TrackInfoUpdate(track, "station_track_info")
                        )
                        await self.play(track=track)
                        continue

                    last_track_index = self.track_list.index(self.now_playing)
                    if last_track_index == len(self.track_list) + 1:  # type: ignore
                        self.stop()
                    else:
                        track = self.track_list[last_track_index + 1]
                        self.app.post_message(
                            TrackInfoUpdate(track, "playlist_track_info")
                        )
                        await self.play(track=track)
                await asyncio.sleep(0.1)
        finally:
            self.playing = False
