import npyscreen
from yandex_music import Playlist, StationResult, Track, TrackShort, TracksList

from ..yandex_music_client import YandexMusicClient
from .playlist_tracks import PlaylistTracksForm


class Pager(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Pager


class SelectStationForm(npyscreen.FormBaseNew):
    def create(self):
        self.name = "Stations"
        self.ym_client = YandexMusicClient()

        y, x = self.useable_space()
        stations_list_width = x - int(x / 3)
        stations_list_height = y - int(y / 8)
        self.stations_ui = self.add(
            npyscreen.MultiLineAction,
            values=[],
            relx=2,
            rely=2,
            max_width=stations_list_width,
            max_height=stations_list_height,
        )
        self.stations_ui.actionHighlighted = self.actionHighlighted
        self.stations_ui.when_cursor_moved = self.update_station_info

        self.station_info = self.add(
            Pager,
            relx=stations_list_width + int(x / 20),
            rely=2,
            max_height=stations_list_height,
        )

    def beforeEditing(self):
        self.update_stations_list()
        self.update_station_info()

    def update_station_info(self):
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

        station_names = [
            (f"{station.station.name} - {station.rup_description}")
            for station in stations
        ]

        self.stations_ui.values = station_names
        self.stations_ui.stations = stations

    def actionHighlighted(self, act_on_this, key_press):
        return
        playlist: Playlist | TracksList = self.station_ui.playlists[
            self.station_ui.cursor_line
        ]
        playlist_tracks: list[TrackShort] | list[Track] = playlist.fetch_tracks()

        if isinstance(playlist_tracks[0], TrackShort):
            playlist_tracks = [
                short_track.track for short_track in playlist_tracks  # type: ignore
            ]

        self.parentApp.getForm("PLAYLIST_TRACKS").tracks = playlist_tracks
        self.parentApp.getForm("PLAYLIST_TRACKS").name = (
            playlist.title if isinstance(playlist, Playlist) else "Likes"
        )
        self.parentApp.switchForm("PLAYLIST_TRACKS")


class StationForm(PlaylistTracksForm):
    def create(self):
        super().create()
