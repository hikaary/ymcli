from textual.screen import Screen

from ymcli.player import Player
from ymcli.yandex_music_client import YandexMusicClient

from ..config import CONTROL_PLAYER_BINDINGS


class BaseScreen(Screen):
    BINDINGS = CONTROL_PLAYER_BINDINGS

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.ym_client = YandexMusicClient()

    async def action_pause(self) -> None:
        await self.player.play_pause()

    async def action_next(self) -> None:
        await self.player.next_track()

    async def action_previous(self) -> None:
        await self.player.previous_track()

    def action_volume_up(self) -> None:
        new_volume = self.player.get_volume() + 5
        self.player.set_volume(new_volume)

    def action_volume_down(self) -> None:
        new_volume = self.player.get_volume() - 5
        self.player.set_volume(new_volume)

    def action_move_track_pos_left(self) -> None:
        self.player.move_track_position(right=False)

    def action_move_track_pos_right(self) -> None:
        self.player.move_track_position(right=True)
