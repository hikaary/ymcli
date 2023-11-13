import npyscreen
from npyscreen.utilNotify import notify_confirm
from vlc import os
from yandex_music import Track

from ..config import MUSIC_DIR
from ..player import Player
from ..yandex_music_client import YandexMusicClient
from . import widgets
from .forms import BaseForm
from .func import seconds_to_minutes


class PlaylistTracksForm(BaseForm):
    def create(self):
        super().create()
        self.name = "PlayListTracks"

        self.tracks: list[Track] | None = None
        self.ym_client = YandexMusicClient()
        self.player = Player()

        tracks_list_widget_width = self.max_x - int(self.max_x / 3)
        self.tracks_list_widget = self.add(
            widgets.MultiLineActionBox,
            values=[],
            relx=2,
            rely=2,
            max_width=tracks_list_widget_width,
            max_height=self.max_widgets_height,
        )
        self.add_hotkeys(self.tracks_list_widget.entry_widget)

        self.track_info_widget = self.add(
            widgets.PagerBox,
            relx=tracks_list_widget_width + int(self.max_x / 20),
            rely=2,
            max_height=self.max_widgets_height,
        )
        self.bar = self.add_bar()

        self.exit_in_progress = False

    def beforeEditing(self):
        self.bar.active_form = "PlayListTracks"
        self.exit_in_progress = False
        self.player.track_list = self.tracks
        self.update_tacks_list()
        self.when_cursor_moved()

    def update_tacks_list(self):
        if self.tracks is None or len(self.tracks) == 0:
            npyscreen.notify_confirm("Not found tracks")
            self.parentApp.switchForm("MAIN")
            return

        for track in self.tracks:
            artists = ",".join(track.artists_name())
            track_name = f"{track.title} - {artists}"
            self.tracks_list_widget.values.append(track_name)

        self.tracks_list_widget.display()

    def when_cursor_moved(self):
        selected_index = self.tracks_list_widget.entry_widget.cursor_line
        if selected_index is None:
            return
        track = self.tracks[selected_index]
        duration = seconds_to_minutes(track.duration_ms // 1000)
        track_info = [
            "Название: " + track.title,
            "Исполнитель: " + ", ".join(track.artists_name()),
            "Длительность: " + duration,
        ]

        self.track_info_widget.values = track_info
        self.track_info_widget.display()

    def when_select(self):
        selected_index = self.tracks_list_widget.entry_widget.cursor_line
        if selected_index is None:
            return
        track = self.tracks[selected_index]
        saved_tracks = os.listdir(MUSIC_DIR)

        if f"{track.id}.mp3" in saved_tracks:
            self.player.play(track=track)
            return

        npyscreen.notify("Track not downloaded. Start download")
        self.ym_client.download(track)
        self.player.play(track=track)
        self.check_next_track_downloaded(selected_index)

    def check_next_track_downloaded(self, now_select_index):
        track = self.tracks[now_select_index + 1]
        saved_tracks = os.listdir(MUSIC_DIR)
        if f"{track.id}.mp3" in saved_tracks:
            return
        self.ym_client.download(track)

    def on_exit(self):
        self.tracks_list_widget.values = []
