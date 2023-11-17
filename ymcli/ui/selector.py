from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Header, LoadingIndicator
from textual.widgets.option_list import Option, Separator
from yandex_music import Playlist, TracksList

from ..player import Player
from ..yandex_music_client import YandexMusicClient
from . import widgets
from .base_screen import BaseScreen


class SelectorInputs(BaseScreen):
    CSS_PATH = "css/selector.tcss"

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.ym_client = YandexMusicClient()

    def compose(self) -> ComposeResult:
        yield Header()
        yield LoadingIndicator()
        yield widgets.Playlists(
            *self.get_playlists(),
            id="playlists",
        )
        with Container(id="bar_container"):
            yield widgets.BarTitle()
            yield widgets.Bar()

    def get_playlists(self) -> list[Option | Separator]:
        likes_tracks: TracksList = self.ym_client.get_likes()
        self.player.playlists = [likes_tracks, likes_tracks]
        playlists: list[Playlist] = self.ym_client.get_playlists()
        values = [
            Option("Моя волна"),
            Separator(),
            Option(f"Любимые - {len(likes_tracks)} песен"),
            Separator(),
        ]
        for playlist in playlists:
            values.append(
                Option(
                    f"{playlist.title} - {playlist.track_count} песен",
                ),
            )
            values.append(Separator())
            self.player.playlists.append(playlist)
        return values
