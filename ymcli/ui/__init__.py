import npyscreen

from .playlist import PlaylistsForm
from .playlist_tracks import PlaylistTracksForm
from .search import SearchForm
from .song import NowPlayingForm


class MyApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", PlaylistsForm)
        self.addForm("SEARCH", SearchForm)
        self.addForm("NOW_PLAYING", NowPlayingForm)
        self.addForm("PLAYLIST_TRACKS", PlaylistTracksForm)

    def change_form(self, name):
        self.switchForm(name)
        self.resetHistory()

    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")
