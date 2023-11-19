from threading import Timer

from textual.widgets import Label, ProgressBar
from yandex_music import Track

from ...player import Player


class Bar(ProgressBar):
    progress_timer: Timer

    def __init__(self):
        super().__init__(show_eta=False)
        self.player = Player()
        self.progress_timer = self.set_interval(  # type: ignore
            1 / 10,
            self.update_bar,
        )

    def update_bar(self) -> None:
        position = self.player.get_position()
        current_track = self.player.get_current_track()
        if current_track and position is not None:
            duration_seconds = current_track.duration_ms // 1000  # type: ignore
            position = position * duration_seconds
            self.update(
                total=duration_seconds,
                progress=position,
            )


class BarTitle(Label):
    def __init__(
        self,
    ) -> None:
        super().__init__(
            id="bar_title",
            renderable="Track not load",
        )

    def update_bar_title(self, track: Track):
        self.update(f"{track.title} by {', '.join(track.artists_name())}")
