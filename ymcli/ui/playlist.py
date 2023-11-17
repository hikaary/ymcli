from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Header, LoadingIndicator
from textual.widgets.option_list import Option, Separator

from ..player import Player
from ..yandex_music_client import YandexMusicClient
from . import widgets
from .base_screen import BaseScreen


class Playlist(BaseScreen):
    CSS_PATH = "css/playlist.tcss"

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.ym_client = YandexMusicClient()

    def compose(self) -> ComposeResult:
        yield Header()
        yield LoadingIndicator(disabled=True)
        yield widgets.TrackList(
            id="playlist_tracks",
        )
        yield widgets.TrackInfo(
            id="playlist_track_info",
        )
        with Container(id="bar_container"):
            yield widgets.BarTitle()
            yield widgets.Bar()

    def get_name_tracks(self) -> list[Option | Separator]:
        name_tracks = []
        for track in self.player.track_list:
            artists = ",".join(track.artists_name())
            track_name = f"{track.title} - {artists}"
            name_tracks.append(Option(track_name))
            name_tracks.append(Separator())

        return name_tracks
