from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Header, LoadingIndicator, RadioButton
from yandex_music import StationResult

from ..config import CONTROL_PLAYER_BINDINGS, SELECT_BINDINGS
from ..player import Player
from ..yandex_music_client import YandexMusicClient
from . import widgets
from .base_screen import BaseScreen


class Stations(BaseScreen):
    CSS_PATH = "css/stations.tcss"
    BINDINGS = SELECT_BINDINGS + CONTROL_PLAYER_BINDINGS

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.ym_client = YandexMusicClient()

    async def on_mount(self) -> None:
        stations = await self.get_stations()
        station_widget = self.query_one("#stations")
        radio_buttons = []
        for station in stations:
            radio_buttons.append(RadioButton(station.station.name))
        station_widget.mount_all(radio_buttons)

    def compose(self) -> ComposeResult:
        yield Header()
        yield LoadingIndicator()
        yield widgets.Notification()

        with Container(id="stations_container"):
            yield widgets.StationsRadioWidget(id="stations")

        yield widgets.TrackInfo(
            id="station_track_info",
        )
        with Container(id="bar_container"):
            yield widgets.BarTitle()
            yield widgets.Bar()

    async def get_stations(self) -> list[StationResult]:
        stations: list[StationResult] = await self.ym_client.radio.get_all_stations()
        self.player.stations = stations
        return stations

    async def action_exit(self) -> None:
        likes_tracks = await self.ym_client.get_likes()
        self.player.playlists = [likes_tracks, likes_tracks]
        playlists = await self.ym_client.get_playlists()
        for playlist in playlists:
            self.player.playlists.append(playlist)
        self.player.stop()
        self.app.switch_mode("main")
