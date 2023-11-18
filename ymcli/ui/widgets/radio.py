from textual.binding import Binding, BindingType
from textual.widgets import RadioSet
from yandex_music import Track

from ...config import CONTROL_PLAYER_BINDINGS
from ...player import Player, TrackInfoUpdate
from ...yandex_music_client import YandexMusicClient


class StationsRadioWidget(RadioSet):
    BINDINGS: list[BindingType] = [
        Binding("j", "next_button", "Down", show=False),  # EU
        Binding("k", "previous_button", "Up", show=False),  # EU
        Binding("b", "exit", "Exit", show=False),  # EN
        Binding("о", "next_button", "Down", show=False),  # RU
        Binding("л", "previous_button", "Up", show=False),  # RU
        Binding("и", "exit", "Exit", show=False),  # RU
        # Other
        Binding("enter", "toggle", "Select", show=False),
    ] + CONTROL_PLAYER_BINDINGS

    def __init__(
        self,
        *content,
        **kwargs,
    ):
        super().__init__(
            *content,
            **kwargs,
        )
        self.ym_client = YandexMusicClient()
        self.player = Player()
        self.radio = self.ym_client.radio

    async def action_toggle(self) -> None:
        super().action_toggle()
        station = self.player.stations[self.pressed_index].station

        load_indicatopr = self.app.query_one("LoadingIndicator")
        load_indicatopr.styles.visibility = "visible"
        track: Track = await self.radio.get_first_track(
            station_id=f"{station.id.type}:{station.id.tag}",
            station_from=station.id_for_from,
        )
        await self.player.play(track=track)
        self.post_message(TrackInfoUpdate(track, "station_track_info"))
