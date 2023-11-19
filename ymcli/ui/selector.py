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

    async def on_mount(self) -> None:
        playlists = await self.get_playlists()
        playlists_widget = self.query_one("#playlists")
        playlists_widget.add_options(playlists)  # type: ignore

    def compose(self) -> ComposeResult:
        yield Header()
        yield LoadingIndicator()
        yield widgets.Notification()

        yield widgets.Playlists(id="playlists")
        with Container(id="bar_container"):
            yield widgets.BarTitle()
            yield widgets.Bar()

    async def get_playlists(self):
        likes_tracks: TracksList = await self.ym_client.get_likes()
        self.player.playlists = [likes_tracks, likes_tracks]
        playlists: list[Playlist] = await self.ym_client.get_playlists()
        options = [
            Option("Моя волна"),
            Separator(),
            Option(f"Любимые - {len(likes_tracks)} песен"),
            Separator(),
        ]
        for playlist in playlists:
            options.extend(
                [
                    Option(
                        f"{playlist.title} - {playlist.track_count} песен",
                    ),
                    Separator(),
                ]
            )
            self.player.playlists.append(playlist)
        return options
