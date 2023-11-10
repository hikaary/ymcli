import threading
import time

import npyscreen
from config import MUSIC_DIR
from npyscreen.wgwidget import curses
from player import Player
from vlc import os
from yandex_music import Track
from yandex_music_client import YandexMusicClient


class TrackBox(npyscreen.BoxTitle):
    _contained_widgets = npyscreen.MultiLineAction

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
        tracks_list_height = y - int(y / 6)
        self.tracks_list = self.add(
            TrackBox,
            values=[],
            relx=2,
            rely=2,
            max_width=tracks_list_widht,
            max_height=tracks_list_height,
        )
        self._add_hotkeys()

        self.track_info = self.add(
            Pager,
            relx=tracks_list_widht + int(x / 20),
            rely=2,
            max_height=tracks_list_height,
        )
        progress_bar_width = x - int(x / 7)
        self.track_title = self.add(
            npyscreen.TitleFixedText,
            name="Track",
            value="No track playing",
            rely=-5,
        )
        self.progress_bar = self.add(
            npyscreen.Slider,
            value=0,
            label=False,
            max_width=progress_bar_width,
            rely=-3,
        )
        self.progress_text = self.add(
            npyscreen.Textfield,
            value="00:00 / 00:00",
            rely=-3,
            relx=-18,
        )

        self.first_edit = True
        self.running = False

    def beforeEditing(self):
        if self.tracks is None or len(self.tracks) == 0:
            npyscreen.notify_confirm("Not found tracks")
            self.parentApp.switchForm("MAIN")
            return
        self._start_progress_thread()
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
        self.check_next_track_downloaded(selected_index)

    def check_next_track_downloaded(self, now_select_index):
        track = self.tracks[now_select_index + 1]
        saved_tracks = os.listdir(MUSIC_DIR)
        if f"{track.id}.mp3" in saved_tracks:
            return
        self.ym_client.download(track)

    def update_bar_title(self, track: Track):
        self.track_title.value = f"{track.title} by {', '.join(track.artists_name())}"
        self.track_title.update()

    def _start_progress_thread(self):
        self.running = True
        self.progress_thread = threading.Thread(
            target=self._progress_update_loop,
            daemon=True,
        )
        self.progress_thread.start()

    def _progress_update_loop(self):
        last_time = time.perf_counter()
        while self.running:
            current_time = time.perf_counter()
            elapsed = current_time - last_time

            if elapsed >= 1.0:
                position = self.player.get_position()
                current_track = self.player.get_current_track()
                if current_track and position is not None:
                    duration_seconds = current_track.duration_ms // 1000  # type: ignore
                    absolute_position = int(position * duration_seconds)
                    self._update_bar_info(
                        duration_seconds=duration_seconds,
                        absolute_position=absolute_position,
                    )

                    if duration_seconds - absolute_position <= 1:
                        self.tracks_list.entry_widget.cursor_line += 1
                        self.select_track()

                last_time = current_time

            time.sleep(0.01)

    def _update_bar_info(
        self,
        duration_seconds: int,
        absolute_position: int,
    ):
        self.progress_bar.out_of = duration_seconds
        self.progress_bar.value = absolute_position

        current_time_formatted = seconds_to_minutes(absolute_position)
        duration_formatted = seconds_to_minutes(duration_seconds)
        self.progress_text.value = f"{current_time_formatted} / {duration_formatted}"

        self.progress_text.display()
        self.progress_bar.display()

    def _stop_progress_thread(self):
        self.running = False
        if self.progress_thread.is_alive():
            self.progress_thread.join()

    def on_clean_up(self):
        self._stop_progress_thread()

    def _add_hotkeys(self):
        self.tracks_list.entry_widget.add_handlers(
            {
                ord("p"): self.h_pause_track,
                curses.ascii.SP: self.h_pause_track,
                curses.ascii.ESC: self.h_exit_to_playlists,
                curses.KEY_RIGHT: self.h_move_track_position_to_right,
                curses.KEY_LEFT: self.h_move_track_position_to_left,
            }
        )

    def h_exit_to_playlists(self, ch):
        self.player.stop()
        self.parentApp.switchForm("MAIN")
        self.tracks_list.values = []
        self._stop_progress_thread()

    def h_move_track_position_to_right(self, ch):
        self.player.move_track_position(right=True)

    def h_move_track_position_to_left(self, ch):
        self.player.move_track_position(right=False)

    def h_pause_track(self, ch):
        self.player.play_pause()


def seconds_to_minutes(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
