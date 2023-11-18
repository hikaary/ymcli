from textual.app import App

from ..player import Player
from .playlist import Playlist
from .selector import SelectorInputs
from .stations import Stations
from .widgets import Animation


class Ymcli(App):
    CSS_PATH = "css/main.tcss"

    MODES = {
        "main": SelectorInputs,
        "playlist": Playlist,
        "stations_list": Stations,
    }

    def __init__(self):
        super().__init__()

    def on_mount(self):
        Player(self.app)
        self.app.switch_mode("main")

    def on_playlists_update_tracks(self, message):
        widget = self.query_one("#playlist_tracks")
        widget.update_track_list(message.track_list)  # type: ignore

    def on_track_info_update(self, message):
        widget = self.query_one("#" + message.widget_selector)
        widget.update_track_info(message.track)  # type: ignore

    def on_bar_info_update(self, message):
        widget = self.query_one("#bar_title")
        widget.update_bar_title(message.track)  # type: ignore

    def on_notification_update(self, message):
        widget = self.query_one("#notification")
        widget.update(message.text)  # type: ignore
        Animation(widget).start()
