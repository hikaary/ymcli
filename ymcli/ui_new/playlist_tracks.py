from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Static
from textual.widgets.option_list import Option, Separator

from ymcli.player import Player
from ymcli.yandex_music_client import YandexMusicClient

from . import widgets


class PlaylistTracks(Screen):
    CSS_PATH = "css/playlisttracks.tcss"

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.ym_client = YandexMusicClient()

    def compose(self) -> ComposeResult:
        # yield Static(str(self.app.playlists))
        yield Header()
        yield widgets.SelectPlayTrack(*self.get_name_tracks())

    def get_name_tracks(self) -> list[Option | Separator]:
        name_tracks = []
        for counter, track in enumerate(self.player.track_list):
            artists = ",".join(track.artists_name())
            track_name = f"{track.title} - {artists}"
            name_tracks.append(Option(track_name, id=str(counter)))
            name_tracks.append(Separator())

        return name_tracks
