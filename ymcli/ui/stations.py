from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Header, LoadingIndicator
from textual.widgets.option_list import Option, Separator
from yandex_music import StationResult

from ..config import CONTROL_PLAYER_BINDINGS, SELECT_BINDINGS
from ..player import Player
from ..yandex_music_client import YandexMusicClient
from . import widgets
from .base_screen import BaseScreen


class Stations(BaseScreen):
    CSS_PATH = "css/stations.tcss"

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.ym_client = YandexMusicClient()

    async def on_mount(self):
        station_options = await self.get_stations()
        widget = self.query_one("#stations")
        widget.add_options(station_options)  # type: ignore

    def compose(self) -> ComposeResult:
        yield Header()
        yield LoadingIndicator()
        yield widgets.Stations(
            id="stations",
        )
        with Container(id="bar_container"):
            yield widgets.BarTitle()
            yield widgets.Bar()

    async def get_stations(self) -> list[Option | Separator]:
        stations: list[StationResult] = await self.ym_client.radio.get_all_stations()
        self.player.stations = stations
        values = []
        for station in stations:
            values.append(
                Option(station.station.name),
            )
            values.append(Separator())
        return values


class StationTracks(BaseScreen):
    CSS_PATH = "css/station_tracks.tcss"
    BINDINGS = SELECT_BINDINGS + CONTROL_PLAYER_BINDINGS

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.ym_client = YandexMusicClient()

    def compose(self) -> ComposeResult:
        yield Header()
        yield LoadingIndicator()
        yield widgets.TrackInfo(
            id="station_track_info",
        )
        with Container(id="bar_container"):
            yield widgets.BarTitle()
            yield widgets.Bar()

    def action_exit(self) -> None:
        self.highlighted = None
        self.player.stop()
        self.app.switch_mode("station_list")
