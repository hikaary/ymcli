from textual.screen import Screen

from ..config import CONTROL_PLAYER_BINDINGS
from ..player import Player
from ..yandex_music_client import YandexMusicClient
from .widgets.label import Notification


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
        self.post_message(Notification.Update(f"Volume: {new_volume}"))

        self.player.set_volume(new_volume)

    def action_volume_down(self) -> None:
        new_volume = self.player.get_volume() - 5
        self.post_message(Notification.Update(f"Volume: {new_volume}"))

        self.player.set_volume(new_volume)

    def action_move_track_pos_left(self) -> None:
        self.player.move_track_position(right=False)

    def action_move_track_pos_right(self) -> None:
        self.player.move_track_position(right=True)

    def action_repeat(self) -> None:
        return
        self.player.repeat = not self.player.repeat

    def action_like_track(self) -> None:
        if self.player.now_playing is None:
            return

        self.post_message(Notification.Update("Like track"))
        self.ym_client.like_track(self.player.now_playing)

    def action_dislike_track(self) -> None:
        if self.player.now_playing is None:
            return

        self.post_message(Notification.Update("Dislike track"))
        self.ym_client.dislike_track(self.player.now_playing)
