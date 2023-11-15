from textual.app import App, ComposeResult
from textual.widgets import Header
from textual.widgets.option_list import Option, Separator
from yandex_music import Playlist, TracksList

from ..player import Player
from ..yandex_music_client import YandexMusicClient
from . import widgets
from .playlist_tracks import PlaylistTracks


class Ymcli(App):
    CSS_PATH = "css/selectplaylist.tcss"

    MODES = {
        "playlisttracks": PlaylistTracks,
    }

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.ym_client = YandexMusicClient()
        self.playlists = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield widgets.SelectPlayListTrack(*self.get_playlists())

    def get_playlists(self) -> list[Option | Separator]:
        likes_tracks: TracksList = self.ym_client.get_likes()
        self.playlists = [1, likes_tracks]
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
            self.playlists.append(playlist)
        return values
