import threading
import time

from yandex_music import Station, StationResult, Track

from ymcli.radio import Radio
from ymcli.ui.func import seconds_to_minutes

from . import widgets
from .forms import BaseForm


class SelectStationForm(BaseForm):
    def create(self):
        super().create()
        self.name = "Stations"

        stations_list_width = self.max_x - int(self.max_x / 3)
        self.stations_ui = self.add(
            widgets.MultiLineActionBox,
            values=[],
            relx=2,
            rely=2,
            max_width=stations_list_width,
            max_height=self.max_widgets_height,
        )

        self.station_info = self.add(
            widgets.PagerBox,
            relx=stations_list_width + int(self.max_x / 20),
            rely=2,
            max_height=self.max_widgets_height,
        )
        self.add_hotkeys(self.stations_ui.entry_widget)

        self.bar = self.add_bar()

    def beforeEditing(self):
        super().beforeEditing()
        self.bar.active_form = "Stations"
        self.update_stations_list()
        self.when_cursor_moved()

    def on_exit(self):
        self.stations_ui.value = None

    def when_cursor_moved(self):
        selected_index = self.stations_ui.entry_widget.cursor_line
        if selected_index is None:
            return
        station: StationResult = self.stations_ui.stations[selected_index]
        self.station_info.values = [
            f"Название станции: {station.rup_title}",
            f"Описание: {station.rup_description}",
        ]
        self.station_info.display()

    def update_stations_list(self):
        stations: list[StationResult] = self.ym_client.radio.get_all_stations()

        station_names = [(f"{station.station.name}") for station in stations]

        self.stations_ui.values = station_names
        self.stations_ui.stations = stations

    def when_select(self):
        station: StationResult = self.stations_ui.stations[self.stations_ui.value]

        self.parentApp.getForm("STATION_TRACKS").station = station.station
        self.parentApp.getForm(
            "STATION_TRACKS"
        ).name = f"{station.rup_title} - {station.station.name}"
        self.parentApp.switchForm("STATION_TRACKS")
        self.stations_ui.value = None


class StationForm(BaseForm):
    def create(self):
        super().create()
        self.name = "StationTracks"
        self.station: Station | None = None

        self.track_info_widget = self.add(
            widgets.PagerBox,
            relx=2,
            rely=2,
            max_height=self.max_widgets_height,
        )
        self.add_hotkeys(self.track_info_widget.entry_widget)
        self.radio: Radio = self.ym_client.radio

        self.bar = self.add_bar()

    def beforeEditing(self):
        super().beforeEditing()
        self.bar.active_form = "StationTracks"
        self.start_station()
        self.playing = True

    def start_station(self):
        track: Track = self.radio.get_first_track(
            station_id=f"{self.station.id.type}:{self.station.id.tag}",
            station_from=self.station.id_for_from,
        )
        self.player.play(track=track)
        self._start_update_track_info()

    def when_cursor_moved(self):
        pass

    def when_select(self):
        pass

    def on_exit(self):
        self.radio.current_track = None
        self.player.stop()
        self._stop_progress_thread()
        self.parentApp.switchForm("SELECT_STATION")
        return True

    def _start_update_track_info(self):
        self.playing = True
        self.progress_thread = threading.Thread(
            target=self._progress_update_loop,
            daemon=True,
        )
        self.progress_thread.start()

    def _stop_progress_thread(self):
        self.playing = False
        if self.progress_thread.is_alive():
            self.progress_thread.join()

    def _progress_update_loop(self):
        while self.playing:
            track = self.player.now_playing
            if track is None:
                continue

            duration = seconds_to_minutes(track.duration_ms // 1000)  # type: ignore
            track_info = [
                "Название: " + track.title,  # type: ignore
                "Исполнитель: " + ", ".join(track.artists_name()),
                "Длительность: " + duration,
            ]

            self.track_info_widget.values = track_info
            self.track_info_widget.display()

            time.sleep(1)
