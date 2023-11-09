import npyscreen

from .playlist import PlaylistsForm
from .playlist_tracks import PlaylistTracksForm
from .search import SearchForm


class MyApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", PlaylistsForm)
        self.addForm("SEARCH", SearchForm)
        self.addForm("PLAYLIST_TRACKS", PlaylistTracksForm)

    def change_form(self, name):
        self.switchForm(name)
        self.resetHistory()

    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")
