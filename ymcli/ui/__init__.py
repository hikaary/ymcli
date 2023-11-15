import npyscreen

from .playlist import PlaylistsForm
from .playlist_tracks import PlaylistTracksForm
from .stations import SelectStationForm, StationForm
from .widgets import ProgressBar


class Ymcli(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", PlaylistsForm)
        self.addForm("PLAYLIST_TRACKS", PlaylistTracksForm)
        bar = ProgressBar()
        bar.start()
        self.addForm("SELECT_STATION", SelectStationForm)
        self.addForm("STATION_TRACKS", StationForm)
