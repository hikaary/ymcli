import threading
import time

import npyscreen
from config import MUSIC_DIR
from player import Player
from vlc import os
from yandex_music import Track
from yandex_music_client import YandexMusicClient


class TrackBox(npyscreen.BoxTitle):
    _contained_widgets = npyscreen.MultiLineAction

    def h_cursor_line_up(self, *args, **keywords):
        self.when_cursor_moved()

    def h_cursor_line_down(self, *args, **keywords):
        self.when_cursor_moved()

    def when_cursor_moved(self):
        self.parent.update_track_info()

    def when_value_edited(self):
        self.parent.select_track()


class Pager(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Pager


class PlaylistTracksForm(npyscreen.FormBaseNew):
    def create(self):
        self.tracks: list[Track] | None = None
        self.ym_client = YandexMusicClient()
        self.player = Player()

        y, x = self.useable_space()
        tracks_list_widht = x - int(x / 3)
        tracks_list_height = y - int(y / 8)
        self.tracks_list = self.add(
            TrackBox,
            values=[],
            relx=2,
            rely=2,
            max_width=tracks_list_widht,
            max_height=tracks_list_height,
        )
        self.track_info = self.add(
            Pager,
            relx=tracks_list_widht + int(x / 20),
            rely=2,
            max_height=tracks_list_height,
        )
        self.track_title = self.add(
            npyscreen.TitleFixedText,
            name="Track",
            value="No track playing",
            # rely=tracks_list_height + 5,
            # relx=2,
        )
        self.progress_bar = self.add(
            npyscreen.Slider,
            value=0,
            label=False,
            # max_width=x - int(x / 6),
        )
        # self.progress_text = self.add(
        #     npyscreen.TitleText,
        #     name="Progress",
        #     value="00:00 / 00:00",
        #     relx=x - int(x / 10) + 1,
        # )

        self.first_edit = True

        self.running = True
        self._start_progress_thread()

    def beforeEditing(self):
        if self.tracks is None or len(self.tracks) == 0:
            npyscreen.notify_confirm("Not found tracks")
            self.parentApp.switchForm("MAIN")
            return
        self.update_tacks_list()
        self.update_track_info()

    def update_tacks_list(self):
        assert self.tracks is not None

        for track in self.tracks:
            if track is None:
                track_name = "Error load track"
            else:
                artists = ",".join(track.artists_name())
                track_name = f"{track.title} - {artists}"
            self.tracks_list.values.append(track_name)

        self.tracks_list.display()

    def update_track_info(self):
        selected_index = self.tracks_list.entry_widget.cursor_line
        if selected_index is None:
            return
        track = self.tracks[selected_index]
        if track is None:
            track_info = ["Error load track info"]
        else:
            duration = seconds_to_minutes(track.duration_ms // 1000)
            track_info = [
                "Название: " + track.title,
                "Исполнитель: " + ", ".join(track.artists_name()),
                "Длительность: " + duration,
            ]

        self.track_info.values = track_info
        self.track_info.display()

    def select_track(self):
        if self.first_edit:
            self.first_edit = False
            return
        selected_index = self.tracks_list.entry_widget.cursor_line
        if selected_index is None:
            return
        track = self.tracks[selected_index]
        saved_tracks = os.listdir(MUSIC_DIR)

        if f"{track.id}.mp3" in saved_tracks:
            self.player.play(track=track)
            self.update_bar_title(track)
            return

        npyscreen.notify("Track not downloaded. Start download")
        self.ym_client.download(track)
        self.player.play(track=track)
        self.update_bar_title(track)

    def update_bar_title(self, track: Track):
        self.track_title.value = f"{track.title} by {', '.join(track.artists_name())}"
        self.track_title.update()

    def _start_progress_thread(self):
        self.progress_thread = threading.Thread(
            target=self._progress_update_loop,
            daemon=True,
        )
        self.progress_thread.start()

    def _progress_update_loop(self):
        while True:
            position = self.player.get_position()
            current_track = self.player.get_current_track()
            if current_track and position is not None:
                duration_seconds = current_track.duration_ms // 1000  # type: ignore
                absolute_position = int(position * duration_seconds)
                self.progress_bar.out_of = duration_seconds
                self.progress_bar.value = absolute_position
                self.progress_bar.display()

            time.sleep(1)

    def _stop_progress_thread(self):
        self.running = False
        if self.progress_thread.is_alive():
            self.progress_thread.join()

    def on_clean_up(self):
        self._stop_progress_thread()


def seconds_to_minutes(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
