import npyscreen
from npyscreen.wgwidget import curses

from ..player import Player
from ..yandex_music_client import YandexMusicClient
from . import widgets


class BaseForm(npyscreen.FormBaseNew):
    def create(self):
        self.max_y, self.max_x = self.useable_space()

        self.player = Player()
        self.ym_client = YandexMusicClient()
        self.exit_in_progress = False
        self.max_widgets_height = self.max_y - int(self.max_y / 6)

    def add_bar(self) -> widgets.ProgressBar:
        bar = widgets.ProgressBar()
        bar.add_widgets(self, self.max_x)
        return bar

    def beforeEditing(self):
        self.exit_in_progress = False

    def add_hotkeys(self, widget):
        widget.add_handlers(
            {
                ord("p"): self.h_previous_track,
                curses.ascii.SP: self.h_pause_track,
                curses.ascii.TAB: lambda _: _,
                curses.ascii.ESC: self.h_exit_to_main,
                curses.KEY_RIGHT: self.h_move_track_position_to_right,
                curses.KEY_LEFT: self.h_move_track_position_to_left,
                ord("r"): self.h_repeat_track,
                curses.KEY_UP: self.h_volume_up,
                curses.KEY_DOWN: self.h_volume_down,
                ord("n"): self.h_next_track,
                ord("d"): self.h_dislike_track,
                ord("l"): self.h_like_track,
            }
        )

    def h_volume_up(self, _):
        new_volume = self.player.get_volume() + 5
        self.player.set_volume(new_volume)

    def h_volume_down(self, _):
        new_volume = self.player.get_volume() - 5
        self.player.set_volume(new_volume)

    def h_repeat_track(self, _):
        self.repeat_track = not self.repeat_track

    def h_exit_to_main(self, _):
        if self.exit_in_progress:
            return
        exit_status = self.on_exit()
        self.exit_in_progress = True
        if exit_status is not None:
            return
        self.parentApp.switchForm("MAIN")

    def h_move_track_position_to_right(self, _):
        self.player.move_track_position(right=True)

    def h_move_track_position_to_left(self, _):
        self.player.move_track_position(right=False)

    def h_pause_track(self, _):
        self.player.play_pause()

    def h_next_track(self, _):
        self.player.next_track()

    def h_previous_track(self, _):
        self.player.previous_track()

    def h_like_track(self, _):
        if self.player.now_playing:
            self.ym_client.like_track(self.player.now_playing)

    def h_dislike_track(self, _):
        if self.player.now_playing:
            self.ym_client.dislike_track(self.player.now_playing)

    def on_exit(self):
        pass
